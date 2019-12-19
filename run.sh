#!/bin/bash
# to use 
# ./run playlist


set -euo pipefail
input="$1"


while IFS= read -r line
do
    p=$(python3 zay.py -s -q --name "$line")
    echo "playing $line" "sleeping $p"
    sleep "$p"
done < "$input"

