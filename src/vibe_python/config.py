import json
from pathlib import Path
from typing import List, Optional, Dict

from .models import Robot

# For Phase 1, we will use a single file as a starting point.
# The path is relative to the project root.
CONFIG_FILE_PATH = Path("configs/sample_robot.json")

class ConfigManager:
    """
    A simple configuration manager for Phase 1.

    It loads a single hardcoded JSON file which can contain a single robot
    object or a list of robot objects. A more robust directory-based loader
    will be implemented in a later phase.
    """
    def __init__(self):
        self._robots: Dict[str, Robot] = {}
        self._load_robots()

    def _load_robots(self):
        if not CONFIG_FILE_PATH.exists():
            print(f"Warning: Configuration file not found at '{CONFIG_FILE_PATH}'. No robots will be loaded.")
            return

        with open(CONFIG_FILE_PATH, "r") as f:
            robots_data = json.load(f)
            
            robots_to_load = []
            if isinstance(robots_data, list):
                robots_to_load = [Robot.model_validate(r) for r in robots_data]
            elif isinstance(robots_data, dict):
                 robots_to_load = [Robot.model_validate(robots_data)]

            self._robots = {r.robot_name: r for r in robots_to_load}
            print(f"Loaded {len(self._robots)} robot(s) from {CONFIG_FILE_PATH}.")

    def get_all_robots(self) -> List[Robot]:
        return list(self._robots.values())

    def get_robot(self, robot_name: str) -> Optional[Robot]:
        return self._robots.get(robot_name) 