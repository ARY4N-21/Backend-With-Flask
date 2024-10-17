import sqlite3

def create_db():
    connection = sqlite3.connect('expense_tracker.db')
    cursor = connection.cursor()

    # Create a table for expenses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_db()
