from app import create_app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

app = create_app()
migrate = Migrate(app, db)

cli = FlaskGroup(app)  # Cria grupo de comandos do Flask CLI

if __name__ == "__main__":
    cli()