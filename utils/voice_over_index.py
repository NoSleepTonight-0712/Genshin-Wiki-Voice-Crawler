# This file is used to get all links to the "Quest with Voice-over" Wiki pages.
import requests
from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin
from utils.global_variables import BASE_URL

URL = 'https://genshin-impact.fandom.com/wiki/Category:Quests_with_Voice-Overs'


def getVoiceOverWikiList() -> List[str]:
    content = requests.get(URL).content
    b = BeautifulSoup(content, features='html.parser')
    a_list = b.find_all('a', class_='category-page__member-link')

    a_node_to_link = (lambda s : urljoin(BASE_URL, s.get('href')))

    return [a_node_to_link(i) for i in a_list]

