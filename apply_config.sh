#!/usr/bin/env bash

file_config=/etc/v2ray/bridge.json
file_newconfig=/root/v2ray/bridge.json_new
file_oldconfig=/root/v2ray/bridge.json_old
file_deleted=/root/v2ray/deleted

cp "$file_config" "$file_oldconfig"
cp "$file_newconfig" "$file_config"
cat "${file_deleted}_pending" >> "$file_deleted"
