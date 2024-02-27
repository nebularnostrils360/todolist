import sqlite3

class dbhelper:
    def __init__(self, user_name):
        self.conn = sqlite3.connect(f"./databases/{user_name}.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS todo(
                            todoid INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT,
                            creationDate DATE NOT NULL,
                            dueDate DATE,
                            completionDate Date
                            );""")
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

    def create(self, title, desc, due_date = None):
        data = title, desc, due_date
        self.cursor.execute("""INSERT INTO 
                            todo(title, description, creationDate, dueDate)
                            VALUES(?, ?,CURRENT_DATE , ?);""", data)
        self.conn.commit()

    def display(self):
        self.cursor.execute("""SELECT * FROM todo;""")
        return self.cursor.fetchall()
        
        
    def delete(self, id):
        popped_tuple = self.cursor.execute(f"SELECT * FROM todo WHERE todoid = {id};").fetchone()
        
        self.cursor.execute(f"DELETE FROM todo WHERE todoid = {id};")
        self.conn.commit()
        return popped_tuple

    def update(self, id, title = None, desc = None, due = None):
        if title:
            self.cursor.execute(f"""UPDATE todo 
                                SET title = ?
                                WHERE todoid = {id};""", (title,))
        if desc:
            self.cursor.execute(f"""UPDATE todo
                    SET description = ?
                    WHERE todoid = {id};""", (desc,))
        if due:
            self.cursor.execute(f"""UPDATE todo
                    SET dueDate = ?
                    WHERE todoid = {id};""", (due,))

        self.conn.commit()
        updated_tuple = self.cursor.execute(f"SELECT * FROM todo WHERE todoid = {id};").fetchone()
        return updated_tuple

    def mark_complete(self, id):
        fetched_tuple = self.cursor.execute(f"SELECT * FROM todo WHERE todoid = {id};").fetchone()
        default_completion_date = fetched_tuple[-1]

        if not default_completion_date:
            self.cursor.execute(f"""UPDATE todo
                                    SET completionDate = CURRENT_DATE
                                    WHERE todoid = {id};""")
            self.conn.commit()
        
        
        return self.cursor.execute(f"SELECT * FROM todo WHERE todoid = {id};").fetchone()

    def getTaskInfo(self, id):
        self.cursor.execute(f"""SELECT * FROM todo WHERE todoid = {id};""")
        return self.cursor.fetchone()


