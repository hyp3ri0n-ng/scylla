#!/bin/bash
# Scylla.sh bash-cli
# Author: Hish-qu-Ten <QHishTenU@protonmail.com>
# Description:
#    Putting the .sh back into scylla.sh 😉

query="" size="" page="" 
set -euo pipefail

while getopts "q:s:p:" option; do
case $option in
    q) query=$OPTARG;;
    s) size=$OPTARG;;
    p) page=$OPTARG;;
    :) echo "Option -$OPTARG requires an argument." >&2
    exit 1;;
esac
done

if [ -z "$query" ]; then
    exec 2>&1; echo "USAGE: scylla.sh -q lucene-query [-s results per page] [-p page]";
    echo "Example: to fetch 100 passwords starting with 1234 run './scylla.sh password:1234* 100' (the last two args are optional)"
    echo "Example2: to fetch the second 200 results from the last query run './scylla.sh password:1234* 100 2'"
    exit 1
fi

# handle optional args
if [ -z "$size" ]; then
    size=100
fi
if [ -z "$page" ]; then
    page=1
fi

start=$((($page - 1) * $size))

main()
{
    fetch_results
}

fetch_results() {
    local response=$(curl -s --show-error -H "Accept: application/json" "https://scylla.sh/search?q=$query&size=$size&start=$start")
    
    # Check jq installed, if not work anyway but look fugly
    if ! [ -x "$(command -v jq)" ]; then
        echo $result
    else
        echo $response | jq .
    fi
}

main
