"""
Main FastAPI application for the TARDIS Lights project.
Provides REST and WebSocket endpoints for controlling LEDs, playing sounds,
and managing animated scenes.
"""
import json
import os
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .led_manager import LEDManager, REAL_HARDWARE
from .scene_manager import SceneManager
from .sound_manager import SoundManager


if os.getenv("ENABLE_DEBUGGER", "").lower() in ("true", "1", "yes"):
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))
    print("DEBUGGER: Waiting for debugger attach on port 5678...", flush=True)
    # debugpy.wait_for_client() # Uncomment if you want to block until attached

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

class FadeToColorRequest(BaseModel):
    """Request schema for fading to a specific color."""
    section: str = ""
    color: Color
    duration: float = 1.0

class BreathRequest(BaseModel):
    """Request schema for the breath effect."""
    section: str = ""
    color: Color
    period: float = 5.0
    count: int = 3

class WipeRequest(BaseModel):
    """Request schema for the wipe effect."""
    section: str = ""
    color: Color
    direction: str = "forward"
    speed: float = 0.1

class ChaseRequest(BaseModel):
    """Request schema for the chase effect."""
    section: str = ""
    color: Color
    spacing: int = 3
    speed: float = 0.1
    count: int = 50

class SparkleRequest(BaseModel):
    """Request schema for the sparkle effect."""
    section: str = ""
    color: Color
    density: int = 5
    duration: float = 5.0

class FlickerRequest(BaseModel):
    """Request schema for the flicker effect."""
    section: str = ""
    color: Color
    intensity: float = 0.5
    duration: float = 5.0

class StrobeRequest(BaseModel):
    """Request schema for the strobe effect."""
    section: str = ""
    color: Color
    frequency: float = 10.0
    duration: float = 5.0

class Scene(BaseModel):
    """Represents an animated scene with a name and description."""
    name: str
    description: str

class SceneList(BaseModel):
    """Container for a list of available animated scenes."""
    scenes: List[Scene]

class SectionConfigItem(BaseModel):
    """A single LED section entry for configuration."""
    name: str
    count: int

class SectionsConfig(BaseModel):
    """Container for the full LED sections configuration."""
    sections: List[SectionConfigItem]

# --- LED Sections Config File ---
CONFIG_FILE = Path(__file__).resolve().parent.parent / "led_sections.json"

DEFAULT_LED_SECTIONS = [
    {"name": "Left Windows", "count": 2},
    {"name": "Rear Windows", "count": 2},
    {"name": "Left Police", "count": 2},
    {"name": "Right Windows", "count": 2},
    {"name": "Front Police", "count": 2},
    {"name": "Front Windows", "count": 2},
    {"name": "Rear Police", "count": 2},
    {"name": "Right Police", "count": 2},
    {"name": "Top Light", "count": 2},
    {"name": "Extra", "count": 0},
]

def load_sections_config() -> list:
    """Load LED sections from JSON config file, or return defaults."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return data.get("sections", DEFAULT_LED_SECTIONS)
    return DEFAULT_LED_SECTIONS

def save_sections_config(sections: list) -> None:
    """Write LED sections to JSON config file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"sections": sections}, f, indent=2)

LED_SECTIONS = load_sections_config()

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

@app.get("/api/config/sections", response_model=SectionsConfig)
def get_config_sections():
    """Return the current LED sections configuration."""
    sections = load_sections_config()
    return {"sections": sections}

@app.post("/api/config/sections")
def save_config_sections(config: SectionsConfig):
    """Save LED sections configuration to disk."""
    sections = [s.model_dump() for s in config.sections]
    save_sections_config(sections)
    return {"status": "Configuration saved"}

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

@app.post("/api/led/fade")
def fade_to_color(request: FadeToColorRequest, background_tasks: BackgroundTasks):
    """Smoothly fade to a specific color."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.fade_to_color, request.section, c, request.duration)
    return {"status": f"Fade started on {request.section if request.section else 'all'}"}

@app.post("/api/led/breath")
def breath(request: BreathRequest, background_tasks: BackgroundTasks):
    """Start a breathing effect."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.breath, request.section, c, request.period, request.count)
    return {"status": f"Breath effect started on {request.section if request.section else 'all'}"}

@app.post("/api/led/wipe")
def wipe(request: WipeRequest, background_tasks: BackgroundTasks):
    """Start a wipe effect."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.wipe, request.section, c, request.direction, request.speed)
    return {"status": f"Wipe effect started on {request.section if request.section else 'all'}"}

@app.post("/api/led/chase")
def chase(request: ChaseRequest, background_tasks: BackgroundTasks):
    """Start a chase effect."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.chase, request.section, c, request.spacing, request.speed, request.count)
    return {"status": f"Chase effect started on {request.section if request.section else 'all'}"}

@app.post("/api/led/sparkle")
def sparkle(request: SparkleRequest, background_tasks: BackgroundTasks):
    """Start a sparkle effect."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.sparkle, request.section, c, request.density, request.duration)
    return {"status": f"Sparkle effect started on {request.section if request.section else 'all'}"}

@app.post("/api/led/flicker")
def flicker(request: FlickerRequest, background_tasks: BackgroundTasks):
    """Start a flicker effect."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.flicker, request.section, c, request.intensity, request.duration)
    return {"status": f"Flicker effect started on {request.section if request.section else 'all'}"}

@app.post("/api/led/strobe")
def strobe(request: StrobeRequest, background_tasks: BackgroundTasks):
    """Start a strobe effect."""
    c = (request.color.r, request.color.g, request.color.b)
    background_tasks.add_task(led_manager.strobe, request.section, c, request.frequency, request.duration)
    return {"status": f"Strobe effect started on {request.section if request.section else 'all'}"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



