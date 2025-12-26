from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import os
from .led_manager import LEDManager, REAL_HARDWARE
from .scene_manager import SceneManager
from .sound_manager import SoundManager

app = FastAPI()

# Configuration for LED Sections
LED_SECTIONS = [
    {"name": "Front Windows", "count": 10},
    {"name": "Left Windows", "count": 10},
    {"name": "Rear Windows", "count": 10},
    {"name": "Right Windows", "count": 10},
    {"name": "Top Light", "count": 10}
]

led_manager = LEDManager(sections=LED_SECTIONS)
sound_manager = SoundManager()
scene_manager = SceneManager(led_manager)

class Color(BaseModel):
    r: int
    g: int
    b: int

class LEDSection(BaseModel):
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
    return {"message": "TARDIS Lights API"}

@app.get("/api/led/sections", response_model=List[LEDSection])
def get_led_sections():
    return LED_SECTIONS

@app.post("/api/led/on")
def turn_on(section: Optional[str] = None):
    led_manager.turn_on(section)
    return {"status": f"LEDs turned on for {section if section else 'all'}"}

@app.post("/api/led/off")
def turn_off(section: Optional[str] = None):
    led_manager.turn_off(section)
    return {"status": f"LEDs turned off for {section if section else 'all'}"}

@app.post("/api/led/color")
def set_color(color: Color, section: Optional[str] = None):
    led_manager.set_color((color.r, color.g, color.b), section)
    return {"status": f"Color set to ({color.r}, {color.g}, {color.b}) for {section if section else 'all'}"}

@app.post("/api/led/pulse")
def pulse(background_tasks: BackgroundTasks, color: Optional[Color] = None, duration: float = 1.0, section: Optional[str] = None):
    c = (color.r, color.g, color.b) if color else None
    background_tasks.add_task(led_manager.pulse, c, duration, section)
    return {"status": f"Pulse effect applied to {section if section else 'all'}"}

@app.post("/api/led/rainbow")
def rainbow(background_tasks: BackgroundTasks, duration: float = 5.0, section: Optional[str] = None):
    background_tasks.add_task(led_manager.rainbow_cycle, duration, section)
    return {"status": f"Rainbow effect started on {section if section else 'all'}"}

@app.get("/api/scenes")
def get_scenes():
    return {"scenes": scene_manager.get_scene_names()}

@app.post("/api/scenes/{scene_name}/play")
def play_scene(scene_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(scene_manager.play_scene, scene_name)
    return {"status": f"Playing scene: {scene_name}"}

# --- Sound Endpoints ---

# Define the data structure for the API response
class Sound(BaseModel):
    fileName: str
    friendlyName: str

@app.get("/api/available-sounds", response_model=List[Sound])
async def get_sounds():
    sounds = []
    sounds_dir = "sounds"
    if os.path.exists(sounds_dir):
        for filename in os.listdir(sounds_dir):
            if filename.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                name_without_ext = os.path.splitext(filename)[0]
                friendly_name = name_without_ext.replace("_", " ").replace("-", " ").title()
                sounds.append(Sound(fileName=filename, friendlyName=friendly_name))
    sounds.sort(key=lambda x: x.friendlyName)
    return sounds

@app.post("/api/play-sound/{file_name}")
def play_sound(file_name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(sound_manager.play_sound, file_name)
    return {"status": f"Playing sound: {file_name}"}

@app.post("/api/stop-sound")
def stop_sound():
    sound_manager.stop_sound()
    return {"status": "Sound stopped"}

# Serve the actual audio files at /sounds/filename.mp3
if not os.path.exists("sounds"):
    os.makedirs("sounds")
app.mount("/sounds", StaticFiles(directory="sounds"), name="sounds")