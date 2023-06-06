import sqlite3
import pandas as pd
import random
import os
import genanki

conn = sqlite3.connect('data/data.sqlite')
cur = conn.cursor()

df = pd.read_csv('selected_sentences.csv')

my_deck = genanki.Deck(
    5432456432423432,
    'Genshin Words')

my_model = genanki.Model(
    657652456445343432,
    "Genshin Words",
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
    }
    """
)

audio_list = []
for _, (_, sentence_id, word_freq) in df.iterrows():
    if word_freq <= 1:
        break

    cur.execute(
        'select dialogue_text, dialogue_audio_name from dialogue where dialogue_id = ?', (sentence_id, ))
    text, audio = cur.fetchone()

    my_note = genanki.Note(
        model=my_model,
        fields=[text, f"[sound:{audio}]"]
    )
    audio_list.append(audio)

    my_deck.add_note(my_note)

my_package = genanki.Package(my_deck)
my_package.media_files = [os.path.join('voice', aud) for aud in audio_list]

my_package.write_to_file('Genshin Words.apkg')

