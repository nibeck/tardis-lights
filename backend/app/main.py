from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .led_manager import LEDManager

app = FastAPI()

# Configuration for LED Groups
LED_GROUPS = [
    {"name": "Group1", "count": 10},
    {"name": "Group2", "count": 10},
    {"name": "Group3", "count": 10},
    {"name": "Group4", "count": 10},
    {"name": "Group5", "count": 10},
]

led_manager = LEDManager(groups=LED_GROUPS)

class Color(BaseModel):
    r: int
    g: int
    b: int

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TARDIS Lights API"}

@app.post("/led/on")
def turn_on(group: Optional[str] = None):
    led_manager.turn_on(group)
    return {"status": f"LEDs turned on for {group if group else 'all'}"}

@app.post("/led/off")
def turn_off(group: Optional[str] = None):
    led_manager.turn_off(group)
    return {"status": f"LEDs turned off for {group if group else 'all'}"}

@app.post("/led/color")
def set_color(color: Color, group: Optional[str] = None):
    led_manager.set_color((color.r, color.g, color.b), group)
    return {"status": f"Color set to ({color.r}, {color.g}, {color.b}) for {group if group else 'all'}"}

@app.post("/led/pulse")
def pulse(background_tasks: BackgroundTasks, color: Optional[Color] = None, duration: float = 1.0, group: Optional[str] = None):
    c = (color.r, color.g, color.b) if color else None
    background_tasks.add_task(led_manager.pulse, c, duration, group)
    return {"status": f"Pulse effect applied to {group if group else 'all'}"}

@app.post("/led/rainbow")
def rainbow(background_tasks: BackgroundTasks, duration: float = 5.0, group: Optional[str] = None):
    background_tasks.add_task(led_manager.rainbow_cycle, duration, group)
    return {"status": f"Rainbow effect started on {group if group else 'all'}"}