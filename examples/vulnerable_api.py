"""
Intentionally vulnerable API code for security audit demonstration.
DO NOT USE IN PRODUCTION.
"""

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# VULNERABILITY: Hardcoded credentials
DB_PASSWORD = "admin123"
API_SECRET = "sk_live_abc123xyz789"

@app.route('/user/<user_id>')
def get_user(user_id):
    """Get user by ID - VULNERABLE TO SQL INJECTION"""
    # VULNERABILITY: SQL injection - user input concatenated into query
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    # VULNERABILITY: Exposing sensitive data (password) in API response
    return jsonify({
        "id": user[0],
        "username": user[1],
        "password": user[2],  # Never expose passwords!
        "email": user[3],
        "ssn": user[4]  # PII exposure
    })

@app.route('/login', methods=['POST'])
def login():
    """User login - MULTIPLE VULNERABILITIES"""
    username = request.json.get('username')
    password = request.json.get('password')

    # VULNERABILITY: No input validation
    # VULNERABILITY: SQL injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        # VULNERABILITY: Logging sensitive data
        print(f"User {username} logged in with password {password}")
        return jsonify({"status": "success", "api_key": API_SECRET})

    # VULNERABILITY: Information disclosure in error message
    return jsonify({"error": "Invalid username or password", "hint": f"No user named {username}"}), 401

@app.route('/search')
def search():
    """Search users - VULNERABLE"""
    search_term = request.args.get('q')

    # VULNERABILITY: No authentication check - anyone can search
    # VULNERABILITY: SQL injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username LIKE '%{search_term}%'")
    results = cursor.fetchall()

    return jsonify(results)

@app.route('/admin/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user - VULNERABLE"""
    # VULNERABILITY: No authorization check - any user can delete any user
    # VULNERABILITY: SQL injection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()

    return jsonify({"status": "deleted"})

@app.route('/exec')
def execute_command():
    """Execute system command - EXTREMELY DANGEROUS"""
    import os
    cmd = request.args.get('cmd')

    # VULNERABILITY: Command injection - arbitrary code execution
    result = os.system(cmd)

    return jsonify({"output": result})

if __name__ == '__main__':
    # VULNERABILITY: Debug mode enabled in production
    # VULNERABILITY: Binding to all interfaces (0.0.0.0)
    app.run(debug=True, host='0.0.0.0', port=5000)
