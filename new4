#!/bin/bash

clear
if [ "$1" == "--help" ]; then
  echo " Usage :- ./`basename $0` "
  exit 0
fi
if [ "$1" == "-h" ]; then
  echo " Usage :- ./`basename $0` "
  exit 0
fi
echo
echo -e "\e[93m Hello ${USER}, its me @webcipher101 \e[00m"
echo "<< your work in progress please wait for some time >>"
echo 
read -p " [+] Enter you domains file path Here : " path
sleep 1
echo " [+] URL enumeration started ,please wait for some time "
sleep 1
cat $path | waybackurls | tee way.txt
sleep 1
cat $path | gau | tee gau.txt
sleep 1
cat way.txt >> gau.txt
sleep 1
cat gau.txt | uro >> uro.txt
sleep 1
sort uro.txt | uniq >> $path.txt
rm -rf way.txt gau.txt uro.txt
mkdir output
mv $path.txt $PWD/output
