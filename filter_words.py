import sqlite3
import itertools
import copy

conn = sqlite3.connect("data/data.sqlite")
cur = conn.cursor()

from word_forms.word_forms import get_word_forms

with open('vocabulary_list/扇贝托福核心词.txt') as f:
    learning_word_list = f.read().strip().split('\n')

def get_word_forms_mix(word):
    result = []
    for i in get_word_forms(word).values():
        result.extend(i)
    return set(result)

cur.execute('update dialogue set word_frequency = 0;')
conn.commit()

missing_words = []
result_dict = dict()
for i, lemma_word in enumerate(learning_word_list):
    word_forms = get_word_forms_mix(lemma_word)
    match_dialogue_id = []
    for w in word_forms:
        cur.execute(f'select dialogue_id from dialogue where dialogue_text LIKE "%{w}%"')
        select_result = cur.fetchall()
        select_result = set(itertools.chain(*select_result))

        match_dialogue_id.extend(select_result)

    match_dialogue_id = set(match_dialogue_id)

    if len(match_dialogue_id) == 0:
        missing_words.append(lemma_word)

    result_dict[lemma_word] = match_dialogue_id

word_result_dict = copy.deepcopy(result_dict)

def reverse_dict(origin_dict):
    sentence_result_dict = dict()
    for word, sentences in origin_dict.items():
        for sentence in sentences:
            try:
                sentence_result_dict[sentence].append(word)
            except:
                sentence_result_dict[sentence] = [word]
    return sentence_result_dict


def sort_reversed_dict(origin_dict):
    return dict(sorted(origin_dict.items(), key=lambda d : len(d[1]), reverse=True))


def removeSentence(sentence_invoke_word_list, sentence_id):
    for w in sentence_invoke_word_list:
        del word_result_dict[w]

selected_sentences = []
sentence_result_dict = sort_reversed_dict(reverse_dict(word_result_dict))

while True:
    pop_sentence_id = list(sentence_result_dict.keys())[0]  # Get the most occurence sentence first.

    # stop condition
    if len(sentence_result_dict[pop_sentence_id]) == 0:
        break

    removeSentence(sentence_result_dict[pop_sentence_id], pop_sentence_id)  # Remove the link in the result_dict

    selected_sentences.append((pop_sentence_id, len(sentence_result_dict[pop_sentence_id])))      # add to result

    sentence_result_dict = sort_reversed_dict(reverse_dict(word_result_dict)) # generate again

    
    if len(sentence_result_dict) == 0:
        break

import pandas as pd
df = pd.DataFrame(selected_sentences, columns=['Sentence ID', 'Word Frequency'])
df.to_csv('selected_sentences.csv')
