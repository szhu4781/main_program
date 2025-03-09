from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['IMAGE_FOLDER'] = os.path.join(os.getcwd(), "static", "images")
app.config['DATA_FILE'] = os.path.join(os.getcwd(), "data.json")

# Enable CORS to allow cross-origin requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Check if the image folder exists
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

# Predefined categories are stored in json file
CATEGORIES = ["Nature", "Animal", "Random", "Landscape", "Food", "People", "Technology", "Art"]

# Load existing image data after checking data file
def load_data():
    if os.path.exists(app.config['DATA_FILE']):
        with open(app.config['DATA_FILE'], "r") as file:
            image_data = json.load(file)
    else:
        image_data = {}
    
    # Check for the images present in the image folder
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.svg'))])

    # New image has default values set to it
    for image in image_files:
        if image not in image_data:
            image_data[image] = {
                "category": "N/A",
                "tags": []
            }

    # Remove images from data.json if they are deleted
    for image in list(image_data.keys()):
        if image not in image_files:
            del image_data[image]

    # Save updated data
    with open(app.config['DATA_FILE'], 'w') as file:
        json.dump(image_data, file, indent=4)
    
    return image_data

# Route to fetch categories
@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify({"categories": CATEGORIES})

# Route to fetch category for a specific image
@app.route('/categories/<image_name>', methods=['GET'])
def get_image_category(image_name):
    # Load existing data
    image_data = load_data()

    # Check if the image exists
    if image_name not in image_data:
        return jsonify({"error": "Image not found"}), 404

    # Get the category of the image
    category = image_data[image_name].get('category', 'Uncategorized')

    # Return the category
    return jsonify({"category": category}), 200

# Route to fetch images
@app.route('/images', methods=['GET'])
def get_images():
    image_folder = app.config['IMAGE_FOLDER']
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.svg'))]
    return jsonify({"images": image_files})

# Categorize image route
@app.route('/categorize', methods=['POST'])
def categorize_img():
    data = request.get_json()
    image_name = data.get('image_name')
    category = data.get('category')

    # Checks if image name or category exists
    if not image_name or not category:
        return jsonify({"error": "missing image name or category"}), 404
    
    # Check if categories are valid
    if category not in CATEGORIES:
        return jsonify({"error": "category is invalid"}), 400

    # Load existing data
    image_data = load_data()

    # Update the image category
    image_data[image_name] = image_data.get(image_name, {})
    image_data[image_name]['category'] = category

    # Save updated data
    with open(app.config['DATA_FILE'], 'w') as file:
        json.dump(image_data, file, indent=4)

    # Return the json response
    return jsonify({
        "message": "Image categorized successfully",
        "image_name": image_name,
        "category": category
    }), 200

@app.route('/tags/<image_name>', methods=['GET'])
def get_tags(image_name):
    # Load existing data
    image_data = load_data()
    # If the image exists and has tags, return them; otherwise, return an empty list
    tags = image_data.get(image_name, {}).get('tags', [])
    return jsonify({"tags": tags}), 200

#Tag Image Route
@app.route('/tags', methods=['POST'])
def tag_image():
    data = request.get_json()
    image_name = data.get('image_name')
    tags = data.get('tags')

# Checks if image name or category exists
    if not image_name or not tags:
        return jsonify({"error": "missing image name or tag"}), 404
    
    # Load existing data
    image_data = load_data()

    # Check if the image exists
    if image_name not in image_data:
        return jsonify({"error": "image not found"}), 404
    
    image_data[image_name]['tags'] = tags
    
    # Save updated data
    with open(app.config['DATA_FILE'], 'w') as file:
        json.dump(image_data, file, indent=4)

    # Return the json response
    return jsonify({
        "message": "Tags updated successfully",
        "image_name": image_name,
        "tags": tags
    }), 200
    
if __name__ == '__main__':
    app.run(debug=True, port=7777)