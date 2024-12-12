import os
import numpy as np
import cv2
from nncf import quantize
from openvino.runtime import Core
from openvino.runtime import serialize

# Paths to the original IR model
MODEL_XML = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.xml"
MODEL_BIN = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.bin"

# Directory for optimized model
OUTPUT_DIR = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/optimized_nncf/"

# Dataset for calibration
DATASET_DIR = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/dataset/images/"

class CalibrationDataset:
    """Wrapper dataset class for NNCF calibration."""
    def __init__(self, dataset_dir):
        self.image_paths = [
            os.path.join(dataset_dir, img_name) for img_name in os.listdir(dataset_dir)
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Read the image
        image = cv2.imread(self.image_paths[idx])
        if image is None:
            raise ValueError(f"Failed to read image at: {self.image_paths[idx]}")

        # Resize the image to match the model's input shape
        resized_image = cv2.resize(image, (480, 368))  # Note: Width=480, Height=368
        normalized_image = resized_image / 255.0
        transposed_image = normalized_image.transpose(2, 0, 1)  # Channels-first
        return np.expand_dims(transposed_image.astype(np.float32), axis=0)

    def get_batch_size(self):
        return 1  # Required for NNCF calibration

    def get_length(self):
        """Return the length of the dataset."""
        return len(self.image_paths)

    def get_inference_data(self):
        """Yield inference-ready data samples."""
        for idx in range(len(self)):
            yield self[idx]


def optimize_model_with_nncf():
    """Optimize the OpenVINO model using NNCF quantization."""
    # Initialize OpenVINO runtime
    core = Core()
    
    # Load the IR model
    model = core.read_model(model=MODEL_XML, weights=MODEL_BIN)

    # Load calibration dataset
    calibration_dataset = CalibrationDataset(DATASET_DIR)

    # Perform quantization using NNCF
    optimized_model = quantize(model, calibration_dataset=calibration_dataset)

    # Save the optimized model
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    optimized_model_xml = os.path.join(OUTPUT_DIR, "optimized_model.xml")
    optimized_model_bin = os.path.join(OUTPUT_DIR, "optimized_model.bin")
    serialize(optimized_model, optimized_model_xml, optimized_model_bin)

    print(f"Optimized model saved to: {optimized_model_xml} and {optimized_model_bin}")


if __name__ == "__main__":
    optimize_model_with_nncf()
