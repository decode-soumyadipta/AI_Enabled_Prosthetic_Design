# File: backend/intel/inference.py

import numpy as np
import cv2
from openvino.runtime import Core

# Paths to the OpenVINO model files
MODEL_XML = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.xml"
MODEL_BIN = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.bin"


# Initialize OpenVINO Core
ie = Core()
model = ie.read_model(model=MODEL_XML)
compiled_model = ie.compile_model(model=model, device_name="CPU")
input_layer = next(iter(compiled_model.inputs))
output_layer = next(iter(compiled_model.outputs))


def preprocess_image(file_path):
    """Preprocess image for inference."""
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    _, thresholded_image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
    resized_image = cv2.resize(thresholded_image, (480, 368))  # Model input size
    normalized_image = resized_image / 255.0
    return np.expand_dims(normalized_image.transpose(2, 0, 1), axis=0).astype(np.float32)


def run_inference(file_path):
    """Run segmentation inference."""
    input_tensor = preprocess_image(file_path)
    result = compiled_model([input_tensor])[output_layer]
    return np.argmax(result[0], axis=0).astype(np.uint8)
