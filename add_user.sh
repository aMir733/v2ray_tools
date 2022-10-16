#!/usr/bin/env bash

file_config=/etc/v2ray/bridge.json
file_newconfig=/root/v2ray/bridge.json_new
v2ray=v2ray
uuid="$($v2ray uuid)"

email="$(grep -F "${1#*@}" "$file_config" | tr -d ' ,"' | sed 's/^email://')"
[[ "$(echo "$email" | wc -l)" != 0 ]] && { echo "user exists" ; exit 1 ;}
cp "$file_config" "$file_newconfig"
cat "$file_config" | jq '(.inbounds[] | select(.protocol=="vmess").settings.clients) += [{"id":"'$uuid'","email":"'$1'","level":1,"alterId":0}]' > "$file_newconfig"
