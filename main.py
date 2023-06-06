from utils.quest_page import Quest
from utils.voice_over_index import getVoiceOverWikiList
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

wiki_list = getVoiceOverWikiList()[:3]

pool = ThreadPoolExecutor(max_workers=4)

def func(link):
    q = Quest(link)
    return q.extractAll()

result = pool.map(func, wiki_list)
    

