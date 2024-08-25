import os

from .abstract import GameSprite
from src.settings import BASE_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class GoalKeeper(GameSprite):
    def __init__(self,
                 start_pos=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50),
                 image_path=['assets', 'img', 'goalkeeper', '1'],
                 start_size=(350, 280)):
        super().__init__(start_pos, image_path, start_size)
        self.animation = True
        self.current_sequence = 1

    def _get_rect(self):
        return self.image.get_rect(center=self.current_position)

    def update(self):
        self.update_position()
        if self.animation:
            self.image_index += self.animation_speed

            if self.image_index >= len(self.sprite_images):
                self.end_animate_sequence()

            self.image = self.sprite_images[int(self.image_index)]
            self.size = self.size[0] - self.zoom_step,  self.size[1] - self.zoom_step
            self.image = self._transform_scale(int(self.size[0]), self.size[1])

    def end_animate_sequence(self):
        self.image_index = len(self.sprite_images) - 1

    def set_image_sequences(self, sequence):
        if sequence != self.current_sequence:
            self.current_sequence = sequence
            self.image_dir = os.path.join(BASE_DIR, *['assets', 'img', 'goalkeeper', str(sequence)])
            self.sprite_images = self.get_sprite_images(self.image_dir)
            self.image_index = 0
            self.image = self.sprite_images[self.image_index]
            self.image = self._transform_scale(*self.size)
