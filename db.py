import sqlite3
import MySQLdb

# Context managery (sám otevírá a zavírá DB, i když se uvnitř stane výjimka)


class SQLite:
    def __init__(self, file="data.sqlite3"):
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


MYSQL_DEFAULT_SETTINGS = {
    # "host": "USERNAME.mysql.pythonanywhere-services.com",
    "host": "localhost",
    "user": "USERNAME",
    "passwd": "PASSWORD",
    "db": "DBNAME",
    "charset": "utf8"
}


class MySQL:
    def __init__(self, **settings):
        self.settings = MYSQL_DEFAULT_SETTINGS.copy()

        for kw in settings:
            self.settings[kw] = settings[kw]

    def __enter__(self):
        self.conn = MySQLdb.connect(**self.settings)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


########################################################################################

if __name__ == "__main__":
    with SQLite("data.db") as cur:
        res = cur.execute("SELECT * FROM table where a=?", [2])
        for x in res.fetchall():
            print(x)
