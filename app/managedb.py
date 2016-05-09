#!/usr/bin/env python
# ensure project path is in PYTHONPATH
import sys
import os

ALEMBIC_INI = 'migrations/alembic.ini'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__+'/..')))

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import app as luggageapp
from alembic.config import Config
from alembic import command

app = luggageapp.flask_app.test_client().application

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@migrate.configure
def configure_alembic(config):
    config.config_file_name = ALEMBIC_INI
    return config


@MigrateCommand.option('-d', '--directory', dest='directory', default=None,
                           help=("migration script directory (default is "
                                 "'migrations')"))
def setup(directory=None):
    """Creates db from scratch based on Flask models"""

    # inside of a "create the database" script, first create
    # tables:
    luggageapp.db.create_all()

    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    alembic_cfg = Config(ALEMBIC_INI)
    command.stamp(alembic_cfg, "head")

if __name__ == '__main__':
    manager.run()
