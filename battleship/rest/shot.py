import logging
from flask import request, current_app
from flask_restful import Resource
from battleship.system.utils import responsify
from battleship.system import tracer
from battleship.repositories.game_repository import GameRepository


class Shot(Resource):

    def post(self):
        """
        Execute a shot and receive the result
        :return:
        """
        try:
            payload = request.get_json(silent=True)

            if not payload:
                return responsify(message='Invalid JSON content, or content-type header '
                                          'is not set to application/json'), 400

            game_id = payload.get('game_id')
            username = payload.get('username')
            shot = payload.get('shot')

            if not game_id:
                logging.debug('no game_id')
                return responsify(message='no game_id'), 400

            if not username:
                logging.debug('no username')
                return responsify(message='no username'), 400

            if not shot:
                logging.debug('no shot')
                return responsify(message='no shot'), 400

            connector = current_app.connector
            game_repository = GameRepository(connector)
            game = game_repository.find_by(uuid=game_id)

            # check if the game exists and is active
            if not game:
                return responsify(message='game_id not found'), 404

            if game['winner']:
                return responsify(status="ended", winner=game['winner']), 200

            if game['active'] == 0:
                return responsify(status="dropped"), 200

            if not game['username_b']:
                return responsify(status="pending"), 200

            # determine which user you are, a or b
            user_key = None
            if game['username_a'] == username:
                user_key = "a"
            if game['username_b'] == username:
                user_key = "b"

            if not user_key:
                return responsify(message='invalid username'), 404

            # determine if it is your turn, by counting the X's
            # every shot results in a X on the grid of the other player
            count_x_a = game['grid_a'].count('X')
            count_x_b = game['grid_b'].count('X')

            # it is not your turn
            if count_x_a == count_x_b and user_key == "b":
                return responsify(status='not your turn')

            username_key = f"username_{user_key}"

            # calculate the position in the string
            row = int(shot['row'])
            col = int(shot['col'])
            position = col + (row - 1) * 10

            # determine the grid of the other player
            grid_key = "grid_a"
            if user_key == "a":
                grid_key = "grid_b"

            # retrieve the grid of the other player
            grid = game[grid_key]

            # retrieve the hit character
            hit_character = grid[position - 1]
            logging.debug(f"{hit_character=}")

            # place an X on the current position
            grid = f"{grid[0:position - 1]}X{grid[position:]}"

            game[grid_key] = grid

            if grid.count("X") + grid.count("0") == 100:
                game['winner'] = game[username_key]
                game['active'] = 0

            game_repository.update(game)
            connector.commit()

            if grid.count("X") + grid.count("0") == 100:
                return responsify(status="ended", winner=game['winner']), 200

            if str(hit_character) in "12345":
                return responsify(status="active", result="hit"), 200

            if hit_character == "0":
                return responsify(status="active", result="miss"), 200

            return responsify(status="active", result="twice"), 200

        except Exception:
            response = tracer.build()
            logging.exception('authentication failed')
            return response, 500
