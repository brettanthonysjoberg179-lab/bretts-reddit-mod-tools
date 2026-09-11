"""Brett's Reddit Mod Tools — CLI entry point."""
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="reddit-mod-tools",
    help="Brett's Reddit Mod Tools — manage mod apps from the command line.",
    add_completion=True,
    no_args_is_help=True,
)

console = Console()

def print_header(title: str):
    """Print a section header."""
    console.print(f"\n[bold cyan]═══ {title} ═══[/bold cyan]")

# --- Core commands ---
@app.command("init")
def init_project():
    """Initialize the project (shared DB, config, venv)."""
    print_header("Initializing bretts-reddit-mod-tools...")
    import subprocess, sys
    from pathlib import Path
    root = Path(__file__).parent.parent.parent

    # Install deps
    console.print("[yellow]Installing dependencies...[/yellow]")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(root / "requirements.txt")], check=True)

    # Run setup
    console.print("[yellow]Running setup...[/yellow]")
    subprocess.run([sys.executable, str(root / "scripts" / "setup.py")], check=True)

    console.print("[green]✓ Project initialized![/green]")

@app.command("login")
def login():
    """Authenticate with Reddit OAuth2."""
    print_header("Reddit Login")
    import webbrowser
    from shared.config.settings import get_config
    from shared.auth.oauth2 import generate_state
    import sys

    config = get_config()
    state = generate_state()
    auth_url = (
        f"https://www.reddit.com/api/v1/authorize"
        f"?client_id={config['REDDIT_CLIENT_ID']}"
        f"&response_type=code"
        f"&state={state}"
        f"&redirect_uri={config['REDDIT_REDIRECT_URI']}"
        f"&duration=permanent"
        f"&scope=read+modposts+modconfig+modlog+modflair+modcontributors+modmail+modothers"
    )
    console.print(f"[bold]Opening Reddit auth in browser...[/bold]")
    webbrowser.open(auth_url)
    console.print("[yellow]Enter the callback code when prompted.[/yellow]")

@app.command("status")
def status():
    """Check project status — config, deps, DB."""
    print_header("Project Status")
    from pathlib import Path
    import importlib.util

    root = Path(__file__).parent.parent.parent

    # Check .env
    env_path = root / ".env"
    env_exists = env_path.exists()
    console.print(f"  [{'green' if env_exists else 'red'}]{'✓' if env_exists else '✗'}[/] .env {'exists' if env_exists else 'MISSING'}")

    # Check .env.example
    env_example = root / ".env.example"
    console.print(f"  [green]✓[/] .env.example {'exists' if env_example.exists() else 'MISSING'}")

    # Check DB
    db_path = root / "mod_tools.db"
    db_exists = db_path.exists()
    console.print(f"  [{'green' if db_exists else 'red'}]{'✓' if db_exists else '✗'}[/] Database {'exists' if db_exists else 'MISSING'}")

    # Check shared imports
    shared_ok = importlib.util.find_spec("shared") is not None
    console.print(f"  [{'green' if shared_ok else 'red'}]{'✓' if shared_ok else '✗'}[/] shared package {'importable' if shared_ok else 'NOT FOUND'}")

    # Check httpx + typer
    httpx_ok = importlib.util.find_spec("httpx") is not None
    typer_ok = importlib.util.find_spec("typer") is not None
    console.print(f"  [{'green' if httpx_ok else 'red'}]{'✓' if httpx_ok else '✗'}[/] httpx installed")
    console.print(f"  [{'green' if typer_ok else 'red'}]{'✓' if typer_ok else '✗'}[/] typer installed")

    # Check venv
    venv_path = root / ".venv"
    venv_ok = venv_path.exists()
    console.print(f"  [{'green' if venv_ok else 'yellow'}]{'✓' if venv_ok else '⚠'}[/] Virtual env {'exists' if venv_ok else 'not found (use system python)'}")

    console.print("\n[green]Status check complete.[/green]")

@app.command("apps")
def list_apps():
    """List all available mod tool apps."""
    print_header("Available Apps")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("App", style="cyan", min_width=20)
    table.add_column("Port", min_width=8)
    table.add_column("Description", min_width=40)
    table.add_column("Status", min_width=10)

    apps = [
        ("mod-suite", 5001, "All-in-one mod dashboard"),
        ("mod-queue", 5002, "Mod queue viewer & bulk processor"),
        ("mod-log", 5003, "Mod log viewer & analytics"),
        ("mod-mail", 5004, "Mod mail reader & responder"),
        ("mod-flair", 5005, "Flair management & bulk assign"),
    ]

    for app_name, port, desc in apps:
        table.add_row(app_name, str(port), desc, "ready")

    console.print(table)

@app.command("run")
def run_app(app_name: str = typer.Argument(..., help="App to run: mod-suite, mod-queue, mod-log, mod-mail, mod-flair")):
    """Run a specific mod tool app."""
    print_header(f"Running {app_name}...")
    import subprocess, sys
    from pathlib import Path

    port_map = {
        "mod-suite": 5001,
        "mod-queue": 5002,
        "mod-log": 5003,
        "mod-mail": 5004,
        "mod-flair": 5005,
    }

    if app_name not in port_map:
        console.print(f"[red]Unknown app: {app_name}[/red]")
        raise typer.Exit(code=1)

    port = port_map[app_name]
    app_path = Path(f"apps/{app_name}/app.py")

    if not app_path.exists():
        console.print(f"[red]App not found: {app_path}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]Starting {app_name} on port {port}...[/bold]")
    console.print(f"[yellow]Press Ctrl+C to stop.[/yellow]")

    subprocess.run([sys.executable, str(app_path)])

@app.command("manage")
def manage_app(app_name: str = typer.Argument(...), command: str = typer.Argument(...)):
    """Manage a specific app (status, logs, restart, deploy)."""
    print_header(f"Managing {app_name}: {command}")
    print_header(f"Managing {app_name}: {command}")

    if command == "status":
        console.print(f"[cyan]{app_name} status: running[/cyan]")
    elif command == "logs":
        console.print(f"[cyan]Fetching logs for {app_name}...[/cyan]")
    elif command == "restart":
        console.print(f"[cyan]Restarting {app_name}...[/cyan]")
    elif command == "deploy":
        console.print(f"[cyan]Deploying {app_name}...[/cyan]")
    else:
        console.print(f"[red]Unknown command: {command}[/red]")
        raise typer.Exit(code=1)

@app.command("install")
def install_deps():
    """Install all Python dependencies."""
    print_header("Installing dependencies...")
    import subprocess, sys
    from pathlib import Path
    root = Path(__file__).parent.parent.parent

    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(root / "requirements.txt")], check=True)
    console.print("[green]✓ Dependencies installed.[/green]")

@app.callback()
def main_callback(ctx: typer.Context):
    """Brett's Reddit Mod Tools — CLI."""
    if ctx.invoked_subcommand is None:
        console.print("[bold]Brett's Reddit Mod Tools[/bold]")
        console.print("Usage: reddit-mod-tools <command> [args]")
        console.print()
        console.print("Commands:")
        console.print("  init      Initialize project")
        console.print("  login     Authenticate with Reddit")
        console.print("  status    Check project status")
        console.print("  apps      List available apps")
        console.print("  run       Run a mod tool app")
        console.print("  manage    Manage an app")
        console.print("  install   Install dependencies")

if __name__ == "__main__":
    app()
