from .abstract import GameSprite


class Kicker(GameSprite):
    animation_speed = 0.3
    start_size = (370, 370)

    def _get_rect(self):
        return self.image.get_rect(bottomleft=self.current_position)

    def end_animate_sequence(self):
        super().end_animate_sequence()
        self.animation = False
