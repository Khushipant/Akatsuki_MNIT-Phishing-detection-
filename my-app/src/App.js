import React from 'react';
import Navbar from './components/Navbar';
import Home from './components/Home';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import './App.css'; 
import Bot from './components/Bot';
import Rtdect from './components/Rtdect'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />}/>
          <Route path="help" element={<Bot />} />
          <Route path="rtd" element={<Rtdect />} />
          <Route path="home" element={<Home />} />
          {/* <Route path="blogs" element={<Blogs />} /> */}
          
      </Routes>
    </BrowserRouter>
  );
}

export default App;
