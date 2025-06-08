import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

from .models import Robot

CONFIG_DIR_PATH = Path("configs/robots.d")

class ConfigManager:
    """
    Manages loading and validation of robot configurations.
    It scans a directory for JSON files, validates them against the Robot model,
    and checks for duplicate robot names.
    """
    def __init__(self):
        load_dotenv()
        self._robots: Dict[str, Robot] = {}
        self.db_connection_string = os.getenv("DB_CONNECTION_STRING")
        self.reload_robots()

    def reload_robots(self):
        """Scans the config directory and loads all robot JSON files."""
        if not CONFIG_DIR_PATH.is_dir():
            print(f"Warning: Configuration directory not found at '{CONFIG_DIR_PATH}'. No robots will be loaded.")
            return
        
        loaded_robots = {}
        for file_path in CONFIG_DIR_PATH.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    robot_data = json.load(f)
                    robot = Robot.model_validate(robot_data)
                    if robot.robot_name in loaded_robots:
                        raise ValueError(f"Duplicate robot_name '{robot.robot_name}' found in {file_path}. Aborting.")
                    loaded_robots[robot.robot_name] = robot
            except Exception as e:
                print(f"Error loading or validating {file_path}: {e}")
        
        self._robots = loaded_robots
        print(f"Loaded {len(self._robots)} robot(s) from '{CONFIG_DIR_PATH}'.")

    def get_all_robots(self) -> List[Robot]:
        return list(self._robots.values())

    def get_robot(self, robot_name: str) -> Optional[Robot]:
        return self._robots.get(robot_name) 