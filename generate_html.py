import re

remove_protocol = re.compile(r"https?://")

def to_local_url(url: str):
    url = remove_protocol.sub('', url.strip()).strip('/')
    url = url.replace('?', '@')
    if not url.endswith('.html'):
        url = url + '.html'

    return "./downloads/" + url

with open('relevant_links.txt', 'r') as input_file:
    links = input_file.readlines()


with open('all_updates.html', 'w') as output_file:
    output_file.write("""
<html>
<head>
  <title>All FFXI Updates</title>
</head>
<body>
    """)
    output_file.writelines([ f'<hr /><h1><a href="{link}">{link}</a></h1><iframe width="1200" height="800" src="{to_local_url(link)}"></iframe>' for link in links ])
    output_file.write("""
</body>
</html>
    """)
