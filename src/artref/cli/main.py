import typer

from artref.core.main import fetch

app = typer.Typer()


@app.command()
def scryfall():
    typer.echo(fetch("scryfall"))


@app.command()
def wallhaven():
    typer.echo(fetch("wallhaven"))


def main():
    app()
