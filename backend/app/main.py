"""
Main FastAPI application for the TARDIS Lights project.
Provides REST and WebSocket endpoints for controlling LEDs, playing sounds,
and managing animated scenes.
"""
import os
from typing import Optional, List

from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .led_manager import LEDManager, REAL_HARDWARE
from .scene_manager import SceneManager
from .sound_manager import SoundManager

app = FastAPI()

class Color(BaseModel):
    """Represents an RGB color with red, green, and blue components."""
    r: int
    g: int
    b: int

class TurnOnRequest(BaseModel):
    """Request schema for turning on LEDs with an optional color and section."""
    color: Optional[Color] = None
    section: str = ""

class PulseRequest(BaseModel):
    """Request schema for initiating a pulse effect with color, duration, and section."""
    color: Optional[Color] = None
    duration: float = 1.0
    section: str = ""

class SetColorRequest(BaseModel):
    """Request schema for setting a specific color for an LED section."""
    color: Color
    section: str = ""

class TurnOffRequest(BaseModel):
    """Request schema for turning off LEDs in a specific section."""
    section: str = ""

class RainbowRequest(BaseModel):
    """Request schema for starting a rainbow cycle effect with a given duration."""
    duration: float = 5.0
    section: str = ""

class Scene(BaseModel):
    """Represents an animated scene with a name and description."""
    name: str
    description: str

class SceneList(BaseModel):
    """Container for a list of available animated scenes."""
    scenes: List[Scene]

# Configuration for LED Sections
LED_SECTIONS = [
    {"name": "Front Windows", "count": 1},
    {"name": "Left Windows", "count": 1},
    {"name": "Rear Windows", "count": 1},
    {"name": "Right Windows", "count": 1},
    {"name": "Front Police", "count": 1},
    {"name": "Left Police", "count": 1},
    {"name": "Rear Police", "count": 1},
    {"name": "Right Police", "count": 1},
    {"name": "Top Light", "count": 1},
    {"name": "Extra", "count": 1}
]

led_manager = LEDManager(sections=LED_SECTIONS)
sound_manager = SoundManager()
scene_manager = SceneManager(led_manager)

class LEDSection(BaseModel):
    """Represents a physical LED section configuration."""
    name: str
    count: int

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LED Endpoints ---
@app.get("/")
def read_root():
    """Return a simple greeting to verify the API is running."""
    return {"message": "TARDIS Lights API"}

@app.get("/api/led/sections", response_model=List[LEDSection])
def get_led_sections():
    """Retrieve the list of available LED sections and their pixel counts."""
    return LED_SECTIONS

@app.post("/api/led/on")
def turn_on(request: TurnOnRequest):
    """
    Turn on LEDs in a specified section with an optional color.
    If no color is provided, the default white color is used.
    If no section is provided, all sections are turned on.
    """
    color_tuple = (
        (request.color.r, request.color.g, request.color.b)
        if request.color else None
    )
    led_manager.turn_on(
        section_name=request.section,
        color=color_tuple
    )
    return {"status": f"LEDs turned on for {request.section if request.section else 'all'}"}

@app.post("/api/led/off")
def turn_off(request: TurnOffRequest):
    """
    Turn off LEDs in a specified section.
    If no section is provided, all sections are turned off.
    """
    led_manager.turn_off(request.section)
    return {"status": f"LEDs turned off for {request.section if request.section else 'all'}"}

@app.post("/api/led/color")
def set_color(request: SetColorRequest):
    """Set a specific RGB color for a given LED section."""
    led_manager.set_color((request.color.r, request.color.g, request.color.b), request.section)
    return {"status": f"Color set to ({request.color.r}, {request.color.g}, {request.color.b}) for {request.section if request.section else 'all'}"}

@app.post("/api/led/pulse")
def pulse(request: PulseRequest, background_tasks: BackgroundTasks):
    """
    Initiate a pulse effect in a specified section.
    The effect runs in the background.
    """
    c = (request.color.r, request.color.g, request.color.b) if request.color else None
    background_tasks.add_task(led_manager.pulse, c, request.duration, request.section)
    return {"status": f"Pulse effect applied to {request.section if request.section else 'all'}"}

@app.post("/api/led/rainbow")
def rainbow(request: RainbowRequest, background_tasks: BackgroundTasks):
    """
    Start a rainbow cycle effect in a specified section.
    The effect runs in the background.
    """
    background_tasks.add_task(led_manager.rainbow_cycle, request.duration, request.section)
    return {"status": f"Rainbow effect started on {request.section if request.section else 'all'}"}

@app.get("/api/scenes", response_model=SceneList)
def get_scenes():
    """Retrieve the list of all available animated scenes."""
    return {"scenes": scene_manager.get_scenes()}

@app.post("/api/scenes/{scene_name}/play")
def play_scene(scene_name: str, background_tasks: BackgroundTasks):
    """
    Start playing a specific animated scene by name.
    The scene execution is handled as a background task.
    """
    background_tasks.add_task(scene_manager.play_scene, scene_name)
    return {"status": f"Playing scene: {scene_name}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Establish a WebSocket connection for real-time communication.
    Currently used to keep a connection open for future updates.
    """
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass

# --- Sound Endpoints ---

# Define the data structure for the API response
class Sound(BaseModel):
    """Represents an audio file available for playback."""
    fileName: str
    friendlyName: str

@app.get("/api/sounds", response_model=List[Sound])
async def get_sounds():
    """Retrieve the list of available audio files and their descriptions."""
    return sound_manager.get_available_sounds()

@app.post("/api/play-sound/{file_name}")
def play_sound(file_name: str, background_tasks: BackgroundTasks):
    """
    Start playing a specific sound file in the background.
    """
    background_tasks.add_task(sound_manager.play_sound, file_name)
    return {"status": f"Playing sound: {file_name}"}

@app.post("/api/stop-sound")
def stop_sound():
    """Stop any currently playing sound."""
    sound_manager.stop_sound()
    return {"status": "Sound stopped"}

# Serve the actual audio files at /sounds/filename.mp3
if not os.path.exists("sounds"):
    os.makedirs("sounds")
app.mount("/sounds", StaticFiles(directory="sounds"), name="sounds")