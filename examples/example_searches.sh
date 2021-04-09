#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

run() {
	echo "$@"
	"$@"
}

# Just three legs between new york, boston, vermont, and harrisburg
echo "Northern trip"
run amtrakomatic --source NewYork --destination Boston --date 08/11/2021
run amtrakomatic --source Boston --destination vermont --date 08/19/2021
run amtrakomatic --source Vermont --destination harrisburg --date 08/25/2021

# Comparing multi stage harrisburg to kansas city!  The prices are actually
# adding up (as in multi stage is not any different).
echo "Single leg harrisburg -> kansascity"
run amtrakomatic --source Harrisburg --destination kansascity --date 08/31/2021

echo "Separate legs harrisburg -> kansascity"
run amtrakomatic --source Harrisburg --destination pittsburgh --date 08/31/2021
run amtrakomatic --source pittsburgh --destination chicago --date 08/31/2021
run amtrakomatic --source chicago --destination kansascity --date 09/01/2021

# Comparing multi stage kansas city to Denver!
echo "Single leg kansascity -> denver"
run amtrakomatic --source KansasCity --destination denver --date 09/15/2021

echo "Separate legs kansascity -> denver"
run amtrakomatic --source KansasCity --destination galesburg --date 09/15/2021
run amtrakomatic --source galesburg --destination denver --date 09/15/2021

# Do a date range price comparison, because this is an expensive overnight train
echo "Running date range price comparison between galesburg and denver"
run amtrakomatic --source galesburg --destination denver --date 09/15/2021
run amtrakomatic --source galesburg --destination denver --date 09/16/2021
run amtrakomatic --source galesburg --destination denver --date 09/17/2021
run amtrakomatic --source galesburg --destination denver --date 09/18/2021
run amtrakomatic --source galesburg --destination denver --date 09/19/2021

# Two legs between denver and sacramento
echo "Running searches between denver and sacramento"
run amtrakomatic --source denver --destination saltlakecity --date 09/30/2021
run amtrakomatic --source SaltLakeCity --destination Sacramento --date 10/07/2021

# Run some northwest searches
echo "Running some northwest california to seattle route examples"
run amtrakomatic --source Sacramento --destination Seattle --date 10/14/2021
run amtrakomatic --source Seattle --destination Chico --date 10/27/2021
run amtrakomatic --source Chico --destination Sanjose --date 11/04/2021

# Run southern routes
echo "Example of southern trip from san jose, CA to new york, NY"
run amtrakomatic --source sanjose --destination losangeles --date 11/18/2021
run amtrakomatic --source losangeles --destination elpaso --date 11/25/2021
run amtrakomatic --source elpaso --destination houston --date 11/30/2021
run amtrakomatic --source Houston --destination washingtondistrict --date 12/08/2021
run amtrakomatic --source washingtondistrict --destination newyork --date 12/18/2021
