import React, { useState, useEffect, useRef } from 'react';

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

  const handleColorChange = (e) => {
    setColor(e.target.value);
  };

  const handleToggle = () => {
    if (isOn) {
      setIsOn(false);
      onCall('/led/off', { section });
    } else {
      setIsOn(true);
      onCall('/led/on', { section, color: hexToRgb(color) });
    }
  };

  const toggleTrackStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    width: '48px',
    height: '26px',
    borderRadius: '13px',
    backgroundColor: isOn ? '#28a745' : '#ccc',
    padding: '3px',
    cursor: 'pointer',
    border: 'none',
    transition: 'background-color 0.2s',
    flexShrink: 0,
  };

  const toggleThumbStyle = {
    width: '20px',
    height: '20px',
    borderRadius: '50%',
    backgroundColor: '#fff',
    transform: isOn ? 'translateX(22px)' : 'translateX(0)',
    transition: 'transform 0.2s',
    boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
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
      <button
        type="button"
        role="switch"
        aria-checked={isOn}
        aria-label={`${section} power`}
        onClick={handleToggle}
        style={toggleTrackStyle}
      >
        <span style={toggleThumbStyle} />
      </button>
    </div>
  );
};

function App() {
  // State variables for managing application data and UI state
  const [status, setStatus] = useState('');
  const [scenes, setScenes] = useState([]); // List of available lighting scenes
  const [selectedScene, setSelectedScene] = useState(''); // Currently selected scene
  const [sounds, setSounds] = useState([]); // List of available sound files
  const [selectedSound, setSelectedSound] = useState(''); // Currently selected sound
  const [sections, setSections] = useState(['All']); // List of available LED sections
  const [activeTab, setActiveTab] = useState('control'); // Active tab: 'control' or 'config'
  const [configSections, setConfigSections] = useState([]); // Section config for Config tab
  const [configStatus, setConfigStatus] = useState(''); // Status message for Config tab
  const [presets, setPresets] = useState({}); // Named LED section presets
  const [sliderMax, setSliderMax] = useState(500); // Slider max for section count inputs
  const [activeSection, setActiveSection] = useState(null); // Index of section being previewed
  const [sectionColors, setSectionColors] = useState({}); // Current display color per section name
  const previewTimeout = useRef(null);

  // Helper function to make API calls to the backend
  const callAPI = async (endpoint, body = {}) => {
    const url = `/api${endpoint}`;

    // Prepare the unified request body
    const requestBody = { ...body };

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

  // Update the displayed color for one section (or all named sections when sectionName is falsy/"All")
  const updateSectionColor = (sectionName, color) => {
    const targets = (!sectionName || sectionName === 'All')
      ? sections.filter(s => s !== 'All')
      : [sectionName];
    setSectionColors(prev => {
      const next = { ...prev };
      targets.forEach(s => { next[s] = color; });
      return next;
    });
  };

  // Wraps callAPI and tracks color changes for endpoints that produce a known final color
  const callAPIAndTrack = (endpoint, body = {}) => {
    callAPI(endpoint, body);
    let color = null;
    if (endpoint === '/led/on')    color = body.color || { r: 255, g: 255, b: 255 };
    else if (endpoint === '/led/off')   color = { r: 0, g: 0, b: 0 };
    else if (endpoint === '/led/color') color = body.color;
    else if (endpoint === '/led/fade')  color = body.color;
    if (color) updateSectionColor(body.section, color);
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

  // Fetch config sections when Config tab is selected; turn off preview when leaving
  useEffect(() => {
    if (activeTab === 'config') {
      fetch('/api/config/sections')
        .then(res => res.json())
        .then(data => {
          if (data.sections) setConfigSections(data.sections);
        })
        .catch(err => console.error('Error fetching config sections:', err));
      fetch('/api/config/sections/presets')
        .then(res => res.json())
        .then(data => {
          if (data.presets) setPresets(data.presets);
        })
        .catch(err => console.error('Error fetching presets:', err));
    } else {
      // Leaving config tab — turn off preview LEDs
      setActiveSection(null);
      fetch('/api/config/sections/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count: 0 }),
      }).catch(err => console.error('Preview cleanup error:', err));
    }
  }, [activeTab]);

  const addSection = () => {
    setConfigSections([...configSections, { name: 'New Section', count: 0 }]);
  };

  const removeSection = (index) => {
    setConfigSections(configSections.filter((_, i) => i !== index));
  };

  const updateSection = (index, field, value) => {
    const updated = configSections.map((s, i) =>
      i === index ? { ...s, [field]: field === 'count' ? parseInt(value) || 0 : value } : s
    );
    setConfigSections(updated);
    if (field === 'count') {
      setActiveSection(index);
      previewSection(index, updated);
    }
  };

  const moveSection = (index, direction) => {
    const newIndex = index + direction;
    if (newIndex < 0 || newIndex >= configSections.length) return;
    const updated = [...configSections];
    [updated[index], updated[newIndex]] = [updated[newIndex], updated[index]];
    setConfigSections(updated);
  };

  const saveConfig = async () => {
    try {
      const response = await fetch('/api/config/sections', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sections: configSections }),
      });
      const data = await response.json();
      setConfigStatus(data.status || 'Saved');
    } catch (error) {
      setConfigStatus('Error saving: ' + error.message);
    }
  };

  const previewSection = (index, sections) => {
    clearTimeout(previewTimeout.current);
    const count = sections.slice(0, index + 1).reduce((sum, s) => sum + s.count, 0);
    previewTimeout.current = setTimeout(() => {
      fetch('/api/config/sections/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count }),
      }).catch(err => console.error('Preview error:', err));
    }, 100);
  };

  const totalLeds = configSections.reduce((sum, s) => sum + s.count, 0);

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

  const tabStyle = (tab) => ({
    padding: '10px 20px',
    cursor: 'pointer',
    border: 'none',
    borderBottom: activeTab === tab ? '3px solid #007bff' : '3px solid transparent',
    background: 'none',
    fontSize: '16px',
    fontWeight: activeTab === tab ? 'bold' : 'normal',
    color: activeTab === tab ? '#007bff' : '#666',
  });

  return (
    <div style={{ padding: '20px' }}>
      <h1>Allons-z</h1>

      <div style={{ display: 'flex', gap: '24px', alignItems: 'flex-start' }}>
      <div style={{ flex: 1, minWidth: 0 }}>

      {/* Tab Navigation */}
      <div style={{ display: 'flex', borderBottom: '1px solid #ddd', marginBottom: '20px' }}>
        <button style={tabStyle('control')} onClick={() => setActiveTab('control')}>Control</button>
        <button style={tabStyle('config')} onClick={() => setActiveTab('config')}>Config</button>
      </div>

      {/* Control Tab */}
      {activeTab === 'control' && (
        <>
          {/* Scene Selection and Execution */}
          <div style={{ marginBottom: '10px' }}>
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
            {sections.map((section) => (
              <SectionRow key={section} section={section} onCall={callAPIAndTrack} />
            ))}
          </div>

          <h2>LED Functions</h2>
          <div style={{ marginBottom: '20px' }}>
            {ledFunctions.map((func, index) => (
              <TestRow
                key={index}
                {...func}
                sections={sections}
                onCall={callAPIAndTrack}
              />
            ))}
          </div>

          {/* Status Display */}
          <p role="status" aria-live="polite">Status: {status}</p>
        </>
      )}

      {/* Config Tab */}
      {activeTab === 'config' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
            <h2 style={{ margin: 0 }}>Section Configuration</h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              {Object.keys(presets).length > 0 && (
                <div style={{ display: 'flex', gap: '4px' }}>
                  <span style={{ fontSize: '14px', color: '#666', alignSelf: 'center', marginRight: '4px' }}>Load preset:</span>
                  {Object.keys(presets).map(name => (
                    <button
                      key={name}
                      onClick={() => { const p = presets[name]; setConfigSections(p); setSliderMax(Math.max(10, ...p.map(s => s.count))); setConfigStatus(''); setActiveSection(null); }}
                      style={{ padding: '4px 10px', fontSize: '13px', textTransform: 'capitalize', cursor: 'pointer' }}
                      title={`Load ${name} preset`}
                    >
                      {name}
                    </button>
                  ))}
                </div>
              )}
              <span style={{ fontSize: '16px', fontWeight: 'bold' }}>Total LEDs: {totalLeds}</span>
            </div>
          </div>

          <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '15px' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                <th style={{ padding: '8px', width: '40px' }}>#</th>
                <th style={{ padding: '8px' }}>Name</th>
                <th style={{ padding: '8px', width: '60px' }}>Start</th>
                <th style={{ padding: '8px' }}>Count</th>
                <th style={{ padding: '8px', width: '100px' }}>Reorder</th>
                <th style={{ padding: '8px', width: '40px' }}></th>
              </tr>
            </thead>
            <tbody>
              {configSections.map((section, index) => {
                const start = configSections.slice(0, index).reduce((sum, s) => sum + s.count, 0);
                return (
                  <tr key={index} onClick={() => { setActiveSection(index); previewSection(index, configSections); }} style={{ borderBottom: '1px solid #eee', cursor: 'pointer', backgroundColor: activeSection === index ? '#e8f0fe' : 'transparent' }}>
                    <td style={{ padding: '8px' }}>{index + 1}</td>
                    <td style={{ padding: '8px' }}>
                      <input
                        type="text"
                        value={section.name}
                        onChange={(e) => updateSection(index, 'name', e.target.value)}
                        style={{ width: '100%', padding: '4px', boxSizing: 'border-box' }}
                      />
                    </td>
                    <td style={{ padding: '8px', textAlign: 'center', color: '#888' }}>{start}</td>
                    <td style={{ padding: '8px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <input
                          type="range"
                          min="0"
                          max={sliderMax}
                          value={section.count}
                          onChange={(e) => updateSection(index, 'count', e.target.value)}
                          style={{ flex: 1 }}
                        />
                        <input
                          type="number"
                          min="0"
                          max={sliderMax}
                          value={section.count}
                          onChange={(e) => updateSection(index, 'count', e.target.value)}
                          style={{ width: '60px', padding: '4px' }}
                        />
                      </div>
                    </td>
                    <td style={{ padding: '8px' }}>
                      {index > 0 && (
                        <button onClick={() => moveSection(index, -1)} style={{ marginRight: '4px' }} title="Move up">^</button>
                      )}
                      {index < configSections.length - 1 && (
                        <button onClick={() => moveSection(index, 1)} title="Move down">v</button>
                      )}
                    </td>
                    <td style={{ padding: '8px' }}>
                      <button onClick={() => removeSection(index)} title="Remove section" style={{ color: 'red', border: 'none', background: 'none', cursor: 'pointer', fontSize: '16px' }}>X</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <button onClick={addSection}>+ Add Section</button>
              <button type="button" onClick={() => { setConfigSections(configSections.map(s => ({ ...s, count: 0 }))); setActiveSection(null); previewSection(-1, []); }} style={{ marginLeft: '15px', fontSize: '14px', background: 'none', border: 'none', padding: 0, color: 'inherit', cursor: 'pointer', textDecoration: 'underline' }}>Reset Counts</button>
            </div>
            <button onClick={saveConfig} style={{ padding: '8px 20px', fontWeight: 'bold' }}>Save Configuration</button>
          </div>

          {configStatus && <p style={{ marginTop: '10px', color: configStatus.startsWith('Error') ? 'red' : 'green' }}>{configStatus}</p>}
        </div>
      )}

      </div>{/* end left column */}

      {/* Right column - Section Visualizer */}
      <div style={{ width: '220px', flexShrink: 0, position: 'sticky', top: '20px' }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#555', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Sections</h3>

        {/* Row 1: Top Light (centered) */}
        {(() => { const c = sectionColors['Top Light']; return (
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '8px' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ width: '60px', height: '60px', backgroundColor: c ? `rgb(${c.r},${c.g},${c.b})` : '#1a1a1a', border: '1px solid #555', borderRadius: '4px' }} />
              <div style={{ fontSize: '9px', marginTop: '3px', lineHeight: '1.2' }}>Top Light</div>
            </div>
          </div>
        ); })()}

        {/* Row 2: Police sections (half height) */}
        <div style={{ display: 'flex', gap: '4px', marginBottom: '8px' }}>
          {['Front Police', 'Left Police', 'Rear Police', 'Right Police'].map(name => {
            const c = sectionColors[name];
            return (
              <div key={name} style={{ flex: 1, textAlign: 'center' }}>
                <div style={{ height: '30px', backgroundColor: c ? `rgb(${c.r},${c.g},${c.b})` : '#1a1a1a', border: '1px solid #555', borderRadius: '3px' }} />
                <div style={{ fontSize: '8px', marginTop: '3px', lineHeight: '1.2', wordBreak: 'break-word' }}>{name}</div>
              </div>
            );
          })}
        </div>

        {/* Row 3: Window sections */}
        <div style={{ display: 'flex', gap: '4px' }}>
          {['Left Front Windows', 'Left Windows', 'Rear Windows', 'Right Windows', 'Right Front Windows'].map(name => {
            const c = sectionColors[name];
            return (
              <div key={name} style={{ flex: 1, textAlign: 'center' }}>
                <div style={{ height: '60px', backgroundColor: c ? `rgb(${c.r},${c.g},${c.b})` : '#1a1a1a', border: '1px solid #555', borderRadius: '3px' }} />
                <div style={{ fontSize: '8px', marginTop: '3px', lineHeight: '1.2', wordBreak: 'break-word' }}>{name}</div>
              </div>
            );
          })}
        </div>
      </div>

      </div>{/* end two-column layout */}

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