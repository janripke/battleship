import logging
from flask import request, current_app
from flask_restful import Resource
import battleship
from battleship.system import utils
from battleship.system import tracer


class ShowProperty(Resource):

    def get(self):
        try:

            property_ = {
                'name': battleship.__title__,
                'version': battleship.__version__
            }

            return utils.responsify(property=property_), 200

        except Exception:
            response = tracer.build()
            logging.exception('show property failed')
            return response, 500


