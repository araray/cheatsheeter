# cli.py
"""
Command-line interface for CheatSheeter.
Provides commands for managing cheatsheets from the terminal.
"""

import os

import click
from marshmallow import ValidationError
from models import CheatSheet


@click.group()
def cli():
    """CheatSheeter CLI - Manage your cheatsheets from the command line."""
    pass


@cli.command()
@click.argument("name")
@click.option("--folder", default="cheatsheets", help="Cheatsheets folder path")
def create(name, folder):
    """Create a new empty cheat sheet."""
    try:
        cheatsheet = CheatSheet(
            name,
            data={
                "title": name.replace("-", " ").replace("_", " ").title(),
                "columns": 1,
                "categories": [],
            },
            cheatsheets_folder=folder,
        )

        if os.path.exists(cheatsheet.file_path):
            click.echo(click.style(f"✗ Cheat sheet '{name}' already exists.", fg="red"))
            return

        cheatsheet.save()
        click.echo(
            click.style(
                f"✓ Cheat sheet '{name}' created at {cheatsheet.file_path}", fg="green"
            )
        )

    except ValueError as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"✗ Unexpected error: {str(e)}", fg="red"))


@cli.command()
@click.option("--folder", default="cheatsheets", help="Cheatsheets folder path")
def list(folder):
    """List all cheat sheets."""
    try:
        cheatsheets = CheatSheet.list_all(folder)

        if not cheatsheets:
            click.echo(click.style("No cheat sheets found.", fg="yellow"))
            return

        click.echo(
            click.style(
                f"\nFound {len(cheatsheets)} cheat sheet(s):\n", fg="cyan", bold=True
            )
        )
        for cs in cheatsheets:
            click.echo(f"  • {cs}")

    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))


@cli.command()
@click.argument("name")
@click.option("--folder", default="cheatsheets", help="Cheatsheets folder path")
def show(name, folder):
    """Show details of a cheat sheet."""
    try:
        cheatsheet = CheatSheet(name, cheatsheets_folder=folder).load()

        click.echo(
            click.style(f"\n{cheatsheet.data.get('title', name)}", fg="cyan", bold=True)
        )
        click.echo(click.style("=" * 60, fg="cyan"))
        click.echo(f"Name: {name}")
        click.echo(f"Columns: {cheatsheet.columns}")
        click.echo(f"Categories: {len(cheatsheet.categories)}")

        if cheatsheet.categories:
            click.echo(click.style("\nCategories:", fg="yellow"))
            for cat in cheatsheet.categories:
                click.echo(f"  • {cat.get('name')} ({len(cat.get('items', []))} items)")

    except FileNotFoundError:
        click.echo(click.style(f"✗ Cheat sheet '{name}' not found.", fg="red"))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))


@cli.command()
@click.argument("name")
@click.option("--folder", default="cheatsheets", help="Cheatsheets folder path")
@click.confirmation_option(prompt="Are you sure you want to delete this cheat sheet?")
def delete(name, folder):
    """Delete a cheat sheet."""
    try:
        cheatsheet = CheatSheet(name, cheatsheets_folder=folder)
        cheatsheet.delete()
        click.echo(click.style(f"✓ Cheat sheet '{name}' deleted.", fg="green"))

    except FileNotFoundError:
        click.echo(click.style(f"✗ Cheat sheet '{name}' not found.", fg="red"))
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))


@cli.command()
@click.argument("name")
@click.option("--folder", default="cheatsheets", help="Cheatsheets folder path")
def validate(name, folder):
    """Validate a cheat sheet's structure."""
    try:
        cheatsheet = CheatSheet(name, cheatsheets_folder=folder).load()
        click.echo(click.style(f"✓ Cheat sheet '{name}' is valid.", fg="green"))

    except FileNotFoundError:
        click.echo(click.style(f"✗ Cheat sheet '{name}' not found.", fg="red"))
    except ValidationError as e:
        click.echo(click.style(f"✗ Validation errors:", fg="red"))
        for field, errors in e.messages.items():
            click.echo(f"  {field}: {', '.join(errors)}")
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"))


if __name__ == "__main__":
    cli()
