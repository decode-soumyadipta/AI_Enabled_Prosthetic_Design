import React, { useEffect, useState } from "react";
import * as THREE from "three";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";

function ResultPage() {
  const [stlFile, setStlFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSTLFile = () => {
      const queryParams = new URLSearchParams(window.location.search);
      const stlFileUrl = queryParams.get("stl_file");

      if (stlFileUrl) {
        setStlFile(stlFileUrl);
        setLoading(false);
      } else {
        setError("STL file URL not found");
        setLoading(false);
      }
    };

    fetchSTLFile();
  }, []);

  useEffect(() => {
    if (stlFile) {
      const viewer = document.getElementById("stlViewer");
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, viewer.clientWidth / viewer.clientHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(viewer.clientWidth, viewer.clientHeight);
      viewer.appendChild(renderer.domElement);

      const light = new THREE.DirectionalLight(0xffffff, 1);
      light.position.set(5, 5, 5);
      scene.add(light);

      const loader = new STLLoader();
      loader.load(
        stlFile,
        (geometry) => {
          const material = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
          const mesh = new THREE.Mesh(geometry, material);
          scene.add(mesh);

          const boundingBox = new THREE.Box3().setFromObject(mesh);
          const center = new THREE.Vector3();
          boundingBox.getCenter(center);

          camera.position.set(center.x, center.y, center.z + 100);
          camera.lookAt(center);

          const animate = () => {
            requestAnimationFrame(animate);
            mesh.rotation.y += 0.01;
            renderer.render(scene, camera);
          };
          animate();
        },
        undefined,
        (error) => {
          setError("Failed to load STL file: " + error.message);
        }
      );
    }
  }, [stlFile]);

  if (loading) return <p>Loading STL file...</p>;
  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <div>
      <h1>Prosthetic Design Results</h1>
      <div id="stlViewer" style={{ width: "100%", height: "500px", border: "1px solid #ccc" }}></div>
    </div>
  );
}

export default ResultPage;
