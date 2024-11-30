import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <h1 className="main-heading">
        <span className="hero-text">Welcome to</span>
        <br />
        <span className="ai-highlight">AI</span>
        <span className="design-text">-Enabled Prosthetic Design.</span>
      </h1>
      <p className="sub-heading">Upload your CT scan, let AI design customizable, 3D-printable prosthetics in STL format.</p>
    <div className="step-cards">
        <div className="card">
          <h2>Step 1:</h2>
          <p>Upload your CT scan</p>
        </div>
        <div className="card">
          <h2>Step 2:</h2>
          <p>AI designs customizable, 3D-printable prosthetics</p>
        </div>
        <div className="card">
          <h2>Step 3:</h2>
          <p>Export in STL file format</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
