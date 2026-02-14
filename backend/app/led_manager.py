import platform
import time
import threading
import sys
import math
import random

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
        """Mock implementation of the NeoPixel class for testing and development."""
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
        """Mock implementation of the board module for non-Raspberry Pi environments."""
        D18 = "D18"
    board = MockBoard()
    neopixel = type('MockNeoPixelModule', (), {'NeoPixel': MockNeoPixel, 'GRB': 'GRB'})()

class LEDManager:
    """Manages LED strips and sections for the TARDIS lights system."""
    MAX_LEDS = 5000  # Fixed buffer size — never recreated

    def __init__(self, sections, pin=board.D18):
        """
        Initialize the LEDManager.

        Args:
            sections (list): A list of dictionaries defining LED sections (e.g., [{'name': 'top', 'count': 10}]).
            pin (board.Pin): The GPIO pin connected to the LED strip.
        """
        self.sections_config = sections
        self.pin = pin
        self.section_ranges = {}
        self.num_leds = 0

        # Build the section ranges
        for section in sections:
            count = section['count']
            name = section['name']
            start = self.num_leds
            end = start + count
            self.section_ranges[name] = (start, end)
            self.num_leds += count

        self.pixels = neopixel.NeoPixel(pin, self.MAX_LEDS, brightness=0.2, auto_write=False)
        self.lock = threading.Lock()

    def _get_range(self, section_name):
        """
        Helper to get the start and end pixel indices for a given section name.

        Args:
            section_name (str, optional): The name of the section. If None, returns the full range.

        Returns:
            tuple: (start_index, end_index)
        """
        if section_name and section_name in self.section_ranges:
            return self.section_ranges[section_name]
        return (0, self.num_leds)

    def set_color(self, color, section_name=None):
        """
        Set the color of a specific section or the entire strip.

        Args:
            color (tuple): The RGB color tuple (r, g, b).
            section_name (str, optional): The name of the section to set. If None, sets the entire strip.
        """
        print ("Section in set_color function: ", section_name)
        start, end = self._get_range(section_name)
        with self.lock:
            try:
                for i in range(start, end):
                    self.pixels[i] = color
                self.pixels.show()
            except Exception as e:
                print(f"Error setting LED color: {e}", file=sys.stderr, flush=True)

    def turn_on(self, section_name=None, color=None):
        """
        Turn on a section or the entire strip with a specific color.

        Args:
            section_name (str, optional): The name of the section to turn on.
            color (tuple, optional): The RGB color tuple. Defaults to white (255, 255, 255).
        """
        if color is None:
            color = (255, 255, 255)  # Default to white
        self.set_color(color, section_name)

    def turn_off(self, section_name=None):
        """
        Turn off a section or the entire strip (set to black).

        Args:
            section_name (str, optional): The name of the section to turn off.
      """
        self.set_color((0, 0, 0), section_name)

    def pulse(self, color=None, duration=1.0, section_name=None):
        """
        Create a pulsing light effect on a section or the entire strip.

        Args:
            color (tuple, optional): The base RGB color to pulse. If None, attempts to use current color.
            duration (float, optional): The duration of the pulse in seconds.
            section_name (str, optional): The name of the section to pulse.
        """
        start, end = self._get_range(section_name)
        
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

    def fade_to(self, target_color, duration=1.0, section_name=None):
        """
        Gradually fade from the current color to a target color.

        Args:
            target_color (tuple): The target RGB color tuple.
            duration (float, optional): The duration of the fade in seconds.
            section_name (str, optional): The name of the section to fade.
        """
        start, end = self._get_range(section_name)
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

    def fade_to_color(self, section, to_color, duration):
        """
        Smoothly fade from the current color to the new color over the duration for the identified section.

        Args:
            section (str): The name of the section.
            to_color (tuple): The target RGB color tuple (r, g, b).
            duration (float): The duration of the fade in seconds.
        """
        start, end = self._get_range(section)
        
        # Calculate steps to maintain approx 50 updates per second
        steps = int(max(1, duration * 50))
        delay = duration / steps

        try:
            start_color = self.pixels[start]
        except Exception:
            start_color = (0, 0, 0)

        for i in range(1, steps + 1):
            ratio = i / steps
            r = int(start_color[0] * (1 - ratio) + to_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + to_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + to_color[2] * ratio)
            current_color = (r, g, b)

            with self.lock:
                for p in range(start, end):
                    self.pixels[p] = current_color
                self.pixels.show()
            time.sleep(delay)

    def breath(self, section, color, period, count):
        """
        A sine-wave fade up and down. This is the signature look of the TARDIS top lantern.

        Args:
            section (str): The name of the section.
            color (tuple): The RGB color tuple (r, g, b).
            period (float): How long one full breath takes in seconds.
            count (int): Number of breaths.
        """
        start, end = self._get_range(section)
        steps = int(max(1, period * 50))
        delay = period / steps

        for _ in range(count):
            for i in range(steps):
                # Calculate sine wave brightness (0.0 to 1.0)
                # Start at -PI/2 (min), go to PI/2 (max), end at 3PI/2 (min)
                angle = (i / steps) * 2 * math.pi - (math.pi / 2)
                brightness = (math.sin(angle) + 1) / 2
                
                current_color = tuple(int(c * brightness) for c in color)

                with self.lock:
                    for p in range(start, end):
                        self.pixels[p] = current_color
                    self.pixels.show()
                time.sleep(delay)
        
        self.turn_off(section)

    def wheel(self, pos):
        """
        Input a value 0 to 255 to get a color value.
        The colours are a transition r - g - b - back to r.
        """
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def rainbow_cycle(self, duration=5.0, section_name=None):
        """
        Cycle through all rainbow colors across the specified section.

        Args:
            duration (float, optional): How long to run the cycle in seconds.
            section_name (str, optional): The name of the section.
        """
        start, end = self._get_range(section_name)
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
        self.turn_off(section_name)

    def cylon(self, color=(255, 0, 0), duration=2.0, section_name=None):
        """
        Create a Cylon-style back-and-forth "scanner" effect.

        Args:
            color (tuple, optional): The RGB color of the scanner. Defaults to red.
            duration (float, optional): The duration of the effect in seconds.
            section_name (str, optional): The name of the section.
        """
        start, end = self._get_range(section_name)
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
            
        self.turn_off(section_name)

    def wipe(self, section, color, direction="forward", speed=0.1):
        """
        Lights up LEDs one by one from one end of the section to the other, like a progress bar filling up.

        Args:
            section (str): The name of the section.
            color (tuple): The RGB color tuple (r, g, b).
            direction (str): "forward" or "reverse".
            speed (float): Delay between pixels in seconds.
        """
        start, end = self._get_range(section)
        
        pixel_range = range(end - 1, start - 1, -1) if direction.lower() == "reverse" else range(start, end)

        for i in pixel_range:
            with self.lock:
                self.pixels[i] = color
                self.pixels.show()
            time.sleep(speed)

    def chase(self, section, color, spacing=3, speed=0.1, count=50):
        """
        A pattern of "pixels on, pixels off" that moves along the strip.

        Args:
            section (str): The name of the section.
            color (tuple): The RGB color tuple (r, g, b).
            spacing (int): Gap between lit pixels.
            speed (float): Delay between steps in seconds.
            count (int): Number of steps to run the chase.
        """
        start, end = self._get_range(section)
        length = end - start

        for i in range(count):
            with self.lock:
                for j in range(length):
                    if (j - i) % spacing == 0:
                        self.pixels[start + j] = color
                    else:
                        self.pixels[start + j] = (0, 0, 0)
                self.pixels.show()
            time.sleep(speed)
        
        self.turn_off(section)

    def sparkle(self, section, sparkle_color, density=5, duration=5.0):
        """
        Randomly turns on individual pixels within the section to a specific color for a split second, then returns them to the background color.

        Args:
            section (str): The name of the section.
            sparkle_color (tuple): The RGB color tuple (r, g, b).
            density (int): How many sparkles at once.
            duration (float): How long the effect lasts in seconds.
        """
        start, end = self._get_range(section)
        length = end - start
        
        if length == 0:
            return

        density = min(density, length)
        start_time = time.time()

        while time.time() - start_time < duration:
            indices = random.sample(range(start, end), density)
            original_colors = {}

            with self.lock:
                for i in indices:
                    try:
                        original_colors[i] = self.pixels[i]
                    except Exception:
                        original_colors[i] = (0, 0, 0)
                    self.pixels[i] = sparkle_color
                self.pixels.show()
            
            time.sleep(0.05) # Short duration for the sparkle

            with self.lock:
                for i in indices:
                    self.pixels[i] = original_colors[i]
                self.pixels.show()
            
            time.sleep(0.05)

    def flicker(self, section, base_color, intensity=0.5, duration=5.0):
        """
        Rapid, randomized brightness changes to simulate a dying bulb or an old fluorescent light.

        Args:
            section (str): The name of the section.
            base_color (tuple): The base RGB color tuple (r, g, b).
            intensity (float): How extreme the flicker is (0.0 to 1.0).
            duration (float): How long the effect lasts in seconds.
        """
        start, end = self._get_range(section)
        start_time = time.time()

        while time.time() - start_time < duration:
            # Random brightness reduction based on intensity
            brightness_factor = 1.0 - (random.random() * intensity)
            current_color = tuple(int(c * brightness_factor) for c in base_color)

            with self.lock:
                for p in range(start, end):
                    self.pixels[p] = current_color
                self.pixels.show()
            
            time.sleep(random.uniform(0.02, 0.1))
        
        self.turn_off(section)

    def strobe(self, section, color, frequency=10.0, duration=5.0):
        """
        High-speed flashing.

        Args:
            section (str): The name of the section.
            color (tuple): The RGB color tuple (r, g, b).
            frequency (float): Flashes per second.
            duration (float): How long the effect lasts in seconds.
        """
        start, end = self._get_range(section)
        period = 1.0 / max(frequency, 0.1)
        half_period = period / 2.0
        start_time = time.time()

        while time.time() - start_time < duration:
            with self.lock:
                for p in range(start, end):
                    self.pixels[p] = color
                self.pixels.show()
            time.sleep(half_period)

            with self.lock:
                for p in range(start, end):
                    self.pixels[p] = (0, 0, 0)
                self.pixels.show()
            time.sleep(half_period)
        
        self.turn_off(section)

    def delay(self, duration):
        """
        Pauses the sequence for a set time in seconds.

        Args:
            duration (float): The duration of the delay in seconds.
        """
        time.sleep(duration)

    def preview_count(self, count, color=(255, 255, 255)):
        """
        Light up LEDs 0 through count-1 for strip calibration.

        Used during configuration to visually show where a cumulative LED
        count lands on the physical strip. Sections are irrelevant here.

        Args:
            count (int): Number of LEDs to light starting from 0. Pass 0 to turn all off.
            color (tuple): RGB color for the lit LEDs.
        """
        count = max(0, min(count, self.MAX_LEDS))

        with self.lock:
            for i in range(self.MAX_LEDS):
                self.pixels[i] = color if i < count else (0, 0, 0)
            self.pixels.show()