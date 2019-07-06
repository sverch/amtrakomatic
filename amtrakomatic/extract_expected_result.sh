#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

NUM_ARGS_REQUIRED=0
if [ $# -ne "${NUM_ARGS_REQUIRED}" ]; then
    cat <<EOF
Usage: $0

    Runs pytest and vomits the json of the expected output for whatever failed.

EOF
    exit 1
fi

pytest -vvvv . | grep -E "^E" | grep -v Assertion | grep -v chars | grep -v First | grep -E -v "^E\s*$" | sed 's/.....\(.*\)/\1/g' | sed "s/'/\"/g" | grep -E -v "^\"" | grep -E -v "\[\]" | sed "s/\"Rail\"/'Rail'/g"
