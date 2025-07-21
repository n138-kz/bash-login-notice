import os
import sys
from re import sub
import json
import requests

config = {
    'discord': {
        'webhook':{
            'url': 'https://discord.com/api/webhooks/',
        },
        'avatar':{
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
try:
    config['env']['tmout'] = int(config['env']['tmout'])
except (ValueError, KeyError):
    pass

print(json.dumps(config,indent=4))
