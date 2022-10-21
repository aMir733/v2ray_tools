# What is this?
A bash script to help you manage your v2ray server.

# What does it do?
- Add, view, delete users to/from your config file
- Assign number of devices a user can connect from
- Tells you if a user exceeds the assigned number of devices (by checking the logs and IP addresses)
- Supports load balanced servers

# How do I use it?

### Adding new users
```bash
root@server:~/v2ray_tools# ./v2ray_tools.sh add 1@user1 1@user2 4@user3
root@server:~/v2ray_tools# ./v2ray_tools.sh apply
root@server:~/v2ray_tools# ./v2ray_tools.sh restart
```

### Invalidate a user's UUID (Delete user)
```bash
root@server:~/v2ray_tools# ./v2ray_tools.sh del 1@joe 4@jane
root@server:~/v2ray_tools# ./v2ray_tools.sh apply
root@server:~/v2ray_tools# ./v2ray_tools.sh restart
```

### Get user's QR code and link
```bash
root@server:~/v2ray_tools# ./v2ray_tools.sh get 1@joe -i [ip address] -n [vpn name]
```

### Check for number of devices used by users
```bash
root@server:~/v2ray_tools# ./v2ray_tools.sh check
```

# Example v2ray configuration file
```json
{
  "log": {
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log",
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "port": 80,
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": "4a9cf2fe-aeca-aa7e-15ac-0278983b07e0",
            "email": "3@jane", // 3 is the number of devices allowed for user jane
            "alterId": 0
          },
          {
            "id": "f872bb51-6c2e-6543-95c5-a756aefe21d6",
            "email": "1@joe",
            "alterId": 0
          }
        ],
      "streamSettings": {
        "network": "ws",
        "path": "/",
        "headers": {
          "Host": "aparat.com"
        }
      }
    }
    }
  ],
  "outbound": {
    "protocol": "freedom",
    "settings": {}
  }
}
```

# Last words
![last-words](https://i.imgur.com/wM4U85h.jpg)
