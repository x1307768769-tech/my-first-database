import sqlite3

# 连接数据库（如果没有会自动创建 todo.db 文件）
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# 创建一张“任务表”（如果表不存在才创建）
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        content TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )
''')

# 插入一条示例任务
c.execute("INSERT INTO tasks (content, done) VALUES ('学习用 GitHub 管理项目', 0)")
conn.commit()

# 查询并打印所有任务
print("当前所有任务：")
for row in c.execute("SELECT id, content, done FROM tasks"):
    status = "✅ 已完成" if row[2] else "⬜ 未完成"
    print(f"{row[0]}. {row[1]} {status}")

conn.close()