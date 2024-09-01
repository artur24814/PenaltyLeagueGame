from .abstract import GameSprite


class Ball(GameSprite):
    animation_speed = 0.2
    zoom_step = 0.3
    speed = 8

    def __init__(self, start_pos, image_path, start_size=(40, 40)):
        super().__init__(start_pos, image_path, start_size)
        self.target_position = None
        self.current_time = 0

    def update_position(self):
        if self.target_position:
            ball_x, ball_y = self.rect.center
            target_x, target_y = self.target_position

            dx = target_x - ball_x
            dy = target_y - ball_y
            dist = (dx**2 + dy**2)**0.45

            if dist < self.speed:
                self.rect.center = self.target_position
                self.moving = False
                self.animation = False
                self.current_time = 0
            else:
                self.rect.center = (ball_x + dx / dist * self.speed, ball_y + dy / dist * self.speed)
                self.current_time += self.animation_speed
