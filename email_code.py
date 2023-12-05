from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json

    sender_email = "your-email@example.com"
    sender_password = "your-email-password"
    
    # Email settings
    smtp_server = "smtp.example.com"
    smtp_port = 587

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = data['to']
    msg['Subject'] = data['subject']
    msg.attach(MIMEText(data['message'], 'plain'))

    # Check if default PDF should be attached
    if data.get('attachDefaultPdf', False):
        # Path to your PDF file
        filepath = 'pdf_files/generated.pdf'
        attachment = open(filepath, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f"attachment; filename= {filepath.split('/')[-1]}")
        
        msg.attach(part)
        attachment.close()

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=6000)
