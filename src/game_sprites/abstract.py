import pygame
import os

from src.settings import BASE_DIR


class GameSprite(pygame.sprite.Sprite):
    animation_speed = 0.15
    zoom_step = 0
    speed = 0

    def __init__(self, start_pos, image_path, start_size):
        super().__init__()
        self.start_pos = start_pos
        self.current_position = self.start_pos
        self.moving = False
        self.animation = False
        self.speed = 4
        self.image_dir = os.path.join(BASE_DIR, *image_path)
        self.images_path_list = sorted(os.listdir(self.image_dir), key=lambda image_p: int(image_p.split('.')[0]))
        self.sprite_images = [pygame.image.load(os.path.join(self.image_dir, image)).convert_alpha() for image in self.images_path_list]
        self.image_index = 0
        self.image = self.sprite_images[self.image_index]
        self.start_size = start_size
        self.size = self.start_size
        self.image = self._transform_scale(*self.size)
        self.rect = self._get_rect()

    def _transform_scale(self, x, y):
        return pygame.transform.scale(self.image, (x, y))

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

    def update_position(self):
        pass

    def end_animate_sequence(self):
        self.image_index = 0
