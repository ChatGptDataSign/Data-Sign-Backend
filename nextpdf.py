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

@app.route('/generate_and_save_pdf', methods=['POST'])
def upload_pdf():
    user_id = request.form.get('reg_id')
    img_data = request.form.get('imgData')

    if not img_data:
        return jsonify({"success": False, "message": "No image data provided"}), 400

    if not user_id:
        return jsonify({"success": False, "message": "User ID is required"}), 400

    try:
        # Generate PDF from image data
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        # Assuming img_data is a data URL, you might need additional processing here
        p.drawImage(img_data, 100, 750, 400, 100)  # Adjust positioning and size as needed
        p.save()

        buffer.seek(0)
        pdf_content = buffer.read()

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL update query
        update_query = "UPDATE users SET pdf_data = %s WHERE reg_id = %s"
        cursor.execute(update_query, (pdf_content, user_id))

        # Check if the row exists and is updated
        if cursor.rowcount == 0:
            return jsonify({"success": False, "message": "No user found with the given reg_id"}), 404

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "PDF updated successfully in the user's row"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=2002)
