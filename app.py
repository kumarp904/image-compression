from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Configuration
UPLOAD_FOLDER = 'uploads/'
COMPRESSED_FOLDER = 'compressed/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

# Ensure the upload and compressed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_image(input_filepath, output_filepath):
    with Image.open(input_filepath) as img:
        img.save(output_filepath, optimize=True, quality=20)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_filepath = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
            file.save(input_filepath)
            compress_image(input_filepath, output_filepath)
            flash('Image has been compressed successfully!')
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded.html', filename=filename)

@app.route('/compressed/<filename>')
def compressed_file(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
