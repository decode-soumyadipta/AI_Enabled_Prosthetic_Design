from flask import Blueprint, request, jsonify
from routes.prosthetic_routes import process_ct_scan

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/process_scan', methods=['POST'])
def process_scan():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    # Process CT scan and return segmentation result
    result = process_ct_scan(file)
    return jsonify({"segmentation_result": result})
