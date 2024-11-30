import React, { useState } from "react";
import axios from "axios";
import STLViewer from "../components/3DViewer";
import "./UploadPage.css"; // Make sure to import the CSS file for styling

function UploadPage() {
  const [file, setFile] = useState(null);
  const [stlUrl, setStlUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [material, setMaterial] = useState("lightweight_carbon_fiber");
  const [size, setSize] = useState("medium");
  const [color, setColor] = useState("#ffffff");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleCustomization = async () => {
    try {
      const response = await axios.post("/prosthetic/customize", {
        material,
        size,
        color,
      });
      alert("Customization applied!");
    } catch (error) {
      console.error("Error customizing prosthetic:", error);
      alert("Error customizing prosthetic. Please try again.");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a CT scan file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const response = await axios.post("/prosthetic/upload", formData);
      setStlUrl(response.data.stl_url);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error generating prosthetic. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <h1 className="heading_page">Upload CT Scan</h1>
      <div className="upload-container">
        <input 
          type="file" 
          id="fileInput" 
          onChange={handleFileChange} 
          accept="image/*" 
          className="file-input" 
        />
        <label htmlFor="fileInput" className="dropbox-label">
          Drag and drop your CT scan image here or click to select
        </label>
      </div>
      <p className="guidelines">
        <strong>Important Guidelines:</strong>
        <ul>
          <li>Only CT scan images are supported.</li>
          <li>Ensure the file size does not exceed 50MB.</li>
          <li>Only .jpg, .png, or .tiff file formats are allowed.</li>
        </ul>
      </p>
      <button onClick={handleUpload} disabled={loading} className="upload-btn">
        {loading ? "Processing..." : "Upload"}
      </button>

      {stlUrl && (
        <div>
          <h2>3D Prosthetic Design</h2>
          <STLViewer stlFileUrl={stlUrl} />
        </div>
      )}
    </div>
  );
}

export default UploadPage;
