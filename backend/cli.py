# cli.py

import click
from models import CheatSheet

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name')
def create(name):
    """Create a new cheat sheet."""
    cheatsheet = CheatSheet(name, data={})
    cheatsheet.save()
    click.echo(f"Cheat sheet '{name}' created.")

@cli.command()
def list():
    """List all cheat sheets."""
    cheatsheets = CheatSheet.list_all()
    for cs in cheatsheets:
        click.echo(cs)

@cli.command()
@click.argument('name')
def delete(name):
    """Delete a cheat sheet."""
    cheatsheet = CheatSheet(name)
    try:
        cheatsheet.delete()
        click.echo(f"Cheat sheet '{name}' deleted.")
    except FileNotFoundError:
        click.echo(f"Cheat sheet '{name}' not found.")

if __name__ == '__main__':
    cli()

