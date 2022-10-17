#!/usr/bin/env bash
# Adds a new user
# Usage: script.sh full@email

# Configuration file
file_config=/etc/v2ray/bridge.json
# Where to save the edited configuration file (Used in apply_config.sh)
file_newconfig=/root/v2ray/bridge.json_new
# Path to v2ray binary (leave it as it is if it's in your path)
v2ray=v2ray
# How to generate the uuid
uuid="$($v2ray uuid)"

email="$(grep -F "${1#*@}" "$file_config" | tr -d ' ,"' | sed 's/^email://')"
[[ "$(echo -n "$email" | wc -c)" != 0 ]] && { echo "user exists" ; exit 1 ;}
cp "$file_config" "$file_newconfig"
cat "$file_config" | jq '(.inbounds[] | select(.protocol=="vmess").settings.clients) += [{"id":"'$uuid'","email":"'$1'","level":1,"alterId":0}]' > "$file_newconfig"
