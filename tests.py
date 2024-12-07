import os.path
import unittest
from datetime import datetime

import diskcache
from requests import RequestException

from py3_workwx.server import Server
from py3_workwx.webhook import Webhook


class MyTestCase(unittest.TestCase):
    def test_webhook(self):
        webhook = Webhook(key="9306875b-67b4-4445-99b9-6131f06a2555")
        state = webhook.send_text(
            content=f"message content {datetime.now()}",
            mentioned_list=[],
            mentioned_mobile_list=[]
        )
        media_id = webhook.upload_media(
            files={
                "file": (
                    "README.md",
                    open(os.path.join(os.getcwd(), "README.md"), "rb")
                )
            }
        )
        print(media_id)
        if media_id:
            webhook.send_file(media_id=media_id)
        self.assertTrue(True, "OK")  # add assertion here

    def test_server(self):
        cache = diskcache.Cache(directory=os.path.join(os.getcwd(), "runtime", "diskcache", "default"))
        server = Server(
            corpid="ww5f2bb01bebafe097",
            corpsecret="caVcNxS9qP8utsCkPaG7NH0I-j1vr9EMRi0WpsvkzVU",
            agentid="1000035",
            cache=cache
        )

        state,_=server.gettoken_with_cache().message_send(
            json={
                "touser": "guolei",
                "msgtype": "text",
                "agentid": server.agentid,
                "text": {
                   "content": f"test message {datetime.now()}",
                }
            }
        )
        if state:
            print("successful")
        media_id,_=server.media_upload(files={
            "file": (
                "README.md",
                open(os.path.join(os.getcwd(), "README.md"), "rb")
            )
        })
        if media_id:
            print(media_id)
        self.assertTrue(True, "OK")


if __name__ == '__main__':
    unittest.main()
