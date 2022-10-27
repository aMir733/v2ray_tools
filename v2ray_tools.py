#!/usr/bin/env python3

from json import loads as jsonloads, dumps as jsondumps, load as jsonload, dump as jsondump
from re import search
from argparse import ArgumentParser as argparse
from base64 import b64encode

default_config = "/usr/local/etc/v2ray/config.json"
default_addr = "1.1.1.1"
default_name = "hello_freedom"
default_size = "auto"
default_del = False
default_service = "v2ray"
default_wait = 90

def _output(level, message):
    if level == 0: # Error
        parser.print_help()
        print("Error:\n\t")
        print(message)
        exit(1)
    elif level == 1: # Warning
        print("[Warning]: " + message)
    elif level == 2: # Info
        print("[Info]: " + message)


def parse_args():
    global parser
    parser = argparse(description='Manage your v2ray config file and its users')
    subparser = parser.add_subparsers(help='Action to take', required=True)
    parser_add = subparser.add_parser('add', help='Add a new user')
    parser_get = subparser.add_parser('get', help='Get user\'s client information')
    parser_inv = subparser.add_parser('invalidate', help='Invalidate a user\'s UUID')
    parser_res = subparser.add_parser('restart', help='Restart the servers')
    parser_chk = subparser.add_parser('check', help='Run user checks')

    # global arguments
    parser.add_argument('-c', '--config', type=str, default=default_config, help='v2ray\'s configuration file. Default: ' + default_config)
    # add arguments
    parser_add.add_argument('users', nargs='+', help='List of users emails to register')
    # get arguments
    parser_get.add_argument('user', type=str, help='User\'s email or UUID')
    parser_get.add_argument('-i', '--ip-address', type=str, default=default_addr, help='IP address for client\'s config file. Default: ' + default_addr)
    parser_get.add_argument('-n', '--name', type=str, default=default_name, help='Name/remark for clients\'s config file. Default: ' + default_name)
    parser_get.add_argument('-q', '--qr-size', type=str, default=default_size, help='Size of the QR code outputted to the screen. Default: ' + default_size)
    # inv arguments
    parser_inv.add_argument('user', type=str, help='User\'s email or UUID')
    parser_inv.add_argument('-d', '--delete-user', action='store_true', default=default_del, help='Deletes the user entirely instead of just invalidating their UUID. Default: ' + str(default_addr))
    # res arguments
    parser_res.add_argument('servers', nargs='+', help='List of servers to restart.')
    parser_res.add_argument('-s', '--service-name', type=str, default=default_service, help='Name of the systemd service on the servers. Default: ' + default_service)
    # chk arguments
    parser_chk.add_argument('-w', '--wait-time', type=int, default=default_wait, help='How long to wait for incoming requests between each run (in seconds). Default: ' + str(default_wait))
    parser_chk.add_argument('-a', '--show-all', action='store_true', default=False, help='Whether to output every user or not. Default: ' + str(False))

    parser_add.set_defaults(func=action_add)
    parser_get.set_defaults(func=action_get)
    parser_inv.set_defaults(func=action_inv)
    parser_res.set_defaults(func=action_res)
    parser_chk.set_defaults(func=action_chk)
    args = parser.parse_args()
    args.__dict__.pop('func')(**vars(args))


def find_inbound(js): # Finds the required inbound for the script to work
    if 'inbound' in js:
        if js['inbound']['settings']['clients'][0]['email'].startswith("admin@"):
            return ('inbound', 'settings', 'clients')
    elif 'inbounds' in js:
        i = 0
        for inbound in js['inbounds']:
            i = i + 1
            if inbound['protocol'] != 'vless' and inbound['protocol'] != 'vmess':
                continue
            if not inbound['settings']['clients'][0]['email'].startswith("admin@"):
                continue
            return ('inbounds', i-1, 'settings', 'clients')
    else:
        _output(0, "No inbound in configuration file")
    _output(0, """Invalid configuration file. 
    Your inbound/inbounds need to have either vmess or vless also
    your first user should have the admin@v2ray_tools email.
    Example: -> inbound/inbounds -> vmess/vless -> settings -> clients -> [0] -> email == admin@whatever""")
    
def get_inbound(config, path):
    with open(config, 'r') as config:
        js = jsonload(config)
    for path in find_inbound(js):
        js = js[path]
    return js

def write_inbound(config, path, inbound):
    with open(config, 'rw') as config:
        js = jsonload(config)
        for path in find_inbound(js):

def action_add(config=None, # Path to v2ray's configuration file
                users=None): # List of emails


def action_get(config=None, # Path to v2ray's configuration file
                user=None, # email or UUID
                ip_address=None, # IP address
                name=None, # VPN name
                qr_size=None): # QR code size: auto|normal|small
    print(kwargs)
    pass

def action_inv(config=None, user=None):
    pass

def action_res():
    pass

def action_chk():
    pass

def main():
    parse_args()

if __name__ == '__main__':
    main()

#DIR_SCRIPT="/root/v2ray_tools"
#DIR_LOG="/var/log/v2ray"
#FILE_CONFIG=/etc/v2ray/config.json
#FILE_NEWCONFIG="$DIR_SCRIPT/$(basename -- "$FILE_CONFIG")_new"
#FILE_OLDCONFIG="$DIR_SCRIPT/$(basename -- "$FILE_CONFIG")_old"
#FILE_DELETED="$DIR_SCRIPT/deleted"
#FILE_STRIKES="$DIR_SCRIPT/strikes"
#FILE_USAGE="$DIR_SCRIPT/usage"
#FILE_EXITERROR="/tmp/v2ray_tools_error"
## --- DEFAULT FLAGS ---
#FLAG_ADDRESS=1.1.1.1
#FLAG_NAME="$(basename -- "$FILE_CONFIG" | sed 's/\.[^.]*$//')"
#FLAG_SECURITY=none
#FLAG_QRSIZE=0
#FLAG_WAITTIME=90
#FLAG_ALLUSERS=0
## --- DEFAULT FLAGS ---
#NAME_SERVICE="v2ray@$(basename -- "$FILE_CONFIG" | sed 's/\.[^.]*$//')"
#LIST_SERVERS=(this)
#PATH_V2RAY=v2ray
#QUERY_INBOUND='if .inbounds == null then .inbound else .inbounds[] end | select(.protocol=="vmess" or .protocol=="vless")'
#
#
#main () {
#    [[ -f "$DIR_SCRIPT" ]] && output ERROR "Invalid directory: $DIR_SCRIPT"
#    [[ -d "$DIR_SCRIPT" ]] || output INFO "Creating directory: $DIR_SCRIPT"
#    [[ $# -eq 0 ]] && output HELP "Nothing to do!"
#    dep_check
#    if [[ "$1" =~ ^- ]] ; then
#        output HELP "Unknown parameter: $1"
#    else
#        case "$1" in
#            get) shift ; get_user $@ ;;
#            add) shift ; add_user $@ ;;
#            del) shift ; del_user $@ ;; 
#            check) shift ; check $@ ;; 
#            apply) shift ; apply ;; 
#            restart) shift ; restart_v2ray ;;
#            *) output HELP "Unknown parameter: $1"
#        esac
#    fi
#    rm -f "$FILE_EXITERROR"
#}
#
#parse_args () {
#    while [[ "$#" -gt 0 ]]; do
#        if [[ "$1" =~ ^- ]] ; then
#            case "$1" in
#                -i|--ip-address) [[ "$2" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] && FLAG_ADDRESS="$2" || output ERROR "Not an IP address: $2" ; shift ;;
#                -n|--vpn-name) FLAG_NAME="$2" ; shift ;;
#                -q|--qr-size) [[ "$2" =~ ^[0-2]$ ]] && FLAG_QRSIZE="$2" || output HELP "$1 $2 is not valid. $1 should be between 0-2." ; shift ;;
#                -w|--wait) [[ "$2" =~ ^[0-9]+$ ]] && FLAG_WAITTIME="$2" || output HELP "$1 $2 is not valied. $1 should be set to an integer" ; shift ;;
#                -a|--all) FLAG_ALLUSERS=1 ;;
#                *) output HELP "Unknown parameter passed: $1" ;;
#            esac
#        else
#            args+=("$1")
#        fi
#        shift
#    done
#}
#
#output() {
#    echo "[$1]: $2"
#    case $1 in
#        ERROR) touch "$FILE_EXITERROR" ; exit 1 ;;
#        HELP) print_usage ; exit 1 ;;
#        ASK) read -p "(Y/n): " answer && [[ ${#answer} == 0 ]] || [[ $answer == [Yy] ]] || exit 1 ;;
#    esac
#}
#
## Outputs user's information in QR code and a link ready to be used in a v2ray client (shadowlink, v2rayng, nekoray)
## Usage: ... -s [IP address] -n [VPN Name on client's phone/computer]
#get_user() {
#    parse_args $@
#    [[ -f "$FILE_CONFIG" ]] || output ERROR "Could not find configuration file $FILE_CONFIG"
#    [[ "${FLAG_QRSIZE}" == 0 ]] && { [[ $(tput cols) -lt 65 ]] && FLAG_QRSIZE=1 || FLAG_QRSIZE=2 ;}
#    for user in ${args[@]} ; do
#        email="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email | test("'"$user"'")).email' "$FILE_CONFIG")"
#        [[ $(echo -n "$email" | grep -c "^") != 1 ]] && { output INFO "Skipping $user: No user was found or multiple users were found." ; continue ;}
#        for i in $email ; do output INFO "Found $email" ; done
#        c_port="$(jq -r "${QUERY_INBOUND}.port" "$FILE_CONFIG")"
#        c_host="$(jq -r "${QUERY_INBOUND}.streamSettings.headers.Host" "$FILE_CONFIG")"
#        c_path="$(jq -r "${QUERY_INBOUND}.streamSettings.path" "$FILE_CONFIG")"
#        c_net="$(jq -r "${QUERY_INBOUND}.streamSettings.network" "$FILE_CONFIG")"
#        uuid="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email=="'"$email"'").id' "$FILE_CONFIG")"
#        [[ ${#uuid} == 0 ]] && output ERROR "No UUID was set for user $email"
#        # TODO: Output vless link if protocol is set to vless
#        final="$(base64 -w 0 <<< '{"add":"'$FLAG_ADDRESS'","aid":"0","host":"'$c_host'","id":"'$uuid'","net":"'$c_net'","path":"'$c_path'","port":"'$c_port'","ps":"'$FLAG_NAME'","scy":"'$FLAG_SECURITY'","sni":"","tls":"","type":"","v":"2"}')"
#        echo -n "vmess://${final}" | qrencode -o - -m "$FLAG_QRSIZE" -t utf8
#        echo "vmess://${final}"
#        echo -n "$final" | base64 -d | jq -c
#    done
#}
#
## Adds a new user to the configuration file
#add_user() {
#    parse_args $@
#    [[ -f "$FILE_CONFIG" ]] || output ERROR "Could not find configuration file $FILE_CONFIG"
#    check_unapplied
#    cp "$FILE_CONFIG" "$FILE_NEWCONFIG"
#    for user in ${args[@]} ; do
#        [[ "$user" =~ ^[0-9]+@.+ ]] || output WARNING "Skipping $user: not valid"
#        grep -qwF "${user#*@}" "$FILE_NEWCONFIG" && { output INFO "Skipping user $user: User exists" ; continue ;}
#        uuid="$($PATH_V2RAY uuid)"
#        jq -r '('"$QUERY_INBOUND"'.settings.clients) += [{"id":"'$uuid'","email":"'$user'","level":1,"alterId":0}]' "$FILE_NEWCONFIG" > "${FILE_NEWCONFIG}_temp"
#        mv "${FILE_NEWCONFIG}_temp" "$FILE_NEWCONFIG"
#    done
#}
#
## Invalidates a user's UUID.
#del_user() {
#    parse_args $@
#    [[ -f "$FILE_CONFIG" ]] || output ERROR "Could not find configuration file $FILE_CONFIG"
#    check_unapplied
#    cp "$FILE_CONFIG" "$FILE_NEWCONFIG"
#    for user in ${args[@]} ; do
#        email="$(jq -r "$QUERY_INBOUND"'.settings.clients[] | select(.email | test("'"$user"'")).email' "$FILE_NEWCONFIG")"
#        [[ $(echo -n "$email" | grep -c "^") != 1 ]] && { output INFO "Skipping $user: No user was found or multiple users were found." ; continue ;}
#        for i in $email ; do output INFO "Found $email" ; done
#        user_jq="$QUERY_INBOUND"'.settings.clients[] | select(.email=="'$email'")'
#        uuid_old="$(jq -r "${user_jq}.id" "$FILE_NEWCONFIG")"
#        uuid_new="$($PATH_V2RAY uuid)"
#        jq -r '('"$user_jq"').id = "'"$uuid_new"'"' "$FILE_NEWCONFIG" > "${FILE_NEWCONFIG}_tmp"
#        mv "${FILE_NEWCONFIG}_tmp" "$FILE_NEWCONFIG"
#        echo "$email $uuid_old" >> ${FILE_DELETED}_pending
#    done
#}
#
## Simply applies the configuration file located at $FILE_NEWCONFIG to $FILE_CONFIG
#apply() {
#    [[ -f "$FILE_CONFIG" ]] || output ERROR "Could not find configuration file $FILE_CONFIG"
#    [[ -f "$FILE_EXITERROR" ]] && { rm -f "$FILE_EXITERROR"; output ASK "Last run was not successful. Are you sure you want to continue?" ;}
#    cp "$FILE_CONFIG" "$FILE_OLDCONFIG"
#    cp "$FILE_NEWCONFIG" "$FILE_CONFIG"
#    if [[ -f "${FILE_DELETED}_pending" ]] ; then
#        cat "${FILE_DELETED}_pending" >> "$FILE_DELETED"
#        :> "${FILE_DELETED}_pending"
#    fi
#}
#
## Used to log the number of devices used by each email.
#check() {
#    # The directory containing the logs from all of your servers (for the current server there should be a file named access.log in this directory)
#    # For other servers, you should make a directory called srv123 where 123 is the number your server's IP address ends in
#    # Your server should also be in the $SERVERS file
#    # Use lsyncd if you have several servers and want to gather all the logs into this current running server
#    parse_args $@
#    [[ -f "$FILE_CONFIG" ]] || output ERROR "Could not find configuration file $FILE_CONFIG"
#    dest="$DIR_SCRIPT/access.log_temp"
#    [[ "$(jq -Mr '.log.access' "$FILE_CONFIG")" != "$DIR_LOG/access.log" ]] && \
#        output ERROR "Your access log is not set to $DIR_LOG/access.log . Please make sure you create the $DIR_LOG directory first before changing it in your configuration file"
#    
#    :> $FILE_STRIKES
#    while true ; do
#            for server in ${LIST_SERVERS[@]} ; do
#                    if [[ $server == this ]] ; then
#                            :> $DIR_LOG/access.log
#                            continue
#                    fi
#                    ssh root@$server "echo -n '' > $DIR_LOG/access.log"
#            done
#            i=0 ; while [ $i -lt $FLAG_WAITTIME ] ; do
#                    sleep 1
#                    echo -ne "${i}/${FLAG_WAITTIME}\r"
#                    i=$(($i+1))
#            done
#            for server in ${LIST_SERVERS[@]} ; do
#                    if [[ $server == this ]] ; then
#                            cat $DIR_LOG/access.log >> $dest
#                            continue
#                    fi
#                    cat $DIR_LOG/srv${server##*.}/access.log >> $dest
#            done
#            cur_all=0
#            max_all=0
#            echo "----> $(date +%y%m%d_%H%M%S):" | tee -a "$FILE_USAGE"
#            for email in $(jq -r "$QUERY_INBOUND"'.settings.clients[] | .email' "$FILE_CONFIG") ; do
#                    cur_conn="$(grep -wF "email: $email" "$dest" | cut -d' ' -f3 | cut -d':' -f1 | sort | uniq | wc -l)"
#                    max_conn="${email%@*}"
#                    if ! [[ "$max_conn" =~ ^[0-9]+$ ]] ; then
#                            echo "${email} ${cur_conn}" | tee -a "$FILE_USAGE"
#                            continue
#                    fi
#                    cur_all=$(($cur_conn + $cur_all)) ; max_all=$(($max_conn + $max_all))
#                    final="${email#*@} ${cur_conn}/${max_conn}"
#                    [[ "$FLAG_ALLUSERS" == 1 ]] && echo "$final"
#                    [[ $cur_conn > $max_conn ]] && echo "$final" | tee -a "$FILE_USAGE" | tee -a "$FILE_STRIKES" 
#            done
#            echo "Total: $cur_all/$max_all" | tee -a "$FILE_USAGE"
#            echo "<----" | tee -a "$FILE_USAGE"
#            :> "$dest"
#    done
#}
#
## Restarts v2ray's service on all servers in servers file
#restart_v2ray() {
#    for server in ${LIST_SERVERS[@]} ; do
#            output INFO "Restarting $NAME_SERVICE on $server server"
#            [[ $server == this ]] && { systemctl restart $NAME_SERVICE ; continue ;}
#            ssh root@$server systemctl restart $NAME_SERVICE || { output WARNING "Skipping $server: failed to restart" ;}
#    done
#}
#
#check_unapplied() {
#    [[ -f "$FILE_NEWCONFIG" ]] && { cmp -s -- "$FILE_CONFIG" "$FILE_NEWCONFIG" \
#        || output ASK "You have un-applied configuration file located at $FILE_NEWCONFIG. Are you sure you want to continue?" ;}
#}
#
#print_usage() {
#    printf "%b" "Usage: ${0} [command] [-inqwa]\n\tcommand)\n\t\tadd) Add new users\n\t\tdel) Invalidate users UUID\n\t\tget) Get user's QR code and link\n\t\tapply) Applies the configuration located at ${FILE_NEWCONFIG} to ${FILE_CONFIG}\n\t\tcheck) Checks the logs and outputs the number of devices used by each user\n\t\terestart) Restarts the v2ray service for servers listed in ${FILE_SERVERS} (use 'this' for current running server)\n\tFlags)\n\t\t-i|--ip-address) IP address of the server to set in the QR code and the link given to the user. Default: ${FLAG_ADDRESS}\n\t\t-n|--vpn-name) A name to set in the QR code and the link given to the user. Default: ${FLAG_NAME}\n\t\t-q|--qr-size) The size of the QR code outputted to the screen. Between 0-2. Set to 0 to detect the screen's size automatically. Default: ${FLAG_QRSIZE}\n\t\t-w|--wait) How long to wait for incoming requests to capture the IP addresses of users (in seconds). Used in the check function. Default: ${FLAG_WAITTIME}\n\t\t-a|--all) Output every user even the ones who haven't exceeded the allowed number of devices. Used in the check function.\n\n"
#}
#
#dep_check() {
#    command -v v2ray >/dev/null || output ERROR "v2ray not found in your PATH"
#    command -v jq qrencode >/dev/null || output ERROR "This script depends on 'jq' and 'qrencode'. Please install them first."
#}
#
#main $@
