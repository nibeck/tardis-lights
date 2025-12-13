import React, { useState } from 'react';

function App() {
  const [status, setStatus] = useState('');

  const callAPI = async (endpoint, body = {}) => {
    let url = `http://192.168.1.161:8000${endpoint}`;
    if (endpoint === '/led/color' && body.r !== undefined) {
      url += `?r=${body.r}&g=${body.g}&b=${body.b}`;
    } else if (endpoint === '/led/pulse' && body.r !== undefined) {
      url += `?r=${body.r}&g=${body.g}&b=${body.b}&duration=${body.duration || 1.0}`;
    }
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: endpoint !== '/led/color' && endpoint !== '/led/pulse' ? { 'Content-Type': 'application/json' } : {},
        body: endpoint !== '/led/color' && endpoint !== '/led/pulse' ? JSON.stringify(body) : undefined,
      });
      const data = await response.json();
      console.log('API Response:', data);  // Debug: log the full response
      setStatus(data.status || JSON.stringify(data));  // Fallback to full data if no status
    } catch (error) {
      console.error('API Error:', error);  // Debug: log the error
      setStatus('Error: ' + error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>TARDIS Lights Controller</h1>
      <button onClick={() => callAPI('/led/on')}>Turn On</button>
      <button onClick={() => callAPI('/led/off')}>Turn Off</button>
      <button onClick={() => callAPI('/led/color', { r: 255, g: 0, b: 0 })}>Set Red</button>
      <button onClick={() => callAPI('/led/pulse', { r: 0, g: 255, b: 0 })}>Pulse Green</button>
      <p>Status: {status}</p>
    </div>
  );
}

export default App;