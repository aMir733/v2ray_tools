#!/usr/bin/env bash

DIR_SCRIPT="$(dirname -- $0)"
DIR_LOG="/var/log/v2ray"
FILE_CONFIG=/etc/v2ray/config.json
FILE_NEWCONFIG="$DIR_SCRIPT/$(basename -- "$FILE_CONFIG")_new"
FILE_OLDCONFIG="$DIR_SCRIPT/$(basename -- "$FILE_CONFIG")_old"
FILE_DELETED="$DIR_SCRIPT/deleted"
FILE_STRIKES="$DIR_SCRIPT/strikes"
FILE_USAGE="$DIR_SCRIPT/usage"
FILE_SERVERS="$DIR_SCRIPT/servers"
FILE_STRIKES="$DIR_SCRIPT/strikes"
FILE_EXITERROR="/tmp/v2ray_tools_error"
NAME_SERVICE="v2ray@$(basename -- "$FILE_CONFIG" | sed 's/\.[^.]*$//')"
NAME_VPN=
LIST_SERVERS="$DIR_SCRIPT/servers"
PATH_V2RAY=v2ray
QUERY_INBOUND='if .inbounds == null then .inbound else .inbounds[] end | select(.protocol=="vmess" or .protocol=="vless")'


main () {
    [[ -f "$FILE_CONFIG" ]] || output ERROR "Could not find configuration file $FILE_CONFIG"
    if [[ "$1" =~ ^- ]] ;then
        output WARNING "Skipping $1. Please specify the flags after the main parameter"
    else
        case "$1" in
            get) shift ; get_user $@ ;;
            add) shift ; add_user $@ ;;
            del) shift ; del_user $@ ;;
            check) shift ; check $@ ;;
            apply) shift ; apply ;;
            restart) shift ; restart_v2ray ;;
            *) output ERROR "Unknown parameter: $1"
        esac
    fi
}

parse_args () {
    while [[ "$#" -gt 0 ]]; do
        if [[ "$1" =~ ^- ]] ; then
            case "$1" in
                -i|--ip-address) [[ "$2" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] && addr="$2" || output ERROR "Not an IP address: $2" ; shift ;;
                -n|--vpn-name) vpn_name="$2" ; shift ;;
                -q|--qr-size) [[ "$2" =~ ^[1-2]$ ]] && qr_size="$2" || output ERROR "$1 $2 is not valid. $1 should be set to either 1 or 2" ; shift ;;
                -w|--wait) [[ "$2" =~ ^[0-9]+[sm]?$ ]] && wait_time=$2 || output ERROR "$1 $2 is not valied. $1 should be set to an integer (optionally followed by either m or s)" ; shift ;;
                -a|--all) all=1 ; shift ;;
                *) output WARNING "Unknown parameter passed: $1" ;;
            esac
        else
            args+=("$1")
        fi
        shift
    done
}

output() {
    echo "$0 [$1]: $2"
    case $1 in
        ERROR) touch "$FILE_EXITERROR" ; exit 1 ;;
        ASK) read -p "(Y/n): " answer && [[ ${#answer} == 0 ]] || [[ $answer == [Yy] ]] || exit 1 ;;
    esac
}

# Outputs user's information in QR code and a link ready to be used in a v2ray client (shadowlink, v2rayng, nekoray)
# Usage: ... -s [IP address] -n [VPN Name on client's phone/computer]
get_user() {
    parse_args $@
    [[ ${#vpn_name} == 0 ]] && vpn_name="$NAME_VPN"
    [[ ${#vpn_name} == 0 ]] && { output WARNING "No VPN Name was set. Using the default name (server)" ; vpn_name=server ;}
    [[ ${#addr} == 0 ]] && output ERROR "No IP address was set."
    [[ ${#qr_size} == 0 ]] && [[ $(tput cols) < 65 ]] && qr_size=1 || qr_size=2
    for user in ${args[@]} ; do
        echo $user
        email="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email | test("'"$user"'")).email' "$FILE_CONFIG")"
        for i in $email ; do output INFO "Found $email" ; done
        [[ $(wc -l <<< "$email") != 1 ]] && output ERROR "No user was found. Or multiple users were found."
        c_port="$(jq -r "${QUERY_INBOUND}.port" "$FILE_CONFIG")"
        c_host="$(jq -r "${QUERY_INBOUND}.streamSettings.headers.Host" "$FILE_CONFIG")"
        c_path="$(jq -r "${QUERY_INBOUND}.streamSettings.path" "$FILE_CONFIG")"
        c_net="$(jq -r "${QUERY_INBOUND}.streamSettings.network" "$FILE_CONFIG")"
        uuid="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email=="'"$email"'").id' "$FILE_CONFIG")"
        [[ ${#uuid} == 0 ]] && output ERROR "No UUID was set for user $email"
        final="vmess://$(base64 -w 0 <<< '{"add":"'$addr'","aid":"0","host":"'$c_host'","id":"'$uuid'","net":"'$c_net'","path":"'$c_path'","port":"'$c_port'","ps":"'$vpn_name'","scy":"none","sni":"","tls":"","type":"","v":"2"}')"
        qrencode -m "$qr_size" -t utf8 <<< "$final"
        echo "$final"
        jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email=="'"$email"'")' "$FILE_CONFIG"
        output INFO "Assigned IP address: $addr"
    done
}

# Adds a new user to the configuration file
add_user() {
    parse_args $@
    check_unapplied
    [[ -f "$FILE_NEWCONFIG" ]] && cmp -s -- "$FILE_CONFIG" "$FILE_NEWCONFIG" \
        || output ASK "You have un-applied configuration file located at $FILE_NEWCONFIG. Are you sure you want to continue?"
    cp "$FILE_CONFIG" "$FILE_NEWCONFIG"
    for user in ${args[@]} ; do
        [[ "$user" =~ ^[0-9]+@.+ ]] || output WARNING "Skipping $user: not valid"
        grep -wF "${user#*@}" "$FILE_NEWCONFIG" && output ERROR "User $user exists"
        uuid="$($V2RAY uuid)"
        cat "$FILE_NEWCONFIG" \
            | jq -r '('"$QUERY_INBOUND"'.settings.clients) += [{"id":"'$uuid'","email":"'$user'","level":1,"alterId":0}]' \
            | tee "$FILE_NEWCONFIG" >/dev/null
    done
}

# Invalidates a user's UUID.
del_user() {
    check_unapplied
    cp "$FILE_CONFIG" "$FILE_NEWCONFIG"
    for user in ${args[@]} ; do
        email="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email | test("'"$user"'")).email' "$FILE_NEWCONFIG")"
        for i in $email ; do output INFO "found $email" ; done
        [[ $(wc -l <<< "$email") != 1 ]] && output ERROR "No user was found. Or multiple users were found."
        user_jq="$QUERY_INBOUND"'.settings.clients[] | select(.email=="'$email'")'
        uuid_old="$(jq -r "${user_jq}.id" "$FILE_NEWCONFIG")"
        uuid_new="$($V2RAY uuid)"
        jq -r '('"$user_jq"').id = "'"$uuid_new"'"' "$FILE_NEWCONFIG" | tee "$FILE_NEWCONFIG" >/dev/null
        echo "$email $uuid_old" >> ${FILE_DELETED}_pending
    done
}

# Simply applies the configuration file located at $FILE_NEWCONFIG to $FILE_CONFIG
apply() {
    [[ -f "$FILE_EXITERROR" ]] && { rm -f "$FILE_EXITERROR"; output ASK "Last run was not successful. Are you sure you want to continue?" ;}
    cp "$FILE_CONFIG" "$FILE_OLDCONFIG"
    cp "$FILE_NEWCONFIG" "$FILE_CONFIG"
    cat "${FILE_DELETED}_pending" >> "$FILE_DELETED"
    :> "${FILE_DELETED}_pending"
}

# Used to log the number of devices used by each email.
check() {
    # The directory containing the logs from all of your servers (for the current server there should be a file named access.log in this directory)
    # For other servers, you should make a directory called srv123 where 123 is the number your server's IP address ends in
    # Your server should also be in the $SERVERS file
    # Use lsyncd if you have several servers and want to gather all the logs into this current running server
    parse_args $@
    dest="$DIR_SCRIPT/access.log_temp"
    [[ ${#wait_time} == 0 ]] && wait_time=90
    [[ "$(jq -Mr '.log.access' "$FILE_CONFIG")" != "$DIR_LOG/access.log" ]] && \
        output ERROR "Your access log is not set to $DIR_LOG/access.log . Please make sure you create the $DIR_LOG directory first before changing it in your configuration file"
    [[ -f "$FILE_SERVERS" ]] || \
        { output WARNING "You did not create the servers file: $FILE_SERVERS. Creating one for you..." ; echo this > "$FILE_SERVERS" ;}
    
    :> $STRIKES
    while true ; do
            for server in "$(cat "$FILE_SERVERS")" ; do
                    if [[ $server == this ]] ; then
                            :> $DIR_LOG/access.log
                            continue
                    fi
                    ssh root@$server "echo -n '' > $DIR_LOG/access.log"
            done
            i=0 ; while [ $i -lt $WAIT ] ; do
                    sleep 1
                    echo -ne "${i}/${WAIT}\r"
                    i=$(($i+1))
            done
            for server in "$(cat "$FILE_SERVERS")" ; do
                    if [[ $server == this ]] ; then
                            cat $DIR_LOG/access.log >> $dest
                            continue
                    fi
                    cat $DIR_LOG/srv${server##*.}/access.log >> $dest
            done
            cur_all=0
            max_all=0
            emails="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | .email' "$FILE_CONFIG")"
            echo "----> $(date +%y%m%d_%H%M%S):" | tee -a "$FILE_USAGE"
            for email in "$emails" ; do
                    cur_conn="$(grep -wF "email: $email" "$dest" | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq | wc -l)"
                    max_conn="${email%@*}"
                    if ! [[ "$max_conn" =~ ^[0-9]+$ ]] ; then
                            echo "${email} ${cur_conn}" | tee -a "$file_usage"
                            continue
                    fi
                    cur_all=$(($cur_conn + $cur_all)) ; max_all=$(($max_conn + $max_all))
                    final="${email#*@} ${cur_conn}/${max_conn}"
                    [[ $all == 1 ]] && echo "$final"
                    [[ $cur_conn > $max_conn ]] && echo "$final" | tee -a "$FILE_USAGE" | tee -a "$FILE_STRIKES" 
            done
            echo "Total: $cur_all/$max_all" | tee -a "$FILE_USAGE"
            echo "<----" | tee -a "$FILE_USAGE"
            :> "$dest"
    done
}

# Restarts v2ray's service on all servers in servers file
restart_v2ray() {
    for server in "$(cat "$FILE_SERVERS")" ; do
            output INFO "Restarting $NAME_SERVICE on $server server"
            [[ $server == this ]] && { systemctl restart $NAME_SERVICE ; continue ;}
            ssh root@$server systemctl restart $NAME_SERVICE || { output WARNING "Skipping $server: failed to restart" ;}
    done
}

check_unapplied() {
    [[ -f "$FILE_NEWCONFIG" ]] && cmp -s -- "$FILE_CONFIG" "$FILE_NEWCONFIG" \
        || output ASK "You have un-applied configuration file located at $FILE_NEWCONFIG. Are you sure you want to continue?"
}

main $@
