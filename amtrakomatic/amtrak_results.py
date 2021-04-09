"""
A class that gives a structured interface to Amtrak results given a raw HTML page.
"""

import typing
import re
import attr
from bs4 import BeautifulSoup
from amtrakomatic import fuzzy_match

# pylint: disable=too-few-public-methods
@attr.s(auto_attribs=True)
class AmtrakResult:
    """
    A single trip result from the results page.
    """
    total_travel_time: str
    legs: typing.List[dict]
    fares: typing.List[str]
    minimum_fare_value_attribute: str
    result_id: str
    add_to_cart_button_name_attribute: str

    @classmethod
    def from_result_and_details(cls, result, details):
        """
        There are two separate HTML blobs that are passed from the selenium part of the code.
        """

        def get_total_travel_time(element):
            return element.find("div", "travel-time").find("span", "text-center").text.strip()

        def get_legs(element):
            def get_station(element):
                return ("%s %s" % (
                    element.find("h5", "station").text.strip(),
                    element.find("h6", "station").text.strip())).strip()

            def get_day_and_time(element):
                time_raw = element.find("p", "time").text
                time_match = re.match(r"(.+)([ap]), (\w+), (\w+) ([0-9]+) (?:\((.*)\))?", time_raw)
                if not time_match:
                    raise Exception("Failed to match time: %s" % time_raw)
                time_str = '%s%s' % (
                        time_match.group(1),
                        "am" if time_match.group(2).strip() == "a" else "pm")
                day_str = '%s, %s %s' % (
                        time_match.group(3),
                        time_match.group(4),
                        time_match.group(5))
                return (time_str.strip(), day_str.strip())

            def get_time(element):
                time_str, _ = get_day_and_time(element)
                return time_str

            def get_day(element):
                _, day_str = get_day_and_time(element)
                return day_str

            def get_train(element):
                return element.find("p", "train").text.strip()

            def get_duration(element):
                return element.find("p", "time").text.split("(")[1].replace(")", "").strip()

            def get_transfer(element):
                transfer_element = element.parent.find("span", "transfer-text")
                if transfer_element:
                    transfer_string = transfer_element.text.split("|")[0]
                    return {
                            "station": fuzzy_match.station_by_code(
                                transfer_string.split("connection in")[1].strip()),
                            "duration": transfer_string.split("connection in")[0].strip(),
                            }
                return {}

            leg_sections = element.find_all("div", "segment")
            legs = []
            for leg_section in leg_sections:
                departure_information = leg_section.find("div", "separator-before")
                arrival_information = leg_section.find("div", "separator-after")
                legs.append({
                    "train_name": get_train(departure_information),
                    "departure_time": get_time(departure_information),
                    "arrival_time": get_time(arrival_information),
                    "departure_day": get_day(departure_information),
                    "arrival_day": get_day(arrival_information),
                    "departure_station": get_station(departure_information),
                    "arrival_station": get_station(arrival_information),
                    "duration": get_duration(departure_information),
                    "transfer": get_transfer(leg_section),
                })
            return legs

        def get_fares(element):
            fare_type_descriptions = element.find_all("p", "service-type")
            fares = []
            for fare_type_description in fare_type_descriptions:
                fare_type = fare_type_description.text.replace("from", "").strip()
                fare_value = fare_type_description.parent.find("span", "amount").text.strip()
                fares.append({"type": fare_type, "value": fare_value})
            return fares

        def get_minimum_fare_value_attribute(_):
            """
            TODO: Get rid of this from the API, it's only for automatically getting me onto the buy
            page, which I don't need.... (maybe, unless it's easy).
            """
            return ""

        def get_add_to_cart_button_name_attribute(_):
            """
            TODO: Get rid of this from the API, it's only for automatically getting me onto the buy
            page, which I don't need.... (maybe, unless it's easy).
            """
            return ""

        result_parsed = BeautifulSoup(result, 'html.parser')
        details_parsed = BeautifulSoup(details, 'html.parser')
        return cls(
            total_travel_time=get_total_travel_time(result_parsed),
            legs=get_legs(details_parsed),
            fares=get_fares(result_parsed),
            minimum_fare_value_attribute=get_minimum_fare_value_attribute(result_parsed),
            add_to_cart_button_name_attribute=
            get_add_to_cart_button_name_attribute(result_parsed),
            result_id=""
            )


    def pretty_print(self):
        """
        Pretty prints this result to the terminal.
        """
        indent = "    "
        first_departure = None
        last_arrival = None
        legs_string = ""
        for leg in self.legs:
            if not first_departure:
                first_departure = "".join(leg["departure_time"].split(" "))
            last_arrival = "".join(leg["arrival_time"].split(" "))
            to_print = ""
            to_print = to_print + "%s%-30s| " % (
                indent,
                leg["train_name"],
                )
            to_print = to_print + "%s -> " % (
                " ".join(leg["departure_time"].split(" ")),
                )
            to_print = to_print + "%s" % (
                " ".join(leg["arrival_time"].split(" "))
                )
            if leg["arrival_day"] and leg["arrival_day"] != leg["departure_day"]:
                to_print = to_print + ", %s" % (
                    leg["arrival_day"],
                    )
                last_arrival = last_arrival + ", " + leg["arrival_day"]
            to_print = to_print + " (%s)" % (
                leg["duration"],
                )
            if leg["transfer"]:
                to_print = to_print + "\n%s%sTransfer in %s: %s" % (
                    indent,
                    indent,
                    "%s, %s (%s)" % (
                        leg["transfer"]["station"]["city"],
                        leg["transfer"]["station"]["state"],
                        leg["transfer"]["station"]["code"]),
                    leg["transfer"]["duration"],
                    )
            legs_string = legs_string + to_print + "\n"
        print("%s -> %s (%s): %s" % (
            first_departure,
            last_arrival,
            self.total_travel_time,
            ", ".join(["%s: %s" % (fare["type"], fare["value"].replace(".00", ""))
                for fare in self.fares]),
            ))
        print(legs_string)
        return True

@attr.s(auto_attribs=True)
class AmtrakResults:
    """
    A list of all results from the results page.
    """
    results: typing.List[AmtrakResult] = []

    def get_by_train_name(self, train_name):
        """
        Get a specific result by train name.
        """
        for result in self.results:
            for leg in result.legs:
                if leg["train_name"] == train_name:
                    return result
        return None

    def pretty_print(self, train_name=None):
        """
        Pretty prints the results to the terminal.
        """
        if train_name:
            result = self.get_by_train_name(train_name)
            if not result:
                print("No train with name %s found! Printing all results." % train_name)
                for result in self.results:
                    result.pretty_print()
            else:
                result.pretty_print()
        else:
            for result in self.results:
                result.pretty_print()
        return True

    def get_all(self):
        """
        Get all results in a list.
        """
        return self.results
