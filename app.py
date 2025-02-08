from flask import Flask, render_template
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/images/<image_name>')
def get_images(image_name):
    return app.send_static_file(f'images/{image_name}')

if __name__ == '__main__':
    app.run(debug=True)