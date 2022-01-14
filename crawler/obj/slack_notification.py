import os
import json
import dotenv
import requests

dotenv.load_dotenv()


class SlackNotification:
    def __init__(self):
        self.web_hook_url = os.getenv('SLACK_WEBHOOK_URL')

    def send_message(self, message):
        data = json.dumps({
            'username': 'incoming-webhook',
            'text': message,
        })
        requests.post(self.web_hook_url, data=data)
