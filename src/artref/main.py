import typer
import uvicorn

from artref.cli.main import app as app_cli
from artref.core.config import SERVER_ADDR, SERVER_PORT

app = typer.Typer(no_args_is_help=True)
app.add_typer(app_cli)


@app.command()
def server(host: str = SERVER_ADDR, port: int = SERVER_PORT, reload: bool = False):
    """Run the server with uvicorn."""
    uvicorn.run("artref.api.main:app", host=host, port=port, reload=reload)


def main():
    app()
