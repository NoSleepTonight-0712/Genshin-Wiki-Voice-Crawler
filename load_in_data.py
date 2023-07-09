from utils.quest_page import Quest
from utils.voice_over_index import getVoiceOverWikiList
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from utils.sentences_difficulty import difficulty_analyze
import sqlite3
from utils.character_voice import getAllCharacterVoiceOverPage, getCharacterVoicesOnPage
from utils.voice_manager import getDestByFileName

LOAD_EVENT_DATA = True
LOAD_CHARACTER_DATA = True

conn = sqlite3.connect("data/data.sqlite")
cur = conn.cursor()
pool = ThreadPoolExecutor(max_workers=8)

if LOAD_EVENT_DATA:
    wiki_list = getVoiceOverWikiList()

    def func(link):
        q = Quest(link)
        return q.extractAll()

    print('Start crawling')
    result = pool.map(func, wiki_list)    

    result = list(result)
    print('Crawling finished. Start storing.')

    # insert into chapter table
    print('Start chapter table.')
    chapters = []
    for quest, _ in result:
        chapters.append((quest['chapter'], quest['quest_type']))
    chapters = set(chapters)

    sql = 'INSERT or ignore INTO chapter (chapter_name, chapter_type_id) values \n'
    for c in chapters:
        chapter_name = c[0]
        sql += f'("""{chapter_name}""", {c[1]}),'
    sql = sql[:-1] + ';'
    cur.execute(sql)
    conn.commit()

    # insert into quest table
    print('Start quest table')
    for quest, _ in result:
        chapter_name = quest['chapter']
        cur.execute("""INSERT or ignore INTO quest (quest_name, chapter_id, quest_link) SELECT ?, chapter_id, ? FROM chapter WHERE chapter_name = ?;""", (quest['quest_name'], quest['quest_link'], f'"{chapter_name}"'))
    conn.commit()

    # insert into dialogue table
    print('Start dialogue table')
    for quest, dialogues in result:
        quest_name = quest['quest_name']
        cur.execute('SELECT quest_id from quest where quest_name = ?', (quest_name, ))
        quest_id = cur.fetchone()[0]

        for dialogue in dialogues:
            cur.execute('insert or ignore into dialogue(dialogue_text, dialogue_quest_id, dialogue_audio_url, max_sentence_length, dialogue_audio_name) values (?, ?, ?, ?, ?)', (dialogue[0], quest_id, dialogue[2], difficulty_analyze(dialogue[0]),dialogue[1]))
            
        conn.commit()


if LOAD_CHARACTER_DATA:
    # insert into character voice.
    print('Start crawling character voices.')
    character_page_list = getAllCharacterVoiceOverPage()

    result = pool.map(getCharacterVoicesOnPage, character_page_list)
    result = list(result)
    print('Crawling finished. Start storing.')

    for r in result:
        if r == None:
            continue
        character_name, character_page_url, voices = r
        chapter_quest_name = f'Character_Voice_{character_name}'
        cur.execute('insert or ignore  into chapter (chapter_name, chapter_type_id) values (?, 6)', (chapter_quest_name, ))

        conn.commit()

        cur.execute('insert or ignore  into quest (quest_name, chapter_id, quest_link) SELECT ?, chapter_id, ? FROM chapter WHERE chapter_name = ?;', (chapter_quest_name, character_page_url, f'{chapter_quest_name}'))

        conn.commit()

        cur.execute('SELECT quest_id from quest where quest_name = ?', (chapter_quest_name, ))
        quest_id = cur.fetchone()[0]

        for text, link, filename in voices:
            filepath = getDestByFileName(chapter_quest_name + filename)[1]
            cur.execute('insert or ignore  into dialogue(dialogue_text, dialogue_quest_id, dialogue_audio_url, max_sentence_length, dialogue_audio_name) values (?, ?, ?, ?, ?)', (text, quest_id, link, difficulty_analyze(text), filepath))
        
        conn.commit()
        print(f'finish {character_name}')

