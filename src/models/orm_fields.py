class BaseField:
    def __init__(self, name=None, null=True, primary=False):
        self.name = name
        self.null = null
        self.primary = primary

    def get_sql(self):
        sql = self.get_basic_sql()
        if not self.null:
            sql += ' NOT NULL'
            if self.primary:
                sql += f'\nPRIMARY KEY ({self.name})'
        return sql

    def get_basic_sql(self) -> str:
        ...


class IntergerField(BaseField):
    def get_basic_sql(self):
        return f'{self.name} INTEGER'


class TextField(BaseField):
    def get_basic_sql(self):
        return f'{self.name} TEXT'


class RealField(BaseField):
    def get_basic_sql(self):
        return f'{self.name} REAL'
