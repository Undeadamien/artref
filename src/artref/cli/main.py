import asyncio

import typer

from artref.core.main import fetch

app = typer.Typer()


@app.command()
def scryfall(query: str):
    typer.echo(asyncio.run(fetch("scryfall", query)))


@app.command()
def wallhaven(query: str):
    typer.echo(asyncio.run(fetch("wallhaven", query)))


def main():
    app()
