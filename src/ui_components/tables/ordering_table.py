from .base_table import BaseTable


class OrderingTable(BaseTable):
    def __init__(self, data=None, headers=None, fields=None, spacing_x=100, spacing_y=50, font=None, color=None, order_func=None):
        super().__init__(data, headers, fields, spacing_x, spacing_y, font, color)
        self.data.sort(key=order_func)
        self.data = self.data[::-1]
