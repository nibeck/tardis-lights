import subprocess
import os
from typing import Optional

# It's good practice to define constants for directories
SOUNDS_DIR = "sounds"

class SoundManager:
    """
    Manages playback of sound files on the server.
    """
    def __init__(self):
        self.current_process: Optional[subprocess.Popen] = None

    def play_sound(self, file_name: Optional[str]):
        """
        Plays a sound file from the sounds directory using a command-line player.
        Stops any currently playing sound before starting the new one.
        """
        if not file_name:
            return

        # Stop any existing sound
        self.stop_sound()

        sound_path = os.path.join(SOUNDS_DIR, file_name)

        if not os.path.exists(sound_path):
            print(f"ERROR: Sound file not found at {sound_path}")
            return

        try:
            # Using 'play' from sox. '-q' for quiet mode.
            # play_sound is now non-blocking (starts the process and returns)
            self.current_process = subprocess.Popen(['play', '-q', sound_path])
        except FileNotFoundError:
            print(f"ERROR: 'sox' (play) command not found. Please install it in your Docker container to play sounds.")
        except Exception as e:
            print(f"ERROR: Failed to start playback for '{file_name}'. Error: {e}")

    def stop_sound(self):
        """
        Stops the currently playing sound, if any.
        """
        if self.current_process and self.current_process.poll() is None:
            # Process is still running
            print("Stopping current sound...")
            self.current_process.terminate()
            try:
                self.current_process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            self.current_process = None