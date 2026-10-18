import random
import sqlite3                      # 导入 Python 内置的 SQLite 数据库模块
from fastapi import FastAPI, HTTPException
from starlette.staticfiles import StaticFiles


app = FastAPI()


def get_connection_db():
    """连接数据库，并让查询结果支持按列名访问"""

    # 打开（或创建）名为 db.sqlite3 的数据库文件
    # 文件不存在时会自动新建一个空的
    connection = sqlite3.connect("DB/music.db")
    # 关键设置：把「行工厂」设为 sqlite3.Row
    # 默认查询返回的是元组，只能 row[0]、row[1] 按下标取
    # 设置后返回的行可像字典一样按列名取，如 row["title"]
    connection.row_factory = sqlite3.Row
    # 把连接对象返回给调用者，调用者用它创建游标、执行 SQL
    return connection

# 主页面接口，随机播放
@app.get("/api/music_xue/random_songs")
async def get_random_songs():
    connection = get_connection_db()
    try:
        row = connection.execute(
            "SELECT * FROM music ORDER BY RANDOM() LIMIT 1"  # 改成只取1首
        ).fetchone()
    finally:
        connection.close()

    if not row:
        raise HTTPException(status_code=404, detail="未找到音乐")

    return dict(row)  # Row转字典，FastAPI才能序列化

# 收藏列表接口
@app.get("/api/music_xue/favorites")
async def get_favorites_list():
    connection = get_connection_db()
    try:
        rows = connection.execute(
            # 把收藏表和歌曲表按 song_id 连起来，取出每首收藏歌的 id、歌名、封面、音频、收藏时间，按收藏时间从新到旧排序
            """
            SELECT m.id, m.title, m.bg, m.audio, f.created_at
            FROM favorites f
            JOIN music m ON m.id = f.song_id
            ORDER BY f.created_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()

# 歌曲详情功能接口
@app.get("/api/music_xue/{song_id}")
async def get_song_by_id(song_id: int):
    connection = get_connection_db()
    try:
        row = connection.execute(
            "SELECT * FROM music WHERE id=?", (song_id,)
        ).fetchone()
    finally:
        connection.close()

    if not row:
        raise HTTPException(status_code=404, detail="未获取到该歌曲")

    return dict(row)

# 歌曲播放次数功能接口
@app.post("/api/music_xue/{song_id}/play")
async def add_play_count(song_id: int):
    connection = get_connection_db()
    try:
        # 1. 查这首歌在不在
        row1=connection.execute(
            "SELECT * FROM music WHERE id=?", (song_id,)
        ).fetchone()
        # 2. 不在 -> raise HTTPException(404, ...)
        if not row1:
            raise HTTPException(status_code=404, detail="未获取到该歌曲")
        # 3. 在 -> UPDATE music SET play_count = play_count + 1 WHERE id=?
        connection.execute(
            "UPDATE music SET play_count = play_count + 1 WHERE id=?", (song_id,)
        )
        # 4. connection.commit()
        connection.commit()
        # 5. 再 SELECT 一次 play_count
        row2 = connection.execute(
            "SELECT * FROM music WHERE id=?", (song_id,)
        ).fetchone()
        # 6. return 一个 dict
        return {"song_id": song_id, "play_count": row2["play_count"]}
    finally:
        connection.close()

# 收藏功能接口
@app.post("/api/music_xue/{song_id}/favorites")
async def add_favorite(song_id: int):
    connection = get_connection_db()
    try:
        # 查询歌曲，是否存在
        row1=connection.execute(
            "SELECT * FROM music WHERE id=?", (song_id,) # 注意：这里的(song_id,)是元组，不能写成(song_id)，因为(song_id)是整数形式
        ).fetchone()
        # 2. 不在 -> raise HTTPException(404, ...)
        if not row1:
            raise HTTPException(status_code=404, detail="未找到该歌曲")
        # 插入歌曲进收藏列表
        connection.execute(
            "INSERT OR IGNORE INTO favorites (song_id) VALUES (?)", (song_id,)  # 为什么用 OR IGNORE？因为你表上有 UNIQUE(song_id)，重复插会报错，IGNORE 让它安静跳过
        )
        connection.commit()
        return {"song_id": song_id, "favorite": True}
    finally:
        connection.close()

# 取消收藏功能接口
@app.delete("/api/music_xue/{song_id}/favorites")
async def delete_favorite(song_id: int):
    connection = get_connection_db()
    try:
        row1 = connection.execute(
            "SELECT * FROM favorites WHERE song_id=?", (song_id,) # 注意：传进来的 song_id 是歌曲 id，所以 WHERE 条件应该是 song_id=?，不是 id=?
        ).fetchone()
        if not row1:
            raise HTTPException(status_code=404, detail="未收藏该歌曲")
        connection.execute(
            "DELETE FROM favorites WHERE song_id=?", (song_id,)
        )  # 注意：DELETE 不返回行，.fetchone() 会报错或者返回 None。DELETE 的返回值是 cursor，你只能看 cursor.rowcount
        connection.commit()
        return {"song_id": song_id, "favorite": False}
    finally:
        connection.close()

# 查看歌曲是否收藏接口
@app.get("/api/music_xue/{song_id}/favorites")
async def get_favorites(song_id: int):
    connection = get_connection_db()
    try:
        row = connection.execute(
            "SELECT 1 FROM favorites WHERE song_id=?",(song_id,)   # 在 favorites 表里找 song_id 等于这个值的行，找到就返回一个 1，找不到就返回空。
        ).fetchone()
    finally:
        connection.close()
    if not row:
        raise HTTPException(status_code=404)
    return dict(row)


# @app.get("/api/music_xue/random_songs")
# async def get_random_songs():
#     connection = get_connection_db()
#     random_sql = "SELECT * FROM music ORDER BY RANDOM() LIMIT 1"
#     music=connection.execute(random_sql).fetchall()
#     connection.close()
#     if not music:
#         raise HTTPException(status_code=404, detail='未找到该iD的音乐')
#     return dict(music)

# @app.get("/api/music_xue/{song_id}")
# async def get_song_by_id(song_id: int):
#     connection = get_connection_db()
#     music=connection.execute(
#         ("SELECT * FROM music WHERE id=?"), (song_id,)
#     ).fetchone()
#     connection.close()
#     if not music:
#         raise HTTPException(status_code=404, detail="未获取到该歌曲")
#     return music

# 挂载静态文件目录
app.mount("/audio", StaticFiles(directory="static/audio"), name="audio")
app.mount("/", StaticFiles(directory="static", html=True), name="static")
