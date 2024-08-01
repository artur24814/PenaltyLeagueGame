from src.models.orm_models import Model


class TestModel(Model):
    __test__ = False
    db_fields_to_lookup = ['_id', 'name', 'second', 'last']

    def __init__(self, name, second, last):
        super().__init__()
        self.name = name
        self.second = second
        self.last = last
