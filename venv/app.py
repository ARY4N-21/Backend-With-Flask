from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('expense_tracker.db')
    conn.row_factory = sqlite3.Row  # Allows access to row data as dict
    return conn

# Initialize the database (Run once to create the table)
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    amount REAL NOT NULL)''')
    conn.commit()
    conn.close()

# Route to get all expenses (GET request)
@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return jsonify([dict(expense) for expense in expenses])

# Route to add a new expense (POST request)
@app.route('/expenses', methods=['POST'])
def add_expense():
    expense_data = request.get_json()
    name = expense_data.get('name')
    amount = expense_data.get('amount')

    if name is None or amount is None:
        return jsonify({'error': 'Invalid input'}), 400

    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO expenses (name, amount) VALUES (?, ?)', (name, amount))
    conn.commit()
    new_expense_id = cursor.lastrowid  # Get the ID of the newly created expense
    conn.close()
    
    # Return the newly created expense as JSON
    return jsonify({'id': new_expense_id, 'name': name, 'amount': amount}), 201

# Route to delete an expense by ID (DELETE request)
@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_db_connection()
    expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (id,)).fetchone()

    if expense is None:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense deleted successfully'})

# Route to update an expense by ID (PUT request)
@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense_data = request.get_json()
    name = expense_data.get('name')
    amount = expense_data.get('amount')

    conn = get_db_connection()
    expense = conn.execute('SELECT * FROM expenses WHERE id = ?', (id,)).fetchone()

    if expense is None:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    if name is None or amount is None:
        conn.close()
        return jsonify({'error': 'Invalid input'}), 400

    conn.execute('UPDATE expenses SET name = ?, amount = ? WHERE id = ?', (name, amount, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense updated successfully'})

if __name__ == '__main__':
    init_db()  # Create the table if it doesn't exist
    app.run(debug=True, port=5001)
