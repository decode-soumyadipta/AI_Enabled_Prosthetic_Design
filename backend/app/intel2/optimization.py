# File: backend/intel/optimization.py
from openvino.tools.pot import PTQ, DataLoader, Metric

def optimize_model():
    """Optimize the model using Post-Training Optimization."""
    optimized_model_path = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/optimized_model.xml"

    # Example POT configuration
    config = {
        "model": "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.xml",
        "engine": "openvino",
        "optimization": ["INT8"],
    }

    # Create the Post-Training Quantization object (PTQ) for INT8 optimization
    pot = PTQ(config)

   
    data_loader = DataLoader()

    # Running the optimization process
    pot.optimize(data_loader, optimized_model_path)

    return optimized_model_path
