#!/usr/bin/env bash

file_config=/etc/v2ray/bridge.json
file_log="$1"
file_strikes=/root/v2ray/strikes

cat "$file_config" | \
	sed 's/^ *\/\/.*//' | \
	jq -r '.inbounds | map(select(.protocol=="vmess"))[].settings.clients[] | .email' | \
	while read email ; do
		cur_conn="$(grep -wF "email: $email" "$file_log" | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq | wc -l)"
		max_conn="${email%@*}"
		if ! [[ "$max_conn" =~ ^[0-9]+$ ]] ; then
			echo "${email} ${cur_conn}"
			continue
		fi
		if [[ "$cur_conn" > $max_conn ]] ; then
			echo "${email#*@} ${cur_conn}/${max_conn}"
			echo "$email" >> "$file_strikes"
		fi
	done

