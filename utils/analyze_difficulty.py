import re

def difficulty_analyze(text: str):
    if ':' in text:
        text = text[text.index(':')+1:].replace('...', '').strip()
    else:
        text = text.replace('...', '').strip()
    sentences = re.split('\.|\?|!', text)
    sentences = [i.strip() for i in sentences]

    length_of_sentences = [len(s.split(' ')) for s in sentences]

    try:
        max_sentence_length = max(length_of_sentences)
    except:
        print(text)

    return max_sentence_length


def isSimpleSentece(sentence_text: str):
    