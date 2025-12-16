import time
import sys
import random
from .led_manager import LEDManager

# Scene Definitions
SCENE_DEFS = {
    "Welcome": [
        {"action": "set_color", "args": [(0, 0, 255)]},
        {"action": "wait", "args": [0.5]},
        {"action": "fade_to", "args": [(0, 255, 0)], "kwargs": {"duration": 1.5}},
        {"action": "wait", "args": [0.5]},
        {"action": "fade_to", "args": [(255, 0, 0)], "kwargs": {"duration": 1.5}},
        {"action": "wait", "args": [0.5]},
        {"action": "turn_off", "kwargs": {"group_name": None}},
    ],
    "Red Alert": [
        {"action": "set_color", "args": [(255, 0, 0)]},
        {"action": "pulse", "kwargs": {"duration": 0.5}},
        {"action": "pulse", "kwargs": {"duration": 0.5}},
        {"action": "pulse", "kwargs": {"duration": 0.5}},
        {"action": "turn_off", "kwargs": {"group_name": None}},
    ],
    "Flash Groups": [
        {"action": "flash_groups_randomly", "kwargs": {"flashes": 3, "delay": 0.15}}
    ],
    "Cylon": [
        {"action": "cylon", "kwargs": {"color": (255, 0, 0), "duration": 2.0}}
    ],
}

class SceneManager:
    def __init__(self, led_manager: LEDManager):
        self.led_manager = led_manager

    def _flash_groups_randomly(self, flashes=3, delay=0.2):
        """Flashes each configured group with random colors."""
        groups = list(self.led_manager.group_ranges.keys())
        for group in groups:
            for _ in range(flashes):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                self.led_manager.set_color((r, g, b), group_name=group)
                time.sleep(delay)
                self.led_manager.turn_off(group_name=group)
                time.sleep(delay)
            time.sleep(0.2) # Pause between groups

    def get_scene_names(self):
        return list(SCENE_DEFS.keys())

    def play_scene(self, scene_name: str):
        if scene_name not in SCENE_DEFS:
            print(f"Error: Scene '{scene_name}' not found.", file=sys.stderr, flush=True)
            return

        actions = SCENE_DEFS[scene_name]
        for step in actions:
            action_name = step["action"]
            args = step.get("args", [])
            kwargs = step.get("kwargs", {})

            if action_name == "wait":
                time.sleep(args[0])
            elif action_name == "flash_groups_randomly":
                self._flash_groups_randomly(**kwargs)
            else:
                getattr(self.led_manager, action_name)(*args, **kwargs)