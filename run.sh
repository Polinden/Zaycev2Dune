#!/bin/bash
# to use 
# ./run playlist

if [[ -z $1 ]] || [[ ! -f $1  ]]
  then
      echo "to use, just give me a playlist file name as a parameter"
      exit 2
fi

echo "I am playing a list given to me"
echo "q - to quit, s - to skip, replay-r"


spause () {
    echo -e "\rplaying \033[36m$1\033[39m" "sleeping $(($2/60)):$(($2%60))"
    for pc in $(seq 1 1 "$2"); do
        pc=$(($pc*1000/$2/10))
        echo -ne "\r\033[32m\033[0K$pc%\033[39m"
        kp1=""; read -t 1 -s -n 1 kp1 || True
        [[ $kp1 = 'q' ]] && break 2
        [[ $kp1 = 's' ]] && break
        if [[ $kp1 = 'r' ]] 
          then 
             if [[ $il -ge 0 ]]; then il=$(( $il - 1 )); fi
             break
        fi
    done
    return 0
}


set -euo pipefail
input="$1"

re='(.*) -##!##- (.*)'

IFS=$'\r\n'; file_lines=$(<"$input"); file_lines=($file_lines)

lsize=${#file_lines[@]}; echo "total songs = $lsize"

for (( il = 0; il < $lsize; il++ ))
do
    line=${file_lines[$il]}
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
      p=$(python3 zay.py -s -q -p --name "$line")
    fi
    [[ ! -z $p ]] && spause "$line" "$p"
done

echo
echo "all done"


