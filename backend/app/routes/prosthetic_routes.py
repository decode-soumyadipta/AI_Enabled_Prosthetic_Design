# File: backend/app/prosthetic_routes.py

import os
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from utils.file_processing import save_file
from intel2.inference import run_inference
from intel2.mesh_processing import process_mesh
from intel2.optimization import optimize_model_with_nncf as optimize_model


prosthetic_blueprint = Blueprint('prosthetic', __name__, template_folder='../templates')

# Define routes
@prosthetic_blueprint.route('/upload', methods=['POST'])
def upload():
    """Handles CT scan upload and prosthetic generation."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    try:
        # Save the uploaded file
        file_path = save_file(file, 'uploads')

        # Run inference
        segmentation_mask = run_inference(file_path)

        # Generate STL file
        stl_file_path = process_mesh(segmentation_mask)

        # Normalize the path for URL generation
        stl_file_path = stl_file_path.replace("\\", "/")

        return redirect(url_for('prosthetic.result', stl_file=stl_file_path))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)


@prosthetic_blueprint.route('/result', methods=['GET'])
def result():
    """Renders the STL file in the result page."""
    stl_file = request.args.get('stl_file')
    if not stl_file:
        return jsonify({"error": "STL file parameter missing"}), 400

    stl_file_path = os.path.join("backend", "app", "static", "prosthetics", os.path.basename(stl_file))
    if not os.path.exists(stl_file_path):
        return jsonify({"error": "STL file not found"}), 404

    stl_file_url = url_for('static', filename=f'prosthetics/{os.path.basename(stl_file)}', _external=True)
    return render_template('result.html', stl_file_url=stl_file_url)
