import time
import platform
import board
import neopixel

def test_leds():
    print(f"System: {platform.system()} Release: {platform.release()}")
    print("Attempting to import board and neopixel...")

    # --- Configuration ---
    # GPIO pin connected to the data line of the NeoPixel strip.
    PIXEL_PIN = board.D18
    # The number of NeoPixels on your strip.
    NUM_PIXELS = 50
    # The order of the pixel colors - GRB, RGB, GRBW, RGBW.
    # If colors are weird when they do light up, try switching this to neopixel.RGB.
    ORDER = neopixel.GRB
    # --- End Configuration ---

    pixels = None
    try:
        print(f"Initializing {NUM_PIXELS} pixels on pin {PIXEL_PIN}...")
        pixels = neopixel.NeoPixel(
            PIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False, pixel_order=ORDER
        )

        print("Setting pixels to WHITE. If they light up, the connection is working.")
        pixels.fill((255, 255, 255))
        pixels.show()
        time.sleep(5)  # Keep them on for 5 seconds

    except Exception as e:
        print(f"\\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if pixels:
            print("Turning pixels off.")
            pixels.fill((0, 0, 0))
            pixels.show()
        print("Test complete.")

if __name__ == "__main__":
    test_leds()