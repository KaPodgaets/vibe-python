import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .models import Robot, TaskRun

class Notifier:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.recipient_emails = os.getenv("RECIPIENT_EMAILS", "").split(',')

    def send_failure_notification(self, robot: Robot, task_run: TaskRun, error_message: str):
        """Sends an email notification for a failed task run."""
        if not all([self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_password, self.recipient_emails]):
            print("Email notifier is not configured. Skipping notification.")
            return

        subject = f"RPA Failure: Robot '{robot.robot_name}' Failed"
        body = f"""
        <h2>RPA Task Failure Report</h2>
        <p><strong>Robot:</strong> {robot.robot_name}</p>
        <p><strong>Task Run ID:</strong> {task_run.id}</p>
        <p><strong>Time of Failure:</strong> {task_run.completed_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        <p><strong>Error Details:</strong></p>
        <pre>{error_message}</pre>
        """

        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = ", ".join(self.recipient_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            print(f"Successfully sent failure notification for task run {task_run.id}.")
        except Exception as e:
            print(f"Failed to send email notification: {e}") 