import os
import numpy as np
import cv2
import trimesh
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from openvino.runtime import Core
from skimage import measure
from utils.file_processing import save_file
import open3d as o3d

prosthetic_blueprint = Blueprint(
    'prosthetic',
    __name__,
    template_folder='../templates'
)

MODEL_XML = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.xml"
MODEL_BIN = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.bin"

# Initialize OpenVINO
ie = Core()
model = ie.read_model(model=MODEL_XML)
compiled_model = ie.compile_model(model=model, device_name="CPU")
input_layer = next(iter(compiled_model.inputs))
output_layer = next(iter(compiled_model.outputs))


def preprocess_ct_scan(image):
    """Preprocesses the CT scan for segmentation."""
    # Threshold the image to remove the background
    _, thresholded_image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)  # Remove black background

    # Apply morphological operations to clean noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_CLOSE, kernel)

    return cleaned_image

def simplify_mesh_with_open3d(mesh):
    """Simplifies a mesh using Open3D."""
    # Convert trimesh to Open3D mesh
    o3d_mesh = o3d.geometry.TriangleMesh()
    o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
    o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)
    
    # Simplify the mesh using Open3D
    simplified_mesh = o3d_mesh.simplify_quadric_decimation(target_number_of_triangles=10000)

    # Convert back to Trimesh
    simplified_vertices = np.asarray(simplified_mesh.vertices)
    simplified_faces = np.asarray(simplified_mesh.triangles)
    simplified_trimesh = trimesh.Trimesh(vertices=simplified_vertices, faces=simplified_faces)
    return simplified_trimesh



def process_ct_scan(file_path):
    """Processes CT scan to generate a segmentation mask."""
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Failed to load image. Ensure the file is a valid CT scan.")

    print(f"Original image shape: {image.shape}")

    # Preprocess the image
    image = preprocess_ct_scan(image)

    # Resize and normalize
    resized_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)  # Convert to RGB for model
    resized_image = cv2.resize(resized_image, (480, 368))  # Resize to model input size
    normalized_image = resized_image / 255.0

    # Create input tensor with batch size
    input_tensor = np.expand_dims(normalized_image.transpose(2, 0, 1), axis=0).astype(np.float32)  # Shape: (1, 3, 368, 480)

    # Perform inference
    result = compiled_model([input_tensor])[output_layer]
    segmentation_mask = np.argmax(result[0], axis=0).astype(np.uint8)

    print(f"Segmentation mask shape: {segmentation_mask.shape}")
    print(f"Segmentation mask values: {np.unique(segmentation_mask)}")

    # Clean segmentation
    cleaned_mask = clean_segmentation(segmentation_mask)
    return cleaned_mask




def clean_segmentation(segmentation_mask):
    """Cleans up the segmentation mask."""
    from skimage.morphology import remove_small_objects

    # Remove small objects and keep the largest connected component
    labeled_mask = measure.label(segmentation_mask, connectivity=2)
    largest_component = labeled_mask == np.argmax(np.bincount(labeled_mask.flat)[1:]) + 1

    # Remove small artifacts
    cleaned_mask = remove_small_objects(largest_component, min_size=500)
    return cleaned_mask.astype(np.uint8)


    
def generate_3d_prosthetic(segmentation_mask):
    """Generates an STL file from the segmentation mask."""
    if segmentation_mask.ndim == 2:
        segmentation_mask = np.expand_dims(segmentation_mask, axis=0)

    # Pad to ensure minimum dimensions
    segmentation_mask = np.pad(segmentation_mask, ((0, max(0, 2 - segmentation_mask.shape[0])),
                                                   (0, max(0, 2 - segmentation_mask.shape[1])),
                                                   (0, max(0, 2 - segmentation_mask.shape[2]))), mode='constant')

    if segmentation_mask.sum() == 0:
        raise ValueError("Segmentation mask contains no valid data for 3D reconstruction.")

    # Generate vertices and faces using marching cubes
    vertices, faces, _, _ = measure.marching_cubes(segmentation_mask, level=0)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Simplify the mesh using Open3D
    mesh = simplify_mesh_with_open3d(mesh)

    # Scale and smooth the mesh for a better fit
    mesh.vertices *= [0.5, 0.5, 0.5]  # Adjust scaling as needed

    # Save STL file
    stl_dir = os.path.join("backend", "app", "static", "prosthetics")
    os.makedirs(stl_dir, exist_ok=True)
    stl_path = os.path.join(stl_dir, "prosthetic_design.stl")
    mesh.export(stl_path)

    return stl_path



@prosthetic_blueprint.route('/result', methods=['GET'])
def result():
    """Returns results including the STL file URL."""
    stl_file = request.args.get('stl_file')
    if not stl_file:
        return jsonify({"error": "STL file parameter missing"}), 400

    # Ensure path normalization for URL generation
    stl_file_name = os.path.basename(stl_file)
    stl_file_path = os.path.join("backend", "app", "static", "prosthetics", stl_file_name)

    if not os.path.exists(stl_file_path):
        print(f"STL file not found: {stl_file_path}")
        return jsonify({"error": f"STL file not found at {stl_file_path}"}), 404

    # Generate the public URL for rendering in the frontend
    stl_file_url = url_for('static', filename=f'prosthetics/{stl_file_name}', _external=False)

    return render_template('result.html', stl_file_url=stl_file_url)




@prosthetic_blueprint.route('/upload', methods=['POST'])
def upload():
    """Handles CT scan upload and prosthetic generation."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    try:
        # Save the uploaded file
        file_path = save_file(file, 'uploads')

        # Process CT scan
        segmentation_mask = process_ct_scan(file_path)

        # Generate STL file
        stl_file_path = generate_3d_prosthetic(segmentation_mask)

        # Normalize the path for URL generation
        stl_file_path = stl_file_path.replace("\\", "/")

        return redirect(url_for('prosthetic.result', stl_file=stl_file_path))
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)


def preprocess_image(file):
    """Preprocesses the uploaded file for model inference."""
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (224, 224))  # Resize to model input size
    image = image / 255.0  # Normalize to [0, 1]
    image = np.expand_dims(image, axis=(0, 1)).astype(np.float32)  # Add batch and channel dimensions
    return image

def clean_segmentation(segmentation_mask):
    """Removes noise and keeps the largest connected component."""
    from skimage import measure

    labels = measure.label(segmentation_mask, connectivity=2)
    largest_label = labels == np.argmax(np.bincount(labels.flat)[1:]) + 1
    return largest_label.astype(np.uint8)

def generate_prosthetic_design(file):
    return {"design": "Generated prosthetic design based on scan."}