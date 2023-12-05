from flask import send_file
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Database connection details
db_config = {
    'host': '72.167.254.238',
    'user': 'apoorva',
    'password': 'Welcome2data',
    'database': 'docu_sign'
}

@app.route('/get_pdf', methods=['GET'])
def get_pdf():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        user_id =1

        # Retrieve the PDF data for the given user ID
        query = "SELECT pdf_data FROM users WHERE reg_id = %s"
        cursor.execute(query, (user_id,))
        pdf_data = cursor.fetchone()

        if pdf_data is None:
            return jsonify({"success": False, "message": "PDF not found for the given user ID"}), 404

        # Create a BytesIO object from the PDF data
        pdf_io = BytesIO(pdf_data[0])

        cursor.close()
        conn.close()

        pdf_io.seek(0)
        return send_file(pdf_io, as_attachment=True, attachment_filename='user_pdf.pdf', mimetype='application/pdf')

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=2003)
