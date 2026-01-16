import React, { useState, useEffect } from 'react';

// Helper function to convert hex color string to RGB object
const hexToRgb = (hex) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : { r: 0, g: 0, b: 0 };
};

const TestRow = ({ label, endpoint, params, sections, onCall }) => {
  const [section, setSection] = useState('All');
  const [color, setColor] = useState('#ff0000');
  const [duration, setDuration] = useState(1.0);
  const [period, setPeriod] = useState(5.0);
  const [count, setCount] = useState(3);
  const [direction, setDirection] = useState('forward');
  const [speed, setSpeed] = useState(0.1);
  const [spacing, setSpacing] = useState(3);
  const [density, setDensity] = useState(5);
  const [intensity, setIntensity] = useState(0.5);
  const [frequency, setFrequency] = useState(10.0);

  // Generate a unique ID prefix for this row's inputs based on the label
  const idPrefix = label.replace(/\s+/g, '-').toLowerCase();

  const handleClick = (e) => {
    e.preventDefault();
    console.log(`Calling ${endpoint}`);
    const body = {};
    if (params.includes('section')) body.section = section;
    if (params.includes('color')) body.color = hexToRgb(color);
    if (params.includes('duration')) body.duration = parseFloat(duration);
    if (params.includes('period')) body.period = parseFloat(period);
    if (params.includes('count')) body.count = parseInt(count);
    if (params.includes('direction')) body.direction = direction;
    if (params.includes('speed')) body.speed = parseFloat(speed);
    if (params.includes('spacing')) body.spacing = parseInt(spacing);
    if (params.includes('density')) body.density = parseInt(density);
    if (params.includes('intensity')) body.intensity = parseFloat(intensity);
    if (params.includes('frequency')) body.frequency = parseFloat(frequency);

    onCall(endpoint, body);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px', flexWrap: 'wrap' }}>
      <button type="button" onClick={handleClick} style={{ marginRight: '10px', minWidth: '120px', marginBottom: '5px' }}>{label}</button>
      {params.includes('section') && (
        <select aria-label={`${label} Section`} value={section} onChange={(e) => setSection(e.target.value)} style={{ marginRight: '10px', padding: '5px', marginBottom: '5px' }}>
          {sections.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      )}
      {params.includes('color') && (
        <input aria-label={`${label} Color`} type="color" value={color} onChange={(e) => setColor(e.target.value)} style={{ marginRight: '10px', marginBottom: '5px' }} />
      )}
      {params.includes('duration') && (
        <>
          <label htmlFor={`${idPrefix}-duration`} style={{ marginRight: '5px', marginBottom: '5px' }}>Duration:</label>
          <input id={`${idPrefix}-duration`} type="number" value={duration} step="0.1" onChange={(e) => setDuration(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Duration" title="Duration (s)" />
        </>
      )}
      {params.includes('period') && (
        <>
          <label htmlFor={`${idPrefix}-period`} style={{ marginRight: '5px', marginBottom: '5px' }}>Period:</label>
          <input id={`${idPrefix}-period`} type="number" value={period} step="0.1" onChange={(e) => setPeriod(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Period" title="Period (s)" />
        </>
      )}
      {params.includes('count') && (
        <>
          <label htmlFor={`${idPrefix}-count`} style={{ marginRight: '5px', marginBottom: '5px' }}>Count:</label>
          <input id={`${idPrefix}-count`} type="number" value={count} step="1" onChange={(e) => setCount(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Count" title="Count" />
        </>
      )}
      {params.includes('direction') && (
        <>
          <label htmlFor={`${idPrefix}-direction`} style={{ marginRight: '5px', marginBottom: '5px' }}>Direction:</label>
          <select id={`${idPrefix}-direction`} value={direction} onChange={(e) => setDirection(e.target.value)} style={{ marginRight: '10px', padding: '5px', marginBottom: '5px' }}>
            <option value="forward">Forward</option>
            <option value="reverse">Reverse</option>
          </select>
        </>
      )}
      {params.includes('speed') && (
        <>
          <label htmlFor={`${idPrefix}-speed`} style={{ marginRight: '5px', marginBottom: '5px' }}>Speed:</label>
          <input id={`${idPrefix}-speed`} type="number" value={speed} step="0.01" onChange={(e) => setSpeed(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Speed" title="Speed (s)" />
        </>
      )}
      {params.includes('spacing') && (
        <>
          <label htmlFor={`${idPrefix}-spacing`} style={{ marginRight: '5px', marginBottom: '5px' }}>Spacing:</label>
          <input id={`${idPrefix}-spacing`} type="number" value={spacing} step="1" onChange={(e) => setSpacing(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Spacing" title="Spacing" />
        </>
      )}
      {params.includes('density') && (
        <>
          <label htmlFor={`${idPrefix}-density`} style={{ marginRight: '5px', marginBottom: '5px' }}>Density:</label>
          <input id={`${idPrefix}-density`} type="number" value={density} step="1" onChange={(e) => setDensity(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Density" title="Density" />
        </>
      )}
      {params.includes('intensity') && (
        <>
          <label htmlFor={`${idPrefix}-intensity`} style={{ marginRight: '5px', marginBottom: '5px' }}>Intensity:</label>
          <input id={`${idPrefix}-intensity`} type="number" value={intensity} step="0.1" min="0" max="1" onChange={(e) => setIntensity(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Intensity" title="Intensity (0-1)" />
        </>
      )}
      {params.includes('frequency') && (
        <>
          <label htmlFor={`${idPrefix}-frequency`} style={{ marginRight: '5px', marginBottom: '5px' }}>Frequency:</label>
          <input id={`${idPrefix}-frequency`} type="number" value={frequency} step="1" onChange={(e) => setFrequency(e.target.value)} style={{ width: '60px', padding: '5px', marginRight: '10px', marginBottom: '5px' }} placeholder="Freq" title="Frequency (Hz)" />
        </>
      )}
    </div>
  );
};

const SectionRow = ({ section, onCall }) => {
  const [color, setColor] = useState('#ff0000');
  const [isOn, setIsOn] = useState(false);

  const idPrefix = section.replace(/\s+/g, '-').toLowerCase();

  const handleColorChange = (e) => {
    setColor(e.target.value);
  };

  const handleOn = () => {
    setIsOn(true);
    onCall('/led/on', { section, color: hexToRgb(color) });
  };

  const handleOff = () => {
    setIsOn(false);
    onCall('/led/off', { section });
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
      <span style={{ minWidth: '150px' }}>{section}</span>
      <input
        type="color"
        value={color}
        onChange={handleColorChange}
        style={{ marginRight: '10px' }}
        aria-label={`${section} Color`}
      />
      <label style={{ marginRight: '10px' }}>
        <input type="radio" name={`power-${idPrefix}`} checked={isOn} onChange={handleOn} style={{ marginRight: '5px' }} />
        On
      </label>
      <label>
        <input type="radio" name={`power-${idPrefix}`} checked={!isOn} onChange={handleOff} style={{ marginRight: '5px' }} />
        Off
      </label>
    </div>
  );
};

function App() {
  // State variables for managing application data and UI state
  const [status, setStatus] = useState('');
  const [selectedGroup, setSelectedGroup] = useState('All'); // Currently selected LED section
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
    if (selectedGroup !== 'All' && requestBody.section === undefined) {
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
          setSelectedScene(data.scenes[0].name);
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

  const ledFunctions = [
    { label: 'Pulse Color', endpoint: '/led/pulse', params: ['section', 'color', 'duration'] },
    { label: 'Rainbow', endpoint: '/led/rainbow', params: ['section', 'duration'] },
    { label: 'Fade to Color', endpoint: '/led/fade', params: ['section', 'color', 'duration'] },
    { label: 'Breath', endpoint: '/led/breath', params: ['section', 'color', 'period', 'count'] },
    { label: 'Wipe', endpoint: '/led/wipe', params: ['section', 'color', 'direction', 'speed'] },
    { label: 'Chase', endpoint: '/led/chase', params: ['section', 'color', 'spacing', 'speed', 'count'] },
    { label: 'Sparkle', endpoint: '/led/sparkle', params: ['section', 'color', 'density', 'duration'] },
    { label: 'Flicker', endpoint: '/led/flicker', params: ['section', 'color', 'intensity', 'duration'] },
    { label: 'Strobe', endpoint: '/led/strobe', params: ['section', 'color', 'frequency', 'duration'] },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>Allons-z</h1>
      {/* Section Selection Dropdown */}
      <div style={{ marginBottom: '10px' }}>
        <label htmlFor="select-light" style={{ marginRight: '10px' }}>Select Light:</label>
        <select
          id="select-light"
          value={selectedGroup}
          onChange={(e) => setSelectedGroup(e.target.value)}
          style={{ padding: '5px' }}
        >
          {sections.map((section) => (
            <option key={section} value={section}>{section}</option>
          ))}
        </select>
      </div>
      {/* Scene Selection and Execution */}
      <div style={{ marginTop: '20px', marginBottom: '10px' }}>
        <label htmlFor="select-scene" style={{ marginRight: '10px' }}>Select Scene:</label>
        <select
          id="select-scene"
          value={selectedScene}
          onChange={(e) => setSelectedScene(e.target.value)}
          style={{ padding: '5px' }}
          disabled={scenes.length === 0}
        >
          {scenes.length === 0 ? (
            <option>Loading...</option>
          ) : (
            scenes.map((scene) => (
              <option key={scene.name} value={scene.name} title={scene.description}>{scene.name}</option>
            ))
          )}
        </select>
        <button onClick={() => callAPI(`/scenes/${selectedScene}/play`)} disabled={!selectedScene} style={{ marginLeft: '10px' }}>
          Run Scene
        </button>
      </div>
      {/* Sound Selection and Playback */}
      <div style={{ marginBottom: '10px' }}>
        <label htmlFor="select-sound" style={{ marginRight: '10px' }}>Select Sound:</label>
        <select
          id="select-sound"
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
      
      <h2>Section Control</h2>
      <div style={{ marginBottom: '20px' }}>
        <button
          type="button"
          onClick={() => callAPI('/led/off', { section: '' })}
          style={{ marginBottom: '10px', padding: '5px 10px', cursor: 'pointer' }}
        >
          All Off
        </button>
        {sections.map((section) => (
          <SectionRow key={section} section={section} onCall={callAPI} />
        ))}
      </div>

      <h2>LED Functions</h2>
      <div style={{ marginBottom: '20px' }}>
        {ledFunctions.map((func, index) => (
          <TestRow
            key={index}
            {...func}
            sections={sections}
            onCall={callAPI}
          />
        ))}
      </div>

      {/* Status Display */}
      <p role="status" aria-live="polite">Status: {status}</p>

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