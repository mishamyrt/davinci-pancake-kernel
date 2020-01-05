from git import get_branch, get_commits

defconfig_path = 'arch/arm64/configs/vendor/davinci_defconfig'
postfix_key = '%LOCAL_VERSION%'

def format_local_version (branch: str) -> str:
    parts = branch.split('/')
    if len(parts) == 1:
        return ''
    if parts[0] == 'feature' or parts[0] == 'upstream':
        return '-' + parts[1]
    return '-' + '-'.join(parts)

def append_postfix(postfix: str) -> None:
    file = open(defconfig_path, 'r+', encoding='utf8')
    text = file.read().replace(postfix_key, postfix)
    file.seek(0)
    file.write(text)
    file.truncate()

append_postfix(format_local_version(get_branch()))
