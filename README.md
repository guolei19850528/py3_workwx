**Read this in other languages: [English](README.md), [中文](README_zh.md).**

# py3-workwx

A Python3 Work Weixin Library By Guolei

# Official Documentation

## [Webhook API](https://developer.work.weixin.qq.com/document/path/91770)

## [Server API](https://developer.work.weixin.qq.com/document/path/90664)

# Installation

```shell
pip install py3-workwx
```

# Example

## Webhook

```python
from py3_workwx.webhook import Webhook

webhook = Webhook(key="<key>")
state, _ = webhook.send_text(
    content="<message content>",
    mentioned_list=[],
    mentioned_mobile_list=[]
)
if state:
    print("successful")
media_id, _ = webhook.upload_media(
    files={
        "file": (
            "<display file name>",
            open("<file path>", "rb")
        )
    }
)
if media_id:
    state, _ = webhook.send_file(media_id=media_id)
if state:
    print("successful")
```
