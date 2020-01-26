import sys
import json
from formatters import today_iso
from git import execute

def sha1(file: str) -> str:
    return execute(f'shasum {file}').split(' ')[0]

version = sys.argv[1]
is_stable = sys.argv[2] == 'stable'

host = 'https://pancake-'
host += 'kernel' if is_stable else 'develop'
host += '.surge.sh'

manifest = {
    'kernel': {
        'name': 'Pancake Kernel',
        'version': version,
        'link': f'{host}/pancake.zip',
        'changelog_url': f'{host}/changelog.txt',
        'sha1': sha1('release/pancake.zip'),
        'date': today_iso()
    },
    'support': {
        'link': 'https://t.me/pancake_kernel'
    }
}

with open('release/index.html', 'w') as outfile:
    json.dump(manifest, outfile)