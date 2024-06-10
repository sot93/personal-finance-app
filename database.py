import sqlite3

class Database:
    def __init__(self, db):
        self.db = db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS καθαρα (item_name text, item_price float, purchase_date date, category text)"
            )
            # Check if 'category' column exists, if not, add it
            cur.execute("PRAGMA table_info(καθαρα)")
            columns = [col[1] for col in cur.fetchall()]
            if 'category' not in columns:
                cur.execute("ALTER TABLE καθαρα ADD COLUMN category TEXT")
            conn.commit()

    def fetch_record(self, query):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    def insert_record(self, item_name, item_price, purchase_date, category):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO καθαρα (item_name, item_price, purchase_date, category) VALUES (?, ?, ?, ?)",
                (item_name, item_price, purchase_date, category)
            )
            conn.commit()

    def remove_record(self, rowid):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM καθαρα WHERE rowid=?", (rowid,))
            conn.commit()

    def update_record(self, item_name, item_price, purchase_date, category, rowid):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE καθαρα SET item_name = ?, item_price = ?, purchase_date = ?, category = ? WHERE rowid = ?",
                (item_name, item_price, purchase_date, category, rowid)
            )
            conn.commit()
import sqlite3

class Database:
    def __init__(self, db):
        self.db = db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS καθαρα (item_name text, item_price float, purchase_date date, category text)"
            )
            # Check if 'category' column exists, if not, add it
            cur.execute("PRAGMA table_info(καθαρα)")
            columns = [col[1] for col in cur.fetchall()]
            if 'category' not in columns:
                cur.execute("ALTER TABLE καθαρα ADD COLUMN category TEXT")
            conn.commit()

    def fetch_record(self, query):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    def insert_record(self, item_name, item_price, purchase_date, category):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO καθαρα (item_name, item_price, purchase_date, category) VALUES (?, ?, ?, ?)",
                (item_name, item_price, purchase_date, category)
            )
            conn.commit()

    def remove_record(self, rowid):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM καθαρα WHERE rowid=?", (rowid,))
            conn.commit()

    def update_record(self, item_name, item_price, purchase_date, category, rowid):
        with sqlite3.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE καθαρα SET item_name = ?, item_price = ?, purchase_date = ?, category = ? WHERE rowid = ?",
                (item_name, item_price, purchase_date, category, rowid)
            )
            conn.commit()
