from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
import os
import io

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('file')
    action = request.form.get('action')  # Dropdown value
    dpi = request.form.get('dpi')  # DPI input field
    width = request.form.get('width')  # Width input field
    height = request.form.get('height')  # Height input field

    # Validate the uploaded file
    if not file or file.filename == '':
        return "No file selected. Please upload an image."

    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        image = Image.open(file_path)

        # Action: Convert to Grayscale
        if action == 'greyscale':
            image = image.convert('L')

        # Action: Change DPI
        if action == 'change_dpi':
            try:
                dpi = int(dpi)
            except (ValueError, TypeError):
                return "Invalid DPI value. Please enter a valid integer."
            image.save(file_path, dpi=(dpi, dpi))

        # Action: Resize
        if action == 'resize':
            try:
                width = int(width)
                height = int(height)
            except (ValueError, TypeError):
                return "Invalid dimensions. Please enter valid integers for width and height."
            image = image.resize((width, height))

        # Save the processed image
        output_buffer = io.BytesIO()
        image_format = request.form.get('format', 'PNG').upper()
        image.save(output_buffer, format=image_format)
        output_buffer.seek(0)

        # Cleanup temporary file
        os.remove(file_path)

        # Serve the processed image
        return send_file(output_buffer, mimetype=f'image/{image_format.lower()}', as_attachment=True, download_name=f'output.{image_format.lower()}')

    except Exception as e:
        # Cleanup and return error
        if os.path.exists(file_path):
            os.remove(file_path)
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
