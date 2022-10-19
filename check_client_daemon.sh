#/usr/bin/env bash
# Used to log users who are being naughty. Also outputs some usage information in $file_usage (see check_client.sh)
# Usage: script.sh

# Path to the file containing the IP addresses of your servers (use this for currently running server)
SERVERS=/root/v2ray_tools/servers
# Where to put the email address of naughty users
STRIKES=/root/v2ray_tools/strikes
# The directory containing the logs from all of your servers (for the current server there should be a file named access.log in this directory)
# For other servers, you should make a directory called srv123 where 123 is the number your server's IP address ends in
# Your server should also be in the $SERVERS file
# Use lsyncd if you have several servers and want to gather all the logs into this current running server
LOG_DIR=/var/log/v2ray
# Where to store the logs temporarily. Change to a safe location if you're paranoid about security.
DEST=$(mktemp)
# How long to wait for incoming requests for each run
WAIT=90

echo -n '' > $STRIKES
while true ; do
	for server in $(cat $SERVERS) ; do
		if [[ $server == this ]] ; then
			echo -n '' > $LOG_DIR/access.log
			continue
		fi
		ssh root@$server "echo -n '' > $LOG_DIR/access.log"
	done
	i=0
	while [ $i -lt $WAIT ] ; do
		sleep 1
		echo -ne "${i}/${WAIT}\r"
		i=$(($i+1))
	done
	for server in $(cat $SERVERS) ; do
		if [[ $server == this ]] ; then
			cat $LOG_DIR/access.log >> $DEST		
			continue
		fi
		cat $LOG_DIR/srv${server##*.}/access.log >> $DEST
	done
	/root/v2ray_tools/check_client.sh $DEST
	echo '--------------------------'
	rm -f $DEST
done
