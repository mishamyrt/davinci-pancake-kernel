import requests
import os
import sys
import json
from git import get_branch
from os import rename
from os.path import join
from formatters import format_local_version, markdown_link

branch = get_branch()

def get_chat_id() -> str:
    if 'private' in branch:
        return '74076749'
    else:
        return os.environ['TELEGRAM_CHAT_ID']

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = get_chat_id()
github_sha = os.environ['GITHUB_SHA']
telegram_api_url = 'https://api.telegram.org/bot' + bot_token
github_commit_url = 'https://github.com/mishamyrt/davinci-pancake-kernel/commit'
github_commits_url = github_commit_url + 's'
out_folder = './out'


def get_api_url(method: str) -> str:
    return telegram_api_url + '/' + method


send_document_url = get_api_url('sendDocument') + '?chat_id=' + chat_id
send_message_url = get_api_url('sendMessage')
delete_message_url = get_api_url('deleteMessage')


def get_commit_url(commit_sha: str) -> str:
    return github_commits_url + '/' + commit_sha


def get_workflow_url(commit_sha: str) -> str:
    return github_commit_url + '/' + commit_sha + '/checks'


def generate_zip_name(branch: str) -> str:
    return 'pancake' + format_local_version(branch) + '.zip'


def get_caption_body(commit_sha: str) -> str:
    return '\nBranch: `' + get_branch() + '`\n' + markdown_link('Commit history', get_commit_url(commit_sha)) + '\n' + markdown_link('Workflow', get_workflow_url(commit_sha))


def post_file(file: str, commit_sha: str) -> None:
    r = requests.post(send_document_url, files={
        'document': open(file, 'rb')
    }, data={
        'caption': 'Build succeeded 🤘' + get_caption_body(commit_sha),
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
    print(post_message('Build started ⭐' + get_caption_body(github_sha)))
elif sys.argv[1] == 'success':
    delete_message(sys.argv[2])
    source_name = join(out_folder, 'pancake-mishamyrt.zip')
    dest_name = join(out_folder, generate_zip_name(get_branch()))
    rename(source_name, dest_name)
    post_file(dest_name, github_sha)
elif sys.argv[1] == 'fail':
    delete_message(sys.argv[2])
    post_message('Build failed 🔥' + get_caption_body(github_sha))
