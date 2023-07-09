import re
from typing import List, Set
from word_forms.word_forms import get_word_forms

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


class Sentence_Analyzer():
    def __init__(self, target_words: List[str]) -> None:
        """Init the Sentence Analyzer

        Parameters
        ----------
        target_words : List[str]
            The words that want to learn.
        """

        # get all words that have the same lemma with target words.
        self.target_words_lemma: Set[str] = set()
        for w in target_words:
            self.target_words_lemma = self.target_words_lemma.union(self.get_word_forms_mix(w))


    def get_word_forms_mix(self, word) -> Set[str]:
        result = []
        for i in get_word_forms(word).values():
            result.extend(i)
        return set(result)
    

    def split_words_from_sentence(self, sentence_text: str) -> Set[str]:
        words = re.split('\.|\?|!|\s|,|\(|\)', sentence_text)
        return set(words)


    def containTargetWordCounts(self, sentence_text: str):
        words = self.split_words_from_sentence(sentence_text)
        word_hit_count = 0
        for word in [w.strip().lower() for w in words if w.strip() != ""]:
            if word in self.target_words_lemma:
                word_hit_count += 1
        
        return word_hit_count


if __name__ == '__main__':
    s = Sentence_Analyzer(['apple', 'are'])
    print(s.isContainTargetWords('Apple likes banana.'))
    print(s.isContainTargetWords('xiaoming likes xiaohong.'))
    print(s.isContainTargetWords('Pigs are animals.'))
    