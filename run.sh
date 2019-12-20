#!/bin/bash
# to use 
# ./run playlist


set -euo pipefail
input="$1"

re='(.*) -##!##- (.*)'

while IFS= read -r line
do
    time="2:22"
    dest=""
    if [[ -z $line ]]; then
        continue
    fi    
    if [[ $line =~ $re ]] ; then
        line="${BASH_REMATCH[1]}"
        dest="${BASH_REMATCH[2]}"
        if [[ $line =~ $re ]] ; then
           line="${BASH_REMATCH[1]}"
           time="$dest"
           dest="${BASH_REMATCH[2]}"
        fi   
    fi
    if [[ ! -z $dest ]] ; then
      p=$(python3 zay.py -s -q --name "$line" --dest "$dest" --time "$time")
    else    
      p=$(python3 zay.py -s -q --name "$line")
    fi
    
    echo "playing $line" "sleeping $p"
    sleep "$p"

done < "$input"

