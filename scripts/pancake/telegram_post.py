import requests
import os
from git import get_branch
from os import rename
from os.path import join
from formatters import format_local_version

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']
github_sha = os.environ['GITHUB_SHA']
telegram_api_url = 'https://api.telegram.org/bot' + bot_token
github_commits_url = 'https://github.com/mishamyrt/davinci-pancake-kernel/commits'
out_folder = './out'

def get_api_url (method: str) -> str:
    return telegram_api_url + '/' + method

def get_commit_url (commit_sha: str) -> str:
    return github_commits_url + '/' + commit_sha

send_document_url = get_api_url('sendDocument') + '?chat_id=' + chat_id

def generate_zip_name(branch: str) -> str:
    return 'pancake' + format_local_version(branch) + '.zip'

def get_caption(commit_sha: str) -> None:
    return 'Branch: `' + get_branch() + '`\n' +  '[Commit history](' + get_commit_url(commit_sha) + ')'

def post_file (file: str, commit_sha: str) -> None:
    r = requests.post(send_document_url, files={
        'document': open(file, 'rb')
    }, data={
        'caption': get_caption(commit_sha),
        'parse_mode': 'MarkdownV2'
    })

source_name = join(out_folder, 'pancake-mishamyrt.zip')
dest_name = join(out_folder, generate_zip_name(get_branch()))
rename(source_name, dest_name)
post_file(dest_name, github_sha)
