from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def split_links(links):
    wiki_links_to_follow = []
    wiki_other_links = []
    skip_links = []
    sqex_forum_links = []
    remaining_links = []

    for link in links:
        if link.startswith('/ffxi/Version_Update'):
            wiki_links_to_follow.append(link)
        elif link.startswith('/ffxi/'):
            wiki_other_links.append(link)
        elif link.startswith("#"):
            skip_links.append(link)
        elif "forum.square-enix.com/ffxi/threads/" in link:
            sqex_forum_links.append(link)
        else:
            remaining_links.append(link)

    return wiki_links_to_follow, sqex_forum_links

def select_matches(elements, matchers: dict):
    results = dict((key, []) for key in matchers)
    no_matches = []
    for element in elements:
        matched = False
        for id, matcher in matchers.items():
            if matcher(element):
                results[id].append(element)
                matched = True
                break
        
        if not matched:
            no_matches.append(element)

    return results, no_matches

def has_any_containing(elements, contained_strings):
    for element in elements:
        for string in contained_strings:
            if string in element:
                return True
    return False

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

wiki_content_class = 'mw-parser-output'

print("Fetching main update page")
wiki_root = 'https://www.bg-wiki.com'
url = wiki_root + '/ffxi/Category:Update_History'
browser.get(url)

print("Parsing main update page")
soup = BeautifulSoup(browser.page_source, 'html.parser')

wiki_page_content = soup.find(class_=wiki_content_class)
all_links: list[str] = [ a['href'] for a in wiki_page_content.find_all("a") if a ]


matches, remaining_links = select_matches(all_links, {
    'wiki_update_links': lambda link: link.startswith('/ffxi/Version_Update'),
    'sqex_forum_links': lambda link: "forum.square-enix.com/ffxi/threads/" in link
})

out_file = open("bg_links.txt", "w")
out_file.writelines([ link + '\n' for link in matches['sqex_forum_links']])
out_file.flush()

print("Fetching relevant sub-pages of wiki to look for links")
for wiki_path in matches['wiki_update_links']:
    is_version_update = "Version_Update" in wiki_path
    current_wiki_page = wiki_root + wiki_path
    browser.get(current_wiki_page)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    wiki_page_content = soup.find(class_=wiki_content_class)
    if wiki_page_content == None:
        print("Couldn't find any content at ", wiki_path)
        continue

    links = [ a['href'] for a in wiki_page_content.find_all("a") ]

    matches, remaining_links = select_matches(links, {
        'wiki_links': lambda link: link.startswith('/') or link.startswith('#'),
        'playonline': lambda link: 'playonline' in link,
    })

    if is_version_update and (len(matches['playonline']) == 0 or not has_any_containing(matches['playonline'], ["comnews", "update"])):
        out_file.write(current_wiki_page + '\n')
    else:
        out_file.writelines([ link + '\n' for link in matches['playonline']])
    out_file.flush()

print("Done!")

out_file.close()
