from utils.sentences_difficulty import Sentence_Analyzer
import sqlite3

conn = sqlite3.connect('data/data.sqlite')
cur  = conn.cursor()

# get chapter_ids
cur.execute('select distinct chapter_id, chapter_name from chapter;')
chapter_infos = cur.fetchall()


# init sentence analyzer
with open('./vocabulary_list/扇贝托福核心词.txt') as f:
    vocab_list = f.read().strip().split('\n')

sentence_analyzer = Sentence_Analyzer(vocab_list)
print('finish init sentence analyzer')

def getEachChapterDifficulty(chapter_id) -> int:
    # get dialogues in specific chapter_id
    cur.execute('''select distinct dialogue_text from dialogue where dialogue_quest_id IN 
                    (select quest_id from quest where chapter_id = ?)''', (chapter_id, ))
    dialogues = cur.fetchall()

    target_word_hit_frequency = 0
    for (dialogue, ) in dialogues:
        target_word_hit_frequency += sentence_analyzer.containTargetWordCounts(dialogue)

    chapter_sentence_count = len(dialogues)
    return target_word_hit_frequency, chapter_sentence_count


chapter_difficulty_list = []
for chapter_id, chapter_name in chapter_infos:
    chapter_difficulty = getEachChapterDifficulty(chapter_id)
    chapter_difficulty_list.append([chapter_id, chapter_name, *chapter_difficulty])
    print(f'finish analyze chapter {chapter_id}, {chapter_name}')

import pandas as pd
df = pd.DataFrame(chapter_difficulty_list, columns=['chapter_id', 'chapter_name', 'difficulty', 'sentence_count'])
df['fifficult_rate'] = df['difficulty'] / df['sentence_count'] * 100
df.to_csv('Chapter_difficulty.csv')

