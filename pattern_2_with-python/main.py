import os
import sys
from re import sub
import json
import math
import datetime
import requests

# IPv4 Is Private address?
def is_private_ipv4(ip_address_str: str) -> bool:
    import ipaddress
    """
    指定されたIPv4アドレスがプライベートIPアドレス (RFC 1918) であるかを判断します。

    プライベートIPアドレスレンジ:
    - 10.0.0.0/8 (10.0.0.0 から 10.255.255.255)
    - 172.16.0.0/12 (172.16.0.0 から 172.31.255.255)
    - 192.168.0.0/16 (192.168.0.0 から 192.168.255.255)

    Args:
        ip_address_str (str): 判定したいIPv4アドレスの文字列。

    Returns:
        bool: プライベートIPアドレスであれば True、そうでなければ False。
    """
    # プライベートIPアドレスのネットワークレンジを定義
    private_networks = [
        ipaddress.ip_network('10.0.0.0/8'),
        ipaddress.ip_network('172.16.0.0/12'),
        ipaddress.ip_network('192.168.0.0/16')
    ]

    try:
        # 入力されたIPアドレスをIPv4アドレスオブジェクトに変換
        ip_addr = ipaddress.ip_address(ip_address_str)

        # 各プライベートネットワークレンジに含まれるかチェック
        for network in private_networks:
            if ip_addr in network:
                return True
        return False

    except ValueError:
        # 無効なIPアドレス文字列が入力された場合
        print(f"エラー: 無効なIPアドレス形式 '{ip_address_str}'")
        return False

# IPv6 Is Private address?
def is_private_ipv6(ip_address_str: str) -> bool:
    import ipaddress
    """
    未指定(Unspecified) |     00…0 (128 ビット)	::/128
    ループバック               0000 0000 ... 0001 (128 ビット)	::1/128
    マルチキャスト             1111 1111	ff00::/8
    リンクローカルユニキャスト	1111 1110 10	fe80::/10
    グローバルユニキャスト	   上記以外
    """
    try:
        ip_address_str_0 = ip_address_str.split(':')[0]
        ip_address_str_0 = bin(int(ip_address_str_0, 16))[2:]
        if False:
            pass
        elif ip_address_str_0[:8] == '1'*8:
            # マルチキャスト ff00::/8
            return True
        elif ip_address_str_0[:10] == '1'*7 + '010':
            # リンクローカルユニキャスト fe80::/10
            return True
        elif ip_address_str == ipaddress.IPv6Address('::'):
            # 未指定(Unspecified) ::/128
            return True
        elif ip_address_str == ipaddress.IPv6Address('::1'):
            # ループバック ::1/128
            return True
        return False
    except ValueError:
        return False

# http/get
def request_get(url='', header={}):
    try:
        api_request = requests.get(url, header)
        api_request.raise_for_status() # 200番台以外のステータスコードの場合、HTTPErrorを発生させる
        return api_request.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTPエラーが発生しました: {errh}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"接続エラーが発生しました: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"タイムアウトエラーが発生しました: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"リクエスト中に予期せぬエラーが発生しました: {err}")
        return None

# exec by subprocess
def os_exec(cmd:str=''):
    if len(cmd.strip())>0:
        return None

def main():
    # config
    config = {
        'discord': {
            'webhook': {
                'url': 'https://discord.com/api/webhooks/',
                'embed': {
                    'image': {
                        'url': '',
                    },
                    'thumbnail': {
                        'url': '',
                    },
                },
                "at_mention": [
                ],
            },
            'avatar': {
                'url': 'https://hangstuck.com/wp-content/uploads/2020/08/bash-official-icon-512x512-1.png',
                'name': sub(r'\..*', '', os.environ.get('HOSTNAME', '')),
            },
        },
        'ipinfo': {
            'auth': {
                'token': '',
                'type': 'Bearer',
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
                'github': {
                    'action': os.environ.get('GITHUB_ACTION', ''),
                    'action_ref': os.environ.get('GITHUB_ACTION_REF', ''),
                    'action_repository': os.environ.get('GITHUB_ACTION_REPOSITORY', ''),
                    'actions': os.environ.get('GITHUB_ACTIONS', ''),
                    'actor': os.environ.get('GITHUB_ACTOR', ''),
                    'actor_id': os.environ.get('GITHUB_ACTOR_ID', ''),
                    'api_url': os.environ.get('GITHUB_API_URL', ''),
                    'base_ref': os.environ.get('GITHUB_BASE_REF', ''),
                    'env': os.environ.get('GITHUB_ENV', ''),
                    'event_name': os.environ.get('GITHUB_EVENT_NAME', ''),
                    'event_path': os.environ.get('GITHUB_EVENT_PATH', ''),
                    'graphql_url': os.environ.get('GITHUB_GRAPHQL_URL', ''),
                    'head_ref': os.environ.get('GITHUB_HEAD_REF', ''),
                    'job': os.environ.get('GITHUB_JOB', ''),
                    'output': os.environ.get('GITHUB_OUTPUT', ''),
                    'path': os.environ.get('GITHUB_PATH', ''),
                    'ref': os.environ.get('GITHUB_REF', ''),
                    'ref_name': os.environ.get('GITHUB_REF_NAME', ''),
                    'ref_protected': os.environ.get('GITHUB_REF_PROTECTED', ''),
                    'ref_type': os.environ.get('GITHUB_REF_TYPE', ''),
                    'repository': os.environ.get('GITHUB_REPOSITORY', ''),
                    'repository_id': os.environ.get('GITHUB_REPOSITORY_ID', ''),
                    'repository_owner': os.environ.get('GITHUB_REPOSITORY_OWNER', ''),
                    'repository_owner_id': os.environ.get('GITHUB_REPOSITORY_OWNER_ID', ''),
                    'retention_days': os.environ.get('GITHUB_RETENTION_DAYS', ''),
                    'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT', ''),
                    'run_id': os.environ.get('GITHUB_RUN_ID', ''),
                    'run_number': os.environ.get('GITHUB_RUN_NUMBER', ''),
                    'server_url': os.environ.get('GITHUB_SERVER_URL', ''),
                    'sha': os.environ.get('GITHUB_SHA', ''),
                    'state': os.environ.get('GITHUB_STATE', ''),
                    'step_summary': os.environ.get('GITHUB_STEP_SUMMARY', ''),
                    'token': os.environ.get('GITHUB_TOKEN', ''),
                    'triggering_actor': os.environ.get('GITHUB_TRIGGERING_ACTOR', ''),
                    'workflow': os.environ.get('GITHUB_WORKFLOW', ''),
                    'workflow_ref': os.environ.get('GITHUB_WORKFLOW_REF', ''),
                    'workflow_sha': os.environ.get('GITHUB_WORKFLOW_SHA', ''),
                    'workspace': os.environ.get('GITHUB_WORKSPACE', ''),
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

    # 1. load the /etc/python/login-notice.json
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
    #   |+----  8) Load succeede /etc/python/login-notice.json
    #   +----- 16) 桁揃え用（非使用）
    config_dir = '/etc/python/'
    if os.path.exists(config_dir+config_file):
        try:
            with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
                try:
                    config_custom = json.load(f)
                    config_loadstate|=8
                except (json.JSONDecodeError, UnicodeDecodeError):
                    config_loadstate^=8
            for key in [
                'discord/webhook/url',
                'ipinfo/auth/token',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]] = config_custom[key[0]][key[1]][key[2]]
                except (NameError, TypeError, KeyError):
                    config_loadstate^=8
            for key in [
                'discord/avatar/url',
                'discord/avatar/name',
                'discord/webhook/at_mention',
                'ipinfo/auth/type',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]] = config_custom[key[0]][key[1]][key[2]]
                except (NameError, TypeError, KeyError):
                    pass
            for key in [
                'discord/webhook/embed/image/url',
                'discord/webhook/embed/thumbnail/url',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]][key[3]][key[4]] = config_custom[key[0]][key[1]][key[2]][key[3]][key[4]]
                except (NameError, TypeError, KeyError):
                    pass
            config['runner']['config']['files'].append(config_dir+config_file)
        except (FileNotFoundError, PermissionError):
            pass
    config_dir = '~/.python/'
    if os.path.exists(config_dir+config_file):
        try:
            with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
                try:
                    config_custom = json.load(f)
                    config_loadstate|=4
                except (json.JSONDecodeError, UnicodeDecodeError):
                    config_loadstate^=4
            for key in [
                'discord/webhook/url',
                'ipinfo/auth/token',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]] = config_custom[key[0]][key[1]][key[2]]
                except (NameError, TypeError, KeyError):
                    config_loadstate^=4
            for key in [
                'discord/avatar/url',
                'discord/avatar/name',
                'discord/webhook/at_mention',
                'ipinfo/auth/type',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]] = config_custom[key[0]][key[1]][key[2]]
                except (NameError, TypeError, KeyError):
                    pass
            for key in [
                'discord/webhook/embed/image/url',
                'discord/webhook/embed/thumbnail/url',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]][key[3]][key[4]] = config_custom[key[0]][key[1]][key[2]][key[3]][key[4]]
                except (NameError, TypeError, KeyError):
                    pass
            config['runner']['config']['files'].append(config_dir+config_file)
        except (FileNotFoundError, PermissionError):
            pass
    config_dir = './'
    if os.path.exists(config_dir+config_file):
        try:
            with open(config_dir+config_file,mode='r',encoding='utf-8') as f:
                try:
                    config_custom = json.load(f)
                    config_loadstate|=2
                except (json.JSONDecodeError, UnicodeDecodeError):
                    config_loadstate^=2
            for key in [
                'discord/webhook/url',
                'ipinfo/auth/token',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]] = config_custom[key[0]][key[1]][key[2]]
                except (NameError, TypeError, KeyError):
                    config_loadstate^=2
            for key in [
                'discord/avatar/url',
                'discord/avatar/name',
                'discord/webhook/at_mention',
                'ipinfo/auth/type',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]] = config_custom[key[0]][key[1]][key[2]]
                except (NameError, TypeError, KeyError):
                    pass
            for key in [
                'discord/webhook/embed/image/url',
                'discord/webhook/embed/thumbnail/url',
            ]:
                key = key.split('/')
                try:
                    config[key[0]][key[1]][key[2]][key[3]][key[4]] = config_custom[key[0]][key[1]][key[2]][key[3]][key[4]]
                except (NameError, TypeError, KeyError):
                    pass
            config['runner']['config']['files'].append(config_dir+config_file)
        except (FileNotFoundError, PermissionError):
            pass
    try:
        config['runner']['config']['loadstate'] = config_loadstate
    except (ValueError, KeyError):
        pass
    if config_loadstate^16==0:
        config_loadstate = 1
        print('[Config] No such file or directory: (global, user, temporary)')
        print('[Config] global: /etc/python/login-notice.json')
        print('[Config] user: ~/.python/login-notice.json')
        print('[Config] temporary: ./login-notice.json')
        print('[Config] Creating minimum temporary config')
        config = {
            'discord': {
                'webhook': {
                    'url': 'https://discord.com/api/webhooks/URL/HERE',
                },
            },
            'ipinfo': {
                'auth': {
                    'token': '',
                },
            },
        }
        with open('./login-notice.json',mode='w',encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        print(f'[{__name__}] Exiting...')
        sys.exit(config_loadstate)
    try:
        with open('./login-notice-json.dat',mode='w',encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except (FileNotFoundError, PermissionError):
        pass
    print(config['env']['os_dependent']['github'])

    try:
        config['env']['tmout'] = int(config['env']['tmout'])
    except (ValueError, KeyError):
        pass

    # shell-command: who
    import subprocess
    cmd = 'who'
    process = (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')

    # 起動
    runtime_epoch = math.trunc(datetime.datetime.now().timestamp())

    # for github action
    external_api = request_get('https://ipinfo.io/', {
        'Authorization': f'''{config['ipinfo']['auth']['type']} {config['ipinfo']['auth']['token']}'''
    })
    external_api = external_api['ip']
    if len(config['env']['os_dependent']['linux']['common']['ssh_client'])<3:
        config['env']['os_dependent']['linux']['common']['ssh_client'] = [external_api,0,0]
    if len(config['env']['os_dependent']['linux']['common']['ssh_connection'])<4:
        config['env']['os_dependent']['linux']['common']['ssh_connection'] = [external_api,0,external_api,0]

    if False:
        pass
    elif is_private_ipv4(config['env']['os_dependent']['linux']['common']['ssh_client'][0]):
        external_api = {
            'ip': config['env']['os_dependent']['linux']['common']['ssh_client'][0],
        }
        external_api = [
            f'''[RFC 1918 IPv4 Private](https://ipinfo.io/{external_api['ip']})'''.strip(),
        ]
        external_api = [item for item in external_api if item != '']
        external_api = '\n'.join(external_api)
    elif is_private_ipv6(config['env']['os_dependent']['linux']['common']['ssh_client'][0]):
        external_api = {
            'ip': config['env']['os_dependent']['linux']['common']['ssh_client'][0],
        }
    else:
        # IpInfo API
        external_api = request_get(f'''https://ipinfo.io/{config['env']['os_dependent']['linux']['common']['ssh_client'][0]}''', {
            'Authorization': f'''{config['ipinfo']['auth']['type']} {config['ipinfo']['auth']['token']}'''
        })
        for key in [
            'ip',
            'hostname', # Legacy Free ipinfo.io API
            'city', # Legacy Free ipinfo.io API
            'region', # Legacy Free ipinfo.io API
            'country', # Legacy Free ipinfo.io API
            'loc', # Legacy Free ipinfo.io API
            'org', # Legacy Free ipinfo.io API
            'postal', # Legacy Free ipinfo.io API
            'timezone', # Legacy Free ipinfo.io API
            'readme', # Legacy Free ipinfo.io API
            'anycast', # Legacy Free ipinfo.io API
            'bogon', # Legacy Free ipinfo.io API
            'asn', # ipinfo.io Lite API
            'as_name', # ipinfo.io Lite API
            'as_domain', # ipinfo.io Lite API
            'country_code', # ipinfo.io Lite API
            'country', # ipinfo.io Lite API
            'continent_code', # ipinfo.io Lite API
            'continent', # ipinfo.io Lite API
        ]:
            if key not in external_api:
                external_api[key] = ''
        if external_api['ip'] == '':
            external_api['ip'] = config['env']['os_dependent']['linux']['common']['ssh_client'][0]
        if external_api['hostname'] == '':
            external_api['hostname'] = external_api['ip']
        print(json.dumps(external_api,indent=4))
        external_api = [
            f'''{external_api['country']} {external_api['region']} {external_api['city']}'''.strip(),
            f'''{external_api['org']}'''.strip(),
            f'''[{external_api['hostname']}](https://ipinfo.io/{external_api['ip']})'''.strip(),
        ]
        external_api = [item for item in external_api if item != '']
        external_api = '\n'.join(external_api)

    # discord_payload_json 組み立て
    discord_payload_json = {
        'username': config['env']['os_dependent']['linux']['common']['hostname'],
        'avatar_url': config['discord']['avatar']['url'],
        'embeds': [],
    }
    discord_embed_json = {
        'title': 'Login Notice',
        'description': '',
        'color': 0xc0c0c0,
        'footer': {
            'text': config['env']['os_dependent']['linux']['common']['hostname'],
            'icon_url': config['discord']['avatar']['url'],
        },
        'timestamp': datetime.datetime.fromtimestamp(runtime_epoch, tz=datetime.timezone.utc).isoformat(),
        'image': {
            'url': config['discord']['webhook']['embed']['image']['url'],
        },
        'thumbnail': {
            'url': config['discord']['webhook']['embed']['thumbnail']['url'],
        },
        'fields': [],
    }
    try:
        if len(config['discord']['webhook']['at_mention'])>0:
            for item in config['discord']['webhook']['at_mention']:
                discord_embed_json['description'] = f'<@{item}>'
    except (ValueError, KeyError):
        pass
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
        'value': f'''[{config['env']['os_dependent']['linux']['common']['ssh_client'][0]}:{config['env']['os_dependent']['linux']['common']['ssh_client'][1]}](https://ipinfo.io/{config['env']['os_dependent']['linux']['common']['ssh_client'][0]})\n{external_api}\n''',
        'inline': False,
    }
    discord_embed_json['fields'].append(discord_field_json)
    discord_field_json = {
        'name': '> Term',
        'value': f'''`{config['env']['os_dependent']['linux']['common']['term']}` `{config['env']['os_dependent']['linux']['common']['ssh_tty']}`''',
        'inline': False,
    }
    discord_embed_json['fields'].append(discord_field_json)
    discord_field_json = {
        'name': '> Login Users',
        'value': process.strip(),
        'inline': False,
    }
    discord_embed_json['fields'].append(discord_field_json)
    discord_payload_json['embeds'].append(discord_embed_json)
    print(json.dumps(discord_payload_json,indent=4))
    print(json.dumps(config,indent=4))

    # Push to Discord
    try: 
        request=requests.post(config['discord']['webhook']['url']+'?wait=true', json=discord_payload_json)
        request.raise_for_status()
        print(json.dumps(request.json(),indent=4))
        return 0
    except requests.exceptions.HTTPError as errh:
        print(f"HTTPエラーが発生しました: {errh}")
        print(request.status_code)
        return 0
    except requests.exceptions.ConnectionError as errc:
        print(f"接続エラーが発生しました: {errc}")
        return 1
    except requests.exceptions.Timeout as errt:
        print(f"タイムアウトエラーが発生しました: {errt}")
        return 1
    except requests.exceptions.RequestException as err:
        print(f"リクエスト中に予期せぬエラーが発生しました: {err}")
        return 1
def test_main():
    assert main() == 0
if __name__ == '__main__':
    main()
