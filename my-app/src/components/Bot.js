import React, { useState, useRef, useEffect } from 'react';
import './Bot.css';
import Navbar from './Navbar';

const ChatBubble = ({ text, isUser, gifLink }) => (
  <div className={`chat-bubble ${isUser ? 'user' : 'bot'}`}>
    {gifLink === "" ? <h3>{text}</h3> : <img className="gif" src={gifLink} alt="gif" />}
  </div>
);

const Bot = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isInputEmpty, setIsInputEmpty] = useState(true); // Track if input is empty
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleUserMessage = async (userText) => {
    setChatHistory((prevHistory) => [
      ...prevHistory,
      { text: userText, isUser: true, gifLink: "" }
    ]);

    try {
      const response = await fetch('http://localhost:5776/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: userText })
      });

      const data = await response.json();

      setChatHistory((prevHistory) => [
        ...prevHistory,
        { text: data.aiResponse, isUser: false, gifLink: "" }
      ]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div><Navbar/>
    <div className="chat-app">
        
      <div className='cont'>
        <div className='chat-container'>
          {chatHistory.map((message, index) => (
            <div key={index} className={`message ${message.isUser ? 'user-message' : 'ai-message'}`}>
              <ChatBubble text={message.text} isUser={message.isUser} gifLink={message.gifLink} />
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <div className='inp-button'>
          <label className="custom-field">
            <input
              type="text"
              placeholder={isInputEmpty ? "Enter Prompt" : ""}
              value={inputValue}
              onChange={(e) => {
                setInputValue(e.target.value);
                setIsInputEmpty(e.target.value === ""); // Update the state based on input value
              }}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleUserMessage(e.target.value);
                  setInputValue("");
                  setIsInputEmpty(true); // Reset input state to empty after sending
                }
              }}
            />
          </label>
          <button
            className="send-button"
            onClick={() => {
              handleUserMessage(inputValue);
              setInputValue('');
              setIsInputEmpty(true); // Reset input state to empty after sending
            }}
          >
            Send
          </button>
        </div>
      </div>
      </div>
    </div>
  );
};

export default Bot;
