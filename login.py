from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
#import bcrypt  # If you are hashing passwords

app = Flask(__name__)
CORS(app)

# Database connection details
db_config = {
    'host': '72.167.254.238',       # or your database host
    'user': 'apoorva',    # your database username
    'password': 'Welcome2data',# your database password
    'database': 'docu_sign'   # your database name
}

def authenticate_user(email, password):
    conn = mysql.connector.connect(**db_config)
    try:
        with conn.cursor(buffered=True) as cursor:
            query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result and result[0] == password
    finally:
        conn.close()



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('emailId')
    password = data.get('password')

    if authenticate_user(email, password):
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=2001)
