import React from 'react';
import './Navbar.css'; // Import the CSS file

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">Akatsuki</div>
      <ul className="nav-links">
        <li><a href="/home">Home</a></li>
        <li><a href="/help">Help</a></li>
        
      </ul>
    </nav>
  );
}

export default Navbar;
