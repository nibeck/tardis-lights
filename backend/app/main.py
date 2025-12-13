from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .led_manager import LEDManager

app = FastAPI()
led_manager = LEDManager()

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
def set_color(r: int, g: int, b: int):
    led_manager.set_color((r, g, b))
    return {"status": f"Color set to ({r}, {g}, {b})"}

@app.post("/led/pulse")
def pulse(r: int = 255, g: int = 0, b: int = 0, duration: float = 1.0):
    led_manager.pulse((r, g, b), duration)
    return {"status": "Pulse effect applied"}