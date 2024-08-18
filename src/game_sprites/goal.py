from src.ui_components.colors import TRANSPARENT_GREEN
from src.settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Goal:
    def __init__(self, width=420, height=150):
        self.width = width
        self.height = height
        self.pos_x = (WINDOW_WIDTH - self.width) // 2
        self.pos_y = ((WINDOW_HEIGHT - self.height) // 2) + 20

    def draw_goal_zones(self, pygame, screen, selected_zone):
        zone_width = self.width // 3
        zone_height = self.height // 3
        for i in range(9):
            col = i % 3
            row = i // 3
            zone_rect = pygame.Rect(self.pos_x + col * zone_width, self.pos_y + row * zone_height, zone_width, zone_height)
            if selected_zone == i:
                pygame.draw.rect(screen, TRANSPARENT_GREEN, zone_rect)

    def get_zone_for_point(self, point):
        if self.pos_x <= point[0] <= self.pos_x + self.width and self.pos_y <= point[1] <= self.pos_y + self.height:
            col = (point[0] - self.pos_x) // (self.width // 3)
            row = (point[1] - self.pos_y) // (self.height // 3)
            return int(row * 3 + col)

        return None

    def get_target_position_for_zone(self, zone):
        zone_width = self.width // 3
        zone_height = self.height // 3
        col = zone % 3
        row = zone // 3
        return (self.pos_x + col * zone_width + zone_width // 2, self.pos_y + row * zone_height + zone_height // 2)
