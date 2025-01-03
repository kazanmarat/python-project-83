import psycopg2
from psycopg2.extras import DictCursor, execute_values
import datetime


class Database():
    """
    A class for interacting with a PostgreSQL database using psycopg2.

    Attributes:
    - database (str): The connection string for the PostgreSQL database.
    - conn (psycopg2.connection): The database connection object.

    Methods:
    - get_content(): Retrieve content from the database.
    - exist_url_id(id): Check if a given URL id exists in the database.
    - find_url_name(name): Find the URL name in the database.
    - save_url(url): Save a new URL in the database.
    - save_url_check(content): Save URL check information in the database.
    - get_content_check(url_id): Retrieve URL check content from the database.
    """
    def __init__(self, database):
        self.database = database
        self.conn = None

    def _connect(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(self.database)
        return self.conn

    def _close(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.close()

    def _commit(self):
        if self.conn is not None and not self.conn.closed:
            self.conn.commit()

    def get_content(self):
        with self._connect() as conn:
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
                            ORDER BY urls.id DESC,
                                url_checks.created_at DESC,
                                url_checks.status_code DESC'''
                            )
                content = [dict(row) for row in cur]
        self._close()
        return content

    def exist_url_id(self, id):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                            SELECT * FROM urls
                            WHERE id = %s''',
                            (id,))
                content = cur.fetchone() or None
        self._close()
        return content

    def find_url_name(self, name):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                            SELECT * FROM urls
                            WHERE name = %s''',
                            (name,))
                content = cur.fetchone() or [None]
            id = content[0]
        self._close()
        return id

    def save_url(self, url):
        with self._connect() as conn:
            with conn.cursor() as cur:
                created_at = datetime.date.today()
                cur.execute('''
                            INSERT INTO urls (name, created_at)
                            VALUES (%s, %s)
                            RETURNING id''',
                            (url, created_at))
                id = cur.fetchone()[0]
            self._commit()
        self._close()
        return id

    def save_url_check(self, content):
        with self._connect() as conn:
            created_at = datetime.date.today()
            check_info = [(content['url_id'],
                           content['status_code'],
                           content['h1'],
                           content['title'],
                           content['description'],
                           created_at)]
            with conn.cursor() as cur:
                query = '''INSERT INTO url_checks
                                (url_id,
                                status_code,
                                h1,
                                title,
                                description,
                                created_at)
                        VALUES %s'''
                execute_values(cur, query, check_info)
            self._commit()
        self._close()

    def get_content_check(self, url_id):
        with self._connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute('''
                            SELECT * FROM url_checks
                            WHERE url_id = %s
                            ORDER BY id DESC''',
                            (url_id,))
                content = cur.fetchall() or {}
        self._close()
        return content
