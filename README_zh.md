# 其他语言版本: [English](README.md), [中文](README_zh.md).**

# py3-workwx

郭磊开发的Python3企业微信类库

# 官方文档

## [群机器人 API](https://developer.work.weixin.qq.com/document/path/91770)

## [服务端 API](https://developer.work.weixin.qq.com/document/path/90664)

# 安装

```shell
pip install py3-workwx
```

# 示例

## 群机器人

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
