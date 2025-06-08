from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .database import DataAccessLayer
from .config import ConfigManager


def _queue_task(dal: DataAccessLayer, robot_name: str):
    """The actual function that the scheduler will call."""
    print(f"Scheduler: Queueing task for robot '{robot_name}'.")
    dal.create_task_run(robot_name=robot_name)

class Scheduler:
    def __init__(self, dal: DataAccessLayer, config_manager: ConfigManager):
        self.dal = dal
        self.config_manager = config_manager
        self.apscheduler = BackgroundScheduler(daemon=True)

    def _load_schedules(self):
        """Loads robot schedules from config and adds them to APScheduler."""
        robots = self.config_manager.get_all_robots()
        for robot in robots:
            if robot.enabled and robot.schedule:
                try:
                    self.apscheduler.add_job(
                        _queue_task,
                        trigger=CronTrigger.from_crontab(robot.schedule.expression),
                        args=[self.dal, robot.robot_name],
                        id=robot.robot_name,
                        replace_existing=True,
                    )
                    print(f"Scheduled robot '{robot.robot_name}' with schedule: '{robot.schedule.expression}'")
                except Exception as e:
                    print(f"Error scheduling robot '{robot.robot_name}': {e}")

    def start(self):
        self._load_schedules()
        self.apscheduler.start()
        print("Scheduler started.")

    def stop(self):
        if self.apscheduler.running:
            self.apscheduler.shutdown()
            print("Scheduler stopped.") 