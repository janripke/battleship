import logging
from flask import request, current_app
from flask_restful import Resource
from battleship.system.utils import responsify
from battleship.system import tracer
from battleship.repositories.game_repository import GameRepository


class Game(Resource):

    def post(self):
        """
        Create a new game or attach to an existing game.
        A very simple mechanism is used, which fails when multiple requests are.
        :return:
        """
        try:
            payload = request.get_json(silent=True)

            if not payload:
                return responsify(message='Invalid JSON content, or content-type header '
                                          'is not set to application/json'), 400

            username = payload.get('username')
            grid = payload.get('grid')

            if not username:
                logging.debug('no username given')
                return responsify(message='no username given'), 400

            if not grid:
                logging.debug('no grid given')
                return responsify(message='no grid given'), 400

            connector = current_app.connector
            game_repository = GameRepository(connector)

            # find other games of this user and close them
            games = game_repository.list_by(username_a=username, active=1)
            for game in games:
                game['active'] = 0
                game_repository.update(game)

            # find other games of this user and close them
            games = game_repository.list_by(username_b=username, active=1)
            for game in games:
                game['active'] = 0
                game_repository.update(game)

            # find an open game.
            game = game_repository.open(username)
            if game:
                game['username_b'] = username
                game['grid_b'] = grid
                game_repository.update(game)

            # no open game found, create one
            if not game:
                game = {
                    'username_a': username,
                    'grid_a': grid
                }
                id_ = game_repository.insert(game)
                game = game_repository.find_by(id=id_)

            connector.commit()
            return responsify(game_id=game['uuid']), 200

        except Exception:
            response = tracer.build()
            logging.exception('authentication failed')
            return response, 500



