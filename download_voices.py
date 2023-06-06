from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import requests
import os
import sqlite3

conn = sqlite3.connect("data/data.sqlite")
cur = conn.cursor()

cur.execute('SELECT dialogue_audio_name, dialogue_audio_url from dialogue;')

records = cur.fetchall()

pool = ThreadPoolExecutor(max_workers=16)

exist_file_list = os.listdir('voice')

def download(record):
    filename, link = record
    filepath = os.path.join('voice', filename)
    if filename in exist_file_list:
        print(f'Skip {filename}')
        return
    
    content = requests.get(link).content

    with open(filepath, 'wb') as f:
        f.write(content)
        print(f'finish {filename}')

if __name__ == '__main__':
    pool.map(download, records)
    pool.shutdown()


