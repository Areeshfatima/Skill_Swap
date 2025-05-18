import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)  # Allow streamlit multithreading
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create user table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT,
                password BLOB,
                is_premium BOOLEAN DEFAULT 0
            )
        """)
        # Create Skills table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                skill_name TEXT,
                skill_type TEXT,  
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def add_users(self, username, email, password, is_premium=False):
        try:
            self.cursor.execute("INSERT INTO users (username, email, password, is_premium) VALUES (?, ?, ?, ?)",
                                (username, email, password, is_premium)
                                )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # username already exists
        
    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()
    
    def add_skill(self, user_id, skill_name, skill_type):
        self.cursor.execute("INSERT INTO skills (user_id, skill_name, skill_type) VALUES (?, ?, ?)",
                            (user_id, skill_name, skill_type)
                            )
        self.conn.commit()

    def get_user_skills(self, user_id, skill_type):
        self.cursor.execute("SELECT skill_name FROM skills WHERE user_id = ? AND skill_type = ?",
                            (user_id, skill_type)
                            )
        return [row[0] for row in self.cursor.fetchall()]
    
    def updated_premium_status(self, user_id, is_premium):
        self.cursor.execute("UPDATE users SET is_premium = ? WHERE id = ?",
                            (user_id, is_premium)
                            )
        self.conn.commit()

    def close(self):
        self.conn.close()

