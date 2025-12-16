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

        def __getitem__(self, index):
            return self.pixels[index]

    # Create mock board and neopixel modules
    class MockBoard:
        D18 = "D18"
    board = MockBoard()
    neopixel = type('MockNeoPixelModule', (), {'NeoPixel': MockNeoPixel, 'GRB': 'GRB'})()

class LEDManager:
    def __init__(self, groups, pin=board.D18):
        self.groups_config = groups
        self.group_ranges = {}
        self.num_leds = 0
        
        # Build the group ranges
        for group in groups:
            count = group['count']
            name = group['name']
            start = self.num_leds
            end = start + count
            self.group_ranges[name] = (start, end)
            self.num_leds += count

        self.pixels = neopixel.NeoPixel(pin, self.num_leds, brightness=0.2, auto_write=False)
        self.lock = threading.Lock()

    def _get_range(self, group_name):
        if group_name and group_name in self.group_ranges:
            return self.group_ranges[group_name]
        return (0, self.num_leds)

    def set_color(self, color, group_name=None):
        start, end = self._get_range(group_name)
        with self.lock:
            try:
                for i in range(start, end):
                    self.pixels[i] = color
                self.pixels.show()
            except Exception as e:
                print(f"Error setting LED color: {e}", file=sys.stderr, flush=True)

    def turn_on(self, group_name=None):
        self.set_color((255, 255, 255), group_name)  # White

    def turn_off(self, group_name=None):
        self.set_color((0, 0, 0), group_name)

    def pulse(self, color=None, duration=1.0, group_name=None):
        start, end = self._get_range(group_name)
        
        if color is None:
            # Try to use the color of the first pixel in the range as the base
            try:
                color = self.pixels[start]
                # If it's black/off, default to white so we see something
                if color == (0, 0, 0):
                    color = (255, 255, 255)
            except:
                color = (255, 255, 255)

        # Simple pulse effect
        for i in range(10):
            brightness = (i / 10.0)
            with self.lock:
                try:
                    dimmed_color = tuple(int(c * brightness) for c in color)
                    for p in range(start, end):
                        self.pixels[p] = dimmed_color
                    self.pixels.show()
                except Exception as e:
                    print(f"Error pulsing LEDs: {e}", file=sys.stderr, flush=True)
            time.sleep(duration / 20)

    def fade_to(self, target_color, duration=1.0, group_name=None):
        start, end = self._get_range(group_name)
        steps = 50  # Number of steps for the fade
        delay = duration / steps

        try:
            # Get the starting color from the first pixel in the range
            start_color = self.pixels[start]
        except Exception:
            start_color = (0, 0, 0)

        for i in range(steps + 1):
            ratio = i / steps
            # Interpolate each color channel
            r = int(start_color[0] * (1 - ratio) + target_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + target_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + target_color[2] * ratio)
            current_color = (r, g, b)

            with self.lock:
                for p in range(start, end):
                    self.pixels[p] = current_color
                self.pixels.show()
            time.sleep(delay)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self, duration=5.0, group_name=None):
        start, end = self._get_range(group_name)
        num_in_range = end - start
        start_time = time.time()
        j = 0
        while time.time() - start_time < duration:
            with self.lock:
                try:
                    for i in range(num_in_range):
                        pixel_index = (i * 256 // num_in_range) + j
                        self.pixels[start + i] = self.wheel(pixel_index & 255)
                    self.pixels.show()
                except Exception as e:
                    print(f"Error in rainbow cycle: {e}", file=sys.stderr, flush=True)
            j = (j + 1) % 256
            time.sleep(0.01)
        # Turn off LEDs after the cycle is complete
        self.turn_off(group_name)

    def cylon(self, color=(255, 0, 0), duration=2.0, group_name=None):
        start, end = self._get_range(group_name)
        num_pixels = end - start
        if num_pixels <= 0:
            return

        step_delay = duration / (2 * num_pixels)

        # Sweep forward and backward
        for i in list(range(num_pixels)) + list(range(num_pixels - 2, -1, -1)):
            with self.lock:
                # Fade all pixels in range to create trail
                for j in range(start, end):
                    current_color = self.pixels[j]
                    self.pixels[j] = tuple(int(c * 0.7) for c in current_color)
                
                # Set the leading pixel
                self.pixels[start + i] = color
                self.pixels.show()
            time.sleep(step_delay)
            
        self.turn_off(group_name)