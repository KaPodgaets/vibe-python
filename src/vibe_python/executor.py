import pyautogui
import time
import threading
import datetime
from pathlib import Path

from .models import Robot, Action, TaskRun
from .database import DataAccessLayer
from .notifier import Notifier

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

def execute_action(action: Action, dal: DataAccessLayer, task_run: TaskRun):
    """Translates a single Action model into a pyautogui call."""
    action_map = {
        "move_to": lambda p: pyautogui.moveTo(p.get('x'), p.get('y'), duration=p.get('duration', 0.2)),
        "click": lambda p: pyautogui.click(**p),
        "double_click": lambda p: pyautogui.doubleClick(**p),
        "write": lambda p: pyautogui.write(p.get('text', ''), interval=p.get('interval', 0.05)),
        "press": lambda p: pyautogui.press(p.get('keys')),
        "hotkey": lambda p: pyautogui.hotkey(*p.get('keys', [])),
        "screenshot": lambda p: _take_screenshot(dal, task_run, p.get('filename')),
        "wait": lambda p: time.sleep(p.get('seconds', 1)),
    }
    
    if action.type in action_map:
        action_map[action.type](action.params)
        dal.add_log_entry(task_run.id, "INFO", f"Action '{action.type}' executed successfully.")
    else:
        raise ValueError(f"Unknown action type: {action.type}")

def _take_screenshot(dal: DataAccessLayer, task_run: TaskRun, filename_prefix: str) -> str:
    """Takes a screenshot, saves it, and logs it to the database."""
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{task_run.id}_{timestamp}.png"
    filepath = screenshots_dir / filename
    
    pyautogui.screenshot(filepath)
    dal.add_log_entry(task_run.id, "INFO", f"Screenshot taken: {filepath}", screenshot_path=str(filepath))
    return str(filepath)

def execute_robot(robot: Robot, dal: DataAccessLayer, notifier: Notifier, task_run: TaskRun):
    """Executes the sequence of actions for a given robot with resilience."""
    max_retries = robot.on_failure.retries
    
    dal.update_task_run_status(task_run.id, "Running")
    dal.add_log_entry(task_run.id, "INFO", f"Starting execution for robot: {robot.robot_name}")

    for attempt in range(max_retries + 1):
        try:
            for i, action in enumerate(robot.actions):
                dal.add_log_entry(
                    task_run.id, "INFO", f"Attempt {attempt+1}, Step {i+1}: Executing '{action.type}' - {action.description or ''}"
                )
                execute_action(action, dal, task_run)

            # If all actions succeeded
            success_message = f"Robot '{robot.robot_name}' completed successfully."
            dal.update_task_run_status(task_run.id, "Success", result_message=success_message)
            dal.add_log_entry(task_run.id, "INFO", success_message)
            print(f"--- {success_message} ---")
            return # Exit after success

        except Exception as e:
            error_message = f"Error during attempt {attempt+1}: {e}"
            print(f"!!! {error_message} !!!")
            
            # Log error and take screenshot
            screenshot_path = _take_screenshot(dal, task_run, "error")
            dal.add_log_entry(
                task_run.id, "ERROR", f"{error_message}. Screenshot saved to {screenshot_path}"
            )

            if attempt < max_retries:
                # This is a retryable attempt
                dal.increment_task_retry_count(task_run.id)
                delay = robot.on_failure.delay_seconds
                retry_log_msg = f"Waiting for {delay} seconds before next attempt..."
                dal.add_log_entry(task_run.id, "WARN", retry_log_msg)
                print(retry_log_msg)
                time.sleep(delay)
            else:
                # All retries have been exhausted
                final_error_msg = f"Robot '{robot.robot_name}' failed after {max_retries+1} attempts."
                dal.update_task_run_status(task_run.id, "Failed", result_message=final_error_msg)
                dal.add_log_entry(task_run.id, "ERROR", final_error_msg)
                notifier.send_failure_notification(robot, task_run, str(e))
                print(f"--- {final_error_msg} ---")
                break # Exit loop after final failure 