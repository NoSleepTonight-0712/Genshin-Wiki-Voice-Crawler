from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import requests
import os
import sqlite3
from utils.voice_manager import getDestByFileName
from pathlib import Path
import wget

conn = sqlite3.connect("data/data.sqlite")
cur = conn.cursor()

cur.execute('SELECT DISTINCT dialogue_audio_name, dialogue_audio_url from dialogue;')
# cur.execute('SELECT dialogue_audio_name, dialogue_audio_url from dialogue where dialogue_quest_id = (select quest_id from quest where chapter_id = 45);')


records = cur.fetchall()
# print(records)
pool = ThreadPoolExecutor(max_workers=16)

def download(record):
    filepath, link = record
    if not Path(os.path.join(*(filepath.split('\\')[:-1]))).exists():
        os.makedirs(os.path.join(*(filepath.split('\\')[:-1])))

    if Path(filepath).exists():
        filename = filepath.split('\\')[-1]
        print(f"Skip {filename}")
        return
    
    wget.download(link, out=filepath)

if __name__ == '__main__':
    pool.map(download, records)
    pool.shutdown()


