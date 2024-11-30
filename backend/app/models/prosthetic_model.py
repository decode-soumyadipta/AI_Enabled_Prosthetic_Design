import numpy as np
import cv2
from openvino.runtime import Core

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
