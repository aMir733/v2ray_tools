#/usr/bin/env bash

SERVERS=/root/v2ray/servers
LOG_DIR=/var/log/v2ray
DEST=$(mktemp)
WAIT=120

while true ; do
	for server in $(cat $SERVERS) ; do
		if [[ $server == this ]] ; then
			echo "" > $LOG_DIR/access.log
			continue
		fi
		ssh root@$server "echo > $LOG_DIR/access.log"
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
	/root/v2ray/check_client.sh $DEST
	rm -f $DEST
done
