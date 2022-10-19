#!/usr/bin/env bash
# Checks the logs for IP addresses coming from one user. Don't run this outside of check_client_daemon.sh
# Usage: script.sh /path/to/log/file

# Configuration file
file_config=/etc/v2ray/config.json
# Log file
file_log="$1"
# Where to report naughty users :)
file_strikes=/root/v2ray_tools/strikes
# Where to reports overall usage
file_usage=/root/v2ray_tools/usage
# jq query to get the right inbound
jq_inbound='if .inbounds == null then .inbound[] else .inbounds[] end | select(.protocol=="vmess" or .protocol=="vless")'

cur_all=0
max_all=0
emails="$(cat "$file_config" | sed 's/^ *\/\/.*//' | jq -r "$jq_inbound"'.settings.clients[] | .email')"
echo "----> $(date +%y%m%d_%H%M%S):" | tee -a "$file_usage"
for email in $(echo $emails) ; do
	cur_conn="$(grep -wF "email: $email" "$file_log" | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq | wc -l)"
	max_conn="${email%@*}"
	if ! [[ "$max_conn" =~ ^[0-9]+$ ]] ; then
		echo "${email} ${cur_conn}" | tee -a "$file_usage"
		continue
	fi
	cur_all=$(($cur_conn + $cur_all))
	max_all=$(($max_conn + $max_all))
	[[ $cur_conn > $max_conn ]] && echo "${email#*@} ${cur_conn}/${max_conn}" | tee -a "$file_usage" | tee -a "$file_strikes"
done
echo "Total: $cur_all/$max_all"
echo "<----" | tee -a "$file_usage"
