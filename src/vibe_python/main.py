import typer
from typing_extensions import Annotated

from .config import ConfigManager
from .executor import execute_robot

app = typer.Typer(help="A Python-based RPA Orchestrator.")

# Initialize the configuration manager once on startup.
try:
    config_manager = ConfigManager()
except Exception as e:
    typer.echo(f"Failed to initialize configuration: {e}", err=True)
    raise typer.Exit(code=1)

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
    robot_name: Annotated[str, typer.Argument(help="The name of the robot to run.")]
):
    """Immediately runs a single robot."""
    typer.echo(f"Attempting to run robot: {robot_name}")
    robot = config_manager.get_robot(robot_name)
    
    if not robot:
        typer.echo(typer.style(f"Error: Robot '{robot_name}' not found.", fg=typer.colors.RED))
        raise typer.Exit(code=1)
    if not robot.enabled:
        typer.echo(typer.style(f"Warning: Robot '{robot_name}' is disabled. Aborting.", fg=typer.colors.YELLOW))
        raise typer.Exit(code=1)

    try:
        execute_robot(robot)
        typer.echo(typer.style(f"Successfully finished running robot '{robot_name}'.", fg=typer.colors.GREEN))
    except Exception as e:
        typer.echo(typer.style(f"An error occurred while running robot '{robot_name}': {e}", fg=typer.colors.RED))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 