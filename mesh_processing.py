# File: backend/intel/mesh_processing.py

import os
import trimesh
import numpy as np
from skimage import measure
import open3d as o3d


def process_mesh(segmentation_mask):
    """Process segmentation mask into STL mesh with analysis."""
    vertices, faces, _, _ = measure.marching_cubes(segmentation_mask, level=0)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Calculate mesh properties
    bounding_box = mesh.bounding_box_oriented.volume
    print(f"Bounding box volume: {bounding_box:.4f}")

    # Convert to Open3D for processing
    o3d_mesh = o3d.geometry.TriangleMesh()
    o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
    o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)

    # Simplify and smooth mesh
    simplified_mesh = o3d_mesh.simplify_quadric_decimation(target_number_of_triangles=10000)
    smoothed_mesh = simplified_mesh.filter_smooth_simple(number_of_iterations=3)

    # Save STL
    stl_dir = "backend/app/static/prosthetics"
    os.makedirs(stl_dir, exist_ok=True)
    stl_path = os.path.join(stl_dir, "prosthetic_design.stl")
    trimesh.Trimesh(np.asarray(smoothed_mesh.vertices), np.asarray(smoothed_mesh.triangles)).export(stl_path)
    return stl_path
