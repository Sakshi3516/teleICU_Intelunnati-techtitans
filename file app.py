[09:31, 15/7/2024] Rohit: from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from ultralytics import YOLO

app = Flask(_name_)

# Set up upload folder
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Load YOLOv8 model
model = YOLO('intelmodel.pt')  # Replace with the path to your YOLOv8 model


@app.route('/')
def index():
    return render_template('trail.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the file with YOLOv8
        results = model(file_path)
        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        results.save(processed_file_path)  # Assuming YOLO saves the result

        # Determine the file type
        file_type = 'image' if file.content_type.startswith('image') else 'video'

        return jsonify(processed_file_url=f'/processed/{filename}', file_type=file_type)
    else:
        return jsonify(error='File not allowed'), 400


@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)


if _name_ == '_main_':
    app.run(debug=True, host='127.0.0.1')
[09:33, 15/7/2024] Rohit: file name app.py