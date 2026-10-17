import sqlite3
import time

# ============================================================
# 阶段一：连接与认证
# ============================================================
# SQLite 是本地文件数据库，没有网络认证环节。
# 如果是 MySQL/PostgreSQL，这里会包含 host/port/user/password。
# connect() 相当于建立了一个"会话"（session）。
conn = sqlite3.connect("demo.db")

# cursor 是会话中的"游标"，所有 SQL 都通过它发送。
cursor = conn.cursor()

# ============================================================
# 阶段二：准备数据（DDL + DML）
# ============================================================
# DDL：创建表结构，相当于定义"书架"。
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT    NOT NULL,
        balance REAL    DEFAULT 0
    )
""")

# 插入初始数据，模拟已有业务数据。
cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", ("Alice", 100.0))
cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", ("Bob",   50.0))
conn.commit()   # 提交事务，数据真正持久化

# ============================================================
# 阶段三：解析与编译（由数据库内部完成，这里做演示说明）
# ============================================================
# 当我们执行下面这条 SQL 时，数据库内部会经历：
#   1. 词法/语法分析   -> 检查 "SELECT" 拼写、括号是否匹配
#   2. 语义分析         -> 检查 users 表、balance 列是否存在
#   3. 生成逻辑计划     -> 先扫描 users，再过滤 balance > 60
#   4. 查询优化         -> 若有索引，决定是否走索引
#   5. 生成物理计划     -> 交给执行引擎
#
# 我们可以用 EXPLAIN QUERY PLAN 查看优化器选择的执行计划：
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE balance > ?", (60,))
print("【执行计划】", cursor.fetchall())
# 输出类似：[(0, 0, 0, 'SCAN users')] 表示全表扫描

# ============================================================
# 阶段四：执行与事务管理
# ============================================================
# 用事务模拟一次转账：Alice 转 30 给 Bob
# 事务保证：要么都成功，要么都回滚（原子性）。
try:
    # BEGIN 开启事务（SQLite 默认 autocommit，这里显式开启）
    conn.execute("BEGIN")

    # --- 步骤 1：扣款 ---
    # 数据库内部会：加锁 -> 写 undo log -> 改内存 -> 写 redo log
    cursor.execute("UPDATE users SET balance = balance - ? WHERE name = ?", (30, "Alice"))

    # --- 步骤 2：入账 ---
    cursor.execute("UPDATE users SET balance = balance + ? WHERE name = ?", (30, "Bob"))

    # --- 步骤 3：提交 ---
    # 提交后 redo log 标记为 committed，事务持久化。
    conn.commit()
    print("【事务】转账成功")

except Exception as e:
    # 任何一步出错，回滚到事务开始前的状态（利用 undo log）。
    conn.rollback()
    print("【事务】转账失败，已回滚：", e)

# ============================================================
# 阶段五：结果返回与清理
# ============================================================
# 查询类操作：执行引擎取数据 -> 通过网络/内存返回给客户端。
cursor.execute("SELECT id, name, balance FROM users ORDER BY id")
rows = cursor.fetchall()        # 一次性取回所有结果
for row in rows:
    print("【查询结果】", row)

# 更新类操作：返回受影响行数。
cursor.execute("UPDATE users SET balance = balance WHERE id = 1")
print("【受影响行数】", cursor.rowcount)

# 资源清理：关闭游标和连接，释放会话资源。
cursor.close()
conn.close()

# ============================================================
# 阶段六：后台异步流程（概念说明，SQLite 中较简化）
# ============================================================
# 在 MySQL/PostgreSQL 等企业级数据库中，还有后台线程：
#   - checkpoint：定期把内存脏页刷回磁盘
#   - purge     ：清理无用的 undo log
#   - 统计信息更新：为优化器提供最新数据分布
#   - 日志归档  ：管理 redo log / binlog 生命周期
#
# SQLite 是嵌入式数据库，这些流程被大幅简化，
# 但 WAL 模式下依然有 checkpoint 机制。