from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH
from src.ui_components.colors import BLACK


class Ball:
    def __init__(self):
        self.start_pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200)
        self.ball_position = self.start_pos
        self.target_position = None
        self.moving = False
        self.speed = 10

    def update_position(self):
        if self.target_position:
            ball_x, ball_y = self.ball_position
            target_x, target_y = self.target_position

            dx = target_x - ball_x
            dy = target_y - ball_y
            dist = (dx**2 + dy**2)**0.5

            if dist < self.speed:
                self.ball_position = self.target_position
                self.moving = False
            else:
                self.ball_position = (ball_x + dx / dist * self.speed, ball_y + dy / dist * self.speed)

    def draw(self, pygame, screen):
        pygame.draw.circle(screen, BLACK, self.ball_position, 15)
