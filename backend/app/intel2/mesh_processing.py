# File: backend/intel/mesh_processing.py

import os
import trimesh
import numpy as np
from skimage import measure
import open3d as o3d


def process_mesh(segmentation_mask):
    """Process segmentation mask into STL mesh."""
    # Generate vertices and faces using marching cubes
    vertices, faces, _, _ = measure.marching_cubes(segmentation_mask, level=0)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Convert trimesh to Open3D
    o3d_mesh = o3d.geometry.TriangleMesh()
    o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
    o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)

    # Simplify mesh
    simplified_mesh = o3d_mesh.simplify_quadric_decimation(target_number_of_triangles=10000)

    # Save as STL
    stl_dir = "backend/app/static/prosthetics"
    os.makedirs(stl_dir, exist_ok=True)
    stl_path = os.path.join(stl_dir, "prosthetic_design.stl")
    trimesh.Trimesh(np.asarray(simplified_mesh.vertices), np.asarray(simplified_mesh.triangles)).export(stl_path)
    return stl_path
