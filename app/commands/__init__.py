import click
from flask.cli import with_appcontext

from .db_reset import reset_db, clear_file_tables
from .db_populate import populate_db_nertags, populate_grammatical_cases


@click.command('db_reset')
@with_appcontext
def reset_db_command():
    reset_db()
    click.echo('The database was reset successfully')


@click.command('db_populate')
@with_appcontext
def populate_db_command():
    populate_db_nertags()
    populate_grammatical_cases()
    click.echo('Ner Tags and Grammatical Cases were successfully added to the database')


@click.command('db_clear_file')
@with_appcontext
def clear_file_tables_command():
    clear_file_tables()
    click.echo('File tables were cleared successfully')
