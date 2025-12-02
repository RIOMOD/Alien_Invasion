# settings.py
class Settings:
    """Lưu tất cả các cài đặt cho trò chơi Alien Invasion."""

    def __init__(self):
        # Cài đặt màn hình
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Cài đặt cho tàu
        self.ship_speed = 0.9  # Giảm tốc độ mặc định
        self._ship_speed_init = self.ship_speed
        self.ship_limit = 3

        # Cài đặt cho đạn (Bullet)
        self.bullet_speed = 3.0
        self._bullet_speed_init = self.bullet_speed
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # Màu xám đậm
        self.bullets_allowed = 3

        # Cài đặt cho hạm đội Alien
        self.alien_speed = 0.5  # Giảm tốc độ alien
        self._alien_speed_init = self.alien_speed

        # note: reset_speed defined as a proper method below
        self.fleet_drop_speed = 6  # Giảm tốc độ rơi
        # fleet_direction = 1 means right; -1 means left
        self.fleet_direction = 1

        # Tốc độ tăng dần khi chơi (dùng khi muốn mở rộng)
        self.speedup_scale = 1.08  # Tăng nhẹ qua mỗi màn

        # Cấu hình phím điều khiển
        self.key_right = 'right'
        self.key_left = 'left'
        self.key_fire = 'space'
        self.key_quit = 'q'
        # game audio and UI
        self.volume = 0.8  # default master volume (0.0 - 1.0)
        self.language = 'en'  # default language: 'vi' or 'en'
        self._load_control_config()
        self._load_game_config()

    def _load_game_config(self):
        import os
        if os.path.exists('game_config.txt'):
            try:
                with open('game_config.txt', 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or ':' not in line:
                            continue
                        k, v = line.split(':', 1)
                        k = k.strip()
                        v = v.strip()
                        if k == 'volume':
                            try:
                                self.volume = max(0.0, min(1.0, float(v)))
                            except:
                                pass
                        elif k == 'language':
                            if v in ('vi', 'en'):
                                self.language = v
            except:
                pass

    def save_game_config(self):
        try:
            with open('game_config.txt', 'w') as f:
                f.write(f"volume: {self.volume}\n")
                f.write(f"language: {self.language}\n")
        except:
            pass

    def _load_control_config(self):
        import os
        if os.path.exists('control_config.txt'):
            try:
                with open('control_config.txt', 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and ':' in line:
                            k, v = line.split(':', 1)
                            k = k.strip()
                            v = v.strip()
                            if k == 'key_right':
                                self.key_right = v
                            elif k == 'key_left':
                                self.key_left = v
                            elif k == 'key_fire':
                                self.key_fire = v
                            elif k == 'key_quit':
                                self.key_quit = v
            except:
                pass

    def save_control_config(self):
        try:
            with open('control_config.txt', 'w') as f:
                f.write(f"key_right: {self.key_right}\n")
                f.write(f"key_left: {self.key_left}\n")
                f.write(f"key_fire: {self.key_fire}\n")
                f.write(f"key_quit: {self.key_quit}\n")
        except:
            pass

    def increase_speed(self):
        """Tăng tốc độ game khi cần (ví dụ khi sang level mới)."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

    def reset_speed(self):
        """Đặt lại tốc độ về giá trị gốc khi bắt đầu game mới."""
        self.ship_speed = self._ship_speed_init
        self.bullet_speed = self._bullet_speed_init
        self.alien_speed = self._alien_speed_init
