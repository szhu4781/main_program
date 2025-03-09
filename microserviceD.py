from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['IMAGE_FOLDER'] = os.path.join(os.getcwd(), "static", "images")

# Check if the image folder exists
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

# Enable CORS to allow cross-origin requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Download count tracker
download_count = {}
max_download = 10

# Store mode preference
user_modes = {}

# Download images route
@app.route('/download/<image_name>', methods=['GET'])
def download_img(image_name):
    # Get the list of images from the images folder
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.svg'))])

    # Check if the image exists
    if image_name not in image_files:
        return jsonify({"error": "Image not found"}), 404
    
    # Track download by IP address
    user_ip = request.remote_addr
    today = datetime.today().date()

    # Check download count for specific user of a specific day
    if user_ip not in download_count:
        download_count[user_ip] = {}

    # Check the current count for today
    if today not in download_count[user_ip]:
        download_count[user_ip][today] = 0

    # Check if the count has reached 10
    if download_count[user_ip][today] >= max_download:
        return jsonify({"error": "Download limit has exceeded. Try again tomorrow."}), 400
    
    try:
        # Increment count for today
        download_count[user_ip][today] += 1

        # Return request for downloading image
        return send_from_directory(image_folder, image_name, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "Download failed", "message": str(e)}), 500 
    
# Deleting images route
@app.route('/delete/<image_name>', methods=['DELETE'])
def delete_img(image_name):
    # Get the list of images from the images folder
    image_folder = os.path.join(app.static_folder, 'images')
    image_path = os.path.join(image_folder, image_name)

    # Check if image exists
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    try: 
        # Delete the image
        os.remove(image_path)
        return jsonify({"message": f"Image {image_name} deleted succesfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete image", "message": str(e)}), 500

# Light/Dark mode route
@app.route('/mode', methods=['GET', 'POST'])
def mode():
    user_ip = request.remote_addr

    if request.method == 'POST':
        data = request.get_json()
        mode = data.get('mode')

        # Check which mode is current enabled
        if mode not in ['light', 'dark']:
            return jsonify({"error": "invalid mode/theme"}), 400
        
        # Save user preference
        user_modes[user_ip] = mode
        return jsonify({"message": f"Mode set to {mode}"}), 200
    
    elif request.method == 'GET':
        mode = user_modes.get(user_ip, 'light')
        return jsonify({"mode": mode}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
