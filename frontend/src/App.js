import React, { useState } from 'react';

function App() {
  const [status, setStatus] = useState('');

  const callAPI = async (endpoint, body = {}) => {
    let url = `http://192.168.1.161:8000${endpoint}`;

    if (endpoint === '/led/pulse' && body.duration !== undefined) {
      url += `?duration=${body.duration}`;
    }

    const options = {
      method: 'POST',
    };

    if (endpoint === '/led/color' || endpoint === '/led/pulse') {
      options.headers = { 'Content-Type': 'application/json' };
      options.body = JSON.stringify(body);
    }

    try {
      const response = await fetch(url, options);
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