from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
from PIL import Image, ImageDraw, ImageFont
import random
import os
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def get_db_connection():
    connection = mysql.connector.connect(
        host='72.167.254.238',  # e.g., 'localhost'
        database='docu_sign',
        user='apoorva',
        password='Welcome2data'
    )
    return connection

# Function to generate a signature image
def generate_signature(name, font_path, font_size):
    # Create an image with a white background
    image = Image.new("RGB", (400, 100), "white")
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size and position
    text_width, text_height = draw.textsize(name, font=font)
    x = (image.width - text_width) / 2
    y = (image.height - text_height) / 2

    # Draw the text on the image
    draw.text((x, y), name, fill="black", font=font)

    return image

def signature_to_base64(signature):
    import base64
    from io import BytesIO
    buffer = BytesIO()
    signature.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

@app.route('/generate_signatures', methods=['POST'])
def generate_signatures():
    data = request.get_json()
    name = data['name']
    font_size = int(data['font_size'])
    
    font_dir = "C:\\Windows\\Fonts"
    font_style_options = [
        os.path.join(font_dir, "arial.ttf"),
        os.path.join(font_dir, "times.ttf"),
        os.path.join(font_dir, "calibri.ttf"),
        os.path.join(font_dir, "verdana.ttf"),
        os.path.join(font_dir, "comic.ttf"),
    ]

    connection = get_db_connection()
    cursor = connection.cursor()

    signatures = []
    for i in range(5):
        random_font_style = font_style_options[i]
        signature = generate_signature(name, random_font_style, font_size)
        signatures.append(signature)

    #for sig in signatures:
    #    base64_signature = signature_to_base64(sig)
        # Assuming 'reg_id' is auto-incremented or provided in the request
        # Modify SQL query as per your table structure and requirements
    query = "INSERT INTO users (reg_id, user_signature) VALUES (%s, %s) ON DUPLICATE KEY UPDATE user_signature = VALUES(user_signature)"
    cursor.execute(query, (2, signature_to_base64(signatures[0])))  # Use actual reg_id if available

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify([signature_to_base64(sig) for sig in signatures])

@app.route('/')
def index():
    return "Server is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
