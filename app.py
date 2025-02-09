from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
app.secret_key = 'c30cbe0237eb99a421b130d09ea75990'

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

    return render_template('gallery.html', images=image_files, prev_img=prev_img, current_img=current_img, next_img=next_img)

# Route to access image folder
@app.route('/images/<image_name>')
def get_images(image_name):
    return app.send_static_file(f'images/{image_name}')

# Route to upload.html
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Check for existing files in POST request
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found in request')
            return redirect(request.url)
        file = request.files['file']

        # Check if any files are selected
        if file.filename == '':
            flash('No files selected')
            return redirect(request.url)
        
        # Redirect to the gallery page after successful upload
        if file and file_format(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash('File uploaded successfully')
            return redirect(url_for('gallery'))
        
        else:
            flash('Invalid file type. Try again.')
            return redirect(request.url)
        
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)