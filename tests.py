import os.path
import unittest
from datetime import datetime

from py3_workwx.webhook import Webhook


class MyTestCase(unittest.TestCase):
    def test_webhook(self):
        webhook = Webhook(key="9306875b-67b4-4445-99b9-6131f06a2555")
        state, _ = webhook.send_text(
            content=f"message content {datetime.now()}",
            mentioned_list=[],
            mentioned_mobile_list=[]
        )
        media_id, _ = webhook.upload_media(
            files={
                "file": (
                    "README.md",
                    open(os.path.join(os.getcwd(), "README.md"), "rb")
                )
            }
        )
        if media_id:
            webhook.send_file(media_id=media_id)
        self.assertTrue(True, "OK")  # add assertion here


if __name__ == '__main__':
    unittest.main()
