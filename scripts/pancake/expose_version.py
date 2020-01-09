from git import get_branch
from formatters import format_local_version

defconfig_path = 'arch/arm64/configs/vendor/davinci_defconfig'
postfix_key = '%LOCAL_VERSION%'

def append_postfix(postfix: str) -> None:
    file = open(defconfig_path, 'r+', encoding='utf8')
    text = file.read().replace(postfix_key, postfix)
    file.seek(0)
    file.write(text)
    file.truncate()

append_postfix(format_local_version(get_branch()))
