import typer
from typing_extensions import Annotated
from typing import Optional
from rich.console import Console
from rich.table import Table
import os
import time
import subprocess

from .config import ConfigManager
from .executor import execute_robot
from .database import DataAccessLayer
from .notifier import Notifier
from .scheduler import start_session_keep_alive, stop_session_keep_alive, scheduler

app = typer.Typer(help="A Python-based RPA Orchestrator.")
console = Console()

# Initialize the configuration manager once on startup.
try:
    config_manager = ConfigManager()
    if not config_manager.db_connection_string:
        console.print("[bold red]Error: DB_CONNECTION_STRING not found in .env file.[/bold red]")
        raise typer.Exit(code=1)
    
    dal = DataAccessLayer(config_manager.db_connection_string)
    notifier = Notifier()

except Exception as e:
    console.print(f"[bold red]Failed to initialize application: {e}[/bold red]")
    raise typer.Exit(code=1)

@app.command()
def init_db():
    """Initializes the database schema. DANGEROUS: Do not run on a DB with data."""
    dal.create_schema()
    console.print("[bold green]Database schema initialized successfully.[/bold green]")

@app.command()
def list_robots():
    """Lists all robots defined in the configuration."""
    typer.echo("Available Robots:")
    robots = config_manager.get_all_robots()
    if not robots:
        typer.echo("  (No robots found in configuration)")
        return
    for robot in robots:
        status = typer.style("enabled", fg=typer.colors.GREEN) if robot.enabled else typer.style("disabled", fg=typer.colors.RED)
        typer.echo(f"  - {robot.robot_name} [{status}]")

@app.command()
def run_now(
    robot_name: Annotated[str, typer.Argument(help="The name of the robot to run.")],
):
    """Immediately runs a single robot."""
    robot = config_manager.get_robot(robot_name)
    
    if not robot:
        console.print(f"[bold red]Error: Robot '{robot_name}' not found.[/bold red]")
        raise typer.Exit(code=1)
    if not robot.enabled:
        console.print(f"[yellow]Warning: Robot '{robot_name}' is disabled. Aborting.[/yellow]")
        raise typer.Exit(code=1)

    console.print(f"Creating task run for robot: [bold cyan]{robot_name}[/bold cyan]")
    task_run = dal.create_task_run(robot_name=robot_name)
    console.print(f"Task run created with ID: {task_run.id}")

    try:
        execute_robot(robot, dal, notifier, task_run)
    except Exception as e:
        console.print(f"[bold red]A critical error occurred while running robot '{robot_name}': {e}[/bold red]")
        raise typer.Exit(code=1)

@app.command()
def status(
    task_run_id: Annotated[Optional[int], typer.Argument(help="The ID of a specific task run.")] = None,
    limit: Annotated[int, typer.Option(help="Number of recent runs to show.")] = 10
):
    """Shows the status of recent or specific task runs."""
    if task_run_id:
        task = dal.get_task_run(task_run_id)
        if not task:
            console.print(f"[bold red]Error: Task Run ID '{task_run_id}' not found.[/bold red]")
            raise typer.Exit(code=1)
        
        console.print(f"[bold]Details for Task Run ID: {task.id}[/bold]")
        console.print(f"  Robot Name: {task.robot_name}")
        console.print(f"  Status: {task.status}")
        console.print(f"  Retries: {task.retry_count}")
        console.print(f"  Result: {task.result_message}")
        console.print(f"  Created: {task.created_at}")
        console.print(f"  Started: {task.started_at}")
        console.print(f"  Completed: {task.completed_at}")

    else:
        tasks = dal.get_latest_task_runs(limit)
        table = Table(title=f"Last {limit} Task Runs")
        table.add_column("ID", justify="right")
        table.add_column("Robot Name")
        table.add_column("Status")
        table.add_column("Created At")
        table.add_column("Completed At")

        for task in tasks:
            status_color = {"Success": "green", "Failed": "red", "Running": "yellow"}.get(task.status, "white")
            table.add_row(
                str(task.id),
                task.robot_name,
                f"[{status_color}]{task.status}[/{status_color}]",
                str(task.created_at),
                str(task.completed_at or "N/A"),
            )
        console.print(table)

@app.command()
def rerun(
    task_run_id: Annotated[int, typer.Argument(help="The ID of the task run to rerun.")]
):
    """Re-queues a past task run for execution by creating a new 'Pending' task."""
    task = dal.get_task_run(task_run_id)
    if not task:
        console.print(f"[bold red]Error: Task Run ID '{task_run_id}' not found.[/bold red]")
        raise typer.Exit(code=1)
    
    new_task = dal.create_task_run(robot_name=task.robot_name)
    console.print(f"Successfully re-queued robot '{task.robot_name}'. New Task Run ID: {new_task.id}")

@app.command()
def start_service():
    """Starts the orchestrator as a long-running service."""
    pid_file = "vibe_python.pid"
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

    console.print("[bold green]Starting RPA Orchestrator Service...[/bold green]")
    start_session_keep_alive()
    scheduler.start()

    try:
        console.print("Orchestrator is running. Press Ctrl+C to stop.")
        while True:
            task = dal.get_next_pending_task()
            if task:
                console.print(f"Picked up task {task.id} for robot '{task.robot_name}'.")
                robot_config = config_manager.get_robot(task.robot_name)
                if robot_config:
                    execute_robot(robot_config, dal, notifier, task)
                else:
                    error_msg = f"Configuration for robot '{task.robot_name}' not found."
                    dal.update_task_run_status(task.id, "Failed", result_message=error_msg)
            else:
                # Sleep for a bit to prevent busy-waiting
                time.sleep(5)
    except KeyboardInterrupt:
        console.print("\nShutting down orchestrator...")
    finally:
        scheduler.stop()
        stop_session_keep_alive()
        os.remove(pid_file)
        console.print("Orchestrator stopped.")

@app.command()
def restart_service():
    """Restarts the orchestrator service using an external script."""
    console.print("Attempting to restart the service...")
    try:
        subprocess.run(["./scripts/restart.bat"], shell=True, check=True)
        console.print("[green]Restart command issued.[/green]")
    except FileNotFoundError:
        console.print("[bold red]Error: restart.bat not found in scripts/ directory.[/bold red]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error executing restart script: {e}[/bold red]")

if __name__ == "__main__":
    app() 