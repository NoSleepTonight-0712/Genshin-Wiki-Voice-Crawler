# This file is used to get all links to the "Quest with Voice-over" Wiki pages.
import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin
try:
    from utils.global_variables import BASE_URL
except:
    from global_variables import BASE_URL

URLs = ['https://genshin-impact.fandom.com/wiki/Category:Quests_with_Voice-Overs',
        'https://genshin-impact.fandom.com/wiki/Category:Quests_with_Voice-Overs?from=Her+Secret',       
        'https://genshin-impact.fandom.com/wiki/Category:Quests_with_Voice-Overs?from=The+Meaning+of+Meaningless+Waiting']


def getVoiceOverWikiListOnPage(url) -> List[str]:
    content = requests.get(url).content
    b = BeautifulSoup(content, features='html.parser')
    a_list = b.find_all('a', class_='category-page__member-link')

    a_node_to_link = (lambda s : urljoin(BASE_URL, s.get('href')))

    return [a_node_to_link(i) for i in a_list]


def getVoiceOverWikiList() -> List[str]:
    result = []
    for i in URLs:
        result.extend(getVoiceOverWikiListOnPage(i))

    return result

if __name__ == '__main__':
    print(getVoiceOverWikiList())