#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

run() {
	echo "$@"
	"$@"
}

run_amtrakomatic() {
	#	echo
	#	echo "####################################################"
	#	echo "# Getting tickets starting on $(date -d "$3" +%A), $3 #"
	#	echo "####################################################"
	#	run amtrakomatic --source "$1" --destination "$2" --date "$3" --train-name "$4" # --dry-run
	#	echo "####################################################"
	#	echo
	#	sleep 10
	echo "$(date -d "$3" +%A), $3: $1 to $2"
}

run_amtrakomatic "New York" "Harrisburg" 06/12/2021 "665 Keystone Service"
run_amtrakomatic "Harrisburg" "Washington DC" 06/14/2021 "93 Northeast Regional"
run_amtrakomatic "Washington DC" Chicago 06/17/2021 "29 Capitol Limited"
run_amtrakomatic Chicago Seattle 06/22/2021 "7 Empire Builder"
run_amtrakomatic Seattle Sacramento 07/03/2021 "11 Coast Starlight"
run_amtrakomatic Sacramento "San Jose" 07/10/2021 "741 Capitol Corridor"
run_amtrakomatic "Emeryville" "Salt Lake City" 07/24/2021 "6 California Zephyr"
run_amtrakomatic "Salt Lake City" "Denver" 07/31/2021 "6 California Zephyr"
run_amtrakomatic "Denver" "Chicago" 08/07/2021 "6 California Zephyr"
run_amtrakomatic "Galesburg" "Kansas City" 08/08/2021 "3 Southwest Chief"
run_amtrakomatic "Chicago" "Winslow" 08/13/2021 "3 Southwest Chief"
run_amtrakomatic "Winslow" "Los Angeles" 08/14/2021 "3 Southwest Chief"
run_amtrakomatic "Los Angeles" "Houston" 08/15/2021 "2 Sunset Limited"
run_amtrakomatic "Houston" "Union Passenger Terminal, New Orleans, LA" 08/22/2021 "2 Sunset Limited"
run_amtrakomatic "Union Passenger Terminal, New Orleans, LA" "Washington DC" 08/24/2021 "20 Crescent"
