Monitoring servers remotely with Nmap and 
Ndiff
Combining tools from the Nmap project allows us to set up a simple but powerful monitoring 
system. This can then be used by system administrators monitoring a web server or by 
penetration testers wanting to surveil a remote system.
This recipe describes how to use bash scripting, cron, Nmap, and Ndiff to set up a monitoring 
system that alerts the user by an e-mail if changes are detected in a network.
How to do it...
Create the directory /usr/local/share/nmap-mon/ to store all the necessary files.
Scan your target host and save the results in the directory that you just created.
# nmap -oX base_results.xml -sV -PN <target>
The resulting file base_results.xml will be used as your base file, meaning that it should 
reflect the known "good" versions and ports.
Copy the file nmap-mon.sh into your working directory. 
The output of the scan will be as follows.
#!/bin/bash 
#Bash script to email admin when changes are detected in a network using 
Nmap and Ndiff. 
# 
www.it-ebooks.infoNmap Fundamentals
42
#Don't forget to adjust the CONFIGURATION variables. 
#Paulino Calderon <calderon@websec.mx> 
# 
#CONFIGURATION 
# 
NETWORK="YOURDOMAIN.COM" 
ADMIN=YOUR@EMAIL.COM 
NMAP_FLAGS="-sV -Pn -p- -T4" 
BASE_PATH=/usr/local/share/nmap-mon/ 
BIN_PATH=/usr/local/bin/ 
BASE_FILE=base.xml 
NDIFF_FILE=ndiff.log 
NEW_RESULTS_FILE=newscanresults.xml 
BASE_RESULTS="$BASE_PATH$BASE_FILE" 
NEW_RESULTS="$BASE_PATH$NEW_RESULTS_FILE" 
NDIFF_RESULTS="$BASE_PATH$NDIFF_FILE" 
if [ -f $BASE_RESULTS ] 
then 
 echo "Checking host $NETWORK" 
 ${BIN_PATH}nmap -oX $NEW_RESULTS $NMAP_FLAGS $NETWORK 
 ${BIN_PATH}ndiff $BASE_RESULTS $NEW_RESULTS > $NDIFF_RESULTS
 if [ $(cat $NDIFF_RESULTS | wc -l) -gt 0 ] 
 then 
 echo "Network changes detected in $NETWORK" 
 cat $NDIFF_RESULTS 
 echo "Alerting admin $ADMIN" 
 mail -s "Network changes detected in $NETWORK" $ADMIN < $NDIFF_
RESULTS 
 fi 
fi 
Update the configuration values according to your system.
NETWORK="YOURDOMAIN.COM"
ADMIN=YOUR@EMAIL.COM 
NMAP_FLAGS="-sV -Pn -p- -T4" 
BASE_PATH=/usr/local/share/nmap-mon/ 
BIN_PATH=/usr/local/bin/ 
BASE_FILE=base.xml 
NDIFF_FILE=ndiff.log 
NEW_RESULTS_FILE=newscanresults.xml 
Make nmap-mon.sh executable by entering the following command:
# chmod +x /usr/local/share/nmap-mon/nmap-mon.sh 
You can now run the script nmap-mon.sh to make sure it is working correctly.
# /usr/local/share/nmap-mon/nmap-mon.sh
Launch your crontab editor:
# crontab -e 
Add the following command:
0 * * * * /usr/local/share/nmap-mon/nmap-mon.sh
You should now receive e-mail alerts when Ndiff detects a change in your network.
