import sqlite3

DATABASE_NAME = "results.db"

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
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
    conn.close()

def save_result(commit_id, upload_date, file_name, number_of_elements, number_of_wall_elements):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO results (commit_id, upload_date, file_name, number_of_elements, number_of_wall_elements)
    VALUES (?, ?, ?, ?, ?)
    ''', (commit_id, upload_date, file_name, number_of_elements, number_of_wall_elements))

    conn.commit()
    conn.close()

def get_previous_results():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    results = cursor.fetchall()

    conn.close()
    return results
