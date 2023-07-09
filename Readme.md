## Version log
Updated 3.8 events (2023-07-09)

## Genshin Wiki Voice Crawler
This repo is used for crawling the Genshin fandom wiki to archieve all the voice (only English) in the game Genshin Impact.  
It will collect voices from Events and Character Voice, and store them to an SQLite database.  
It can also export these voice to an Anki card desk for English learning.  

本项目用于抓取原神fandom wiki上的语音（包括角色语音和任务语音，仅英语）。  
抓取到的数据将存储于SQLite数据库。  
支持导出为Anki卡组。




## 执行顺序  Process

### 建表  Create the table
安装SQLite3  
执行`sqlite3 data.sqlite`，在`data`文件夹下创建数据库文件`data.sqlite`  
执行`SQL/create table.sql`建表

Install SQLite3  
execute `sqlite3 data.sqlite` to create the database file `data.sqlite` under `data` folder.
execute `SQL/create table.sql` to create tables.

#### 索引数据下载   Download Index data
执行`load_in_data.py`，数据会自动录入数据库。
execute `load_in_data.py`, data downloaded will be recorded in the database.


#### 音频数据下载   Download Voice media file
执行`download_voices.py`，数据将下载到`voice`文件夹下。
execute `download_voice.py`, data will be downloaded to `voice` folder.


#### 导出为Anki卡组   Export as Anki deck
修改或执行`export_each_event.py`，或者使用`export_cards_by_SQL`自定义导出。  
`export_each_event.py`将会将逐个任务的全部语音依次导出至`export`文件夹。
modify or execute `export_each_event.py`, or use `export_cards_by_SQL` to export whatever you want by SQL.
`export_each_event.py` will export each voice in each event to `export` folder.



