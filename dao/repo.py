'''
    created on 04 January 2020
    
    @author: Gergely
'''
import psycopg2
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DbConnectionHelper:
    def __init__(self, db_name, user='postgres', password='postgres', host='localhost'):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host

    def to_psycopg2(self):
        return f"dbname='{self.db_name}' user='{self.user}' password='{self.password}' host='{self.host}'"


class DbOperation:
    def __init__(self, connection_params: DbConnectionHelper, table_name, key, params=None):
        self.table_name = table_name
        self.connection_params = connection_params
        self.params = params
        self.is_select = False
        self.key = key

    def _build_sql(self):
        raise NotImplementedError

    def get_resource_id(self):
        return f"""{self.connection_params.db_name}${self.table_name}{'$' + str(
            self.key) if self.key is not None else ''}"""

    def execute(self):
        connection = psycopg2.connect(self.connection_params.to_psycopg2())
        cursor = connection.cursor()
        cursor_params = self._build_sql()
        logger.info(f'Executing {cursor_params}')
        cursor.execute(*cursor_params)
        if self.is_select:
            return cursor.fetchall()
        else:
            connection.commit()


class InsertOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, key=None, params=None,
                 is_explicit=True):
        super().__init__(connection_params, table_name, key, params)
        assert params is not None
        self.is_explicit = is_explicit

    def _build_sql(self):
        column_names = '(' + ', '.join(['id'] + list(self.params.keys())) + ')'
        column_vals = '(' + '%s,' * (len(self.params)) + '%s)'
        sql = f"INSERT INTO {self.table_name} {column_names if self.is_explicit else ''} VALUES {column_vals}"
        return sql, tuple(([self.key] + list(self.params.values())))


class UpdateOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, key, params):
        super().__init__(connection_params, table_name, key, params)

    def _build_sql(self):
        assert len(self.params) >= 1
        params = tuple(self.params.keys())
        column_names = ', '.join(map(lambda x: x + ' = %s', params))
        where_params = 'id = %s'
        sql = f'UPDATE {self.table_name} SET {column_names} WHERE {where_params}'
        return sql, tuple(list(self.params.values()) + [self.key])


class SelectOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, key=None, params=None):
        super().__init__(connection_params, table_name, params)
        self.is_select = True
        self.key = key

    def _build_sql(self):
        column_names = 'AND '.join(map(lambda x: x + ' = %s ', tuple(self.params.keys()))) if self.params else None
        sql = f'SELECT * FROM {self.table_name}'
        if self.key:
            sql += f' WHERE id = %s '
            if column_names:
                sql += column_names
        args = (self.key,) if not self.params else tuple([self.key] + list(self.params.values()))
        return sql, args


class DeleteOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, key=None, params=None):
        super().__init__(connection_params, table_name, key, params)

    def _build_sql(self):
        sql = f'DELETE FROM {self.table_name}'
        if self.key:
            sql += f" WHERE id = %s"
        return sql, (self.key,)


'''
connection = DbConnectionHelper('MovieRental')
print('     initial', SelectOperation(connection, 'client').execute())

update_operation = UpdateOperation(connection, 'client', key=12, params={'email': 'ahoy@mail'})
update_operation.execute()
print('after update', SelectOperation(connection, 'client').execute())

insert_operation = InsertOperation(connection, 'client', key=12,
                                   params={'name': 'once again', 'email': 'hot@mail', 'age': 22})
print(insert_operation._build_sql())
insert_operation.execute()
print('after insert', SelectOperation(connection, 'client').execute())

delete_operation = DeleteOperation(connection, 'client', key=12)
delete_operation.execute()
print('after delete', SelectOperation(connection, 'client').execute())
connection = DbConnectionHelper('MovieRental')
print(SelectOperation(connection, 'client').get_resource_id())
'''
