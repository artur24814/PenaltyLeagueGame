from src.models.orm_models import Model


class TestModel(Model):
    __test__ = False

    def __init__(self, name, second, last):
        super().__init__()
        self.name = name
        self.second = second
        self.last = last
