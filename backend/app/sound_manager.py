import subprocess
import os
from typing import Optional

# It's good practice to define constants for directories
SOUNDS_DIR = "sounds"

class SoundManager:
    """
    Manages playback of sound files on the server.
    """
    def play_sound(self, file_name: Optional[str]):
        """
        Plays a sound file from the sounds directory using a command-line player.

        This assumes a program like 'mpg123' is installed in the environment
        for playing MP3 files.
        """
        if not file_name:
            return

        sound_path = os.path.join(SOUNDS_DIR, file_name)

        if not os.path.exists(sound_path):
            print(f"ERROR: Sound file not found at {sound_path}")
            return

        try:
            # Using 'play' from sox. '-q' for quiet mode to prevent console output.
            subprocess.run(['play', '-q', sound_path], check=True)
        except FileNotFoundError:
            print(f"ERROR: 'sox' (play) command not found. Please install it in your Docker container to play sounds.")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to play sound '{file_name}'. Stderr: {e.stderr}")