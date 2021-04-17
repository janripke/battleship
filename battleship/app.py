from uuid import uuid4

import click
from flask import Flask
from flask_restful import Api
from paprika_connector.connectors.connector_factory import ConnectorFactory

from battleship.system import utils
from battleship.rest.properties.show_property import ShowProperty
from battleship.rest.game import Game
from battleship.rest.status import Status
from battleship.rest.shot import Shot

application = Flask(__name__)
api = Api(application)

ds = utils.load_json('battleship-ds.json')
connector = ConnectorFactory.create_connector(ds)
application.connector = connector

# set the secret, jwt uses this.
# every time the rest server start a new secret is created. Sessions do not survive a reboot.
application.config['SECRET_KEY'] = uuid4().hex

# initialize the logger
utils.load_logger('log.json', 'battleship')

# api.add_resource(Auth, '/auth')
api.add_resource(ShowProperty, '/properties/show')
api.add_resource(Game, '/battleship/game')
api.add_resource(Status, '/battleship/status')
api.add_resource(Shot, '/battleship/shot')


@click.command()
@click.option('-d', '--debug', required=False, default=False, is_flag=True)
@click.option('-p', '--port', required=False, type=int, default=5003)
@click.option('-h', '--host', required=False, default='0.0.0.0')
def main(debug, port, host):
    application.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    main(args=None)
