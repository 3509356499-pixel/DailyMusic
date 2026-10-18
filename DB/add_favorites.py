import sqlite3



conn = sqlite3.connect('music.db')
cursor = conn.cursor()
# 建立favorites数据表
cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites ( 
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  
-- 约束：PRIMARY KEY主键，后面加上AUTOINCREMENT就是自增，插入时可不写id，数据库自动写入
song_id INTEGER NOT NULL,
created_at TEXT DEFAULT CURRENT_TIMESTAMP,
UNIQUE(song_id))  
-- 数据库约束，UNIQUE唯一：这列的值不可重复，写在定义后面，单独一行，是表级约束
""")
conn.commit()
print('建表成功，已成功创建favorite.db数据表')
cursor.execute("PRAGMA table_info(favorites)")       # PRAGMA table_info(favorites) 是 SQLite 特有的元信息查询命令，用来查一张表有哪些列。它不是查业务数据，是查表结构。
for row in cursor.fetchall():
    print(row)
conn.close()
