develop_postfix = '-develop'

def format_local_version (branch: str) -> str:
    parts = branch.split('/')
    if len(parts) == 1:
        if parts[0] == 'ten':
            return ''
        elif develop_postfix in parts[0]:
            return develop_postfix
        else:
            return '-' + parts[0]
    if parts[0] == 'feature' or parts[0] == 'upstream':
        return '-' + parts[1]
    return '-' + '-'.join(parts)

def markdown_link(text: str, url: str) -> str:
	return '[' + text + '](' + url + ')'