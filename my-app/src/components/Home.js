import React, { useState } from 'react';
import './Home.css'; // Import the CSS file
import Popup from './Popup'; // Import the Popup component
import Navbar from './Navbar';

function Home() {
  const [isPopupVisible, setPopupVisible] = useState(false);
  const [url, setUrl] = useState(''); // State to store the URL

  const openPopup = () => {
    setPopupVisible(true);
  };

  const closePopup = () => {
    setPopupVisible(false);
  };

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  return (
    <div className="Home">
        <Navbar/>
      <div className="content-container">
        <h1 className="title">WELCOME TO THE FUTURE OF</h1>
        <p className="subtitle">FRAUD DETECTION</p>
        <p className="description">
          You can check the website for the chances of it being a phishing website. Just enter the link below to check for its trustability.
        </p>
        <div className="search">
          <div className="search-box">
            <input
              type="text"
              placeholder="Enter the link to check for phishing"
              value={url}
              onChange={handleUrlChange}
            />
          </div>
          <button type="submit" className="submit-button" onClick={openPopup}>
            Submit
          </button>
        </div>
      </div>
      {isPopupVisible && <Popup url={url} onClose={closePopup} />}
    </div>
  );
}

export default Home;
