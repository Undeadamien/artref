import typer
import uvicorn

from artref.cli.main import app as app_cli
from artref.core.config import settings

app = typer.Typer(no_args_is_help=True)
app.add_typer(app_cli)


@app.command()
def server(
    host: str = settings.server_addr,
    port: int = settings.server_port,
    reload: bool = True,
):
    """Run the server with uvicorn."""
    uvicorn.run("artref.api.main:app", host=host, port=port, reload=reload)


def main():
    app()


if __name__ == "__main__":
    main()
