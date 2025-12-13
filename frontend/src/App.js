import React, { useState } from 'react';

function App() {
  const [status, setStatus] = useState('');
  const [selectedGroup, setSelectedGroup] = useState('All');
  const [selectedColor, setSelectedColor] = useState('#ff0000');
  const groups = ['All', 'Front', 'Left', 'Back', 'Right', 'Top'];

  const callAPI = async (endpoint, body = {}) => {
    let url = `http://192.168.1.161:8000${endpoint}`;
    const params = new URLSearchParams();

    if (endpoint === '/led/pulse' && body.duration !== undefined) {
      params.append('duration', body.duration);
    }
    if (selectedGroup !== 'All') {
      params.append('group', selectedGroup);
    }
    const queryString = params.toString();
    if (queryString) {
      url += `?${queryString}`;
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

  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>TARDIS Lights Controller</h1>
      <div style={{ marginBottom: '10px' }}>
        <label style={{ marginRight: '10px' }}>Select Group:</label>
        <select
          value={selectedGroup}
          onChange={(e) => setSelectedGroup(e.target.value)}
          style={{ padding: '5px' }}
        >
          {groups.map((group) => (
            <option key={group} value={group}>{group}</option>
          ))}
        </select>
      </div>
      <div style={{ marginBottom: '10px' }}>
        <label style={{ marginRight: '10px' }}>Select Color:</label>
        <input
          type="color"
          value={selectedColor}
          onChange={(e) => setSelectedColor(e.target.value)}
        />
      </div>
      <button onClick={() => callAPI('/led/on')}>Turn On</button>
      <button onClick={() => callAPI('/led/off')}>Turn Off</button>
      <button onClick={() => callAPI('/led/color', hexToRgb(selectedColor))}>Set Color</button>
      <button onClick={() => callAPI('/led/pulse', hexToRgb(selectedColor))}>Pulse Color</button>
      <button onClick={() => callAPI('/led/rainbow')}>Rainbow</button>
      <p>Status: {status}</p>
    </div>
  );
}

export default App;