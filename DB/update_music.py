# 把 Python 里写死的 10 首薛之谦歌曲数据，批量写入一个 SQLite 数据库文件 music.db 中，方便后续查询/展示


import sqlite3
songs = [
    {
        "id": 1,
        "title": "认真的雪",
        "year": 2006,
        "tag": "爱情/伤感",
        "score": 9.5,
        "desc": "薛之谦早期的代表作，中式R&B曲风，记录了一段凄美的爱情记忆。",
        "bg": "/cover1.jpg",
        "audio": "/audio/1.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/c00909gbzLn"
    },
    {
        "id": 2,
        "title": "演员",
        "year": 2015,
        "tag": "爱情/纠结",
        "score": 9.8,
        "desc": "薛氏情歌的巅峰之作，以\"在爱情面前，我不是一位演员\"为理念，唱出感情中的无奈。",
        "bg": "/cover2.jpg",
        "audio": "/audio/2.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/o0016t2ucce"
    },
    {
        "id": 3,
        "title": "绅士",
        "year": 2015,
        "tag": "爱情/隐忍",
        "score": 9.6,
        "desc": "表达\"朋友以上，恋人未满\"的绅士概念，旋律舒缓，歌词深情。",
        "bg": "/cover3.jpg",
        "audio": "/audio/3.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦, 裴涩琪",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/z0016p7fv5s"
    },
    {
        "id": 4,
        "title": "丑八怪",
        "year": 2013,
        "tag": "自嘲/社会",
        "score": 9.7,
        "desc": "李荣浩作曲，薛之谦以冷酷语气自嘲，讽刺外表与内心的反差。",
        "bg": "/cover4.jpg",
        "audio": "/audio/4.mp3",
        "lyricist": "甘世佳",
        "composer": "李荣浩",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/r0023z3ybcu"
    },
    {
        "id": 5,
        "title": "天外来物",
        "year": 2020,
        "tag": "爱情/幻想",
        "score": 9.4,
        "desc": "薛之谦作词，曲风斑斓，被形容为\"第12号初秋奏鸣曲\"。",
        "bg": "/cover5.jpg",
        "audio": "/audio/5.mp3",
        "lyricist": "薛之谦",
        "composer": "罗小黑",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/t0035otrp1j"
    },
    {
        "id": 6,
        "title": "我好像在哪见过你",
        "year": 2016,
        "tag": "爱情/回忆",
        "score": 9.3,
        "desc": "动画电影《精灵王座》主题曲，延续薛氏情歌的细腻与伤感。",
        "bg": "/cover6.jpg",
        "audio": "/audio/6.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/b0020rlv2g6"
    },
    {
        "id": 7,
        "title": "意外",
        "year": 2013,
        "tag": "摇滚/爱情",
        "score": 9.2,
        "desc": "流行摇滚风格，杨子朴作词曲，是薛之谦转型期的代表作品之一。",
        "bg": "/cover7.jpg",
        "audio": "/audio/7.mp3",
        "lyricist": "杨子朴",
        "composer": "杨子朴",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq/mv/f00138jq44x"
    },
    {
        "id": 8,
        "title": "刚刚好",
        "year": 2016,
        "tag": "爱情/释怀",
        "score": 9.1,
        "desc": "网络剧《我与你的光年距离》主题曲，旋律层次分明，副歌记忆点极高。",
        "bg": "/cover8.jpg",
        "audio": "/audio/8.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/c00200si22o"
    },
    {
        "id": 9,
        "title": "你还要我怎样",
        "year": 2013,
        "tag": "爱情/苦情",
        "score": 9.5,
        "desc": "招牌薛氏情歌，正话反说的歌词，情绪从冷静到激动再回归冷静。",
        "bg": "/cover9.jpg",
        "audio": "/audio/9.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/yqq/mv/m/013ybtFU157HaW.html"
    },
    {
        "id": 10,
        "title": "方圆几里",
        "year": 2013,
        "tag": "爱情/一厢情愿",
        "score": 9.0,
        "desc": "爱情微电影《最熟悉的陌生人》主题曲，唱出一厢情愿的坚守。",
        "bg": "/cover10.jpg",
        "audio": "/audio/10.mp3",
        "lyricist": "薛之谦",
        "composer": "薛之谦",
        "director": "未知",
        "actors": "薛之谦",
        "video_url": "https://y.qq.com/n/ryqq_v2/mv/q00118hy3yb"
    }
]


# 创建数据库路径
DB_PATH= "music.db"

# 连接数据库
connect=sqlite3.connect(DB_PATH)
# 创建游标对象
cursor=connect.cursor()

# 为了防止再次运行的时候运行失败，得先把之前建的表删除
cursor.execute("DROP TABLE IF EXISTS music")
# 建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS music (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
year INTEGER NOT NULL,
tag TEXT NOT NULL,
score REAL NOT NULL,
desc TEXT NOT NULL,
bg TEXT NOT NULL,
audio TEXT NOT NULL,
lyricist TEXT NOT NULL,
composer TEXT NOT NULL,
director TEXT NOT NULL,
actors TEXT NOT NULL,
video_url TEXT
)
""")

# 为了避免重复运行会重复插入，在插入前先写入一个删除表里的数据
cursor.execute("DELETE FROM music" )
# 循环插入数据
for song in songs:
    cursor.execute("INSERT INTO music(title,year,tag,score,desc,bg,audio,lyricist,composer,director,actors,video_url)VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(
        song['title'],
        song['year'],
        song['tag'],
        song['score'],
        song['desc'],
        song['bg'],
        song['audio'],
        song['lyricist'],
        song['composer'],
        song['director'],
        song['actors'],
        song['video_url']
    ))


# 这里重新写一个插入方法：建表手写 + 插入用字典动态生成
# 建表：
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS music (
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     year INTEGER NOT NULL,
#     tag TEXT NOT NULL,
#     score REAL NOT NULL,
#     "desc" TEXT NOT NULL,
#     bg TEXT NOT NULL,
#     audio TEXT NOT NULL,
#     lyricist TEXT NOT NULL,
#     composer TEXT NOT NULL,
#     director TEXT NOT NULL,
#     actors TEXT NOT NULL,
#     video_url TEXT
# )
# """)
#
# # 插入：用字典动态生成 SQL
# for song in songs:
#     # 去掉 id，让数据库自增
#     data = {k: v for k, v in song.items() if k != "id"}
#
#     # 字段名：每个 key 加双引号，防止 desc 等关键字冲突
#     cols = ", ".join(f'"{k}"' for k in data.keys())
#     # 占位符：有几个字段就几个 ?
#     placeholders = ", ".join(["?"] * len(data))
#
#     sql = f'INSERT INTO music ({cols}) VALUES ({placeholders})'
#     cursor.execute(sql, list(data.values()))

# 这里新建一个收藏表格



connect.commit()
print('数据插入成功，已成功创建music.db数据表')
connect.close()