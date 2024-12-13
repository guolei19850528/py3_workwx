# py3-workwx

The Python3 Work Weixin Library Developed By Guolei

# Documentation

## [Webhook API](https://developer.work.weixin.qq.com/document/path/91770)

## [Server API](https://developer.work.weixin.qq.com/document/path/90664)

# Installation

```shell
pip install py3-workwx==1.1.13
```

# Example

## Webhook

```python
from py3_workwx.webhook import Webhook

webhook = Webhook(key="<key>")

state = webhook.send(
    json=webhook.send_text_formatter(f"测试信息")
)
if state:
    print("send message success")
else:
    print("send message failed")
media_id = webhook.upload_media(
    files={
        "file": ("README.md", open("README.md", "rb")),
    }
)
if media_id:
    print("upload file success")
    state = webhook.send(
        json=webhook.send_file_formatter(media_id)
    )
    if state:
        print("send file success")
    else:
        print("send file failed")
else:
    print("upload media failed")
```

## Server API

```python
import os.path
from datetime import datetime

import diskcache

from py3_workwx.server import Server

cache = diskcache.Cache(directory=os.path.join(os.getcwd(), "runtime", "diskcache", "default"))

server = Server(
    corpid="<corpid>",
    corpsecret="<corpsecret>",
    agentid="<agentid>",
    cache=cache
)

state = server.gettoken_with_cache().message_send(
    json={
        "touser": "your name",
        "msgtype": "text",
        "agentid": server.agentid,
        "text": {
            "content": f"测试信息",
        }
    }
)
if state:
    print("send message success")
else:
    print("send message failed")
media_id = server.media_upload(files={
    "file": (
        "README.md",
        open("README.md", "rb")
    )
})
if media_id:
    print("upload file success")
else:
    print("upload file failed")
```