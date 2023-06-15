import requests
from bs4 import BeautifulSoup
from utils.global_variables import BASE_URL
from urllib.parse import urljoin


def getVoiceOverPageByIndexPage(url):
    content = requests.get(url).content
    b = BeautifulSoup(content, features='lxml')
    return [urljoin(BASE_URL, i.get('href')) for i in b.find_all('a', class_='category-page__member-link') if ('Category' not in i.get('href')) and len(i.get('href').split('/')) == 4]

def getAllCharacterVoiceOverPage():
    result = getVoiceOverPageByIndexPage('https://genshin-impact.fandom.com/wiki/Category:Character_Voice-Overs')
    result.extend(getVoiceOverPageByIndexPage('https://genshin-impact.fandom.com/wiki/Category:Character_Voice-Overs?from=Nilou+Voice-Overs'))
    return result


def getCharacterVoicesOnPage(character_page_url):
    b = BeautifulSoup(requests.get(character_page_url).content, features='lxml')
    character_name = b.find('h1').text.strip().split('/')[0]
    table = b.find('span', id='Story').parent.find_next('table')

    print(f'crawling {character_name}')

    if character_name != 'Traveler':
        result = []
        for td in table.find_all('td'):
            link = td.find('a').get('href')
            text = td.find('span', lang='en').text
            filename = [i for i in link.split('/') if i.endswith('.ogg')][0]
            result.append((text, link, filename))

        return character_name, character_page_url, result
    else:
        # Traveler ignore. Too long.
        pass




