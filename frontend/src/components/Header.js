import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="container">
        <h1>AI-Enabled Prosthetic Design</h1>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/upload">Upload</Link>
          <Link to="/results">Results</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
