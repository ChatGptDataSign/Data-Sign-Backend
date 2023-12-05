import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2-medium"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Define a folder to store generated PDFs
pdf_folder = "pdf_files"

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 50)

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1,
                            pad_token_id=tokenizer.eos_token_id,
                            attention_mask=torch.ones(input_ids.shape, dtype=torch.long))
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return jsonify({"response": response})

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    response_text = data.get('response', '')

    # Generate a PDF and save it
    pdf_filename = os.path.join(pdf_folder, 'generated.pdf')

    # Create a PDF document using ReportLab
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    paragraph = Paragraph(response_text, styles["Normal"])
    story.append(paragraph)
    doc.build(story)

    return send_from_directory(pdf_folder, 'generated.pdf')

@app.route('/')
def index():
    return "Server is running!"

if __name__ == '__main__':
    # Create the PDF folder if it doesn't exist
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    app.run(host='0.0.0.0', port=5000)
