import React, { useState, useEffect } from 'react';
import './Popup.css';
import warn from "./warning.png"
import shield from "./shield.png"

function Popup({ url, onClose }) {
  const [isMalicious, setIsMalicious] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkUrl = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5776/check_url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      console.log(data);
  
      // Check the final_result value in the response
      if (data.final_result === 1) {
        // Handle the case where final_result is 1
        setIsMalicious(false);
      } else {
        // Handle the case where final_result is 0
        setIsMalicious(true);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  

  useEffect(() => {
    checkUrl();
  }, [url]);

  return (
    <div className="popup">
      {loading && <div>Loading...</div>}
      {isMalicious && !loading && (
        <div className="red-border">
          <img src={warn} alt="Danger" />
          <div>Fraudulent website</div>
          <button className="report-button">Report</button>
      <button onClick={onClose} className="close-button">
        Close
      </button>
        </div>
      )}
      {!isMalicious && !loading && (
        <div className="green-border">
          <img src={shield} alt="Safety" />
          <div>Safe to use</div>
          <button onClick={onClose} className="close-button">
        Close
      </button>
        </div>
      )}
    </div>
  );
}

export default Popup;
