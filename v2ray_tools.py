#!/usr/bin/env python3

from json import loads as jsonloads, dumps as jsondumps, load as jsonload, dump as jsondump
from re import search
from argparse import ArgumentParser as argparse
from base64 import b64encode

default_clinets = "clients.txt"
default_config = "/usr/local/etc/v2ray/config.json"
default_addr = "1.1.1.1"
default_name = "hello_freedom"
default_size = "auto"
default_del = False
default_service = "v2ray"
default_wait = 90


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

    parser_add.set_defaults(func=arg_add)
    parser_get.set_defaults(func=arg_get)
    parser_inv.set_defaults(func=arg_inv)
    parser_res.set_defaults(func=arg_res)
    parser_chk.set_defaults(func=arg_chk)
    args = parser.parse_args()
    args.__dict__.pop('func')(**vars(args))


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

def arg_add(cur,
        users=[], # List of users to add
        ): # <- :)
    for user in users:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", )


def arg_get(user=None, # email or UUID
                ip_address=None, # IP address
                name=None, # VPN name
                qr_size=None): # QR code size: auto|normal|small
    print(kwargs)
    pass

def arg_get(config=None, user=None):
    pass

def arg_res():
    pass

def arg_chk():
    pass

def main():
    parse_args()

if __name__ == '__main__':
    main()
