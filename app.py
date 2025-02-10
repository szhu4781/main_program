from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'secret_key'

# Configuring upload folder and allowed file formats
UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')
SUFFIX = {'png', 'jpg', 'jpeg', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check for allowed file format
def file_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in SUFFIX

# Route to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to gallery.html
@app.route('/gallery')
def gallery():
    # Get the list of images from the images folder
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.svg'))])
    
    if not image_files:
        return render_template('gallery.html', images=[], prev_img=None, current_img=None, next_img=None)

    # Set initial images to display
    current_img = image_files[0]
    prev_img = image_files[-1]  # Last image is the previous image for the first slide
    next_img = image_files[1] if len(image_files) > 1 else current_img

    # Get the upload date for each image
    image_date = {}
    for image in image_files:
        image_path =  os.path.join(image_folder, image)
        timestamp = os.path.getctime(image_path)
        date_format = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        image_date[image] = date_format

    return render_template('gallery.html', images=image_files, prev_img=prev_img, current_img=current_img, next_img=next_img, image_dates=image_date)

# Route to access image folder
@app.route('/images/<image_name>')
def get_images(image_name):
    return app.send_static_file(f'images/{image_name}')

# Route to upload.html
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'files' not in request.files:
            flash('No files found in request')
            return redirect(request.url)

        files = request.files.getlist('files')  # Get multiple files

        if not files or all(file.filename == '' for file in files):
            flash('No files selected')
            return redirect(request.url)

        uploaded_files = []

        for file in files:  
            if file and file_format(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(filename)
        
        if uploaded_files:
            flash(f'Successfully uploaded: {", ".join(uploaded_files)}')
            return redirect(url_for('gallery'))
        else:
            flash('No valid files. Try again.')
        
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
