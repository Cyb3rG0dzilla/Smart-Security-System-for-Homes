#! /bin/bash

#start script
figlet -f slant.tlf "#recon-map"
echo -e "\e[33m by: @ WebCipher101"

# check root usage
if [[ "${UID}" -eq 0 ]]
then
    echo -e "\e[32m >>> you are root ,go ahead..!!**"
else
    echo -e "\e[91m >>> warning : your not root user."
fi

sleep 2
im=${USER}

echo -e "\e[37m><><>< HEY $im i will take 10 to 15 min to complete your task ><><><"
sleep 2
# get input from user
echo -e "\e[92m >>> Enter your target domain : "

# read input or domain name
read target

# make specific directory based on domain name
mkdir $target
echo " >>> your target name is >>> $target"
sleep 2

echo -e "\e[37m          *** initial recon is started    ***     "
# using nmap for port scanning
echo -e "\e[37m          *** Nmap is started             ***     "
sudo nmap -open $target >> nmap-output.txt
sleep 20

sleep 10

# whois for more info about target
echo "          *** whois lookup is started    ***       "
whois $target >> whois-output.txt

sleep 7

# nslookup for checking dnsrecord
echo "          *** nslookup is started        ***       "
nslookup $target >> dns-record.txt

sleep 7

# find emails,host,ip using theHarvester
echo "          *** theHarvester is started    ***       "
theHarvester -d $target >> theHarvester.txt

sleep 10

mypwd=${PWD}

sleep 2

#moving all outputs to specific folder
sudo mv nmap-output.txt $mypwd/$target/
sleep 2
sudo mv whois-output.txt $mypwd/$target/
sleep 2
sudo mv dns-record.txt $mypwd/$target/
sleep 2
sudo mv theHarvester.txt $mypwd/$target/
