import os
from contextlib import contextmanager
import pymysql

class Database:
    """Uma conexão e uma transação por operação de negócio."""
    @contextmanager
    def transaction(self):
        conn = pymysql.connect(host=os.getenv('DB_HOST', '127.0.0.1'),
            port=int(os.getenv('DB_PORT', '3306')), user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''), database=os.getenv('DB_NAME', 'projeto_integrado'),
            charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, connect_timeout=5)
        try:
            with conn.cursor() as cursor:
                yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
