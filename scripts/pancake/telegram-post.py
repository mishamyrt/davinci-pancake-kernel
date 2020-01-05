import requests
import os
from datetime import datetime
from git import get_branch, get_commits

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = '-344877533'
telegram_api_url = 'https://api.telegram.org/bot' + bot_token

def get_api_url (method: str) -> str:
    return telegram_api_url + '/' + method

send_message_url = get_api_url('sendMessage')
send_document_url = get_api_url('sendDocument') + '?chat_id=' + chat_id

def post_kernel_file () -> None:
    post_file('out/pancake-mishamyrt.zip')

def format_commits () -> str:
    return '```\n' + get_commits(15) + '\n```'

def get_caption() -> None:
    return 'Branch: `' + get_branch() + '`\n' +  'Latest commits:\n' + format_commits()

def post_caption() -> None:
    r = requests.get(send_message_url, data={
        'chat_id': chat_id,
        'text': get_caption(),
        'parse_mode': 'MarkdownV2'
    })
    print(r.text)

def post_file (file: str) -> None:
    r = requests.post(send_document_url, files={
        'document': open(file, 'rb')
    })
    print(r.text)

post_kernel_file()
post_caption()
