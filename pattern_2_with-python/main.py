import os
import sys
from re import sub
import json
import requests

config = {
    'discord': {
        'webhook': {
            'url': 'https://discord.com/api/webhooks/',
        },
        'avatar': {
            'url': 'https://hangstuck.com/wp-content/uploads/2020/08/bash-official-icon-512x512-1.png',
            'name': sub('\.*', '', os.environ.get('HOSTNAME', '')),
        },
    },
    'env': {
        'user': os.environ.get('USER', ''),
        'hostname': os.environ.get('HOSTNAME', ''),
        'ssh_client': os.environ.get('SSH_CLIENT', '').split(sep=' '),
        'SSH_CONNECTION': os.environ.get('SSH_CONNECTION', '').split(sep=' '),
        'term': os.environ.get('TERM', ''),
        'ssh_tty': os.environ.get('SSH_TTY', ''),
        'lang': os.environ.get('LANG', ''),
        'shell': os.environ.get('SHELL', ''),
        'tmout': os.environ.get('TMOUT', ''),
        'path': os.environ.get('PATH', '').split(sep=':'),
    },
    'runner': {
        'config': {
            'loadstate': 0,
        },
    },
}

# 1. load the /etc/discord/login-notice.json
# 2. load the ~/.python/login-notice.json and override
# 3. load the ./login-notice.json and override
config_file = 'login-notice.json'
config_loadstate = 16 # 0b10000
# 0b10000
#   ^^^^^
#   |||||
#   ||||+-  1) エラー扱い
#   |||+--  2) Load succeede ./login-notice.json
#   ||+---  4) Load succeede ~/.python/login-notice.json
#   |+----  8) Load succeede /etc/discord/login-notice.json
#   +----- 16) 桁揃え用（非使用）
config_dir = '/etc/discord/'
if os.path.exists(config_dir+config_file):
    try:
        with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
            config|=json.load(f)
            config_loadstate|=8
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
        pass
config_dir = '~/.python/'
if os.path.exists(config_dir+config_file):
    try:
        with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
            config|=json.load(f)
            config_loadstate|=4
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
        pass
config_dir = './'
if os.path.exists(config_dir+config_file):
    try:
        with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
            config|=json.load(f)
            config_loadstate|=2
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
        pass
try:
    config['runner']['config']['loadstate'] = config_loadstate
except (ValueError, KeyError):
    pass
if config_loadstate^16==0:
    config_loadstate = 1
    print('[Config] No such file or directory: (global, user, temporary)')
    print(f'[{__name__}] Exiting...')
    sys.exit(config_loadstate)

try:
    config['env']['tmout'] = int(config['env']['tmout'])
except (ValueError, KeyError):
    pass

print(json.dumps(config,indent=4))
