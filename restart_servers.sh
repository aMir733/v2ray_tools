#!/usr/bin/env bash
# Restarts $SERVICE on all servers in $SERVERS
# Usage: script.sh

# File containing the IP address of all your servers
SERVERS=/root/v2ray_tools/servers
# systemd v2ray service name
SERVICE=v2ray

for server in $(cat "$SERVERS") ; do
	[[ $server == this ]] && { systemctl restart $SERVICE ; continue ;}
	echo "restarting $SERVICE $server"
	ssh root@$server systemctl restart $SERVICE || { echo $server failed to restart ; exit 1 ;}
done
