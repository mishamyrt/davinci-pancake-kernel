import os

def execute (command: str) -> str:
    return os.popen(command).read().strip()

def get_branch () -> str:
    return execute('echo ${GITHUB_REF#refs/heads/}')

def get_commits (count: int) -> str:
    return '\n'.join(
        [ll.rstrip() for ll in execute('git log -' + str(count) + ' --pretty=%B').splitlines() if ll.strip()])
