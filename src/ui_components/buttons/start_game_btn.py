from .base_button import BaseBtn


class StartGameBtn(BaseBtn):
    def click(self, func):
        super().click(func)
        print('Click.....')
