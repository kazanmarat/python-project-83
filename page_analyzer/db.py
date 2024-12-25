import psycopg2
from psycopg2.extras import DictCursor
import datetime


class Database():
    def __init__(self, database):
        self.database = database

    def _connect(self):
        return psycopg2.connect(self.database)

    def get_content(self):
        conn = self._connect()
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                        SELECT * FROM urls
                        ORDER BY id DESC'''
                        )
            content = [dict(row) for row in cur]
        conn.close()
        return content

    def find_url_id(self, id):
        conn = self._connect()
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                        SELECT * FROM urls
                        WHERE id = %s''',
                        (id,))
            content = cur.fetchone() or [None]
        conn.close()
        return content

    def find_url_name(self, name):
        conn = self._connect()
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                        SELECT * FROM urls
                        WHERE name = %s''',
                        (name,))
            content = cur.fetchone() or [None]
        id = content[0]
        conn.close()
        return id

    def save_url(self, url):
        created_at = datetime.date.today()
        conn = self._connect()
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO urls (name, created_at)
                        VALUES (%s, %s)
                        RETURNING id''',
                        (url, created_at))
            id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return id
