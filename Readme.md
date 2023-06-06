## 执行顺序

### 建表
安装SQLite3  
执行`sqlite3 data.sqlite`，在`data`文件夹下创建数据库文件`data.sqlite`  
执行`SQL/create table.sql`建表

#### 索引数据下载
执行`load_in_data.py`，数据会自动录入数据库。

#### 例句选取
执行`filter_words.py`，生成`selected_sentences.csv`例句索引文件

#### 制卡
执行`export_anki_cards.py`，生成anki卡组。

