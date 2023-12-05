from flask import Flask, request, jsonify
import re
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database connection details
db_config = {
    'host': '72.167.254.238',       # or your database host
    'user': 'apoorva',    # your database username
    'password': 'Welcome2data',# your database password
    'database': 'docu_sign'   # your database name
}

def is_valid_email(email):
    """Simple regex for validating an Email."""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

def is_valid_password(password):
    """Check if the password is at least 8 characters with letters and numbers."""
    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return re.fullmatch(regex, password)

def email_exists(email):
    """Check if an email already exists in the database."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True)

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result is not None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extracting data
    fname = data.get('fname')
    lname = data.get('lname')
    emailId = data.get('emailId')
    password = data.get('password')
    cpassword = data.get('cpassword')

    # Implement your validation logic here
    # For example, check if passwords match, if email is valid, etc.

    # Password Matching
    if password != cpassword:
        return jsonify({"success": False, "message": "Passwords do not match."}), 400

    # Password Validation
    if not is_valid_password(password):
        return jsonify({"success": False, "message": "Password must be at least 8 characters long and include both letters and numbers."}), 400

    # Email Verification
    if not is_valid_email(emailId):
        return jsonify({"success": False, "message": "Invalid email format."}), 400
    
    # Check if email already exists
    if email_exists(emailId):
        return jsonify({"success": False, "message": "An account with this email already exists."}), 400


    # If everything is fine
    print("Registration Data:", data)
    print(fname)
    print(lname)
    print(emailId)
    print(password)
    print(cpassword)

    # You can add database interaction here
    # Database interaction
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = ("INSERT INTO users (fname, lname, email, password) "
                 "VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (fname, lname, emailId, password))

        conn.commit()
        cursor.close()
        conn.close()

        print("Database done")

        return jsonify({"success": True, "message": "Registration successful"})
    except mysql.connector.Error as err:
        print("Database error: {}".format(err))
        return jsonify({"success": False, "message": "Database error"}), 500

    # Sending a response back to the frontend
    return jsonify({"success": True, "message": "Registration successful"})

if __name__ == '__main__':
    app.run(debug=True, port=2000)
