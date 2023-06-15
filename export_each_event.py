from export_cards_by_SQL import export_cards_by_SQL
import sqlite3
import os
from pathlib import Path

conn = sqlite3.connect('data/data.sqlite')
cur = conn.cursor()

# get chapter list
cur.execute('SELECT DISTINCT chapter_id, chapter_name from chapter;')
chapter_list = cur.fetchall()

# export each event
for chapter_id, chapter_name in chapter_list:
    print(f'processing {chapter_name}')
    chapter_name = chapter_name.replace('"', '').replace("'", '').replace(':', '').replace('?', '')

    if not Path(os.path.join('export', chapter_name)).exists():
        os.mkdir(os.path.join('export', chapter_name))

    cur.execute('SELECT DISTINCT quest_id, quest_name from quest where chapter_id = ?', (chapter_id, ))
    quest_ids = cur.fetchall()

    for (quest_id, quest_name) in quest_ids:
        SQL = 'SELECT DISTINCT dialogue_text, dialogue_audio_name FROM (SELECT * FROM dialogue WHERE \n dialogue_quest_id = ? ORDER BY dialogue_id)'
        SQL_PARAMS = (quest_id,)

        EXPORT_DECK_NAME = quest_name

        export_cards_by_SQL(SQL, SQL_PARAMS, EXPORT_DECK_NAME, os.path.join('export', chapter_name))


