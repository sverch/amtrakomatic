"""
A class that gives a structured interface to Amtrak results given a raw HTML page.
"""

import typing
import attr
from bs4 import BeautifulSoup

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

@attr.s(auto_attribs=True)
class AmtrakResults:
    """
    A list of all results from the results page.
    """
    results: typing.List[AmtrakResult] = []

    @classmethod
    def from_html(cls, html):
        """
        Parses the html into a list of AmtrakResult objects.
        """
        soup = BeautifulSoup(html, 'html.parser')
        raw_results = soup.find_all("table", "newFareFamilyTable")

        def get_total_travel_time(element):
            total_travel_time = element.find("span", "total_travel_time")
            if total_travel_time:
                return total_travel_time.string.split(u'\xa0')[0]
            return None

        def get_legs(element):

            def find_duration(element):
                duration = None
                duration = element.find("h2", "duration_lg")
                if duration and duration.string.replace(u'\xa0', u''):
                    return duration.string
                return element.find(
                    "span", "ff_seg_duration").string.strip().rstrip(")").lstrip("(")

            # Yes, this is actually the most reliable predictor of where the times will be for a
            # specific leg.
            legs_info_raw = element.find_all("div", "row_one")
            legs_train_names = element.find_all("span", id="_service_span")
            transfers = element.find_all("span", "transfer_copy")
            if len(legs_info_raw) != len(transfers) + 1:
                raise Exception("Got invalid leg times and transfers: %s, %s" % (
                    legs_info_raw, transfers))
            if len(legs_info_raw) != len(legs_train_names):
                raise Exception("Got invalid leg times and train_names: %s, %s" % (
                    legs_info_raw, legs_train_names))
            leg_info = []
            for leg_num, leg_info_raw in enumerate(legs_info_raw):
                leg_times = leg_info_raw.find_all("h2", "time_lg")
                departure_time = leg_times[0].string.strip()
                arrival_time = leg_times[1].contents[0].strip()
                arrival_day_element = leg_info_raw.find("div", "depart_date_sm")
                arrival_day = ""
                if arrival_day_element:
                    arrival_day = arrival_day_element.string.strip()
                transfer = {}
                if leg_num < len(legs_info_raw) - 1:
                    transfer_info = transfers[leg_num].string.split("|")
                    transfer = {"station": transfer_info[0].strip().replace("\n", ""),
                                "duration": transfer_info[1].strip()}
                leg_info.append({
                    "train_name": legs_train_names[leg_num].string.strip(),
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "arrival_day": arrival_day,
                    "duration": find_duration(leg_info_raw),
                    "transfer": transfer,
                })
            return leg_info

        def get_fares(element):
            fares = element.find_all("table", "ffam-price-container")
            # It would be nice to include the names of the fares, but that would have to be parsed
            # elsewhere.  Plus, points pages do not have the fare names header.
            text_fares = []
            for fare in fares:
                text_fares.append(fare.find("span", "radio-button__text").string)
            return text_fares

        def get_minimum_fare_value_attribute(element):
            fares = element.find_all("table", "ffam-price-container")
            # It would be nice to include the names of the fares, but that would have to be parsed
            # elsewhere.  Plus, points pages do not have the fare names header.
            minimum_fare_value_attribute = None
            for fare in fares:
                if fare.find("span", "radio-button__text").string:
                    minimum_fare_value_attribute = fare.find("input").attrs["value"]
                    break
            return minimum_fare_value_attribute

        def get_add_to_cart_button_name_attribute(element):
            addtocartbutton = element.find("input", "addtocart")
            if addtocartbutton:
                return addtocartbutton.attrs["name"]
            return ""

        results = []
        for raw_result in raw_results:
            results.append(AmtrakResult(
                total_travel_time=get_total_travel_time(raw_result),
                legs=get_legs(raw_result),
                fares=get_fares(raw_result),
                minimum_fare_value_attribute=get_minimum_fare_value_attribute(raw_result),
                add_to_cart_button_name_attribute=
                get_add_to_cart_button_name_attribute(raw_result),
                result_id=raw_result.attrs["id"]
                ))

        return cls(results)

    def get_by_train_name(self):
        """
        Get a specific result by train name.
        """
        return self.results

    def get_all(self):
        """
        Get all results in a list.
        """
        return self.results
