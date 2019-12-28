#!/bin/bash
HISTFILE=~/.bash_history
set -o history
if [[ -z $1 ]] 
then
   history | grep -e "--name \'" | awk -v z=\' '{gsub(".+name |"z, "", $0); print $0}'
else
   cat $1 | grep -e "--name \'" | awk -v z=\' '{gsub(".+name |"z, "", $0); print $0}'
fi   
