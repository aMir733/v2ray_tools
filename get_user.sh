#!/usr/bin/env bash

file_config=/etc/v2ray/bridge.json
addr=${2}
c_port="$(cat "$file_config" | jq -r '.inbounds[] | select(.protocol=="vmess").port')"
c_host="$(cat "$file_config" | jq -r '.inbounds[] | select(.protocol=="vmess").streamSettings.headers.Host')"
c_path="$(cat "$file_config" | jq -r '.inbounds[] | select(.protocol=="vmess").streamSettings.path')"
c_net="$(cat "$file_config" | jq -r '.inbounds[] | select(.protocol=="vmess").streamSettings.network')"
email="$(grep -F "$1" "$file_config" | tr -d ' ,"' | sed 's/^email://')"

[[ ${#addr} == 0 ]] && exit 1
[[ "$(echo "$email" | wc -l)" != 1 ]] && { echo "no user or multiple users" ; exit 1 ;}
uuid="$(cat "$file_config" | jq -r '.inbounds[] | select(.protocol=="vmess").settings.clients[] | select(.email=="'$email'").id')"
[[ ${#uuid} == 0 ]] && exit 1
final="vmess://$(echo -n '{"add":"'$addr'","aid":"0","host":"'$c_host'","id":"'$uuid'","net":"'$c_net'","path":"'$c_path'","port":"'$c_port'","ps":"mobileaftab","scy":"none","sni":"","tls":"","type":"","v":"2"}' | base64 --wrap=0)"
clear
qrencode -m 2 -t utf8 <<< "$final"
echo "$final"
cat "$file_config" | jq '.inbounds[] | select(.protocol=="vmess").settings.clients[] | select(.email=="'$email'")'
echo $addr
