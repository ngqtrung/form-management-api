import click

from app import create_app
from app.common.utils import log, setup_logging


@click.group()
def cli():
    """Form Management API command-line entry point."""


@cli.command("api")
@click.option("--host", default="0.0.0.0", help="Host to bind the dev server to.")
@click.option("--port", default="5000", help="Port to bind the dev server to.")
@click.option("--debug/--no-debug", default=True, help="Enable Flask debug/reload mode.")
def run_api(host, port, debug):
    """Start the Flask development server. Usage: python run.py api"""
    setup_logging()
    log.info(f"Starting Form Management API on {host}:{port} (debug={debug})")
    app = create_app()
    app.run(host=host, port=int(port), debug=debug)


@cli.command("seed")
def run_seed():
    """Seed permissions, roles and demo users/forms. Usage: python run.py seed"""
    setup_logging()
    from scripts.seed import seed

    app = create_app()
    with app.app_context():
        log.info("Seeding permissions, roles, demo users and demo form...")
        seed()
        log.info("Seed complete.")


if __name__ == "__main__":
    cli()
