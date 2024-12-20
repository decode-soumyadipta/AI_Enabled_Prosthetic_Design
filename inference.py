# File: backend/intel/inference_comparison.py

import numpy as np
import cv2
import argparse
import os
import time
import matplotlib.pyplot as plt
from openvino.runtime import Core

# Paths to the OpenVINO model files
SIMPLE_MODEL_XML = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/unet-camvid-onnx-0001.xml"
OPTIMIZED_MODEL_XML = "C:/Users/soumy/OneDrive/Desktop/AI_Enabled_Prosthetic_Design/backend/intel/unet-camvid-onnx-0001/FP16/optimized_nncf/optimized_model.xml"

# Initialize OpenVINO Core
ie = Core()

def preprocess_image(file_path):
    """Preprocess image for inference."""
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Error: Unable to read the image file at {file_path}.")
    _, thresholded_image = cv2.threshold(image, 10, 255, cv2.THRESH_BINARY)
    resized_image = cv2.resize(thresholded_image, (480, 368))
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
    normalized_image = rgb_image / 255.0
    transposed_image = normalized_image.transpose(2, 0, 1)
    input_tensor = np.expand_dims(transposed_image, axis=0)
    return input_tensor.astype(np.float32)

def calculate_accuracy(predicted_mask, ground_truth_path):
    """Calculate pixel-wise accuracy."""
    ground_truth = cv2.imread(ground_truth_path, cv2.IMREAD_GRAYSCALE)
    if ground_truth is None:
        raise ValueError(f"Error: Unable to read the ground truth file at {ground_truth_path}.")
    ground_truth = cv2.resize(ground_truth, predicted_mask.shape[::-1])  # Resize to match prediction shape
    correct = np.sum(predicted_mask == ground_truth)
    total = ground_truth.size
    return correct / total

def run_inference(file_path, model_path, device="CPU", ground_truth_path=None):
    """Run segmentation inference and measure performance."""
    model = ie.read_model(model=model_path)
    compiled_model = ie.compile_model(model=model, device_name=device)
    input_tensor = preprocess_image(file_path)

    # Measure inference time
    start_time = time.time()
    results = compiled_model([input_tensor])  # Returns a dictionary of outputs
    inference_time = time.time() - start_time

    # Process segmentation mask
    result = next(iter(results.values()))  # Access the first output
    segmentation_mask = np.argmax(result, axis=1).squeeze().astype(np.uint8)

    # Calculate accuracy if ground truth is provided
    accuracy = None
    if ground_truth_path:
        accuracy = calculate_accuracy(segmentation_mask, ground_truth_path)

    return inference_time, accuracy

def plot_comparative_metrics(metrics):
    """Plot comparative inference time and accuracy as a bar graph with a separation line."""
    labels = [
        "Simple model-CPU",
        "Optimized model-CPU",
        "Simple model-GPU",
        "Optimized model-GPU"
    ]
    times = [metrics[label]["time"] for label in labels]
    accuracies = [metrics[label]["accuracy"] for label in labels]

    # Create a bar graph
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(x, times, color=["blue", "green", "skyblue", "lightgreen"], alpha=0.7)

    # Annotate bars with inference time and accuracy
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.02,
            f"{times[i]:.2f}s",
            ha="center",
            fontsize=10,
            color="black",
        )
        if accuracies[i] is not None:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.1,
                f"Acc: {accuracies[i] * 100:.2f}%",
                ha="center",
                fontsize=10,
                color="darkgreen",
            )

    # Add vertical separation line
    ax.axvline(x=1.5, color="gray", linestyle="--", linewidth=1)  # Add a vertical line between CPU and GPU

    # Add labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15)
    ax.set_ylabel("Inference Time (s)")
    ax.set_title(
        "Inference Time and Accuracy Comparison:\n"
        "Simple UNet Model vs NNCF Optimized UNet Segmentation Model"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Run inference comparison for simple and optimized models on CPU and GPU.")
    parser.add_argument("--input", type=str, required=True, help="Path to input image file")
    parser.add_argument("--ground_truth", type=str, required=True, help="Path to ground truth image file")
    args = parser.parse_args()

    metrics = {}

    # Run inference for both models on CPU and GPU
    print("Running inference for all configurations...")
    for model_name, model_path in [("Simple model", SIMPLE_MODEL_XML), ("Optimized model", OPTIMIZED_MODEL_XML)]:
        for device in ["CPU", "GPU"]:
            label = f"{model_name}-{device}"  # Match labels used in the graph
            time_, accuracy = run_inference(args.input, model_path, device=device, ground_truth_path=args.ground_truth)
            metrics[label] = {"time": time_, "accuracy": accuracy}
            print(f"{label}: Time: {time_:.4f}s, Accuracy: {accuracy * 100:.2f}%" if accuracy is not None else f"{label}: Time: {time_:.4f}s")

    # Plot the metrics
    plot_comparative_metrics(metrics)

if __name__ == "__main__":
    main()
