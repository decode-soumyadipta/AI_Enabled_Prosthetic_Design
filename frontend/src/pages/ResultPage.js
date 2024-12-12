/* File: ResultPage.js */
import React, { useState, useEffect } from "react";
import * as THREE from "three";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import './ResultPage.css';

function ResultPage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [material, setMaterial] = useState("PLA");
  const [physicsAnalysis, setPhysicsAnalysis] = useState("");

  useEffect(() => {
    if (file) {
      const fileReader = new FileReader();
      fileReader.onload = () => {
        const arrayBuffer = fileReader.result;
        renderSTLFile(arrayBuffer);
      };
      fileReader.onerror = () => setError("Failed to read the file");
      fileReader.readAsArrayBuffer(file);
    }
  }, [file]);

  const renderSTLFile = (arrayBuffer) => {
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
    const geometry = loader.parse(arrayBuffer);
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
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("No file selected");
    }
  };

  const handleMaterialChange = (e) => {
    const selectedMaterial = e.target.value;
    setMaterial(selectedMaterial);

    let analysis = `Calculating physics for ${selectedMaterial} material...`;
    setPhysicsAnalysis(analysis);
  };

  return (
    <div className="result-page">
      <h1>Prosthetic Design Results</h1>
      <div>
        <label htmlFor="stlFileInput">Select STL File:</label>
        <input
          type="file"
          id="stlFileInput"
          accept=".stl"
          onChange={handleFileChange}
          style={{ marginBottom: "20px" }}
        />
      </div>
      {error && <div className="error-message">{error}</div>}
      <div id="stlViewer" className="stl-viewer"></div>

      <div className="material-selection">
        <label htmlFor="materialSelection">Select Material:</label>
        <select id="materialSelection" value={material} onChange={handleMaterialChange}>
          <option value="PLA">PLA</option>
          <option value="ABS">ABS</option>
          <option value="PETG">PETG</option>
          <option value="Nylon">Nylon</option>
        </select>
      </div>

      <div className="physics-analysis">
        <h3>Physics Analysis:</h3>
        <textarea value={physicsAnalysis} readOnly />
      </div>
    </div>
  );
}

export default ResultPage;
