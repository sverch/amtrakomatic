"""
Library to handle fuzzy matching of amtrak station names to get amtrak station codes.
"""
import csv
import pathlib
import os
from fuzzywuzzy import process

AMTRAK_STATIONS_CSV = os.path.join(pathlib.Path(__file__).parent, 'Amtrak_Stations.csv')

def load_stations():
    """
    Loads the stations CSV into a map keyed by full station name.
    """
    with open(AMTRAK_STATIONS_CSV) as amtrak_stations:
        header_skipped = False
        stations = []
        reader = csv.reader(amtrak_stations, delimiter=',', quotechar='"')
        for fields in reader:
            if not header_skipped:
                header_skipped = True
                continue
            stations.append({
                "name": fields[4],
                "code": fields[3],
                "city": fields[5],
                "state": fields[6]
                })
    station_map = {}
    for station_info in stations:
        station_map[station_info["name"]] = station_info
    return station_map

AMTRAK_STATIONS = load_stations()

def station(name):
    """
    Given a rough station name, does a fuzzy match on all Amtrak stations to return the proper
    station code.
    """
    matched_station = process.extractOne(name, AMTRAK_STATIONS.keys())[0]
    return (matched_station, AMTRAK_STATIONS[matched_station]["code"])

def station_by_code(code):
    """
    Finds all station information by code.
    """
    for amtrak_station in AMTRAK_STATIONS.values():
        if amtrak_station["code"] == code:
            return amtrak_station
    return {}
