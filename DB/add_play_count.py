import sqlite3

connection = sqlite3.connect('music.db')
cursor = connection.cursor()
#使用异常处理防止文件再次运行时会出现已增加过要加的列表而报错
try:
    # 给数据库加列   SQL标准里改表结构用 ALTER TABLE
    cursor.execute("ALTER TABLE music ADD COLUMN play_count INTEGER DEFAULT 0")     # ADD COLUMN play_count：加一列，叫 play_count  INTEGER：类型是整数 DEFAULT 0：已有行和以后新插入的行，默认都是 0
    connection.commit()
    print("添加成功")
except sqlite3.OperationalError as e:   # sqlite3.OperationalError：只接住 SQLite 的"操作错误"这一类; as e：把错误对象存到变量 e
    if "duplicate column" in str(e):   #"duplicate column" in ...：判断错误文字里有没有这个片段
        print("列已存在，跳过")
    else:
        raise   #raise：把原异常重新抛出去，让程序正常报错

# 验证是否加列成功
cursor.execute("PRAGMA table_info(music)")    # PRAGMA是SQLite的一个特殊命令，用来查数据库的元信息。PRAGMA table_info(music) 的意思是：告诉我 music 这张表有哪些列、每列的类型、默认值、是否主键
columns = cursor.fetchall()   # fetchall() 的作用是：把结果全部取回来，变成一个 Python 列表。
for col in columns:
    print(col)
connection.commit()
connection.close()