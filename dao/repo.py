'''
    created on 04 January 2020
    
    @author: Gergely
'''
import psycopg2


class DbConnectionHelper:
    def __init__(self, db_name, user='postgres', password='postgres', host='localhost'):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host

    def to_psycopg2(self):
        return f"dbname='{self.db_name}' user='{self.user}' password='{self.password}' host='{self.host}'"


class DbOperation:
    def __init__(self, connection_params: DbConnectionHelper, table_name, params):
        self.table_name = table_name
        self.connection_params = connection_params
        self.params = params
        self.is_select = False

    def _build_sql(self):
        raise NotImplementedError

    def execute(self):
        connection = psycopg2.connect(self.connection_params.to_psycopg2())
        cursor = connection.cursor()
        cursor_params = self._build_sql()

        cursor.execute(*cursor_params)
        if self.is_select:
            return cursor.fetchall()
        else:
            connection.commit()


class InsertOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, **params):
        super().__init__(connection_params, table_name, params)

    def _build_sql(self):
        column_names = '(' + ', '.join(self.params.keys()) + ')'
        column_vals = '(' + '%s,' * (len(self.params) - 1) + '%s)'
        sql = f"INSERT INTO {self.table_name} {column_names} VALUES {column_vals}"
        return sql, tuple(self.params.values())


class UpdateOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, **params):
        super().__init__(connection_params, table_name, params)

    def _build_sql(self):
        assert len(self.params) > 1
        params = tuple(self.params.keys())
        column_names = ', '.join(map(lambda x: x + ' = %s', params[:-1]))
        where_params = params[-1] + ' = %s'
        sql = f'UPDATE {self.table_name} SET {column_names} WHERE {where_params}'
        return sql, tuple(self.params.values())


class SelectOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, **params):
        super().__init__(connection_params, table_name, params)
        self.is_select = True

    def _build_sql(self):
        column_names = 'AND '.join(map(lambda x: x + ' = %s ', tuple(self.params.keys())))
        sql = f'SELECT * FROM {self.table_name}'
        if column_names:
            sql += f' WHERE {column_names}'
        return sql, tuple(self.params.values())


class DeleteOperation(DbOperation):
    def __init__(self, connection_params: DbConnectionHelper, table_name, **params):
        super().__init__(connection_params, table_name, params)

    def _build_sql(self):
        assert len(self.params) > 0
        column_names = 'AND '.join(map(lambda x: x + ' = %s ', tuple(self.params.keys())))
        sql = f'DELETE FROM {self.table_name} WHERE {column_names}'
        return sql, tuple(self.params.values())


i = InsertOperation(DbConnectionHelper('MovieRental'), 'client', name='custom', email='custom@gmail.com', age=12,
                    id=12)
i.execute()
j = DeleteOperation(DbConnectionHelper('MovieRental'), 'client', id=12)

print(j.execute())
