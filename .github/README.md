# [_DEFAULTREPOS](https://github.com/n138-kz/_DEFAULTREPOS)

## Quick setup

<details>

### if you’ve done this kind of thing before

```sh
git clone https://github.com/n138-kz/_DEFAULTREPOS.git
```

```sh
git clone git@github.com:n138-kz/_DEFAULTREPOS.git
```

### …or create a new repository on the command line

```sh
touch README.md
git init
git add README.md
git commit -m init
git branch -M main
git remote add origin git@github.com:n138-kz/_DEFAULTREPOS.git
git branch --set-upstream-to=origin/main main
git config pull.rebase false
git fetch
git pull
git merge --allow-unrelated-histories origin/main
git push -u origin main
```

- [git merge --allow-unrelated-histories origin/main](https://qiita.com/mei28/items/85bc881ac1f26332ac15)

### …or push an existing repository from the command line

```sh
git remote add origin git@github.com:n138-kz/_DEFAULTREPOS.git
git branch -M main
git push -u origin main
```

### pull an another existing repository from the command line

```sh
git config pull.rebase false
git branch -r
git pull origin {remote-repos-name}:{local-repos-name}
git checkout {local-repos-name}
git branch --set-upstream-to=origin/{remote-repos-name} {local-repos-name}
```

</details>

## github repository initial setup

1. "Actions secrets and variables" > "Repository secrets" 移動し、`DISCORD_WEBHOOK_URL` を設定  
  値は Discord webhook url を設定

```
DISCORD_WEBHOOK_URL
```

## Activity

[![GitHub repo license](https://img.shields.io/github/license/n138-kz/_DEFAULTREPOS)](/LICENSE)
[![GitHub repo size](https://img.shields.io/github/repo-size/n138-kz/_DEFAULTREPOS)](/../../)
[![GitHub repo file count](https://img.shields.io/github/directory-file-count/n138-kz/_DEFAULTREPOS)](/../../)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/n138-kz/_DEFAULTREPOS)](/../../)
[![GitHub last commit](https://img.shields.io/github/last-commit/n138-kz/_DEFAULTREPOS)](/../../commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/n138-kz/_DEFAULTREPOS)](/../../commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/t/n138-kz/_DEFAULTREPOS)](/../../commits)
[![GitHub issues](https://img.shields.io/github/issues/n138-kz/_DEFAULTREPOS)](/../../issues)
[![GitHub issues closed](https://img.shields.io/github/issues-closed/n138-kz/_DEFAULTREPOS)](/../../issues)
[![GitHub pull requests closed](https://img.shields.io/github/issues-pr-closed/n138-kz/_DEFAULTREPOS)](/../../pulls)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/n138-kz/_DEFAULTREPOS)](/../../pulls)
[![GitHub language count](https://img.shields.io/github/languages/count/n138-kz/_DEFAULTREPOS)](/../../)
[![GitHub top language](https://img.shields.io/github/languages/top/n138-kz/_DEFAULTREPOS)](/../../)

## Github RestAPI

```http
GET https://api.github.com/repos/n138-kz/_DEFAULTREPOS
```

<details>

  [n138-kz/_DEFAULTREPOS](https://api.github.com/repos/n138-kz/_DEFAULTREPOS) (Public repos only)
  
</details>

## Refs

- [![](https://www.google.com/s2/favicons?size=64&domain=https://github.com)_DEFAULTREPOS](https://github.com/n138-kz/_DEFAULTREPOS/)

## License

[Copyright (c) 2025 Yuu Komiya (n138), Under MIT License](LICENSE)  

<details>

[MIT_License | wikipedia](https://ja.wikipedia.org/wiki/MIT_License)

[The MIT License](https://opensource.org/license/mit/)
> [n138-kz/*](./) is licensed under the `MIT License`.  
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> `Copyright <YEAR> <COPYRIGHT HOLDER>`
> 
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[The MIT License](https://opensource.org/license/mit/)
> [n138-kz/*](./) は、MIT ライセンスに基づいてライセンスされています。  
> 以下に定める条件に従い、本ソフトウェアおよび関連文書のファイル（以下「ソフトウェア」）の複製を取得するすべての人に対し、ソフトウェアを無制限に扱うことを無償で許可します。これには、ソフトウェアの複製を使用、複写、変更、結合、掲載、頒布、サブライセンス、および/または販売する権利、およびソフトウェアを提供する相手に同じことを許可する権利も無制限に含まれます。  
>
> `Copyright (c) <著作権発生年> <著作権保持者名>`
> 
> 上記の著作権表示および本許諾表示を、ソフトウェアのすべての複製または重要な部分に記載するものとします。
>
> ソフトウェアは「現状のまま」で、明示であるか暗黙であるかを問わず、何らの保証もなく提供されます。ここでいう保証とは、商品性、特定の目的への適合性、および権利非侵害についての保証も含みますが、それに限定されるものではありません。
> 作者または著作権者は、契約行為、不法行為、またはそれ以外であろうと、ソフトウェアに起因または関連し、あるいはソフトウェアの使用またはその他の扱いによって生じる一切の請求、損害、その他の義務について何らの責任も負わないものとします。

### Permissions / 許可
- Commercial use / 商用利用
- Modification / 改変
- Distribution / 再配布
- Private use / 私的使用 

### Limitations / 制限事項
- Liability / 発生した問題に責任を負わない
- Warranty / 無保証

</details>
