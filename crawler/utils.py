import re
import json
import os
import requests
import dotenv

dotenv.load_dotenv()

def get_rid_of_text(string_soup):
    cleaned_text = re.sub('</.*>', '', string_soup)
    cleaned_text = re.sub('<br/>', '', cleaned_text)
    cleaned_text = re.sub('<p.*>', '', cleaned_text)
    cleaned_text = re.sub('<ul.*>', '', cleaned_text)
    cleaned_text = re.sub('<li>', '', cleaned_text)
    cleaned_text = re.sub('<span.*>', '', cleaned_text)
    cleaned_text = re.sub('<a.*>', '', cleaned_text)
    cleaned_text = re.sub('\u3000', '', cleaned_text)
    cleaned_text = re.sub('(\r|\t)', '', cleaned_text)
    cleaned_text = cleaned_text.replace('\n', '')
    cleaned_text = cleaned_text.replace(' ', '')
    return cleaned_text

def preprocess_text(text):
    return bytes(re.sub(' +', ' ', text.strip().replace('\t', ' ').replace("\u3000", ' ').replace('\xa0', ' ')\
        .replace('\n', ' ').replace('<br/>', ' ').replace('\\', '\\\\')), 'utf-8').decode('utf-8', 'ignore')

def send_text_to_slack(text):
    slack_url = os.getenv('SLACK_WEBHOOK_URL')
    data = json.dumps({
        'username': 'incoming-webhook',
        'text': text,
    })
    requests.post(slack_url, data=data)

SUNMOON_BUS = (
    "id", # id
    "title", # バスのタイトル
    "creation_date", # 作成日
)
