#!/usr/bin/env bash

SERVERS=/root/v2ray/servers
SERVICE=v2ray@bridge

for server in $(cat "$SERVERS") ; do
	[[ $server == this ]] && { systemctl restart $SERVICE ; continue ;}
	echo "restarting $SERVICE $server"
	ssh root@$server systemctl restart $SERVICE || { echo $server failed to restart ; exit 1 ;}
done
