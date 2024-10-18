import sqlite3

def create_db():
    connection = sqlite3.connect('expense_tracker.db')
    cursor = connection.cursor()

    # Create a table for expenses with timestamps
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Automatically sets when the record is created
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP -- Can be updated on record change if needed
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_db()
