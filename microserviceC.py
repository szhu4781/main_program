from flask import Flask, request, jsonify
import os
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['DATA_FILE'] = os.path.join(os.getcwd(), "data.json")

# Enable CORS for frontend integration
CORS(app, resources={r"/*": {"origins": "*"}})

# Load existing image data or initialize empty
def load_data():
    if os.path.exists(app.config['DATA_FILE']):
        with open(app.config['DATA_FILE'], "r") as file:
            return json.load(file)
    return {}

# Save updated data
def save_data(data):
    with open(app.config['DATA_FILE'], "w") as file:
        json.dump(data, file, indent=4)

# Rout for adding image context
@app.route('/context', methods=['POST'])
def add_context():
    data = request.get_json()
    image_name = data.get('image_name')
    name = data.get('name')
    description = data.get('description')

    if not image_name or not name or not description:
        return jsonify({"error": "missing image name, name, or description"}), 404

    # Load existing data and update context
    image_data = load_data()
    
    # Ensure the image entry exists before updating
    if image_name not in image_data:
        image_data[image_name] = {"category": "N/A", "tags": []}

    image_data[image_name]["name"] = name
    image_data[image_name]["description"] = description

    # Save changes
    save_data(image_data)

    return jsonify({
        "message": "Image context updated successfully",
        "image_name": image_name,
        "name": name,
        "description": description
    }), 200

# Route for searching images by tags or categories
@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({"error": "no search query provided"}), 400

    # Load image data
    image_data = load_data()
    results = []

    # Check for matches in category, tags, name, or description
    for image_name, details in image_data.items():
        category = details.get("category", "").lower()
        tags = [tag.lower() for tag in details.get("tags", [])]
        name = details.get("name", "").lower()
        description = details.get("description", "").lower()

        if query in category or query in tags or query in name or query in description:
            results.append(image_name)

    # Return search results
    if results:
        return jsonify({"matching_images": results}), 200
    else:
        return jsonify({"message": "No matching images found"}), 404

# Route for getting the image context
@app.route('/context/<image_name>', methods=['GET'])
def get_context(image_name):
    image_data = load_data()
    image_details = image_data.get(image_name, {})

    if not image_details:
        return jsonify({"error": "No context found for this image"}), 404

    # Returns attributes in json format
    return jsonify({
        "image_name": image_name,
        "name": image_details.get("name", "N/A"),
        "description": image_details.get("description", "No description available")
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=4444)
