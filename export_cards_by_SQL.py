import sqlite3
import pandas as pd
import random
import os
import genanki
import pathlib
from typing import Tuple

###   SETTINGS   ###
# The final SQL will be the conbination of SQL_HEAD and SQL_CLAUSE.
# please select dialogue_text, dialogue_audio_name FROM dialogue if you don't want
# to further modify the code behind.
SQL = 'SELECT dialogue_text, dialogue_audio_name FROM dialogue WHERE \n dialogue_quest_id = (SELECT quest_id FROM quest where chapter_id = ?)'
SQL_PARAMS = (1,)

EXPORT_DECK_NAME = ''


def export_cards_by_SQL(sql: str, sql_params: Tuple[str], export_deck_name: str, export_dir = '', check=False) -> None: 
    """This function is used to export cards by SQL.

    Parameters
    ----------
    sql : string
        The SQL string you want to execute. Use ? to fill the param's blank.

    sql_params : Tuple[str]
        The SQL params Tuple of the sql string.
        For example, you may use `SELECT dialogue_text, dialogue_audio_name FROM dialogue WHERE dialogue_text LIKE "?"`,
        and pass the sql_params as `('%Paimon%, )` to select all dialogues whoes text contain 'Paimon'.

    export_deck_name : str
        The deck name. Please make it unique.

    export_dir : str
        The deck destination.

    check : bool, default=False.
        If check is set to True, it will check the existent of each audio file, but will make the program slower.
        In most cases, keep it as False. It will automatically enable checking if there are some files missing.
    """
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
            {'name': 'Media'},
            {'name': 'SentenceNumber'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<div>Sentence NO. {{SentenceNumber}}</div><div>{{Media}}</div>',
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

    cur.execute(sql, sql_params)

    select_result = cur.fetchall()

    audio_list = []
    for i, (text, audio) in enumerate(select_result):
        if check:
            if not pathlib.Path(audio).exists():
                continue
        audio_name = audio.split('\\')[-1]
        note = genanki.Note(
            model=genshin_model,
            fields=[text, f"[sound:{audio_name}]", str(i+1)]
        )
        audio_list.append(audio)
        genshin_deck.add_note(note)


    genshin_package = genanki.Package(genshin_deck)
    genshin_package.media_files = audio_list

    try:
        genshin_package.write_to_file(os.path.join(export_dir, f'{export_deck_name}.apkg'))
        print(f'finish export {export_deck_name}')
    except:
        # maybe some audio file(s) are broken.
        print(f'@@@@@ WARNING: {export_deck_name} may be broken! @@@@@@')
        export_cards_by_SQL(sql, sql_params, export_deck_name, export_dir, check=True)


    cur.close()
    conn.close()



if __name__ == '__main__':
    export_cards_by_SQL(SQL, SQL_PARAMS, EXPORT_DECK_NAME)

