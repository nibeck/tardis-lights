import platform
import time

if platform.system() == 'Linux' and 'raspberrypi' in platform.uname().release.lower():
    import board
    import neopixel
else:
    # Mock for development on non-rPi systems
    class MockNeoPixel:
        def __init__(self, pin, num, brightness=1.0, auto_write=True):
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

    board = type('MockBoard', (), {'D18': None})()
    neopixel = type('MockNeoPixelModule', (), {'NeoPixel': MockNeoPixel})()

class LEDManager:
    def __init__(self, num_leds=50, pin=board.D18):
        self.num_leds = num_leds
        self.pixels = neopixel.NeoPixel(pin, num_leds, brightness=0.2, auto_write=False)

    def set_color(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def turn_on(self):
        self.set_color((255, 255, 255))  # White

    def turn_off(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def pulse(self, color, duration=1.0):
        # Simple pulse effect
        for i in range(10):
            brightness = (i / 10.0)
            self.pixels.fill(tuple(int(c * brightness) for c in color))
            self.pixels.show()
            time.sleep(duration / 20)
        for i in range(10, 0, -1):
            brightness = (i / 10.0)
            self.pixels.fill(tuple(int(c * brightness) for c in color))
            self.pixels.show()
            time.sleep(duration / 20)