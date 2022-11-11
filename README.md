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

#### [Example v2ray configuration](example_config.json)
```

# Last words
![last-words](https://i.imgur.com/wM4U85h.jpg)
