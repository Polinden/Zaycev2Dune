#!/bin/bash
# to use 
# ./run playlist


echo "I play a list given to me"
echo "q - to quit, s - to skip"



spause () {
    echo -e "\rplaying \033[36m$1\033[39m" "sleeping $(($2/60)):$(($2%60))"
    for pc in $(seq 1 1 "$2"); do
        pc=$(($pc*1000/$2/10))
        echo -ne "\r\033[32m\033[0K$pc%\033[39m"
        kp1=""; read -t 1 -s -n 1 kp1 || True
        [[ $kp1 = 'q' ]] && break 2 
        [[ $kp1 = 's' ]] && break
    done
}


set -euo pipefail
input="$1"

re='(.*) -##!##- (.*)'

IFS=$'\r\n'; file_lines=$(<"$input"); file_lines=($file_lines)

for line in ${file_lines[@]}
do
    time="2:22"; dest=""
    if [[ -z $line ]]; then
        continue
    fi    
    if [[ $line =~ $re ]] ; then
        line="${BASH_REMATCH[1]}"; dest="${BASH_REMATCH[2]}"
        if [[ $line =~ $re ]] ; then
           line="${BASH_REMATCH[1]}"; time="$dest"; dest="${BASH_REMATCH[2]}"
        fi   
    fi
    if [[ ! -z $dest ]] ; then
      p=$(python3 zay.py -s -q --name "$line" --dest "$dest" --time "$time")
    else    
      p=$(python3 zay.py -s -q --name "$line")
    fi
    spause "$line" "$p"
done

echo
echo "all done"


