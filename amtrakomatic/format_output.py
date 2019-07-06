"""
Library to nicely format the result output.
"""
def print_result(result):
    """
    Print a single result.
    """
    indent = "    "
    first_departure = None
    last_arrival = None
    legs_string = ""
    for leg in result.legs:
        if not first_departure:
            first_departure = "".join(leg["departure_time"].split(" "))
        last_arrival = "".join(leg["arrival_time"].split(" "))
        to_print = ""
        to_print = to_print + "%s%-30s| " % (
            indent,
            leg["train_name"],
            )
        to_print = to_print + "%s -> " % (
            "".join(leg["departure_time"].split(" ")),
            )
        to_print = to_print + "%s" % (
            "".join(leg["arrival_time"].split(" "))
            )
        if leg["arrival_day"]:
            to_print = to_print + ", %s" % (
                leg["arrival_day"],
                )
            last_arrival = last_arrival + ", " + leg["arrival_day"]
        to_print = to_print + " (%s)" % (
            leg["duration"],
            )
        if leg["transfer"]:
            to_print = to_print + "\n%s%sTRANSFER: %s (%s)" % (
                indent,
                indent,
                leg["transfer"]["station"],
                leg["transfer"]["duration"],
                )
        legs_string = legs_string + to_print + "\n"
    print("%s -> %s (%s): %s" % (
        first_departure,
        last_arrival,
        result.total_travel_time,
        ", ".join([fare.replace(".00", "") for fare in result.fares]),
        ))
    print(legs_string)

def print_results(results):
    """
    Print the results in an easy to read table.
    """
    for result in results:
        print_result(result)
    return True
