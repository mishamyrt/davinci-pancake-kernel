import os

def execute (command: str) -> str:
    return os.popen(command).read().strip()

def get_branch () -> str:
    return execute('echo ${GITHUB_REF#refs/heads/}')
