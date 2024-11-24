import React, { useState } from 'react';

function Upload() {
  const [file, setFile] = useState(null);

  const handleUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = () => {
    console.log('File uploaded:', file);
    // Add upload logic here
  };

  return (
    <div>
      <h2>Upload CT Scan</h2>
      <input type="file" onChange={handleUpload} />
      <button onClick={handleSubmit}>Upload</button>
    </div>
  );
}

export default Upload;
