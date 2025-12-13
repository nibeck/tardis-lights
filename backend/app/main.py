from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .led_manager import LEDManager

app = FastAPI()
led_manager = LEDManager(num_leds=50)

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
def turn_on():
    led_manager.turn_on()
    return {"status": "LEDs turned on"}

@app.post("/led/off")
def turn_off():
    led_manager.turn_off()
    return {"status": "LEDs turned off"}

@app.post("/led/color")
def set_color(color: Color):
    led_manager.set_color((color.r, color.g, color.b))
    return {"status": f"Color set to ({color.r}, {color.g}, {color.b})"}

@app.post("/led/pulse")
def pulse(background_tasks: BackgroundTasks, color: Optional[Color] = None, duration: float = 1.0):
    c = (color.r, color.g, color.b) if color else None
    background_tasks.add_task(led_manager.pulse, c, duration)
    return {"status": "Pulse effect applied"}

@app.post("/led/rainbow")
def rainbow(background_tasks: BackgroundTasks, duration: float = 5.0):
    background_tasks.add_task(led_manager.rainbow_cycle, duration)
    return {"status": "Rainbow effect started"}