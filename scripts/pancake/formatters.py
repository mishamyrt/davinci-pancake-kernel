def format_local_version (branch: str) -> str:
    parts = branch.split('/')
    if len(parts) == 1:
        return ''
    if parts[0] == 'feature' or parts[0] == 'upstream':
        return '-' + parts[1]
    return '-' + '-'.join(parts)

def markdown_link(text: str, url: str) -> str:
	return '[' + text + '](' + url + ')'