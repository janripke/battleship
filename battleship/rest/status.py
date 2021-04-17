import logging
from flask import request, current_app
from flask_restful import Resource
from battleship.system.utils import responsify
from battleship.system import tracer
from battleship.repositories.game_repository import GameRepository


class Status(Resource):

    def get(self):
        """
        Retrieve the status of the given game_id.
        :return: { "status": "pending/active/dropped" }
        """
        try:
            connector = current_app.connector

            game_id = request.args.get('game_id')

            if not game_id:
                return responsify(message='no game_id'), 400

            game_repository = GameRepository(connector)
            game = game_repository.find_by(uuid=game_id)

            if not game:
                return responsify(message='game_id not found'), 404

            if game['active'] == 0:
                return responsify(status="dropped"), 200

            if not game['username_b']:
                return responsify(status="pending"), 200

            return responsify(status="active"), 200

        except Exception:
            response = tracer.build()
            logging.exception('show property failed')
            return response, 500


