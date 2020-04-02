import requests
import sys
import json
from os import environ
from shutil import copyfile
from os.path import join

file_name = ''
if ('FILE_NAME' in environ):
    file_name = environ['FILE_NAME']
branch = environ['BRANCH']
token = environ['TOKEN']
chat_id = environ['CHAT_ID']
commit_hash = environ['COMMIT']

telegram_prefix = f'https://api.telegram.org/bot{token}'
commit_prefix = 'https://github.com/mishamyrt/davinci-pancake-kernel/commit'
commits_prefix = f'{commit_prefix}s'

def markdown_link(text: str, url: str) -> str:
	return  f'[{text}]({url})'

def get_api_url(method: str) -> str:
    return f'{telegram_prefix}/{method}'

send_document_url = f'{get_api_url("sendDocument")}?chat_id={chat_id}' 
send_message_url = get_api_url('sendMessage')
delete_message_url = get_api_url('deleteMessage')

def get_commit_url(commit_sha: str) -> str:
    return f'{commits_prefix}/{commit_sha}'

def get_workflow_url(sha1: str) -> str:
    return f'{commit_prefix}/{sha1}/checks'

def get_caption_body(commit_sha: str) -> str:
    return (
        f"\nBranch: `{branch}`\n"
        f"{markdown_link('Commit history', get_commit_url(commit_sha))}\n"
        f"{markdown_link('Workflow', get_workflow_url(commit_sha))}"
    )

def post_file(file: str, commit_sha: str) -> None:
    r = requests.post(send_document_url, files={
        'document': open(f'./{file}', 'rb')
    }, data={
        'caption': 'Successfully baked 🤘' + get_caption_body(commit_sha),
        'parse_mode': 'MarkdownV2'
    })

def post_message(message: str) -> str:
    r = requests.post(send_message_url, {
        'text': message,
        'parse_mode': 'MarkdownV2',
        'chat_id': chat_id
    })
    return json.loads(r.text)['result']['message_id']


def delete_message(message_id: str) -> None:
    r = requests.post(delete_message_url, {
        'chat_id': chat_id,
        'message_id': message_id
    })


if sys.argv[1] == 'start':
    print(post_message('Baking started ⏲' + get_caption_body(commit_hash)))
elif sys.argv[1] == 'success':
    if (len(sys.argv) > 2):
        delete_message(sys.argv[2])
    post_file(file_name, commit_hash)
elif sys.argv[1] == 'fail':
    delete_message(sys.argv[2])
    post_message('Baking failed 🔥' + get_caption_body(commit_hash))
