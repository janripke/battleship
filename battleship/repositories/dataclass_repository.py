from uuid import uuid4
from paprika_connector.connectors.repository import Repository
from paprika_connector.system.formatters import set_formatter, values_formatter


def where_formatter(dict_):
    columns = []
    if dict_:
        keys = dict_.keys()
        for key in keys:
            if dict_[key] is None:
                columns.append(f'{key} is null')
            if dict_[key]:
                columns.append(f'{key}=:{key}')
        columns = " and ".join(columns)
        return f'where {columns}'
    return ''


class DataclassRepository(Repository):

    def __init__(self, connector, table_name):
        Repository.__init__(self, connector)
        self.__table_name = table_name

    def get_table_name(self):
        return self.__table_name

    def find_by_uuid(self, uuid_):
        # with self.get_connection() as cursor:
        table_name = self.get_table_name()

        statement = f'select * from {table_name} where uuid=:uuid and active=1'
        params = {
            'uuid': uuid_
        }
        return self._find(statement, params)

    def find_by(self, **kwargs):
        # with self.get_connection() as cursor:
        table_name = self.get_table_name()

        order_by = kwargs.get('order_by', '')
        if order_by:
            kwargs.pop('order_by')
            order_by = f"order by {order_by}"

        statement = f'select * from {table_name} {where_formatter(kwargs)} {order_by}'
        return self._find(statement, kwargs)

    def list(self):
        table_name = self.get_table_name()
        statement = f'select * from {table_name} where active=1'

        params = {}
        return self._list(statement, params)

    def list_by(self, **kwargs):
        table_name = self.get_table_name()

        order_by = kwargs.get('order_by', '')
        if order_by:
            kwargs.pop('order_by')
            order_by = f"order by {order_by}"

        statement = f'select * from {table_name} {where_formatter(kwargs)} {order_by}'
        return self._list(statement, kwargs)

    def insert(self, data_object):
        table_name = self.get_table_name()

        uuid_ = data_object.get('uuid', str(uuid4()))
        data_object['uuid'] = uuid_

        statement = f'insert into {table_name} {values_formatter(data_object, ignore_none=False)} returning id'
        return self._insert(statement, data_object)

    def update(self, data_object, where=None):
        table_name = self.get_table_name()

        if not where:
            where = {
                'uuid': data_object['uuid']
            }

        excludes = ['id', 'uuid']
        statement = f'update {table_name} set {set_formatter(data_object, excludes)} {where_formatter(where)}'

        if where:
            keys = where.keys()
            for key in keys:
                data_object[key] = where[key]

        self._delete(statement, data_object)

    def delete(self, **kwargs):
        table_name = self.get_table_name()

        statement = f'delete from {table_name} {where_formatter(kwargs)}'
        self._delete(statement, kwargs)
