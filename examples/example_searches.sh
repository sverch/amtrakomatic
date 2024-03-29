#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

run () {
    echo "$@"
    "$@"
}



# Just three legs between new york, boston, vermont, and harrisburg
echo "Northern trip"
run python main.py --source NewYork --destination Boston --date  08/11/2019
run python main.py --source Boston --destination vermont --date  08/19/2019
run python main.py --source Vermont --destination harrisburg --date  08/25/2019

# Comparing multi stage harrisburg to kansas city!  The prices are actually
# adding up (as in multi stage is not any different).
echo "Single leg harrisburg -> kansascity"
run python main.py --source Harrisburg --destination kansascity --date  08/31/2019

echo "Separate legs harrisburg -> kansascity"
run python main.py --source Harrisburg --destination pittsburgh --date 08/31/2019
run python main.py --source pittsburgh --destination chicago --date 08/31/2019
run python main.py --source chicago --destination kansascity --date 09/01/2019



# Comparing multi stage kansas city to Denver!
echo "Single leg kansascity -> denver"
run python main.py --source KansasCity --destination denver --date  09/15/2019

echo "Separate legs kansascity -> denver"
run python main.py --source KansasCity --destination galesburg --date  09/15/2019
run python main.py --source galesburg --destination denver --date  09/15/2019

# Do a date range price comparison, because this is an expensive overnight train
echo "Running date range price comparison between galesburg and denver"
run python main.py --source galesburg --destination denver --date  09/15/2019
run python main.py --source galesburg --destination denver --date  09/16/2019
run python main.py --source galesburg --destination denver --date  09/17/2019
run python main.py --source galesburg --destination denver --date  09/18/2019
run python main.py --source galesburg --destination denver --date  09/19/2019

# Two legs between denver and sacramento
echo "Running searches between denver and sacramento"
run python amtrakomatic/main.py --source denver --destination saltlakecity --date  09/30/2019
run python amtrakomatic/main.py --source SaltLakeCity --destination Sacramento --date  10/07/2019

# Run some northwest searches
echo "Running some northwest california to seattle route examples"
run python amtrakomatic/main.py --source Sacramento --destination Seattle --date  10/14/2019
run python amtrakomatic/main.py --source Seattle --destination Chico --date  10/27/2019
run python amtrakomatic/main.py --source Chico --destination Sanjose --date  11/04/2019

# Run southern routes
echo "Example of southern trip from san jose, CA to new york, NY"
run python amtrakomatic/main.py --source sanjose --destination losangeles --date  11/18/2019
run python amtrakomatic/main.py --source losangeles --destination elpaso --date  11/25/2019
run python amtrakomatic/main.py --source elpaso --destination houston --date  11/30/2019
run python amtrakomatic/main.py --source Houston --destination washingtondistrict --date  12/08/2019
run python amtrakomatic/main.py --source washingtondistrict --destination newyork --date  12/18/2019
