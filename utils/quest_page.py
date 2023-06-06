# This file is used for analyze quest page.

# Story Quest Example: https://genshin-impact.fandom.com/wiki/A_Bewildering_Fate
# Archon Quest Example: https://genshin-impact.fandom.com/wiki/A_Forest_of_Change
# Hangout Quest Example: https://genshin-impact.fandom.com/wiki/A_Knight%27s_Journey_Through_Liyue
# Event Quest Example: https://genshin-impact.fandom.com/wiki/A_Gathering_of_Outlanders

import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict
try:
    from utils.global_variables import *
except:
    from global_variables import *


class Quest():
    def __init__(self, url, default_character=CHARACTER_AETHER) -> None:
        """Init the quest by url. 

        Parameters
        ----------
        url : string
            The quest wiki page URL
        default_character : CHARACTER_AETHER or CHARACTER_LUMINE, optional
            Who is the traveler, by default CHARACTER_AETHER
            As the traveler's speaking is usually out of voice, so choose the opposite of your like is better.
            E.G. You want to listen more about Lumine, so please choose Aether as the character. In that case, 
            Lumine will speak in such as "We will be reunited" more.
        """
        self.url = url

        self.default_character = default_character

        content = requests.get(url).content

        self.dom = BeautifulSoup(content, features='lxml')

        self._initQuestMetaData()

    def _initQuestMetaData(self):
        """initialize the quest name and metadata, includes quest type, quest belongings, quest characters, etc.
        """
        quest_name = self.dom.find('div', id='mw-content-text').find('h2', class_="pi-item pi-item-spacing pi-title pi-secondary-background").text

        # filter quest name, for it will be used as file name.
        # Only allow letter and digits.
        quest_name = "".join(filter(str.isalnum, quest_name))

        quest_metadata = self.dom.find('div', id='mw-content-text').find_all('div', class_="pi-item pi-data pi-item-spacing pi-border-color")

        quest_metadata: dict = dict(filter(lambda m : m[0] != 'rewards', [(lambda m : (m.get('data-source'), m.div.text))(i) for i in quest_metadata]))   # split the key and value, and drop the reward record.

        if quest_metadata['type'] == 'Archon':
            self.quest_type = QUEST_TYPE_ARCHON
        elif quest_metadata['type'] == 'Story (Event)':
            self.quest_type = QUEST_TYPE_EVENT
        elif quest_metadata['type'] == 'Story':     # contains Story and Hangout
            if 'group' in quest_metadata and quest_metadata['group'] == 'Hangout Event':
                self.quest_type = QUEST_TYPE_HANGOUT
            else:
                self.quest_type = QUEST_TYPE_STORY
        else:
            self.quest_type = QUEST_TYPE_OTHER

        self.quest_name = quest_name
        self.quest_metadata = quest_metadata


    def extractDialogue(self, dialogue_record: BeautifulSoup):
        """Give a dialogue element by <dd> tag, and return its text and voice.
        Sometimes there will be multiple voices caused by the choice of Traveler.
        We only extract the Lumine voices. 

        Parameters
        ----------
        dialogue_record : <dd> element
            The <dd> tag element.
        """
        audios = dialogue_record.find_all('span', class_='audio-button')
        if self.default_character == CHARACTER_AETHER:
            AUDIO_INDEX = 0
        else:
            AUDIO_INDEX = 1

        # extract audio links
        if len(audios) == 0 or dialogue_record.find('dd') != None:
            # This is not a voice-over text (Such as Traveler's speaking)
            return None
        else:
            audio_link = audios[AUDIO_INDEX].a.get('href')  # Extract the choosen character's voice.

            audio_name = self.quest_name.replace(' ', '_') + '__' + ([i for i in audio_link.split('/') if i.endswith('.ogg')][0])
        
        # extract text
        for i in dialogue_record.find_all('span'):
            i.clear()

        audio_text = dialogue_record.text.strip()

        return audio_text, audio_name, audio_link


    def extractAllDialogues(self) -> List[Tuple[str, str, str]]:
        dds = self.dom.find('div', class_='dialogue').find_all('dd')
        result = []

        for dd in dds:
            r = self.extractDialogue(dd)
            if type(r) == type((1,)):    # has voice-over
                result.append(r)
        return result
    
    def getMetaData(self) -> Dict:
        try:
            chapter = self.quest_metadata['chapter']
        except:
            chapter = 'None'
            
        return {
            'quest_name': self.quest_name,
            'quest_type': self.quest_type,
            'chapter': chapter,
            'quest_link': self.url
        }
    
    def extractAll(self) -> Tuple[Dict, List[Tuple[str, str, str]]]:
        """extract all data from quest

        Returns
        -------
        Tuple[Dict, List[Tuple[str, str, str]]]
            MetaData, Dialogues
        """
        return self.getMetaData(), self.extractAllDialogues()
    

if __name__ == '__main__':
    q = Quest('https://genshin-impact.fandom.com/wiki/A_Soul_Set_Apart')
    result = q.extractAllDialogues()
   
    
        
