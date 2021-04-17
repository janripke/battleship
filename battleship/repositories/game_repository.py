from battleship.repositories.dataclass_repository import DataclassRepository


class GameRepository(DataclassRepository):

    def __init__(self, connector):
        DataclassRepository.__init__(self, connector, 'games')

    def open(self, username):
        statement = "select * from games where username_b is null and username_a <> :username_a and active=1"

        params = {
            'username_a': username
        }

        return self._find(statement, params)
