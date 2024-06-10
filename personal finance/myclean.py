import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS καθαρα (item_name text, item_price float, purchase_date date, category text)")
        self.conn.commit()

        # Προσθήκη της στήλης 'category' αν δεν υπάρχει ήδη
        self.cur.execute("PRAGMA table_info(καθαρα)")
        columns = [col[1] for col in self.cur.fetchall()]
        if 'category' not in columns:
            self.cur.execute("ALTER TABLE καθαρα ADD COLUMN category TEXT")
            self.conn.commit()

    def fetchRecord(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insertRecord(self, item_name, item_price, purchase_date, category):
        self.cur.execute("INSERT INTO καθαρα (item_name, item_price, purchase_date, category) VALUES (?, ?, ?, ?)",
                         (item_name, item_price, purchase_date, category))
        self.conn.commit()

    def removeRecord(self, rwid):
        self.cur.execute("DELETE FROM καθαρα WHERE rowid=?", (rwid,))
        self.conn.commit()

    def updateRecord(self, item_name, item_price, purchase_date, category, rid):
        self.cur.execute("UPDATE καθαρα SET item_name = ?, item_price = ?, purchase_date = ?, category = ? WHERE rowid = ?",
                         (item_name, item_price, purchase_date, category, rid))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
