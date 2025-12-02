import pygame
import os
from pygame.sprite import Sprite


class Alien(Sprite):
    """Lớp đại diện cho một alien duy nhất trong hạm đội."""

    def __init__(self, ai_game, skin=None, boss=False):
        """Khởi tạo alien và đặt vị trí ban đầu."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Boss alien
        self.boss = boss
        if boss:
            # Boss có kích thước lớn hơn và màu đặc biệt
            self.image = pygame.Surface((120, 120))
            self.image.fill((255, 100, 0))
        else:
            # Alien thường: kích thước theo loại
            alien_sizes = [(40, 40), (60, 60), (80, 80), (100, 100)]
            idx = 0
            if skin:
                for i, s in enumerate(["alien1", "alien2", "alien3", "alien4"]):
                    if s in skin:
                        idx = i
                        break
            size = alien_sizes[idx]
            def try_load_and_scale(path):
                img = pygame.image.load(path)
                return pygame.transform.scale(img, size)

            def try_load_skin(base):
                for ext in [".png", ".jpg", ".bmp"]:
                    fname = base + ext
                    if os.path.exists(fname):
                        try:
                            return try_load_and_scale(fname)
                        except:
                            continue
                return None

            img = None
            if skin:
                base, ext = os.path.splitext(skin)
                img = try_load_skin(base)
            if img is None:
                for base in ["images/alien1", "images/alien2", "images/alien3", "images/alien4", "images/alien"]:
                    img = try_load_skin(base)
                    if img is not None:
                        break
            if img is not None:
                self.image = img
            else:
                self.image = pygame.Surface(size)
                self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        # Bắt đầu mỗi alien mới ở gần góc trên bên trái màn hình.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Lưu trữ vị trí ngang chính xác của alien.
        self.x = float(self.rect.x)

    def update(self):
        """Di chuyển alien sang phải hoặc trái."""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Trả về True nếu alien chạm mép màn hình."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
