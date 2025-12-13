import platform
import time
import threading
import sys

try:
    import board
    import neopixel
    print(f"DEBUG: Hardware libraries loaded. Board ID: {getattr(board, 'board_id', 'unknown')}", flush=True)
    REAL_HARDWARE = True
except (ImportError, NotImplementedError, Exception) as e:
    print(f"DEBUG: Could not load hardware libraries ({e}). Using Mock LEDs.", flush=True)
    REAL_HARDWARE = False

if not REAL_HARDWARE:
    # Mock for development on non-rPi systems
    class MockNeoPixel:
        def __init__(self, pin, num, brightness=1.0, auto_write=True, pixel_order=None):
            self.num = num
            self.brightness = brightness
            self.auto_write = auto_write
            self.pixels = [(0, 0, 0)] * num

        def fill(self, color):
            self.pixels = [color] * self.num

        def show(self):
            print(f"Mock LED show: {self.pixels[:5]}...")  # Show first 5 for brevity

        def __setitem__(self, index, color):
            self.pixels[index] = color

    # Create mock board and neopixel modules
    class MockBoard:
        D18 = "D18"
    board = MockBoard()
    neopixel = type('MockNeoPixelModule', (), {'NeoPixel': MockNeoPixel, 'GRB': 'GRB'})()

class LEDManager:
    def __init__(self, num_leds=50, pin=board.D18):
        self.num_leds = num_leds
        self.pixels = neopixel.NeoPixel(pin, num_leds, brightness=0.2, auto_write=False)
        self.lock = threading.Lock()

    def set_color(self, color):
        with self.lock:
            try:
                self.pixels.fill(color)
                self.pixels.show()
            except Exception as e:
                print(f"Error setting LED color: {e}", file=sys.stderr, flush=True)

    def turn_on(self):
        self.set_color((255, 255, 255))  # White

    def turn_off(self):
        with self.lock:
            try:
                self.pixels.fill((0, 0, 0))
                self.pixels.show()
            except Exception as e:
                print(f"Error turning off LEDs: {e}", file=sys.stderr, flush=True)

    def pulse(self, color, duration=1.0):
        # Simple pulse effect
        for i in range(10):
            brightness = (i / 10.0)
            with self.lock:
                try:
                    self.pixels.fill(tuple(int(c * brightness) for c in color))
                    self.pixels.show()
                except Exception as e:
                    print(f"Error pulsing LEDs: {e}", file=sys.stderr, flush=True)
            time.sleep(duration / 20)
        for i in range(10, 0, -1):
            brightness = (i / 10.0)
            with self.lock:
                try:
                    self.pixels.fill(tuple(int(c * brightness) for c in color))
                    self.pixels.show()
                except Exception as e:
                    print(f"Error pulsing LEDs: {e}", file=sys.stderr, flush=True)
            time.sleep(duration / 20)