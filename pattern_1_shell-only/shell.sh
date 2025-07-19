export discord_webhook_url=https://discord.com/api/webhooks/
export discord_avatar_url=https://hangstuck.com/wp-content/uploads/2020/08/bash-official-icon-512x512-1.png
export discord_avatar_name=${HOSTNAME%%.*}

runtime=$(date +%s)
discord_embed_json='{"title": "Login Notice","fields": [{"name": "> Date","value": "<t:'"${runtime}"':F>(<t:'"${runtime}"':R>)"},{"name": "> User","value": "`'${USER}'@'${HOSTNAME}'`"},{"name": "> From","value": "['$(echo ${SSH_CLIENT}|awk -v 'OFS=:' '{print $1,$2}')'](https://ipinfo.io/'$(echo ${SSH_CLIENT}|awk '{print $1}')')"},{"name": "> Term","value": "`'${TERM}'` `'${SSH_TTY}'`"}],"> color": "'$((16#c0c0c0))'","footer": {"text": "'${HOSTNAME}'","icon_url": "'${discord_avatar_url}'"},"timestamp": "'$(date --utc '+%Y-%m-%dT%H:%M:%S.000Z')'"}'
discord_embed_json_p0=${discord_embed_json}
discord_payload_json='{"username":"'${discord_avatar_name}'","avatar_url":"'${discord_avatar_url}'","embeds":['${discord_embed_json}']}'
discord_payload_json_p0=${discord_payload_json}

test -d /tmp/discord_embed_json || mkdir /tmp/discord_embed_json
echo ${discord_payload_json} > /tmp/discord_embed_json/${HOSTNAME%%.*}_${runtime}.json
curl -s -X POST -H 'Content-Type: application/json' --data "${discord_payload_json}" ${discord_webhook_url}'?wait=true' | jq > /tmp/discord_embed_json/${HOSTNAME%%.*}_${runtime}.log.json

export discord_webhook_loginhistory_id=$(cat /tmp/discord_embed_json/${HOSTNAME%%.*}_${runtime}.log.json | jq -r .id)
discord_embed_json=$(echo ${discord_embed_json} | jq '.fields |= .+[{"name":"> MessageID","value":"['${discord_webhook_loginhistory_id}']('${discord_webhook_url}'/messages/'${discord_webhook_loginhistory_id}')"}]')
discord_payload_json='{"username":"'${discord_avatar_name}'","avatar_url":"'${discord_avatar_url}'","embeds":['${discord_embed_json}']}'
curl -s -X PATCH -H 'Content-Type: application/json' --data "${discord_payload_json}" ${discord_webhook_url}/messages/${discord_webhook_loginhistory_id}'?wait=true' | jq > /tmp/discord_embed_json/${HOSTNAME%%.*}_${runtime}_p1.log.json

ipinfo_token='xxxxxxxxxxxxxx'
external_api=$(curl -s -H "Authorization: Bearer ${ipinfo_token}" https://ipinfo.io/$(echo ${SSH_CONNECTION} | awk '{print $1}')/json | sed -z 's/[\f\r\n]/\\n/g' | sed 's/"/\\"/g')
external_api=$(curl -s -H "Authorization: Bearer ${ipinfo_token}" https://ipinfo.io/$(echo ${SSH_CONNECTION} | awk '{print $1}')/json | sed -z 's/[\f\r\n]/\\n/g')
external_api=$(curl -s -H "Authorization: Bearer ${ipinfo_token}" https://ipinfo.io/$(echo ${SSH_CONNECTION} | awk '{print $1}')/json)
external_api=$(echo ${external_api}|jq -r .org)
external_api='Org: '${external_api}
external_api=$(echo ${external_api}|sed 's/ /_/g')
discord_embed_json=$(echo ${discord_embed_json} | jq '.fields |= .+[{"name":"> ipinfo.io","value":"'${external_api}'"}]')
discord_payload_json='{"username":"'${discord_avatar_name}'","avatar_url":"'${discord_avatar_url}'","embeds":['${discord_embed_json}']}'
curl -s -X PATCH -H 'Content-Type: application/json' --data "${discord_payload_json}" ${discord_webhook_url}/messages/${discord_webhook_loginhistory_id}'?wait=true' | jq > /tmp/discord_embed_json/${HOSTNAME%%.*}_${runtime}_p1.log.json

#curl -X POST -F 'avatar_url='${discord_avatar_url} -F 'username='${HOSTNAME%.*} -F 'content=Hello,world' ${discord_webhook_url}
#curl -X POST -F 'avatar_url='${discord_avatar_url} -F 'username='${HOSTNAME%.*} -F files=@.bashrc ${discord_webhook_url}
