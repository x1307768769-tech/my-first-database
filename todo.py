import sqlite3


def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def show_tasks():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    print("\n======= 当前所有任务 =======")
    for row in c.execute("SELECT id, content, done FROM tasks"):
        status = "✅ 已完成" if row[2] else "⬜ 未完成"
        print(f"{row[0]}. {row[1]} {status}")
    print("============================\n")
    conn.close()


def add_task(content):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (content, done) VALUES (?, ?)", (content, 0))
    conn.commit()
    conn.close()
    print(f"已添加任务：{content}")


def mark_done(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET done = 1, completed_at = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"任务 {task_id} 已标记为完成！")


def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"任务 {task_id} 已删除！")


def import_from_file(filename):
    """从文本文件批量导入任务，每行一个任务"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        count = 0
        for line in lines:
            content = line.strip()
            if content:
                conn = sqlite3.connect('todo.db')
                c = conn.cursor()
                c.execute("INSERT INTO tasks (content, done) VALUES (?, ?)", (content, 0))
                conn.commit()
                conn.close()
                count += 1

        print(f"✅ 成功从 {filename} 导入了 {count} 个任务！")
    except FileNotFoundError:
        print(f"❌ 文件 {filename} 不存在，请先创建它")


def main():
    init_db()
    while True:
        print("请选择操作：")
        print("1. 查看所有任务")
        print("2. 添加任务")
        print("3. 标记任务完成")
        print("4. 删除任务")
        print("5. 从文件批量导入")
        print("6. 退出")
        choice = input("请输入数字(1-6): ")

        if choice == "1":
            show_tasks()
        elif choice == "2":
            content = input("请输入任务内容: ")
            add_task(content)
        elif choice == "3":
            task_id = input("请输入要完成的任务ID: ")
            mark_done(task_id)
        elif choice == "4":
            task_id = input("请输入要删除的任务ID: ")
            delete_task(task_id)
        elif choice == "5":
            filename = input("请输入文件名(如 tasks.txt): ")
            import_from_file(filename)
        elif choice == "6":
            print("再见！")
            break
        else:
            print("输入有误，请重新选择")


if __name__ == "__main__":
    main()