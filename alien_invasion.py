# alien_invasion.py
import pygame
import sys
import os
from ship import Ship
from bullet import Bullet
from alien import Alien
from settings import Settings
from powerup import PowerUp
from localization import Translator


class AlienInvasion:
    def _draw_control_menu(self):
        """Vẽ menu tùy chỉnh điều khiển với hỗ trợ đa ngôn ngữ."""
        self.screen.fill((240, 240, 255))
        
        # Title
        title_text = self.translator('control_settings')
        title = self.font_big.render(title_text, True, (0, 100, 200))
        rect = title.get_rect(center=(self.settings.screen_width//2, 80))
        self.screen.blit(title, rect)
        
        # Key labels in current language
        key_labels = {
            'key_right': self.translator('right_key'),
            'key_left': self.translator('left_key'),
            'key_fire': self.translator('fire_key'),
            'key_quit': self.translator('quit_key')
        }
        
        y0 = 200
        for i, (k, v) in enumerate(self.control_keys.items()):
            label_text = key_labels.get(k, k)
            txt = self.font.render(f"{label_text} {v}", True, (0, 0, 0))
            self.screen.blit(txt, (200, y0 + i*60))
        
        # Instruction
        instruct_text = self.translator('press_key')
        instruct = self.font.render(instruct_text + " ESC: " + self.translator('back'), True, (100, 100, 255))
        self.screen.blit(instruct, (200, y0 + 300))

    def _handle_control_menu_event(self, event):
        if event.key == pygame.K_ESCAPE:
            # Lưu cấu hình và thoát về menu
            self.settings.key_right = self.control_keys['key_right']
            self.settings.key_left = self.control_keys['key_left']
            self.settings.key_fire = self.control_keys['key_fire']
            self.settings.key_quit = self.control_keys['key_quit']
            self.settings.save_control_config()
            self.state = 'menu'
        else:
            # Đổi phím điều khiển
            key_names = ['key_right', 'key_left', 'key_fire', 'key_quit']
            for k in key_names:
                if event.mod & pygame.KMOD_SHIFT:
                    # Nếu giữ SHIFT, đổi key_quit
                    self.control_keys['key_quit'] = pygame.key.name(
                        event.key).upper()
                    break
                elif event.mod & pygame.KMOD_CTRL:
                    # Nếu giữ CTRL, đổi key_fire
                    self.control_keys['key_fire'] = pygame.key.name(
                        event.key).upper()
                    break
                elif event.mod & pygame.KMOD_ALT:
                    # Nếu giữ ALT, đổi key_left
                    self.control_keys['key_left'] = pygame.key.name(
                        event.key).upper()
                    break
                else:
                    # Mặc định đổi key_right
                    self.control_keys['key_right'] = pygame.key.name(
                        event.key).upper()
                    break
    # ...existing code...

    def __init__(self):
        self.settings = Settings()
        # Initialize translator with current language setting
        self.translator = Translator(self.settings.language)
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Skin options
        self.ship_skins = ["images/ship1.png", "images/ship2.png",
                           "images/ship3.png", "images/ship4.png"]
        self.alien_skins = ["images/alien1.png", "images/alien2.png",
                            "images/alien3.png", "images/alien4.png"]
        self.bullet_skins = ["images/bullet1.png", "images/bullet2.png",
                             "images/bullet3.png", "images/bullet4.png"]
        self.bg_images = ["images/background.png", "images/bg.png", "images/background2.png",
                          "images/bg2.png", "images/background.jpg", "images/bg.jpg"]
        # Lựa chọn skin hiện tại (index)
        self.selected_ship_skin = 0
        self.selected_alien_skin = 0
        self.selected_bullet_skin = 0
        self.selected_bg = 0
        # Số level đã qua
        self.level = 1
        # Load background đầu tiên
        self.background = self._load_bg(self.selected_bg)
        # Game state: 'menu', 'playing', 'gameover', 'paused', 'control_menu', 'instructions', 'settings'
        self.state = 'menu'
        self.paused = False  # Track pause state during playing
        self.control_keys = {
            'key_right': self.settings.key_right,
            'key_left': self.settings.key_left,
            'key_fire': self.settings.key_fire,
            'key_quit': self.settings.key_quit
        }
        # Game mode selection
        self.game_modes = ['Classic', 'Endless', 'Boss Rush']
        self.menu_game_mode = 0
        self.game_mode = 'Classic'
        self.boss_animation_frame = 0
        # Game stats
        self.score = 0
        self.high_score = self._load_high_score()
        self.rankings = self._load_rankings()
        self.player_name = ""
        self.ships_left = self.settings.ship_limit
        # Ưu tiên font Arial Unicode MS để hỗ trợ tiếng Việt, fallback sang Arial
        font_name = None
        for fname in ["Arial Unicode MS", "arial", "Tahoma", "DejaVu Sans"]:
            try:
                f = pygame.font.SysFont(fname, 24)
                if f:
                    font_name = fname
                    break
            except:
                continue
        if not font_name:
            font_name = None
        self.font_small = pygame.font.SysFont(font_name, 32)
        self.font = pygame.font.SysFont(font_name, 48)
        self.font_big = pygame.font.SysFont(font_name, 72)
        # Khởi tạo các nhóm sprite
        self.ship = Ship(self, skin=self.ship_skins[self.selected_ship_skin])
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Hiệu ứng nổ
        self.explosions = []
        # Âm thanh
        pygame.mixer.init()
        try:
            self.snd_shoot = pygame.mixer.Sound("sound/shoot.wav")
        except:
            self.snd_shoot = None
        try:
            self.snd_explosion = pygame.mixer.Sound("sound/explosion.wav")
        except:
            self.snd_explosion = None
        # Power-up
        from powerup import PowerUp
        self.powerups = pygame.sprite.Group()
        self.powerup_types = ['speed', 'multi_bullet', 'heal']
        self.powerup_images = {
            'speed': 'images/powerup_speed.png',
            'multi_bullet': 'images/powerup_multi.png',
            'heal': 'images/powerup_heal.png'
        }
        self.multi_bullet_timer = 0
        # Cooldown bắn đạn liên tục
        self.fire_delay = 180  # ms
        self.last_fire_time = 0
        self.fire_pressed = False
        # Apply stored volume to mixer if available
        try:
            pygame.mixer.music.set_volume(self.settings.volume)
        except Exception:
            pass

        # UI state: 'settings' for configuration screen
        self.state = self.state  # keep existing initialization

    def _load_bg(self, idx):
        # Load background theo index, fallback sang fill màu nếu không có
        for i in range(len(self.bg_images)):
            fname = self.bg_images[(idx + i) % len(self.bg_images)]
            if os.path.exists(fname):
                try:
                    return pygame.image.load(fname)
                except:
                    continue
        return None

    def _load_high_score(self):
        if os.path.exists("high_score.txt"):
            try:
                with open("high_score.txt") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def _load_rankings(self):
        rankings = []
        if os.path.exists("ranking.txt"):
            try:
                with open("ranking.txt") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split(',')
                            if len(parts) == 2:
                                name, score = parts
                                try:
                                    rankings.append((name, int(score)))
                                except:
                                    continue
            except:
                pass
        return sorted(rankings, key=lambda x: x[1], reverse=True)

    def _save_ranking(self, name, score):
        self.rankings.append((name, score))
        self.rankings = sorted(
            self.rankings, key=lambda x: x[1], reverse=True)[:5]
        try:
            with open("ranking.txt", "w") as f:
                f.write("# Bảng xếp hạng\n# Format: name,score\n")
                for n, s in self.rankings:
                    f.write(f"{n},{s}\n")
        except:
            pass

    def _save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("high_score.txt", "w") as f:
                    f.write(str(self.high_score))
            except:
                pass

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.state == 'menu':
                    if event.key == pygame.K_RETURN:
                        self.game_mode = self.game_modes[self.menu_game_mode]
                        self._start_game()
                    elif event.key == pygame.K_c:
                        self.state = 'control_menu'
                    elif event.key == pygame.K_h:
                        self.state = 'instructions'
                    elif event.key == pygame.K_RIGHT:
                        self.menu_game_mode = (
                            self.menu_game_mode + 1) % len(self.game_modes)
                    elif event.key == pygame.K_LEFT:
                        self.menu_game_mode = (
                            self.menu_game_mode - 1) % len(self.game_modes)
                elif self.state == 'gameover':
                    if event.key == pygame.K_r:
                        self._start_game()
                    elif event.key == pygame.K_m:
                        self.state = 'menu'
                elif self.state == 'playing':
                    # ESC to pause game
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    else:
                        self._check_keydown_events(event)
                elif self.state == 'control_menu':
                    self._handle_control_menu_event(event)
                elif self.state == 'instructions':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
                elif self.state == 'settings':
                    # ESC to close settings and go back to menu
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'menu'
            elif event.type == pygame.KEYUP and self.state == 'playing':
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == 'menu':
                    # Click start button
                    if hasattr(self, '_menu_start_btn_rect') and self._menu_start_btn_rect.collidepoint(event.pos):
                        self.game_mode = self.game_modes[self.menu_game_mode]
                        self._start_game()
                    # Click settings button
                    if hasattr(self, '_menu_settings_rect') and self._menu_settings_rect.collidepoint(event.pos):
                        self.state = 'settings'
                    # Click game mode buttons
                    for idx in range(len(self.game_modes)):
                        rect_attr = f'_menu_mode_{idx}_rect'
                        if hasattr(self, rect_attr) and getattr(self, rect_attr).collidepoint(event.pos):
                            self.menu_game_mode = idx
                elif self.state == 'settings':
                    # volume decrease
                    if hasattr(self, '_settings_dec_rect') and self._settings_dec_rect.collidepoint(event.pos):
                        self.settings.volume = max(0.0, self.settings.volume - 0.1)
                        try:
                            pygame.mixer.music.set_volume(self.settings.volume)
                        except:
                            pass
                        self.settings.save_game_config()
                    # volume increase
                    if hasattr(self, '_settings_inc_rect') and self._settings_inc_rect.collidepoint(event.pos):
                        self.settings.volume = min(1.0, self.settings.volume + 0.1)
                        try:
                            pygame.mixer.music.set_volume(self.settings.volume)
                        except:
                            pass
                        self.settings.save_game_config()
                    # language toggle - also update translator
                    if hasattr(self, '_settings_lang_rect') and self._settings_lang_rect.collidepoint(event.pos):
                        self.settings.language = 'en' if self.settings.language == 'vi' else 'vi'
                        self.translator.set_language(self.settings.language)
                        self.settings.save_game_config()
                    # back
                    if hasattr(self, '_settings_back_rect') and self._settings_back_rect.collidepoint(event.pos):
                        self.state = 'menu'
                elif self.state == 'playing' and self.paused:
                    # Handle pause menu button clicks
                    if hasattr(self, '_pause_resume_rect') and self._pause_resume_rect.collidepoint(event.pos):
                        # Resume game
                        self.paused = False
                    elif hasattr(self, '_pause_restart_rect') and self._pause_restart_rect.collidepoint(event.pos):
                        # Restart game
                        self._start_game()
                        self.paused = False
                    elif hasattr(self, '_pause_menu_rect') and self._pause_menu_rect.collidepoint(event.pos):
                        # Return to menu
                        self.state = 'menu'
                        self.paused = False

    def _check_keyup_events(self, event):
        key_right_code = pygame.key.key_code(
            self.control_keys['key_right'].lower())
        key_left_code = pygame.key.key_code(
            self.control_keys['key_left'].lower())
        if event.key == key_right_code:
            self.ship.moving_right = False
        elif event.key == key_left_code:
            self.ship.moving_left = False
        key_fire_code = pygame.key.key_code(
            self.control_keys['key_fire'].lower())
        if event.key == key_fire_code:
            self.fire_pressed = False

    def _create_fleet(self):
        # Game mode logic
        if self.game_mode == 'Boss Rush':
            boss = Alien(self, boss=True)
            boss.rect.x = self.settings.screen_width // 2 - boss.rect.width // 2
            boss.rect.y = 60
            boss.animation_frames = [pygame.Surface(
                (boss.rect.width, boss.rect.height)) for _ in range(4)]
            for i, surf in enumerate(boss.animation_frames):
                surf.fill((255, 100 + i*30, 0))
            boss.current_frame = 0
            self.aliens.add(boss)
            return
        elif self.game_mode == 'Endless':
            alien = Alien(
                self, skin=self.alien_skins[self.selected_alien_skin])
            alien_width, alien_height = alien.rect.size
            number_aliens_x = max(
                2, (self.settings.screen_width - (2 * alien_width)) // (4 * alien_width))
            for alien_number in range(int(number_aliens_x)):
                skin = self.alien_skins[(
                    self.selected_alien_skin + alien_number) % len(self.alien_skins)]
                self._create_alien(alien_number, 0, skin=skin)
            self.settings.fleet_drop_speed = 1
            return
        # Classic: original logic
        # Boss xuất hiện ở các level chia hết cho 5
        if self.level % 5 == 0:
            boss = Alien(self, boss=True)
            boss.rect.x = self.settings.screen_width // 2 - boss.rect.width // 2
            boss.rect.y = 60
            self.aliens.add(boss)
            return
        alien = Alien(self, skin=self.alien_skins[self.selected_alien_skin])
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = max(2, available_space_x //
                      (5 * alien_width))  # Ít alien hơn nữa
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = max(1, available_space_y //
                          (5 * alien_height))  # Ít hàng hơn nữa
        number_aliens_x += min(self.level // 4, 1)
        number_rows += min(self.level // 6, 1)
        # Safety caps to avoid huge fleets that can freeze the game
        # (clamp to reasonable maxima)
        MAX_ALIENS_PER_ROW = 12
        MAX_ROWS = 6
        if number_aliens_x > MAX_ALIENS_PER_ROW:
            print(f"[WARN] Clamping number_aliens_x {number_aliens_x} -> {MAX_ALIENS_PER_ROW}")
            number_aliens_x = MAX_ALIENS_PER_ROW
        if number_rows > MAX_ROWS:
            print(f"[WARN] Clamping number_rows {number_rows} -> {MAX_ROWS}")
            number_rows = MAX_ROWS
        print(f"[DEBUG] Creating fleet for level={self.level} cols={number_aliens_x} rows={number_rows}")
        # Random skin cho alien nếu level >= 3
        for row_number in range(int(number_rows)):
            for alien_number in range(int(number_aliens_x)):
                if self.level >= 3:
                    skin_idx = (self.selected_alien_skin +
                                alien_number + row_number) % len(self.alien_skins)
                    skin = self.alien_skins[skin_idx]
                else:
                    skin = self.alien_skins[self.selected_alien_skin]
                self._create_alien(alien_number, row_number, skin=skin)

    def _create_alien(self, alien_number, row_number, skin=None):
        alien = Alien(self, skin=skin)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_keydown_events(self, event):
        key_right_code = pygame.key.key_code(
            self.control_keys['key_right'].lower())
        key_left_code = pygame.key.key_code(
            self.control_keys['key_left'].lower())
        key_quit_code = pygame.key.key_code(
            self.control_keys['key_quit'].lower())
        key_fire_code = pygame.key.key_code(
            self.control_keys['key_fire'].lower())
        if event.key == key_right_code:
            self.ship.moving_right = True
        elif event.key == key_left_code:
            self.ship.moving_left = True
        elif event.key == key_quit_code:
            self._save_high_score()
            sys.exit()
        elif event.key == key_fire_code:
            self.fire_pressed = True

    def _fire_bullet(self):
        """Bắn đạn với loại đạn khác nhau tùy theo tàu được chọn."""
        # Xác định loại đạn dựa trên tàu
        bullet_types = {
            0: 'normal',      # Alpha: Normal bullets
            1: 'missile',     # Beta: Heavy fire missiles
            2: 'laser',       # Gamma: Rapid fire laser
            3: 'spiral'       # Delta: Energy spiral bullets
        }
        bullet_type = bullet_types.get(self.ship.ship_index, 'normal')
        
        # Extra patterns for multi-bullet mode
        extra_patterns = {
            0: ['circle', 'triangle', 'square'],        # Alpha: Adds circle, triangle, square
            1: ['missile', 'missile', 'missile'],       # Beta: Extra missiles
            2: ['laser', 'laser', 'spiral'],            # Gamma: Laser + spiral mix
            3: ['spiral', 'spiral', 'circle']           # Delta: Spiral + circle energy
        }
        
        if self.multi_bullet_timer > 0:
            # Wider spread: five bullets for stronger multi-bullet skill
            extra_list = extra_patterns.get(self.ship.ship_index, ['normal', 'normal', 'normal'])
            bullet_variants = [bullet_type] + extra_list[:2]  # Base + 2 extras
            
            for i, dx in enumerate([-30, -15, 0, 15, 30]):
                # Alternate between base type and extra types for visual variety
                variant_type = bullet_variants[i % len(bullet_variants)]
                new_bullet = Bullet(
                    self, skin=self.bullet_skins[self.selected_bullet_skin], 
                    dx=dx, bullet_type=variant_type)
                self.bullets.add(new_bullet)
            if self.snd_shoot:
                self.snd_shoot.stop()  # Đảm bảo không bị chồng âm
                self.snd_shoot.play()
        else:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(
                    self, skin=self.bullet_skins[self.selected_bullet_skin],
                    bullet_type=bullet_type)
                self.bullets.add(new_bullet)
                if self.snd_shoot:
                    self.snd_shoot.stop()
                    self.snd_shoot.play()

    def _check_bullet_alien_collisions(self):
        import random
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for bullets, aliens_hit in collisions.items():
                # Check if it's a missile for special explosion
                is_missile = bullets.bullet_type == 'missile'
                explosion_size = 60 if is_missile else 40
                explosion_timer = 15 if is_missile else 30
                
                for alien in aliens_hit:
                    self.score += 50
                    # Hiệu ứng nổ - lớn hơn cho tên lửa
                    for offset in (range(-15, 20, 10) if is_missile else [0]):
                        # Missile creates area damage
                        self.explosions.append({
                            'pos': (alien.rect.centerx + offset, alien.rect.centery),
                            'timer': explosion_timer,
                            'size': explosion_size,
                            'is_missile': is_missile
                        })
                    
                    if self.snd_explosion:
                        self.snd_explosion.play()
                    # Power-up: increase chance and favor multi_bullet
                    if random.random() < 0.7:  # 70% chance to drop a power-up
                        # make multi_bullet significantly more likely
                        ptype = random.choices(self.powerup_types, weights=[1, 5, 1])[0]
                        img = self.powerup_images.get(ptype)
                        powerup = PowerUp(alien.rect.centerx,
                                          alien.rect.centery, ptype, img)
                        # make power-ups fall slowly for easier collection
                        powerup.fall_speed = 0.5
                        self.powerups.add(powerup)
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            # Sang level mới: tăng level, đổi background và skin alien
            if self.game_mode == 'Endless':
                # Endless: respawn aliens immediately, don't increase level
                self._create_fleet()
            else:
                old_level = self.level
                self.level += 1
                print(f"[INFO] Level up {old_level} -> {self.level}")
                self.selected_bg = (self.selected_bg + 1) % len(self.bg_images)
                self.selected_alien_skin = (
                    self.selected_alien_skin + 1) % len(self.alien_skins)
                self.background = self._load_bg(self.selected_bg)
                # create fleet inside try-except to avoid crashes
                try:
                    self._create_fleet()
                except Exception as e:
                    print(f"[ERROR] _create_fleet failed at level {self.level}: {e}")
                    # fallback: reset to a small safe fleet
                    self.aliens = pygame.sprite.Group()
                    self.selected_alien_skin = 0
                    for r in range(2):
                        for c in range(3):
                            self._create_alien(c, r, skin=self.alien_skins[0])

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        if self.state != 'playing':
            return
        self.ships_left -= 1
        if self.ships_left > 0:
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.time.delay(500)
        else:
            self._save_high_score()
            self.state = 'gameover'

    def run_game(self):
        while True:
            self._check_events()
            if self.state == 'playing' and not self.paused:
                self.ship.update()
                self.bullets.update()
                self.powerups.update()
                for bullet in self.bullets.copy():
                    if bullet.rect.bottom <= 0:
                        self.bullets.remove(bullet)
                for powerup in self.powerups.copy():
                    if powerup.rect.top > self.settings.screen_height:
                        self.powerups.remove(powerup)
                self._check_bullet_alien_collisions()
                self._update_aliens()
                self._check_powerup_ship_collisions()
                if pygame.sprite.spritecollideany(self.ship, self.aliens):
                    self._ship_hit()
                self._check_aliens_bottom()
                # Bắn đạn liên tục khi giữ phím
                if self.fire_pressed:
                    now = pygame.time.get_ticks()
                    if now - self.last_fire_time >= self.fire_delay:
                        self._fire_bullet()
                        self.last_fire_time = now
            self._update_screen()

    def _check_powerup_ship_collisions(self):
        collisions = pygame.sprite.spritecollide(
            self.ship, self.powerups, True)
        for powerup in collisions:
            if powerup.ptype == 'speed':
                self.settings.ship_speed *= 1.5
            elif powerup.ptype == 'multi_bullet':
                # Grant a longer multi-bullet duration for stronger effect
                self.multi_bullet_timer = 600  # ~10s
            elif powerup.ptype == 'heal':
                self.ships_left = min(self.ships_left + 1, 5)

    def _start_game(self):
        # Reset lại tốc độ về mặc định mỗi khi bắt đầu game mới
        self.settings.reset_speed()
        self.score = 0
        self.ships_left = self.settings.ship_limit
        self.level = 1
        self.selected_bg = 0
        # Đảm bảo các biến menu_skin luôn tồn tại, fallback về 0 nếu chưa có
        self.selected_alien_skin = getattr(self, 'menu_alien_skin', getattr(self, 'selected_alien_skin', 0))
        self.selected_ship_skin = getattr(self, 'menu_ship_skin', getattr(self, 'selected_ship_skin', 0))
        self.selected_bullet_skin = getattr(self, 'menu_bullet_skin', getattr(self, 'selected_bullet_skin', 0))
        self.background = self._load_bg(self.selected_bg)
        if hasattr(self, 'aliens'):
            self.aliens.empty()
        if hasattr(self, 'bullets'):
            self.bullets.empty()
        self.ship = Ship(self, skin=self.ship_skins[self.selected_ship_skin])
        self.ship.start_spawn_animation()  # Start rotation animation
        
        # Apply fire rate from ship stats
        ship_stats = self.ship.get_ship_stats()
        self.fire_delay = int(180 / ship_stats['fire_rate'])  # Base 180ms, adjusted by fire_rate
        self.last_fire_time = 0
        
        self._create_fleet()
        self.state = 'playing'

    def _draw_hud(self):
        """Draw the HUD with score, ship info, and stats."""
        # Draw semi-transparent background panel for HUD
        hud_height = 80
        hud_surface = pygame.Surface((self.settings.screen_width, hud_height))
        hud_surface.set_alpha(200)
        hud_surface.fill((10, 10, 30))  # Dark blue background
        self.screen.blit(hud_surface, (0, 0))
        
        # Draw top border line
        pygame.draw.line(self.screen, (0, 200, 255), (0, hud_height), 
                        (self.settings.screen_width, hud_height), 2)
        
        # Left side: Score and Ships info - small font
        score_str = f"{self.translator('score')}: {self.score:,}"
        score_img = self.font_small.render(score_str, True, (255, 200, 0))
        self.screen.blit(score_img, (20, 10))
        
        ships_str = f"{self.translator('ships')}: {self.ships_left}"
        ships_img = self.font_small.render(ships_str, True, (100, 200, 255))
        self.screen.blit(ships_img, (20, 45))
        
        # Center: Ship Name and Ability with special styling
        ship_stats = self.ship.get_ship_stats()
        ship_name = ship_stats.get('name', 'Unknown')
        ability = ship_stats.get('ability', 'balanced')
        
        # Ability color based on type
        ability_colors = {
            'balanced': (100, 200, 255),
            'heavy_fire': (255, 100, 100),
            'rapid_fire': (100, 255, 100),
            'tanky': (255, 180, 0)
        }
        ability_color = ability_colors.get(ability, (100, 200, 255))
        
        ship_name_str = f"{ship_name}"
        ship_name_img = self.font_small.render(ship_name_str, True, (0, 255, 200))
        self.screen.blit(ship_name_img, (self.settings.screen_width//2 - 50, 12))
        
        ability_display = ability.upper().replace('_', ' ')
        ability_img = self.font_small.render(f"[{ability_display}]", True, ability_color)
        self.screen.blit(ability_img, (self.settings.screen_width//2 - 75, 45))
        
        # Right side: Ship Stats with bars - organized in 2 columns
        stats_x = self.settings.screen_width - 360
        
        # Damage stat with bar
        damage = ship_stats.get('damage', 1.0)
        damage_str = f"{self.translator('dmg')}: {damage:.1f}x"
        damage_img = self.font_small.render(damage_str, True, (255, 100, 100))
        self.screen.blit(damage_img, (stats_x, 10))
        # Damage bar
        bar_width = 50
        bar_height = 6
        damage_fill = int(bar_width * min(damage / 2.0, 1.0))
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (stats_x + 85, 13, bar_width, bar_height))
        pygame.draw.rect(self.screen, (255, 100, 100), 
                        (stats_x + 85, 13, damage_fill, bar_height))
        
        # Fire Rate stat with bar
        fire_rate = ship_stats.get('fire_rate', 1.0)
        fire_str = f"{self.translator('rof')}: {fire_rate:.1f}x"
        fire_img = self.font_small.render(fire_str, True, (100, 200, 255))
        self.screen.blit(fire_img, (stats_x, 45))
        # Fire rate bar
        fire_fill = int(bar_width * min(fire_rate / 1.5, 1.0))
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (stats_x + 85, 48, bar_width, bar_height))
        pygame.draw.rect(self.screen, (100, 200, 255), 
                        (stats_x + 85, 48, fire_fill, bar_height))
        
        # Right side second column: Bullet Speed and Energy
        stats_x2 = self.settings.screen_width - 180
        
        # Bullet Speed stat with bar
        bullet_speed = ship_stats.get('bullet_speed', 1.0)
        spd_str = f"{self.translator('spd')}: {bullet_speed:.1f}x"
        spd_img = self.font_small.render(spd_str, True, (100, 255, 100))
        self.screen.blit(spd_img, (stats_x2, 10))
        # Speed bar
        speed_fill = int(bar_width * min(bullet_speed / 1.5, 1.0))
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (stats_x2 + 75, 13, bar_width, bar_height))
        pygame.draw.rect(self.screen, (100, 255, 100), 
                        (stats_x2 + 75, 13, speed_fill, bar_height))
        
        # Energy stat with bar
        energy = ship_stats.get('energy', 1.0)
        energy_str = f"{self.translator('nrg')}: {energy:.1f}x"
        energy_img = self.font_small.render(energy_str, True, (255, 200, 100))
        self.screen.blit(energy_img, (stats_x2, 45))
        # Energy bar
        energy_fill = int(bar_width * min(energy / 1.5, 1.0))
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (stats_x2 + 75, 48, bar_width, bar_height))
        pygame.draw.rect(self.screen, (255, 200, 100), 
                        (stats_x2 + 75, 48, energy_fill, bar_height))

    def _update_screen(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.settings.bg_color)
        if self.state == 'menu':
            self._draw_menu()
        elif self.state == 'settings':
            self._draw_settings()
        elif self.state == 'playing':
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.powerups.draw(self.screen)
            # Vẽ hiệu ứng nổ
            for exp in self.explosions:
                size = exp.get('size', 40)
                is_missile = exp.get('is_missile', False)
                timer = exp['timer']
                pos = exp['pos']
                
                if is_missile:
                    # Missile explosion: larger, multi-ring
                    main_radius = size - timer * 2
                    if main_radius > 0:
                        pygame.draw.circle(self.screen, (255, 150, 0), pos, main_radius)
                    # Outer ring
                    outer_radius = size + 10 - timer
                    if outer_radius > 0:
                        pygame.draw.circle(self.screen, (255, 100, 0), pos, outer_radius, 2)
                else:
                    # Normal explosion: single circle
                    pygame.draw.circle(self.screen, (255, 100, 0),
                                     pos, size - timer * 2)
            # Giảm timer, xóa hiệu ứng khi hết
            self.explosions = [
                exp for exp in self.explosions if exp['timer'] > 0]
            for exp in self.explosions:
                exp['timer'] -= 1
            if self.multi_bullet_timer > 0:
                self.multi_bullet_timer -= 1
            
            # Draw HUD with score and ship stats
            self._draw_hud()
            
            # Draw pause menu if paused
            if self.paused:
                self._draw_pause_menu()
        elif self.state == 'gameover':
            self._draw_gameover()
        elif self.state == 'instructions':
            self._draw_instructions()
        pygame.display.flip()

    def _draw_instructions(self):
        """Vẽ màn hình hướng dẫn với hỗ trợ đa ngôn ngữ."""
        self.screen.fill((245, 245, 255))
        
        # Title
        title_text = self.translator('instructions')
        title = self.font_big.render(title_text, True, (0, 100, 200))
        rect = title.get_rect(center=(self.settings.screen_width//2, 80))
        self.screen.blit(title, rect)
        
        # Instructions text based on language
        if self.settings.language == 'vi':
            lines = [
                "Mục tiêu: Tiêu diệt tất cả quái vật và vượt qua các cấp độ.",
                "Di chuyển: {} (phải), {} (trái)".format(
                    self.control_keys['key_right'].upper(), self.control_keys['key_left'].upper()),
                "Bắn: {}".format(self.control_keys['key_fire'].upper()),
                "Thoát: {}".format(self.control_keys['key_quit'].upper()),
                "Power-up: Thu thập vật phẩm để tăng tốc độ, bắn nhiều đạn, hồi máu.",
                "BXH: Lưu điểm và tên người chơi, top 5 người chơi.",
                "Điều khiển: Bấm C ở menu để thay đổi phím.",
                "Bấm ESC để quay lại menu."
            ]
        else:
            lines = [
                "Goal: Destroy all aliens and pass levels.",
                "Move: {} (right), {} (left)".format(
                    self.control_keys['key_right'].upper(), self.control_keys['key_left'].upper()),
                "Shoot: {}".format(self.control_keys['key_fire'].upper()),
                "Quit: {}".format(self.control_keys['key_quit'].upper()),
                "Power-up: Collect items to speed up, multi-bullet, heal.",
                "Ranking: Save score and name, top 5 players.",
                "Control settings: Press C in menu to change keys.",
                "Press ESC to return to menu."
            ]
        
        for i, line in enumerate(lines):
            txt = self.font.render(line, True, (30, 30, 80))
            self.screen.blit(txt, (120, 180 + i*50))

    def _draw_settings(self):
        """Vẽ màn hình cài đặt với hỗ trợ đa ngôn ngữ."""
        # Settings screen: volume control and language toggle
        self.screen.fill((245, 245, 255))
        
        # Title
        title_text = self.translator('settings')
        title = self.font_big.render(title_text, True, (0, 100, 200))
        rect = title.get_rect(center=(self.settings.screen_width//2, 80))
        self.screen.blit(title, rect)

        # Volume label and buttons
        vol_text = self.translator('volume')
        vol_label = self.font.render(f"{vol_text} {int(self.settings.volume*100)}%", True, (0, 0, 0))
        self.screen.blit(vol_label, (120, 200))
        # Decrease
        dec_rect = pygame.Rect(120, 260, 60, 60)
        pygame.draw.rect(self.screen, (200, 60, 60), dec_rect, border_radius=8)
        self.screen.blit(self.font.render("-", True, (255,255,255)), self.font.render("-", True, (255,255,255)).get_rect(center=dec_rect.center))
        # Increase
        inc_rect = pygame.Rect(200, 260, 60, 60)
        pygame.draw.rect(self.screen, (60, 180, 60), inc_rect, border_radius=8)
        self.screen.blit(self.font.render("+", True, (255,255,255)), self.font.render("+", True, (255,255,255)).get_rect(center=inc_rect.center))

        # Language toggle
        lang_label_text = self.translator('language')
        lang_display = self.translator('vietnamese' if self.settings.language == 'vi' else 'english')
        lang_label = self.font.render(f"{lang_label_text} {lang_display}", True, (0,0,0))
        self.screen.blit(lang_label, (120, 360))
        
        lang_rect = pygame.Rect(120, 420, 200, 60)
        pygame.draw.rect(self.screen, (80, 120, 200), lang_rect, border_radius=8)
        lang_txt_str = self.translator('toggle_language')
        lang_txt = self.font.render(lang_txt_str, True, (255,255,255))
        self.screen.blit(lang_txt, lang_txt.get_rect(center=lang_rect.center))

        # Back button
        back_rect = pygame.Rect(self.settings.screen_width-180, self.settings.screen_height-80, 160, 50)
        pygame.draw.rect(self.screen, (80,80,80), back_rect, border_radius=8)
        back_text = self.translator('back')
        back_txt = self.font.render(back_text, True, (255,255,255))
        self.screen.blit(back_txt, back_txt.get_rect(center=back_rect.center))

        # store interactive rects
        self._settings_dec_rect = dec_rect
        self._settings_inc_rect = inc_rect
        self._settings_lang_rect = lang_rect
        self._settings_back_rect = back_rect

    def _draw_menu(self):
        import math
        # Background fill
        self.screen.fill((20, 20, 40))
        
        # Animated background stars
        t = pygame.time.get_ticks() // 10
        for i in range(30):
            x = int((i*37 + t*3) % self.settings.screen_width)
            y = int((i*53 + t*2) % self.settings.screen_height)
            r = 2 + (i % 3)
            pygame.draw.circle(self.screen, (200, 200, 255), (x, y), r)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # ============ TOP SECTION: Title + Settings ============
        # Animated title
        title_color = (0, 200 + int(55*math.sin(t/20)), 100)
        title_text = self.translator('title')
        title = self.font_big.render(title_text, True, title_color)
        rect = title.get_rect(center=(self.settings.screen_width//2, 50))
        self.screen.blit(title, rect)

        # Settings button (top-right corner)
        set_w, set_h = 120, 50
        set_x, set_y = self.settings.screen_width - set_w - 20, 20
        set_rect = pygame.Rect(set_x, set_y, set_w, set_h)
        set_color = (100, 100, 255) if set_rect.collidepoint(mouse) else (80, 80, 140)
        pygame.draw.rect(self.screen, set_color, set_rect, border_radius=8)
        set_txt_text = self.translator('settings')
        set_txt = self.font.render(set_txt_text, True, (255, 255, 255))
        self.screen.blit(set_txt, set_txt.get_rect(center=set_rect.center))
        self._menu_settings_rect = set_rect

        # ============ LEFT SECTION: Game Modes ============
        left_x = 60
        y_start = 150
        
        # Game mode title
        mode_title_text = self.translator('classic')  # Will display game modes
        mode_title = self.font.render("Chế độ chơi:", True, (100, 200, 255)) if self.settings.language == 'vi' else self.font.render("Game Mode:", True, (100, 200, 255))
        self.screen.blit(mode_title, (left_x, y_start))
        
        # Game mode buttons
        for idx, mode in enumerate(self.game_modes):
            mode_y = y_start + 50 + idx*70
            mode_w, mode_h = 200, 55
            mode_rect = pygame.Rect(left_x, mode_y, mode_w, mode_h)
            mode_color = (0, 200, 100) if self.menu_game_mode == idx else (80, 120, 150)
            if mode_rect.collidepoint(mouse):
                mode_color = (0, 220, 120)
            pygame.draw.rect(self.screen, mode_color, mode_rect, border_radius=8)
            mode_txt = self.font.render(mode, True, (255, 255, 255))
            self.screen.blit(mode_txt, mode_txt.get_rect(center=mode_rect.center))
            # Store rects for event handling
            setattr(self, f'_menu_mode_{idx}_rect', mode_rect)

        # ============ CENTER SECTION: Ship Selection ============
        center_x = (self.settings.screen_width - 400) // 2
        ship_y_base = 150
        
        # Ship skins title
        ship_label_text = self.translator('select_ship')
        ship_label = self.font.render(ship_label_text, True, (100, 200, 255))
        self.screen.blit(ship_label, (center_x, ship_y_base))
        
        # Ship skins grid
        self.menu_ship_skin = getattr(self, 'menu_ship_skin', self.selected_ship_skin)
        ships_per_row = 3
        ship_size = 70
        ship_spacing = 100
        
        for idx, fname in enumerate(self.ship_skins):
            row = idx // ships_per_row
            col = idx % ships_per_row
            x = center_x + 20 + col*ship_spacing
            y = ship_y_base + 60 + row*ship_spacing
            
            if os.path.exists(fname):
                img = pygame.image.load(fname)
                img = pygame.transform.scale(img, (ship_size, int(ship_size*0.8)))
                rect_img = img.get_rect(center=(x, y))
                self.screen.blit(img, rect_img)
                border_color = (0, 255, 0) if rect_img.collidepoint(mouse) else (0, 200, 255) if self.menu_ship_skin == idx else (100, 100, 100)
                pygame.draw.rect(self.screen, border_color, rect_img, 3)
                if rect_img.collidepoint(mouse) and click[0]:
                    self.menu_ship_skin = idx
                    self.selected_ship_skin = idx

        # ============ RIGHT SECTION: Ranking + High Score ============
        right_x = self.settings.screen_width - 320
        hs_label = self.translator('high_score')
        hs = self.font.render(f"{hs_label}: {self.high_score}", True, (255, 180, 0))
        self.screen.blit(hs, (right_x, y_start))
        
        rank_title = self.translator('ranking')
        txt_rank = self.font.render(f"{rank_title}:", True, (255, 100, 0))
        self.screen.blit(txt_rank, (right_x, y_start + 50))
        for i, (name, score) in enumerate(self.rankings[:5]):
            rank_txt = self.font.render(f"{i+1}. {name}: {score}", True, (0, 200, 255))
            self.screen.blit(rank_txt, (right_x + 10, y_start + 90 + i*40))

        # ============ BOTTOM SECTION: Instructions + START Button ============
        # Instructions (in game language)
        if self.settings.language == 'vi':
            instruct = self.font.render("ENTER: Chơi | C: Phím | H: Trợ giúp | ESC: Menu", True, (100, 150, 200))
        else:
            instruct = self.font.render("ENTER: Play | C: Keys | H: Help | ESC: Menu", True, (100, 150, 200))
        instruct_rect = instruct.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height - 120))
        self.screen.blit(instruct, instruct_rect)

        # START Button
        btn_w, btn_h = 300, 70
        btn_x = self.settings.screen_width//2 - btn_w//2
        btn_y = self.settings.screen_height - btn_h - 20
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        btn_color = (0, 220, 120) if btn_rect.collidepoint(mouse) else (0, 180, 100)
        pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=15)
        txt_btn = self.font_big.render("BẮT ĐẦU", True, (255, 255, 255))
        self.screen.blit(txt_btn, txt_btn.get_rect(center=btn_rect.center))
        self._menu_start_btn_rect = btn_rect
        self._menu_start_btn_rect = btn_rect

    def _draw_gameover(self):
        over = self.font_big.render(self.translator('game_over'), True, (255, 50, 50))
        rect = over.get_rect(
            center=(self.settings.screen_width//2, self.settings.screen_height//3))
        self.screen.blit(over, rect)
        score = self.font.render(f"{self.translator('score')}: {self.score}", True, (0, 200, 100))
        rect2 = score.get_rect(
            center=(self.settings.screen_width//2, self.settings.screen_height//2))
        self.screen.blit(score, rect2)
        if self.settings.language == 'vi':
            hs = self.font.render(
                f"Điểm cao: {self.high_score}", True, (255, 180, 0))
        else:
            hs = self.font.render(
                f"High Score: {self.high_score}", True, (255, 180, 0))
        rect3 = hs.get_rect(
            center=(self.settings.screen_width//2, self.settings.screen_height//2+50))
        self.screen.blit(hs, rect3)
        if self.settings.language == 'vi':
            again = self.font.render("Bấm R để chơi lại", True, (100, 100, 255))
        else:
            again = self.font.render("Press R to restart", True, (100, 100, 255))
        rect4 = again.get_rect(
            center=(self.settings.screen_width//2, self.settings.screen_height//2+120))
        self.screen.blit(again, rect4)
        if self.settings.language == 'vi':
            menu = self.font.render(
                "Bấm M để về menu", True, (100, 100, 255))
        else:
            menu = self.font.render(
                "Press M to return to menu", True, (100, 100, 255))
        rect5 = menu.get_rect(
            center=(self.settings.screen_width//2, self.settings.screen_height//2+170))
        self.screen.blit(menu, rect5)
        # Enter player name if score > 0 and not entered
        if self.score > 0 and not self.player_name:
            self.player_name = self._get_player_name()
            self._save_ranking(self.player_name, self.score)
        if self.score > 0 and self.player_name:
            txt = self.font.render(
                f"Your name: {self.player_name}", True, (0, 0, 0))
            self.screen.blit(txt, (self.settings.screen_width //
                             2-100, self.settings.screen_height//2+200))

    def _draw_pause_menu(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause menu popup
        popup_width, popup_height = 500, 350
        popup_x = (self.settings.screen_width - popup_width) // 2
        popup_y = (self.settings.screen_height - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        
        # Draw popup background
        pygame.draw.rect(self.screen, (30, 30, 60), popup_rect, border_radius=15)
        pygame.draw.rect(self.screen, (100, 100, 255), popup_rect, 3, border_radius=15)
        
        # Title
        if self.settings.language == 'vi':
            title = self.font_big.render("TẠM DỪNG", True, (255, 255, 100))
        else:
            title = self.font_big.render("PAUSED", True, (255, 255, 100))
        title_rect = title.get_rect(center=(popup_x + popup_width//2, popup_y + 40))
        self.screen.blit(title, title_rect)
        
        # Three buttons: Resume, Restart, Menu
        button_width, button_height = 150, 60
        button_y_start = popup_y + 130
        button_spacing = 80
        
        mouse = pygame.mouse.get_pos()
        
        # Resume button
        resume_x = popup_x + (popup_width - button_width) // 2
        self._pause_resume_rect = pygame.Rect(resume_x, button_y_start, button_width, button_height)
        resume_color = (100, 200, 100) if self._pause_resume_rect.collidepoint(mouse) else (80, 160, 80)
        pygame.draw.rect(self.screen, resume_color, self._pause_resume_rect, border_radius=8)
        if self.settings.language == 'vi':
            resume_txt = self.font.render("Tiếp tục", True, (255, 255, 255))
        else:
            resume_txt = self.font.render("Resume", True, (255, 255, 255))
        self.screen.blit(resume_txt, resume_txt.get_rect(center=self._pause_resume_rect.center))
        
        # Restart button
        restart_x = popup_x + (popup_width - button_width) // 2
        restart_y = button_y_start + button_spacing
        self._pause_restart_rect = pygame.Rect(restart_x, restart_y, button_width, button_height)
        restart_color = (200, 180, 80) if self._pause_restart_rect.collidepoint(mouse) else (180, 160, 60)
        pygame.draw.rect(self.screen, restart_color, self._pause_restart_rect, border_radius=8)
        if self.settings.language == 'vi':
            restart_txt = self.font.render("Chơi lại", True, (255, 255, 255))
        else:
            restart_txt = self.font.render("Restart", True, (255, 255, 255))
        self.screen.blit(restart_txt, restart_txt.get_rect(center=self._pause_restart_rect.center))
        
        # Menu button
        menu_x = popup_x + (popup_width - button_width) // 2
        menu_y = restart_y + button_spacing
        self._pause_menu_rect = pygame.Rect(menu_x, menu_y, button_width, button_height)
        menu_color = (200, 100, 100) if self._pause_menu_rect.collidepoint(mouse) else (180, 80, 80)
        pygame.draw.rect(self.screen, menu_color, self._pause_menu_rect, border_radius=8)
        menu_txt = self.font.render(self.translator('menu'), True, (255, 255, 255))
        self.screen.blit(menu_txt, menu_txt.get_rect(center=self._pause_menu_rect.center))

    def _get_player_name(self):
        import pygame
        name = ""
        active = True
        clock = pygame.time.Clock()
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 10 and event.unicode.isprintable():
                            name += event.unicode
            self.screen.fill((255, 255, 255))
            txt = self.font.render(
                "Nhập tên (ENTER để xác nhận):", True, (0, 0, 0))
            self.screen.blit(txt, (100, 200))
            name_txt = self.font.render(name, True, (0, 100, 200))
            self.screen.blit(name_txt, (100, 260))
            pygame.display.flip()
            clock.tick(30)
        return name if name else "Player"


if __name__ == '__main__':
    pygame.init()
    ai = AlienInvasion()
    ai.run_game()
