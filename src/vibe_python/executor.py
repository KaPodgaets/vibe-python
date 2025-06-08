import pyautogui
import time
import threading
from .models import Robot, Action

_keep_alive_thread = None
_keep_alive_stop_event = threading.Event()

def _session_keep_alive_worker():
    """
    Worker function to periodically move the mouse slightly to prevent
    RDP session lock or screen saver activation.
    """
    print("Session keep-alive worker started.")
    while not _keep_alive_stop_event.wait(timeout=180): # 3-minute interval
        try:
            current_pos = pyautogui.position()
            # A very small, quick, and non-disruptive move
            pyautogui.move(1, 1, duration=0.1)
            pyautogui.move(-1, -1, duration=0.1)
            # Ensure the mouse returns exactly to its original position
            pyautogui.moveTo(current_pos)
            print("Keep-alive tick.")
        except pyautogui.FailSafeException:
            print("Fail-safe triggered during keep-alive. Pausing keep-alive.")
            # If user moves mouse to a corner, wait longer before trying again
            time.sleep(60)
    print("Session keep-alive worker stopped.")

def start_session_keep_alive():
    """Starts the session keep-alive mechanism in a background thread."""
    global _keep_alive_thread
    if _keep_alive_thread is None or not _keep_alive_thread.is_alive():
        _keep_alive_stop_event.clear()
        _keep_alive_thread = threading.Thread(target=_session_keep_alive_worker, daemon=True)
        _keep_alive_thread.start()

def stop_session_keep_alive():
    """Stops the session keep-alive mechanism."""
    global _keep_alive_thread
    if _keep_alive_thread and _keep_alive_thread.is_alive():
        _keep_alive_stop_event.set()
        _keep_alive_thread.join(timeout=5)
        _keep_alive_thread = None

def execute_action(action: Action):
    """Translates a single Action model into a pyautogui call."""
    action_map = {
        "move_to": lambda p: pyautogui.moveTo(p.get('x'), p.get('y'), duration=p.get('duration', 0.2)),
        "click": lambda p: pyautogui.click(**p),
        "double_click": lambda p: pyautogui.doubleClick(**p),
        "write": lambda p: pyautogui.write(p.get('text', ''), interval=p.get('interval', 0.05)),
        "press": lambda p: pyautogui.press(p.get('keys')),
        "hotkey": lambda p: pyautogui.hotkey(*p.get('keys', [])),
        "screenshot": lambda p: pyautogui.screenshot(p.get('filename')),
        "wait": lambda p: time.sleep(p.get('seconds', 1)),
    }
    
    if action.type in action_map:
        action_map[action.type](action.params)
    else:
        raise ValueError(f"Unknown action type: {action.type}")

def execute_robot(robot: Robot):
    """Executes the sequence of actions for a given robot (Phase 1 basic implementation)."""
    print(f"--- Starting execution for robot: {robot.robot_name} ---")
    for i, action in enumerate(robot.actions):
        print(f"Step {i+1}: Executing action '{action.type}' - {action.description or ''}")
        try:
            execute_action(action)
        except Exception as e:
            print(f"!!! ERROR on step {i+1} ({action.type}): {e}")
            print(f"--- Halting execution for robot: {robot.robot_name} ---")
            raise  # Re-raise exception to be handled by the caller
    print(f"--- Finished execution for robot: {robot.robot_name} ---") 