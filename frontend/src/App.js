import React, { useState } from 'react';

function App() {
  const [status, setStatus] = useState('');

  const callAPI = async (endpoint, body = {}) => {
    try {
      const response = await fetch(`http://192.168.1.161:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await response.json();
      setStatus(data.status);
    } catch (error) {
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