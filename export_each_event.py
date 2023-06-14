from export_cards_by_SQL import export_cards_by_SQL
import sqlite3

conn = sqlite3.connect('data/data.sqlite')
cur = conn.cursor()

# get chapter list
cur.execute('SELECT distinct chapter_id, chapter_name from chapter;')
chapter_list = cur.fetchall()

# export each event
for chapter_id, chapter_name in chapter_list:
    print(f'processing {chapter_name}')
    SQL_HEAD = 'SELECT dialogue_text, dialogue_audio_name FROM dialogue WHERE'
    SQL_CLAUSE = 'dialogue_quest_id = (SELECT quest_id FROM quest where chapter_id = ?)'
    SQL_PARAMS = (chapter_id,)

    EXPORT_DECK_NAME = chapter_name

    export_cards_by_SQL(SQL_HEAD, SQL_CLAUSE, SQL_PARAMS, EXPORT_DECK_NAME, 'export')

