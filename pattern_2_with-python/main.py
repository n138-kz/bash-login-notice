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
            'name': sub('\.*', '', os.environ.get('HOSTNAME')),
        },
    },
}

print(json.dumps(config,indent=4))
