from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .led_manager import LEDManager

app = FastAPI()
led_manager = LEDManager()

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
def pulse(background_tasks: BackgroundTasks, color: Color, duration: float = 1.0):
    background_tasks.add_task(led_manager.pulse, (color.r, color.g, color.b), duration)
    return {"status": "Pulse effect applied"}