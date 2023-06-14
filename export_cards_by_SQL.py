import sqlite3
import pandas as pd
import random
import os
import genanki
import pathlib

###   SETTINGS   ###
# The final SQL will be the conbination of SQL_HEAD and SQL_CLAUSE.
# please select dialogue_text, dialogue_audio_name FROM dialogue if you don't want
# to further modify the code behind.
SQL_HEAD = 'SELECT dialogue_text, dialogue_audio_name FROM dialogue WHERE'
SQL_CLAUSE = 'dialogue_quest_id = (SELECT quest_id FROM quest where chapter_id = ?)'
SQL_PARAMS = (1,)

EXPORT_DECK_NAME = ''


def export_cards_by_SQL(sql_head, sql_clause, sql_params, export_deck_name, export_dir = '', check=False):
    # clear export deck name
    export_deck_name = export_deck_name.replace('"', '').replace("'", '').replace(':', '').replace('?', '')

    ###  CARD TEMPLATES  ###
    genshin_deck = genanki.Deck(
        hash(export_deck_name),
        export_deck_name)


    genshin_model = genanki.Model(
        hash(export_deck_name) + 1,
        "Genshin Sentences",
        fields=[
            {'name': 'Answer'},
            {'name': 'Media'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Media}}',
                'afmt': '{{FrontSide}}<hr id="answer"><span id="answer-text">{{Answer}}</span>'
            }
        ],
        css="""
        #answer-text {
            font-size: 28px;
            font-family: Arial;
            margin: 16px;
        }
        """
    )


    # connect to SQLite3 database
    conn = sqlite3.connect('data/data.sqlite')
    cur = conn.cursor()

    sql = sql_head + ' \n ' + sql_clause

    cur.execute(sql, sql_params)

    select_result = cur.fetchall()

    audio_list = []
    for text, audio in select_result:
        if check:
            if not pathlib.Path(os.path.join('voice', audio)).exists():
                continue
        note = genanki.Note(
            model=genshin_model,
            fields=[text, f"[sound:{audio}]"]
        )
        audio_list.append(audio)
        genshin_deck.add_note(note)


    genshin_package = genanki.Package(genshin_deck)
    genshin_package.media_files = [os.path.join('voice', aud) for aud in audio_list]

    try:
        genshin_package.write_to_file(os.path.join(export_dir, f'{export_deck_name}.apkg'))
    except:
        # maybe some audio file(s) are broken.
        print(f'@@@@@ WARNING: {export_deck_name} may be broken! @@@@@@')
        export_cards_by_SQL(sql_head, sql_clause, sql_params, export_deck_name, export_dir, check=True)


    cur.close()
    conn.close()



if __name__ == '__main__':
    export_cards_by_SQL(SQL_HEAD, SQL_CLAUSE, SQL_PARAMS, EXPORT_DECK_NAME)

