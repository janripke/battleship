import unittest

from tests.base_test import BaseTestCase
from paprika_connector.connectors.connector_factory import ConnectorFactory
from battleship.system.requestors import RestRequest
from battleship.system import utils
from battleship.repositories.game_repository import GameRepository


class TestRest(BaseTestCase):
    def game(self, game_):
        url = f'{TestRest.ENDPOINT}/battleship/game'

        proxies = TestRest.REQUESTS_PROXIES
        request = RestRequest(proxies=proxies)
        response = request.post(url, game_)

        status_code = response.status_code
        expected = 200
        self.assertEqual(expected, status_code, 'invalid status_code')

        content = response.json()
        self.assertIsNotNone(content, 'no content')

        game_id = content.get('game_id')
        self.assertIsNotNone(content, 'no game_id')
        return game_id

    def status(self, game_id):
        url = f'{TestRest.ENDPOINT}/battleship/status?game_id={game_id}'

        proxies = TestRest.REQUESTS_PROXIES
        request = RestRequest(proxies=proxies)
        response = request.get(url)

        status_code = response.status_code
        expected = 200
        self.assertEqual(expected, status_code, 'invalid status_code')

        content = response.json()
        self.assertIsNotNone(content, 'no content')

        status = content.get('status')
        self.assertIsNotNone(content, 'no status')
        return status

    def shot(self, game_id, username, shot):
        url = f'{TestRest.ENDPOINT}/battleship/shot'
        proxies = TestRest.REQUESTS_PROXIES
        request = RestRequest(proxies=proxies)

        shot_ = {
            "game_id": game_id,
            "username": username,
            "shot": shot
        }

        response = request.post(url, shot_)

        status_code = response.status_code
        expected = 200
        self.assertEqual(expected, status_code, 'invalid status_code')

        content = response.json()
        self.assertIsNotNone(content, 'no content')

        return content

    def test_show_property(self):
        url = f'{TestRest.ENDPOINT}/properties/show'
        proxies = TestRest.REQUESTS_PROXIES

        request = RestRequest(proxies=proxies)
        response = request.get(url)

        status_code = response.status_code
        expected = 200
        self.assertEqual(expected, status_code, 'invalid status_code')

        content = response.json()
        self.assertIsNotNone(content, 'no content')

        property_ = content.get('property')
        self.assertIsNotNone(property_, 'no property')

        name = property_.get('name')
        self.assertEqual('battleship', name)

    def test_game_one_user(self):
        """
        This test passes when a game is created for a single user, username_a
        :return:
        """
        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        ds = utils.load_json('battleship-ds.json')
        connector = ConnectorFactory.create_connector(ds)

        game_repository = GameRepository(connector)
        game = game_repository.find_by(uuid=game_id)
        self.assertIsNotNone(game, 'no game')

        username_a = game.get('username_a')
        self.assertIsNotNone(username_a, 'no username_a')
        self.assertEqual('jan', username_a, 'invalid username')

    def test_game_two_users(self):
        """
        This test passes when username_b kees is connected to the game of username_a jan.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        username_a_game_id = self.game(game)

        game = {
            'username': 'kees',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        username_b_game_id = self.game(game)

        self.assertEqual(username_a_game_id, username_b_game_id, 'game_id does not match')

        ds = utils.load_json('battleship-ds.json')
        connector = ConnectorFactory.create_connector(ds)

        game_repository = GameRepository(connector)
        game = game_repository.find_by(uuid=username_a_game_id)
        self.assertIsNotNone(game, 'no game')

        username_a = game.get('username_a')
        self.assertIsNotNone(username_a, 'no username_a')
        self.assertEqual('jan', username_a, 'invalid username')

        username_b = game.get('username_b')
        self.assertIsNotNone(username_b, 'no username_b')
        self.assertEqual('kees', username_b, 'invalid username')

    def test_status_pending(self):
        """
        This test passes when the status of the game is pending.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)
        status = self.status(game_id)

        self.assertEqual('pending', status)

    def test_status_active(self):
        """
        This test passes when the status of the game is active.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        game = {
            'username': 'kees',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        status = self.status(game_id)

        self.assertEqual('active', status)

    def test_status_dropped(self):
        """
        This test passes when the status of the game is dropped.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        first_game_id = self.game(game)

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)
        status = self.status(first_game_id)

        self.assertEqual('dropped', status)

    def test_shot_player_a_hit(self):
        """
        This test passes when the shot results in a hit.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        game = {
            'username': 'kees',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        # assume being player a
        shot = {
            "row": "1",
            "col": "2"
        }
        response = self.shot(game_id, 'jan', shot)

        status = response.get('status')
        result = response.get('result')
        self.assertIsNotNone(status, 'no status')
        self.assertIsNotNone(result, 'no result')
        self.assertEqual('hit', result, 'invalid result')

        ds = utils.load_json('battleship-ds.json')
        connector = ConnectorFactory.create_connector(ds)

        game_repository = GameRepository(connector)
        game = game_repository.find_by(uuid=game_id)

        grid = game['grid_b']
        expected = "0X00222200" \
                   "0300000000" \
                   "0310000000" \
                   "0010005000" \
                   "0010005000" \
                   "0010044400" \
                   "0010000000" \
                   "0000000000" \
                   "0000000000" \
                   "0000000000"
        self.assertEqual(expected, grid, "invalid grid")

    def test_shot_player_a_miss(self):
        """
        This test passes when the shot results in a hit.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        game = {
            'username': 'kees',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        # assume being player a
        shot = {
            "row": "2",
            "col": "1"
        }
        response = self.shot(game_id, 'jan', shot)

        status = response.get('status')
        result = response.get('result')
        self.assertIsNotNone(status, 'no status')
        self.assertIsNotNone(result, 'no result')
        self.assertEqual('miss', result, 'invalid result')

        ds = utils.load_json('battleship-ds.json')
        connector = ConnectorFactory.create_connector(ds)

        game_repository = GameRepository(connector)
        game = game_repository.find_by(uuid=game_id)

        grid = game['grid_b']
        expected = "0300222200" \
                   "X300000000" \
                   "0310000000" \
                   "0010005000" \
                   "0010005000" \
                   "0010044400" \
                   "0010000000" \
                   "0000000000" \
                   "0000000000" \
                   "0000000000"
        self.assertEqual(expected, grid, "invalid grid")

    def test_shot_player_b_hit(self):
        """
        This test passes when the shot results in a hit.
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        game = {
            'username': 'kees',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        # assume being player a
        shot = {
            "row": "1",
            "col": "2"
        }
        response = self.shot(game_id, 'jan', shot)

        # assume being player b
        shot = {
            "row": "3",
            "col": "2"
        }
        response = self.shot(game_id, 'kees', shot)

        status = response.get('status')
        result = response.get('result')
        self.assertIsNotNone(status, 'no status')
        self.assertIsNotNone(result, 'no result')
        self.assertEqual('hit', result, 'invalid result')

        ds = utils.load_json('battleship-ds.json')
        connector = ConnectorFactory.create_connector(ds)

        game_repository = GameRepository(connector)
        game = game_repository.find_by(uuid=game_id)

        grid = game['grid_a']
        expected = "0300222200" \
                   "0300000000" \
                   "0X10000000" \
                   "0010005000" \
                   "0010005000" \
                   "0010044400" \
                   "0010000000" \
                   "0000000000" \
                   "0000000000" \
                   "0000000000"
        self.assertEqual(expected, grid, "invalid grid")

    def test_shot_player_b_invalid_turn(self):
        """
        This test passes when a invalid turn is detected
        :return:
        """

        game = {
            'username': 'jan',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        game = {
            'username': 'kees',
            'grid': '0300222200030000000003100000000010005000001000500000100444000010000000000000000000000000000000000000'
        }
        game_id = self.game(game)

        # assume being player b
        shot = {
            "row": "1",
            "col": "2"
        }
        response = self.shot(game_id, 'kees', shot)
        status = response.get('status')
        self.assertEqual('not your turn', status)


if __name__ == '__main__':
    unittest.main()
