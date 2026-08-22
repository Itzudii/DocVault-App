from pathlib import Path
import sqlite3
from kivy.utils import platform

if platform == "android":

    from android.storage import app_storage_path

    DB_PATH = Path(app_storage_path()) / "docvault.db"

else:

    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / "docvault.db"


# Make sure the database directory exists
DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Connect
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    custom_name TEXT NOT NULL,
    original_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


class Database:

    @staticmethod
    def add_document(custom_name, original_name, file_path, file_type):
        cursor.execute("""
        INSERT INTO documents(custom_name, original_name, file_path, file_type)
        VALUES (?, ?, ?, ?)
        """, (custom_name, original_name, file_path, file_type))
        conn.commit()

    @staticmethod
    def get_document(doc_id):
        cursor.execute("""
            SELECT id, custom_name, original_name, file_path, file_type, created_at
            FROM documents
            WHERE id = ?
        """, (doc_id,))

        return cursor.fetchone()

    @staticmethod
    def get_documents():
        cursor.execute("""
        SELECT id, custom_name, original_name, file_path, file_type
        FROM documents
        ORDER BY created_at DESC
        """)
        return cursor.fetchall()

    @staticmethod
    def rename_document(doc_id, new_name):
        cursor.execute("""
        UPDATE documents
        SET custom_name=?
        WHERE id=?
        """, (new_name, doc_id))
        conn.commit()

    @staticmethod
    def delete_document(doc_id):
        cursor.execute("""
        DELETE FROM documents
        WHERE id=?
        """, (doc_id,))
        conn.commit()

    @staticmethod
    def get_document_count():
        cursor.execute("""
            SELECT COUNT(*)
            FROM documents
        """)
    
        return cursor.fetchone()[0]