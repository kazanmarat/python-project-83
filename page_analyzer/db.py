import psycopg2
from psycopg2.extras import DictCursor, execute_values
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
                        SELECT DISTINCT ON (urls.id)
                            urls.id,
                            urls.name,
                            url_checks.created_at,
                            url_checks.status_code
                        FROM urls
                        LEFT JOIN url_checks
                        ON urls.id = url_checks.url_id
                        ORDER BY urls.id,
                            url_checks.created_at DESC,
                            url_checks.status_code DESC'''
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

    def save_url_check(self, url_id, status_code):
        h1 = ''
        title = ''
        description = ''
        created_at = datetime.date.today()
        check_info = [(url_id, status_code, h1, title, description, created_at)]
        conn = self._connect()
        with conn.cursor() as cur:
            query = '''INSERT INTO url_checks
                       (url_id, status_code, h1, title, description, created_at)
                       VALUES %s'''
            execute_values(cur, query, check_info)
        conn.commit()
        conn.close()

    def get_content_check(self, url_id):
        conn = self._connect()
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute('''
                        SELECT * FROM url_checks
                        WHERE url_id = %s
                        ORDER BY id DESC''',
                        (url_id,))
            content = cur.fetchall() or {}
        conn.close()
        return content
