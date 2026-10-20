import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect(
            "database/stones.db",
            check_same_thread=False
        )

        self.create_tables()

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT,
            stone_type TEXT,
            confidence REAL,
            color TEXT,
            location TEXT,
            note TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def add_analysis(
        self,
        image_path,
        stone_type,
        confidence,
        color,
        note=""
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO stones (
                image_path,
                stone_type,
                confidence,
                color,
                note
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                image_path,
                stone_type,
                confidence,
                color,
                note
            )
        )

        self.conn.commit()

    def get_analysis_count(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM stones"
        )

        row = cursor.fetchone()

        return row[0] if row else 0

    def get_last_analysis(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            stone_type,
            confidence,
            created_at
        FROM stones
        ORDER BY id DESC
        LIMIT 1
        """)

        return cursor.fetchone()

    def get_most_detected(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            stone_type,
            COUNT(*)
        FROM stones
        GROUP BY stone_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """)

        return cursor.fetchone()

    def get_last_analyses(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            id,
            stone_type,
            confidence,
            created_at
        FROM stones
        ORDER BY id DESC
        LIMIT 100
        """)

        return cursor.fetchall()

    def delete_analysis(
        self,
        analysis_id
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM stones
            WHERE id=?
            """,
            (analysis_id,)
        )

        self.conn.commit()

    def clear_history(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "DELETE FROM stones"
        )

        self.conn.commit()

    def get_stone_statistics(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            stone_type,
            COUNT(*)
        FROM stones
        GROUP BY stone_type
        ORDER BY COUNT(*) DESC
        """)

        return cursor.fetchall()

    def get_analysis_by_id(self, analysis_id):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                stone_type,
                confidence,
                color,
                note,
                created_at

            FROM stones

            WHERE id=?
            """,
            (analysis_id,)
        )

        return cursor.fetchone()
    def close(self):

        if self.conn:
            self.conn.close()


db = Database()