import pygame
from pygame.sprite import Sprite


class PowerUp(Sprite):
    def __init__(self, x, y, ptype, img_path=None):
        super().__init__()
        self.ptype = ptype
        if img_path and img_path != '' and img_path is not None:
            try:
                self.image = pygame.image.load(img_path)
                self.image = pygame.transform.scale(self.image, (40, 40))
            except:
                self.image = pygame.Surface((40, 40))
                self.image.fill((0, 255, 255))
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.y += 3
