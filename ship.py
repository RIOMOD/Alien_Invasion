import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Lớp đại diện cho tàu của người chơi với các kỹ năng khác nhau."""

    # Ship stats: (name, damage, bullet_speed, fire_rate, energy, special_ability)
    SHIP_STATS = {
        0: {'name': 'Alpha', 'damage': 1.0, 'bullet_speed': 1.0, 'fire_rate': 1.0, 'energy': 1.0, 'ability': 'balanced'},
        1: {'name': 'Beta', 'damage': 1.5, 'bullet_speed': 0.8, 'fire_rate': 0.8, 'energy': 1.2, 'ability': 'heavy_fire'},
        2: {'name': 'Gamma', 'damage': 0.7, 'bullet_speed': 1.4, 'fire_rate': 1.3, 'energy': 0.8, 'ability': 'rapid_fire'},
        3: {'name': 'Delta', 'damage': 1.0, 'bullet_speed': 1.0, 'fire_rate': 1.0, 'energy': 1.5, 'ability': 'tanky'},
    }

    def __init__(self, ai_game, skin=None):
        """Khởi tạo tàu và đặt nó ở vị trí ban đầu. Có thể truyền vào skin (đường dẫn ảnh)."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        import os
        image_loaded = False
        
        # Xác định index tàu từ skin
        self.ship_index = 0
        if skin:
            for i, s in enumerate(["ship1", "ship2", "ship3", "ship4"]):
                if s in skin:
                    self.ship_index = i
                    break
        
        # Lấy thống kê tàu
        self.stats = self.SHIP_STATS.get(self.ship_index, self.SHIP_STATS[0])
        
        # Kích thước tàu khác nhau theo loại
        ship_sizes = [(40, 32), (60, 48), (80, 64), (100, 80)]
        size = ship_sizes[self.ship_index]
        
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

        if skin:
            base, ext = os.path.splitext(skin)
            img = try_load_skin(base)
            if img is not None:
                self.image = img
                image_loaded = True
            else:
                image_loaded = False
        if not image_loaded:
            for base in ["images/ship1", "images/ship2", "images/ship3", "images/ship4", "images/ship"]:
                img = try_load_skin(base)
                if img is not None:
                    self.image = img
                    image_loaded = True
                    break
        if not image_loaded:
            self.image = pygame.Surface(size)
            self.image.fill((0, 0, 255))
        
        self.rect = self.image.get_rect()

        # Đặt tàu ở giữa đáy màn hình
        self.rect.midbottom = self.screen_rect.midbottom

        # Lưu giá trị x chính xác cho việc di chuyển
        self.x = float(self.rect.x)

        # Cờ di chuyển
        self.moving_right = False
        self.moving_left = False
        
        # Animation attributes
        self.rotation_angle = 0
        self.rotation_speed = 0
        self.spin_timer = 0
        self.spin_duration = 0
        self.pulse_scale = 1.0
        self.pulse_direction = 1
        self.animation_enabled = True
        self.base_image = self.image.copy()
        
        # Energy system
        self.current_energy = self.stats['energy'] * 100
        self.max_energy = self.stats['energy'] * 100
        self.energy_regen = 0.5 * self.stats['energy']

    def start_spawn_animation(self):
        """Bắt đầu hiệu ứng xoay khi tàu xuất hiện."""
        self.spin_timer = 0
        self.spin_duration = 30  # Frames
        self.rotation_speed = 12  # Độ/frame

    def update(self):
        """Cập nhật vị trí tàu theo các cờ di chuyển và hiệu ứng animation."""
        # Cập nhật vị trí
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = int(self.x)
        
        # Cập nhật animation
        if self.animation_enabled:
            self._update_animations()
        
        # Cập nhật năng lượng (tự phục hồi)
        self.current_energy = min(self.current_energy + self.energy_regen, self.max_energy)

    def _update_animations(self):
        """Cập nhật các hiệu ứng animation của tàu."""
        # Spawn spin animation
        if self.spin_timer < self.spin_duration:
            self.rotation_angle += self.rotation_speed
            self.spin_timer += 1
        else:
            self.rotation_angle = 0
        
        # Pulse effect (tỉ lệ phóng to/nhỏ)
        self.pulse_scale += 0.02 * self.pulse_direction
        if self.pulse_scale >= 1.1:
            self.pulse_direction = -1
        elif self.pulse_scale <= 0.95:
            self.pulse_direction = 1

    def _get_rotated_image(self):
        """Lấy hình ảnh tàu có xoay."""
        if self.rotation_angle == 0:
            return self.base_image
        
        # Xoay hình ảnh
        rotated = pygame.transform.rotate(self.base_image, self.rotation_angle)
        
        # Phóng to/nhỏ theo pulse
        if self.pulse_scale != 1.0:
            new_width = int(rotated.get_width() * self.pulse_scale)
            new_height = int(rotated.get_height() * self.pulse_scale)
            if new_width > 0 and new_height > 0:
                rotated = pygame.transform.scale(rotated, (new_width, new_height))
        
        return rotated

    def blitme(self):
        """Vẽ tàu lên màn hình tại vị trí hiện tại với hiệu ứng animation."""
        if self.animation_enabled:
            rotated_image = self._get_rotated_image()
            # Lấy rect mới để giữ tàu ở trung tâm
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            self.screen.blit(rotated_image, rotated_rect)
        else:
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Đặt tàu vào giữa màn hình (dùng khi bắt đầu lại)."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.current_energy = self.max_energy
        self.start_spawn_animation()
    
    def get_ship_stats(self):
        """Trả về thống kê của tàu."""
        return self.stats


