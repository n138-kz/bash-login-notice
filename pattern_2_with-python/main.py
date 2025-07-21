import os
import sys
from re import sub
import json
import math
import datetime
import requests

# config
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
        'os_dependent': {
            'linux': {
                'common': {
                    'ssh_client': os.environ.get('SSH_CLIENT', '').split(sep=' '),
                    'ssh_connection': os.environ.get('SSH_CONNECTION', '').split(sep=' '),
                    'term': os.environ.get('TERM', ''),
                    'ssh_tty': os.environ.get('SSH_TTY', ''),
                    'lang': os.environ.get('LANG', ''),
                    'shell': os.environ.get('SHELL', ''),
                    'tmout': os.environ.get('TMOUT', ''),
                    'path': os.environ.get('PATH', '').split(sep=':'),
                    'home': os.environ.get('HOME', ''),
                    'user': os.environ.get('USER', ''),
                    'pwd': os.environ.get('PWD', ''),
                    'oldpwd': os.environ.get('OLDPWD', ''),
                    'hostname': os.environ.get('HOSTNAME', ''),
                    'histsize': os.environ.get('HISTSIZE', ''),
                    'histfilesize': os.environ.get('HISTFILESIZE', ''),
                    'logname': os.environ.get('LOGNAME', ''),
                    'mail': os.environ.get('MAIL', ''),
                    'editor': os.environ.get('EDITOR', ''),
                    'pager': os.environ.get('PAGER', ''),
                },
                'debian': {
                    'debian_frontend': os.environ.get('DEBIAN_FRONTEND', ''),
                    'ls_colors': os.environ.get('LS_COLORS', ''),
                },
                'redhat': {
                    'cvs_rsh': os.environ.get('CVS_RSH', ''),
                    'xdg_runtime_dir': os.environ.get('XDG_RUNTIME_DIR', ''),
                    'dbus_session_bus_address': os.environ.get('DBUS_SESSION_BUS_ADDRESS', ''),
                },
            },
            'windows': {
                'system': {
                    'systemroot': os.environ.get('SystemRoot', ''),
                    'windir': os.environ.get('windir', ''), # SystemRootと同じ値であることが多い
                    'systemdrive': os.environ.get('SystemDrive', ''),
                    'path': os.environ.get('PATH', ''),
                    'pathext': os.environ.get('PATHEXT', ''),
                    'comspec': os.environ.get('ComSpec', ''),
                    'programfiles': os.environ.get('ProgramFiles', ''),
                    'programfiles(x86)': os.environ.get('ProgramFiles(x86)', ''),
                    'commonprogramfiles': os.environ.get('CommonProgramFiles', ''),
                    'commonprogramfiles(x86)': os.environ.get('CommonProgramFiles(x86)', ''),
                    'programdata': os.environ.get('ProgramData', ''),
                    'allusersprofile': os.environ.get('ALLUSERSPROFILE', ''), # ProgramDataと同じ値であることが多い
                    'computername': os.environ.get('COMPUTERNAME', ''),
                    'os': os.environ.get('os', ''),
                },
                'user': {
                    'username': os.environ.get('USERNAME', ''),
                    'userprofile': os.environ.get('USERPROFILE', ''),
                    'homedrive': os.environ.get('HOMEDRIVE', ''),
                    'homepath': os.environ.get('HOMEPATH', ''),
                    'appdata': os.environ.get('APPDATA', ''),
                    'localappdata': os.environ.get('LOCALAPPDATA', ''),
                    'temp': os.environ.get('TEMP', ''),
                    'tmp': os.environ.get('TMP', ''),
                },
            },
        },
    },
    'runner': {
        'config': {
            'loadstate': 0,
            'files': [],
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
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['webhook']['url']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['avatar']['url']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['avatar']['name']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            config_loadstate|=8
            config['runner']['config']['files'].append(config_dir+config_file)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
        pass
config_dir = '~/.python/'
if os.path.exists(config_dir+config_file):
    try:
        with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['webhook']['url']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['avatar']['url']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['avatar']['name']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            config_loadstate|=4
            config['runner']['config']['files'].append(config_dir+config_file)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
        pass
config_dir = './'
if os.path.exists(config_dir+config_file):
    try:
        with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['webhook']['url']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['avatar']['url']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            try:
                config['discord']['webhook']['url'] = json.load(f)['discord']['avatar']['name']
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
                pass
            config_loadstate|=2
            config['runner']['config']['files'].append(config_dir+config_file)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError, UnicodeDecodeError, NameError, TypeError):
        pass
try:
    config['runner']['config']['loadstate'] = config_loadstate
except (ValueError, KeyError):
    pass
if config_loadstate^16==0:
    config_loadstate = 1
    print('[Config] No such file or directory: (global, user, temporary)')
    print('[Config] global: /etc/discord/login-notice.json')
    print('[Config] user: ~/.python/login-notice.json')
    print('[Config] temporary: ./login-notice.json')
    print('[Config] Creating minimum temporary config')
    config = {
        'discord': {
            'webhook': {
                'url': 'https://discord.com/api/webhooks/URL/HERE',
            },
        },
    }
    with open('./login-notice.json',mode='w',encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    print(f'[{__name__}] Exiting...')
    sys.exit(config_loadstate)

try:
    config['env']['tmout'] = int(config['env']['tmout'])
except (ValueError, KeyError):
    pass

# 起動
runtime_epoch = math.trunc(datetime.datetime.now().timestamp())

# discord_payload_json 組み立て
discord_payload_json = {
    'embeds': [],
}
discord_embed_json = {
    'title': 'Login Notice',
    'color': 0xc0c0c0,
    'footer': {
        'text': config['env']['os_dependent']['linux']['common']['hostname'],
        'icon_url': config['discord']['avatar']['url'],
    },
    'timestamp': datetime.datetime.fromtimestamp(runtime_epoch, tz=datetime.timezone.utc).isoformat(),
    'fields': [],
}
discord_field_json = {
    'name': '',
    'value': '',
    'inline': False,
}
discord_field_json = {
    'name': '> Date',
    'value': f'<t:{runtime_epoch}:F>(<t:{runtime_epoch}:R>)',
    'inline': False,
}
discord_embed_json['fields'].append(discord_field_json)
discord_field_json = {
    'name': '> User',
    'value': f'''`{config['env']['os_dependent']['linux']['common']['user']}@{config['env']['os_dependent']['linux']['common']['hostname']}`''',
    'inline': False,
}
discord_embed_json['fields'].append(discord_field_json)
discord_field_json = {
    'name': '> From',
    'value': f'''[{config['env']['os_dependent']['linux']['common']['ssh_client'][0]}:{config['env']['os_dependent']['linux']['common']['ssh_client'][1]}](https://ipinfo.io/{config['env']['os_dependent']['linux']['common']['ssh_client'][0]})''',
    'inline': False,
}
discord_embed_json['fields'].append(discord_field_json)
discord_field_json = {
    'name': '> Term',
    'value': f'''`{config['env']['os_dependent']['linux']['common']['term']}` `{config['env']['os_dependent']['linux']['common']['ssh_tty']}`''',
    'inline': False,
}
discord_embed_json['fields'].append(discord_field_json)
discord_payload_json['embeds'].append(discord_embed_json)
print(json.dumps(config,indent=4))
print(json.dumps(discord_payload_json,indent=4))
