# pattern_2_with-python

## Install

1. 任意のディレクトリ（例： `/usr/local/bin` ） に [`main.py`](main.py) を配置
2. 以下のディレクトリのいずれかに `login-notice.json` を新規作成
    - /etc/python/login-notice.json
    - ~/.python/login-notice.json
    - ./login-notice.json
    
    ```json
    {
        "discord": {
            "webhook": {
                "url": "https://discord.com/api/webhooks/URL/HERE",
                "embed": {
                    "image": {
                        "url": "(option; なくてもOK)"
                    },
                    "thumbnail": {
                        "url": "(option; なくてもOK)"
                    }
                },
                "at_mention": [
                    "数字のID（ロールメンションは頭に「&」をつける）"
                ]
            }
        },
        "ipinfo": {
            "auth": {
                "token": ""
            }
        }
    }
    ```
3. `/etc/profile` に `python3 /usr/local/bin/main.py` を記述
4. ログインして確認（動作確認は `python3 /usr/local/bin/main.py` 実行して確認）
