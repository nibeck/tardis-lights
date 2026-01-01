import React, { useState, useEffect } from 'react';

function App() {
  // State variables for managing application data and UI state
  const [status, setStatus] = useState('');
  const [selectedGroup, setSelectedGroup] = useState('All'); // Currently selected LED section
  const [selectedColor, setSelectedColor] = useState('#ff0000'); // Currently selected color (hex)
  const [scenes, setScenes] = useState([]); // List of available lighting scenes
  const [selectedScene, setSelectedScene] = useState(''); // Currently selected scene
  const [sounds, setSounds] = useState([]); // List of available sound files
  const [selectedSound, setSelectedSound] = useState(''); // Currently selected sound
  const [sections, setSections] = useState(['All']); // List of available LED sections

  // Helper function to make API calls to the backend
  const callAPI = async (endpoint, body = {}) => {
    const url = `/api${endpoint}`;

    // Prepare the unified request body
    const requestBody = { ...body };
    if (selectedGroup !== 'All') {
      requestBody.section = selectedGroup;
    }

    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody),
    };

    try {
      const response = await fetch(url, options);
      const data = await response.json();
      console.log('API Response:', data);
      setStatus(data.status || JSON.stringify(data));
    } catch (error) {
      console.error('API Error:', error);
      setStatus('Error: ' + error.message);
    }
  };

  // Helper function to convert hex color string to RGB object
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
  };

  // Helper function to format date as MM/DD/YY. HH:MM:SS
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;

    const pad = (num) => num.toString().padStart(2, '0');
    const datePart = `${pad(date.getMonth() + 1)}/${pad(date.getDate())}/${date.getFullYear().toString().slice(-2)}`;
    const timePart = `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;

    return `${datePart}. ${timePart}`;
  };

  // Effect hook to fetch initial data when the component mounts
  useEffect(() => {
    // Fetch available LED sections
    const fetchSections = async () => {
      try {
        const response = await fetch('/api/led/sections');
        const data = await response.json();
        setSections(['All', ...data.map(s => s.name)]);
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    };

    // Fetch available lighting scenes
    const fetchScenes = async () => {
      try {
        const response = await fetch('/api/scenes');
        const data = await response.json();
        if (data.scenes && data.scenes.length > 0) {
          setScenes(data.scenes);
          setSelectedScene(data.scenes[0]);
        }
      } catch (error) {
        console.error('Error fetching scenes:', error);
        setStatus('Error fetching scenes: ' + error.message);
      }
    };

    // Fetch available sound files
    const fetchSounds = async () => {
      try {
        const response = await fetch('/api/sounds');
        const data = await response.json();
        if (Array.isArray(data)) {
          setSounds(data);
          if (data.length > 0) {
            setSelectedSound(data[0].fileName);
          }
        } else {
          console.error('Sounds API returned non-array:', data);
          setSounds([]);
        }
      } catch (error) {
        console.error('Error fetching sounds:', error);
        setSounds([]);
      }
    };

    fetchSections();
    fetchScenes();
    fetchSounds();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Allons-z</h1>
      {/* Section Selection Dropdown */}
      <div style={{ marginBottom: '10px' }}>
        <label style={{ marginRight: '10px' }}>Select Light:</label>
        <select
          value={selectedGroup}
          onChange={(e) => setSelectedGroup(e.target.value)}
          style={{ padding: '5px' }}
        >
          {sections.map((section) => (
            <option key={section} value={section}>{section}</option>
          ))}
        </select>
      </div>
      {/* Color Picker */}
      <div style={{ marginBottom: '10px' }}>
        <label style={{ marginRight: '10px' }}>Select Color:</label>
        <input
          type="color"
          value={selectedColor}
          onChange={(e) => setSelectedColor(e.target.value)}
        />
      </div>
      {/* Scene Selection and Execution */}
      <div style={{ marginTop: '20px', marginBottom: '10px' }}>
        <label style={{ marginRight: '10px' }}>Select Scene:</label>
        <select
          value={selectedScene}
          onChange={(e) => setSelectedScene(e.target.value)}
          style={{ padding: '5px' }}
          disabled={scenes.length === 0}
        >
          {scenes.length === 0 ? (
            <option>Loading...</option>
          ) : (
            scenes.map((scene) => (
              <option key={scene} value={scene}>{scene}</option>
            ))
          )}
        </select>
        <button onClick={() => callAPI(`/scenes/${selectedScene}/play`)} disabled={!selectedScene} style={{ marginLeft: '10px' }}>
          Run Scene
        </button>
      </div>
      {/* Sound Selection and Playback */}
      <div style={{ marginBottom: '10px' }}>
        <label style={{ marginRight: '10px' }}>Select Sound:</label>
        <select
          value={selectedSound}
          onChange={(e) => setSelectedSound(e.target.value)}
          style={{ padding: '5px' }}
          disabled={sounds.length === 0}
        >
          {Array.isArray(sounds) && sounds.map((sound) => (
            <option key={sound.fileName} value={sound.fileName}>{sound.friendlyName}</option>
          ))}
        </select>
        <button onClick={() => callAPI(`/play-sound/${selectedSound}`)} disabled={!selectedSound} style={{ marginLeft: '10px' }}>
          Play Sound
        </button>
        <button onClick={() => callAPI('/stop-sound')} style={{ marginLeft: '10px' }}>
          Stop Sound
        </button>
      </div>
      {/* Manual LED Controls */}
      <button onClick={() => callAPI('/led/on', { color: hexToRgb(selectedColor) })}>Turn On</button>
      <button onClick={() => callAPI('/led/off')}>Turn Off</button>
      <button onClick={() => callAPI('/led/color', { color: hexToRgb(selectedColor) })}>Set Color</button>
      <button onClick={() => callAPI('/led/pulse', { color: hexToRgb(selectedColor), duration: 1.0 })}>Pulse Color</button>
      <button onClick={() => callAPI('/led/rainbow', { duration: 5.0 })}>Rainbow</button>
      {/* Status Display */}
      <p>Status: {status}</p>

      {/* Footer with Build Info */}
      <div style={{
        marginTop: '40px',
        fontSize: '12px',
        color: '#666',
        borderTop: '1px solid #eee',
        paddingTop: '10px'
      }}>
        Build: {process.env.REACT_APP_BUILD_ID} | {formatDate(process.env.REACT_APP_BUILD_DATE)}
      </div>
    </div>
  );
}

export default App;