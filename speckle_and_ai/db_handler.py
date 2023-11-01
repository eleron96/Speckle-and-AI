import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="results.db"):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                commit_id TEXT,
                upload_date TEXT,
                file_name TEXT,
                number_of_elements INTEGER,
                number_of_wall_elements INTEGER
            )
            ''')
            conn.commit()

    def save_result(self, commit_id, upload_date, file_name, number_of_elements, number_of_wall_elements):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO results (commit_id, upload_date, file_name, number_of_elements, number_of_wall_elements)
            VALUES (?, ?, ?, ?, ?)
            ''', (commit_id, upload_date, file_name, number_of_elements, number_of_wall_elements))
            conn.commit()

    def get_previous_results(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM results")
            results = cursor.fetchall()
        return results

