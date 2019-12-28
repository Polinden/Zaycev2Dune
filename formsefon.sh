#!/bin/bash

echo $1 $2 $3 $4 > test

#edit url and other data
dune_url="http://192.168.77.50"
dune_ftp="/D"
dune_ssh_user=root
dune_ssh_pass=""


dune_ip=(${dune_url//\/\// })
dune_ip="${dune_ip[1]}"
ping_res=`ping -c 1 "$dune_ip" 1> /dev/null; echo $?`
if [[ ! "$ping_res" = 0 ]]
  then 
    echo "Dune on IP adress $dune_ip not found"
    exit 2 
fi	

if [[ ! -z "$2" ]]
  then
    dune_url="$2"
fi
if [[ ! -z "$3" ]]
  then
    dune_ftp="$3"
fi        
if [[ ! -z "$4" ]]
  then
    dune_ssh_user="$4"
fi        
if [[ ! -z "$5" ]]
  then
    dune_ssh_pass="$5"
fi        

ssh_url="${dune_url//http:\/\//$dune_ssh_user@}"  
p1=$(echo "$1" | cut -d'/' -f 1-3)

play_load=("rm $dune_ftp/1.mp3; "\
          "/opt/bin/curl -L -b cookiefile -c cookiefile --insecure $p1 --output $dune_ftp/1.mp3; "\
          "/opt/bin/curl -L -b cookiefile -c cookiefile --insecure $1  --output $dune_ftp/1.mp3")

cat <<EOF>14e.tmp
spawn ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 $ssh_url "${play_load[*]}"
match_max 100000
expect "*?assword:*"
send -- "$dune_ssh_pass\r"
send -- "\r"
interact
EOF

expect 14e.tmp
curl --silent -X GET "$dune_url/cgi-bin/do?cmd=start_file_playback&media_url=storage_name:/$dune_ftp/1.mp3"


