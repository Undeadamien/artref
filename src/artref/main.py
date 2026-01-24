import typer
import uvicorn

from artref.cli.main import app as app_cli

app = typer.Typer()
app.add_typer(app_cli)


@app.command()
def server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    uvicorn.run(
        "artref.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


def main():
    app()
