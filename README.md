[Uploading README.md…]()
# DailyMusic 薛之谦音乐小站

一个基于 **FastAPI + SQLite** 的轻量级音乐网站示例项目，展示薛之谦的代表歌曲，包含歌曲列表、详情页、随机推荐和播放计数功能。

## ✨ 功能特性

- 🎵 内置 10 首薛之谦经典歌曲数据（标题、年份、评分、简介、作词作曲、MV 链接等）
- 🎲 随机推荐一首歌曲
- 📄 歌曲详情页展示
- 🔢 播放次数统计（点击播放自动 +1）
- 🖼️ 静态资源托管（封面图、音频文件、前端页面）

## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.13 | 开发语言 |
| FastAPI | Web 框架 |
| Uvicorn | ASGI 服务器 |
| SQLite | 本地数据库（内置模块，无需安装） |
| HTML / CSS / JS | 前端页面 |

## 📂 项目结构

```
DailyMusic_xue/
├── main.py              # FastAPI 主应用，API 接口与静态资源挂载
├── update_music.py      # 初始化脚本：创建 music 表并写入 10 首歌曲数据
├── add_play_count.py    # 扩展脚本：为 music 表添加 play_count 播放计数字段
├── db_demo.py           # SQLite 数据库学习演示脚本（与项目主功能无关）
├── music.db             # SQLite 数据库（运行时生成，未纳入版本控制）
├── static/
│   ├── index.html       # 首页（歌曲列表）
│   ├── detail.html      # 歌曲详情页
│   ├── cover1~10.jpg    # 歌曲封面图
│   └── audio/           # 歌曲音频（版权保护，未纳入版本控制）
└── .gitignore           # Git 忽略规则
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn
```

### 2. 初始化数据库

```bash
python update_music.py       # 创建 music 表并写入歌曲数据
python add_play_count.py     # 添加 play_count 播放计数字段
```

### 3. 启动服务

```bash
uvicorn main:app --reload
```

启动后访问：

- 前端页面：http://127.0.0.1:8000
- 接口文档（Swagger UI）：http://127.0.0.1:8000/docs

## 🔌 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/music_xue/random_songs` | 随机返回 1 首歌曲 |
| GET | `/api/music_xue/{song_id}` | 按 ID 获取指定歌曲 |
| POST | `/api/music_xue/{song_id}/play` | 播放计数 +1，返回最新播放次数 |

### 返回示例

`GET /api/music_xue/random_songs` 响应：

```json
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
  "video_url": "https://y.qq.com/n/ryqq_v2/mv/c00909gbzLn",
  "play_count": 0
}
```

## 📝 说明

- 本项目为学习演示用途，音频文件与封面图片受版权保护，未包含在仓库中，需自行补充到 `static/audio/` 与 `static/` 目录。
- 数据库文件（`music.db`）未纳入版本控制，首次运行请先执行初始化脚本。
