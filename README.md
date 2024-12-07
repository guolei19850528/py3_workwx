# Read this in other languages: [English](https://github.com/guolei19850528/py3_workwx/blob/main/README.md), [中文](https://github.com/guolei19850528/py3_workwx/blob/main/README_zh.md)

# py3-workwx

The Python3 Work Weixin Library Developed By Guolei

# Official Documentation

## [Webhook API](https://developer.work.weixin.qq.com/document/path/91770)

## [Server API](https://developer.work.weixin.qq.com/document/path/90664)

# Installation

```shell
pip install py3-workwx
```

# Example

# Webhook

```python
from py3_workwx.webhook import Webhook

webhook = Webhook(key="<key>")
state = webhook.send_text(
    content="<message content>",
    mentioned_list=[],
    mentioned_mobile_list=[]
)
if state:
    print("successful")
media_id = webhook.upload_media(
    files={
        "file": (
            "<display file name>",
            open("<file path>", "rb")
        )
    }
)
if media_id:
    state = webhook.send_file(media_id=media_id)
if state:
    print("successful")
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
        "touser": "user",
        "msgtype": "text",
        "agentid": server.agentid,
        "text": {
            "content": f"test message {datetime.now()}",
        }
    }
)
if state:
    print("successful")
media_id = server.media_upload(files={
    "file": (
        "README.md",
        open(os.path.join(os.getcwd(), "README.md"), "rb")
    )
})
if media_id:
    print(media_id)
```