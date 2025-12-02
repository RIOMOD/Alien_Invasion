# bullet.py
import pygame
from pygame.sprite import Sprite
import math


class Bullet(Sprite):
    """Lớp quản lý đạn được bắn từ tàu với nhiều loại đạn khác nhau."""

    def __init__(self, ai_game, skin=None, dx=0, bullet_type='normal'):
        """Tạo một đối tượng đạn tại vị trí hiện tại của tàu."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.color = self.settings.bullet_color
        
        # Lấy thống kê tàu để áp dụng damage và bullet_speed
        self.ship_stats = ai_game.ship.get_ship_stats() if hasattr(ai_game.ship, 'get_ship_stats') else {}
        self.damage = self.ship_stats.get('damage', 1.0)
        self.bullet_speed_multiplier = self.ship_stats.get('bullet_speed', 1.0)
        
        # Bullet type and behavior
        self.bullet_type = bullet_type
        self.lifetime = 0  # For animations
        
        # Lưu vị trí ban đầu
        self.x = float(ai_game.ship.rect.centerx)
        self.y = float(ai_game.ship.rect.top)
        self.dx = dx
        
        # Setup visual based on bullet type
        self._setup_bullet_visual()

    def _setup_bullet_visual(self):
        """Thiết lập hình ảnh/hình dạng đạn dựa trên loại."""
        if self.bullet_type == 'normal':
            self._setup_normal_bullet()
        elif self.bullet_type == 'circle':
            self._setup_circle_bullet()
        elif self.bullet_type == 'triangle':
            self._setup_triangle_bullet()
        elif self.bullet_type == 'square':
            self._setup_square_bullet()
        elif self.bullet_type == 'laser':
            self._setup_laser_bullet()
        elif self.bullet_type == 'missile':
            self._setup_missile_bullet()
        elif self.bullet_type == 'spiral':
            self._setup_spiral_bullet()

    def _setup_normal_bullet(self):
        """Đạn thường - hình chữ nhật xanh dương."""
        self.rect = pygame.Rect(0, 0, 8, 32)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (0, 200, 255)
        self.width = 8
        self.height = 32

    def _setup_circle_bullet(self):
        """Đạn hình tròn - bay vòng tròn."""
        self.radius = 6
        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (0, 255, 100)
        self.center_y = self.y
        self.orbit_radius = 30
        self.orbit_angle = 0
        self.rotation = 0
        self.rotation_speed = 3

    def _setup_triangle_bullet(self):
        """Đạn hình tam giác."""
        self.size = 10
        self.rect = pygame.Rect(0, 0, self.size*2, self.size*2)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (255, 100, 0)
        self.rotation = 0
        self.rotation_speed = 5

    def _setup_square_bullet(self):
        """Đạn hình vuông."""
        self.size = 12
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (255, 50, 200)
        self.rotation = 0
        self.rotation_speed = 4

    def _setup_laser_bullet(self):
        """Đạn tia laser - nhanh, sáng, có lửa."""
        self.rect = pygame.Rect(0, 0, 4, 40)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (0, 255, 255)
        self.trail_points = []
        self.max_trail_length = 8
        self.glow_intensity = 255

    def _setup_missile_bullet(self):
        """Đạn tên lửa - to hơn, bay chậm hơn, nổ khi chạm."""
        self.rect = pygame.Rect(0, 0, 16, 24)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (255, 150, 0)
        self.smoke_trail = []
        self.max_smoke_length = 15
        self.rotation = 0
        self.is_exploding = False
        self.explosion_timer = 0
        self.explosion_duration = 10
        self.explosion_radius = 0

    def _setup_spiral_bullet(self):
        """Đạn bay theo hình xoáy."""
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.center = (int(self.x), int(self.y))
        self.color = (150, 100, 255)
        self.spiral_angle = 0
        self.spiral_speed = 0.3
        self.spiral_radius = 20
        self.center_x = self.x
        self.rotation = 0

    def update(self):
        """Di chuyển và cập nhật đạn theo loại của nó."""
        bullet_speed = self.settings.bullet_speed * self.bullet_speed_multiplier
        
        if self.bullet_type == 'normal':
            self._update_normal()
        elif self.bullet_type == 'circle':
            self._update_circle(bullet_speed)
        elif self.bullet_type == 'triangle':
            self._update_triangle(bullet_speed)
        elif self.bullet_type == 'square':
            self._update_square(bullet_speed)
        elif self.bullet_type == 'laser':
            self._update_laser(bullet_speed)
        elif self.bullet_type == 'missile':
            self._update_missile(bullet_speed)
        elif self.bullet_type == 'spiral':
            self._update_spiral(bullet_speed)
        
        self.lifetime += 1

    def _update_normal(self):
        """Cập nhật đạn thường - bay thẳng lên."""
        bullet_speed = self.settings.bullet_speed * self.bullet_speed_multiplier
        self.y -= bullet_speed
        self.rect.centery = int(self.y)
        self.rect.centerx = int(self.x) + self.dx

    def _update_circle(self, bullet_speed):
        """Cập nhật đạn tròn - bay vòng tròn."""
        self.y -= bullet_speed * 0.6
        self.orbit_angle += 0.15
        
        # Vị trí orbit
        orbit_x = math.cos(self.orbit_angle) * self.orbit_radius
        self.x += orbit_x * 0.05
        
        self.rect.center = (int(self.x), int(self.y))
        self.rotation = (self.rotation + self.rotation_speed) % 360

    def _update_triangle(self, bullet_speed):
        """Cập nhật đạn tam giác."""
        self.y -= bullet_speed * 0.8
        self.rect.centery = int(self.y)
        self.rect.centerx = int(self.x) + self.dx
        self.rotation = (self.rotation + self.rotation_speed) % 360

    def _update_square(self, bullet_speed):
        """Cập nhật đạn vuông."""
        self.y -= bullet_speed * 0.7
        self.x += self.dx * 0.5
        self.rect.center = (int(self.x), int(self.y))
        self.rotation = (self.rotation + self.rotation_speed) % 360

    def _update_laser(self, bullet_speed):
        """Cập nhật tia laser - bay nhanh với trail."""
        self.y -= bullet_speed * 1.5
        self.rect.center = (int(self.x), int(self.y))
        
        # Trail effect
        self.trail_points.append((int(self.x), int(self.y)))
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)
        
        # Glow effect giảm dần
        self.glow_intensity = max(100, self.glow_intensity - 5)

    def _update_missile(self, bullet_speed):
        """Cập nhật tên lửa - bay chậm hơn, có khí thải."""
        self.y -= bullet_speed * 0.5
        self.rect.centery = int(self.y)
        self.rect.centerx = int(self.x) + self.dx
        
        # Smoke trail
        self.smoke_trail.append({
            'x': int(self.x),
            'y': int(self.y),
            'alpha': 200,
            'size': 8
        })
        if len(self.smoke_trail) > self.max_smoke_length:
            self.smoke_trail.pop(0)
        
        # Update smoke
        for smoke in self.smoke_trail:
            smoke['alpha'] -= 15
            smoke['size'] -= 0.3

    def _update_spiral(self, bullet_speed):
        """Cập nhật đạn xoáy - bay lên theo hình xoáy."""
        self.y -= bullet_speed * 0.9
        self.spiral_angle += self.spiral_speed
        
        # Hình xoáy
        offset_x = math.cos(self.spiral_angle) * self.spiral_radius
        self.x = self.center_x + offset_x
        
        self.rect.center = (int(self.x), int(self.y))
        self.rotation = (self.rotation + 8) % 360

    def draw_bullet(self):
        """Vẽ đạn lên màn hình."""
        if self.bullet_type == 'normal':
            self._draw_normal()
        elif self.bullet_type == 'circle':
            self._draw_circle()
        elif self.bullet_type == 'triangle':
            self._draw_triangle()
        elif self.bullet_type == 'square':
            self._draw_square()
        elif self.bullet_type == 'laser':
            self._draw_laser()
        elif self.bullet_type == 'missile':
            self._draw_missile()
        elif self.bullet_type == 'spiral':
            self._draw_spiral()

    def _draw_normal(self):
        """Vẽ đạn thường."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def _draw_circle(self):
        """Vẽ đạn tròn."""
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)
        # Inner glow
        pygame.draw.circle(self.screen, (100, 255, 150), self.rect.center, self.radius//2)

    def _draw_triangle(self):
        """Vẽ đạn tam giác."""
        size = self.size
        angle_rad = math.radians(self.rotation)
        
        # Tính điểm tam giác
        points = []
        for i in range(3):
            angle = angle_rad + (i * 2 * math.pi / 3)
            x = self.rect.centerx + size * math.cos(angle)
            y = self.rect.centery + size * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(self.screen, self.color, points)
        # Border
        pygame.draw.polygon(self.screen, (255, 200, 0), points, 2)

    def _draw_square(self):
        """Vẽ đạn vuông."""
        angle_rad = math.radians(self.rotation)
        
        # Tính điểm vuông xoay
        size = self.size
        points = []
        for i in range(4):
            angle = angle_rad + (i * math.pi / 2)
            x = self.rect.centerx + size * math.cos(angle)
            y = self.rect.centery + size * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(self.screen, self.color, points)
        # Border
        pygame.draw.polygon(self.screen, (255, 255, 0), points, 2)

    def _draw_laser(self):
        """Vẽ tia laser với trail."""
        # Draw trail
        if len(self.trail_points) > 1:
            for i in range(len(self.trail_points) - 1):
                alpha = int(200 * (i / len(self.trail_points)))
                g_component = min(200 + alpha//2, 255)  # Clamp to max 255
                color = (0, g_component, 255)
                pygame.draw.line(self.screen, color, 
                               self.trail_points[i], self.trail_points[i + 1], 3)
        
        # Draw main laser beam
        glow_color = (0, 255, 255)
        pygame.draw.rect(self.screen, glow_color, self.rect)
        # Glow effect
        pygame.draw.circle(self.screen, (100, 255, 255), self.rect.center, 6)

    def _draw_missile(self):
        """Vẽ tên lửa với khí thải."""
        # Draw smoke trail first (behind)
        for smoke in self.smoke_trail:
            if smoke['alpha'] > 0:
                smoke_surface = pygame.Surface((int(smoke['size']*2), int(smoke['size']*2)))
                smoke_surface.set_alpha(int(smoke['alpha']))
                smoke_surface.fill((150, 150, 150))
                self.screen.blit(smoke_surface, 
                               (smoke['x'] - int(smoke['size']), 
                                smoke['y'] - int(smoke['size'])))
        
        # Draw missile
        pygame.draw.rect(self.screen, self.color, self.rect)
        # Nose cone
        nose_points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left + 2, self.rect.centery),
            (self.rect.right - 2, self.rect.centery)
        ]
        pygame.draw.polygon(self.screen, (255, 200, 0), nose_points)
        # Fire at back
        pygame.draw.polygon(self.screen, (255, 100, 0), 
                          [(self.rect.centerx, self.rect.bottom + 5),
                           (self.rect.left, self.rect.bottom),
                           (self.rect.right, self.rect.bottom)])

    def _draw_spiral(self):
        """Vẽ đạn xoáy."""
        pygame.draw.circle(self.screen, self.color, self.rect.center, 5)
        # Outer glow
        pygame.draw.circle(self.screen, (200, 150, 255), self.rect.center, 8, 1)
        
        # Draw spiral trail lines
        for i in range(1, 4):
            trail_x = self.center_x + math.cos(self.spiral_angle - i*0.5) * self.spiral_radius
            trail_y = self.y + i * 15
            pygame.draw.circle(self.screen, (150, 100, 255), (int(trail_x), int(trail_y)), 3, 1)

