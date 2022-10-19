#!/usr/bin/env bash
# Invalidates a user's UUID.
# Usage: script.sh partial@email

# Configuration file
file_config=/etc/v2ray/config.json
# Where to save the edited configuration file (Used in apply_config.sh)
file_newconfig=/root/v2ray_tools/config.json_new
# Where to save pending deleted users (Used in apply_config.sh)
file_deleted=/root/v2ray_tools/deleted_pending
# Path to v2ray
v2ray=v2ray
# How to generate the uuid
uuid_new="$($v2ray uuid)"
# jq query to get the right inbound
jq_inbound='if .inbounds == null then .inbound else .inbounds[] end | select(.protocol=="vmess" or .protocol=="vless")'

email="$(grep -F "$1" "$file_config" | tr -d ' ,"' | sed 's/^email://')"
[[ "$(echo "$email" | wc -l)" != 1 ]] && { echo "no user or multiple users" ; exit 1 ;}

user_jq="$jq_inbound"'.settings.clients[] | select(.email=="'$email'")'
uuid_old="$(cat "$file_config" | jq -r "${user_jq}.id")"
cat "$file_config" | jq '('"$user_jq"').id = "'"$uuid_new"'"' > "$file_newconfig" || exit 1
echo -n '' > $file_deleted
echo "$email $uuid_old" >> $file_deleted
echo "user $email was deleted"
