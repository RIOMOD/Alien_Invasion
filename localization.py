# localization.py
"""Hệ thống dịch ngôn ngữ cho game"""

TRANSLATIONS = {
    'vi': {
        # Menu
        'title': 'ALIEN INVASION',
        'settings': 'CÀI ĐẶT',
        'instructions': 'HƯỚNG DẪN',
        'back': 'Quay lại',
        'start': 'BẮT ĐẦU',
        'quit': 'THOÁT',
        
        # Game modes
        'classic': 'CLASSIC',
        'endless': 'ENDLESS',
        'select_ship': 'CHỌN TÀU',
        'ranking': 'BXH',
        'high_score': 'ĐIỂM CAO NHẤT',
        
        # Settings
        'volume': 'Âm lượng:',
        'language': 'Ngôn ngữ:',
        'vietnamese': 'Tiếng Việt',
        'english': 'English',
        'toggle_language': 'Chuyển ngôn ngữ',
        'controls': 'Điều khiển',
        'change_controls': 'Thay đổi phím',
        
        # Instructions
        'goal': 'Mục tiêu: Tiêu diệt tất cả quái vật và vượt qua các cấp độ.',
        'move_right': 'Di chuyển: {0} (phải), {1} (trái)',
        'shoot': 'Bắn: {0}',
        'quit_game': 'Thoát: {0}',
        'powerup': 'Power-up: Thu thập vật phẩm để tăng tốc độ, bắn nhiều đạn, hồi máu.',
        'ranking_desc': 'BXH: Lưu điểm và tên người chơi, top 5 người chơi.',
        'control_desc': 'Điều khiển: Bấm C ở menu để thay đổi phím.',
        'esc_menu': 'Bấm ESC để quay lại menu.',
        'pause': 'Tạm dừng',
        'resume': 'Tiếp tục',
        'restart': 'Chơi lại',
        'menu': 'Menu',
        
        # Game Over
        'game_over': 'GAME OVER',
        'final_score': 'ĐIỂM CUỐI CÙNG: ',
        'play_again': 'Chơi lại',
        
        # HUD
        'score': 'Score:',
        'ships': 'Tàu:',
        'best': 'Best:',
        'dmg': 'DMG:',
        'rof': 'ROF:',
        'spd': 'SPD:',
        'nrg': 'NRG:',
        
        # Control menu
        'control_settings': 'CÀI ĐẶT ĐIỀU KHIỂN',
        'right_key': 'Phím phải:',
        'left_key': 'Phím trái:',
        'fire_key': 'Phím bắn:',
        'quit_key': 'Phím thoát:',
        'press_key': 'Bấm một phím...',
        
        # Messages
        'level_up': 'LEVEL UP!',
        'wave': 'WAVE',
    },
    'en': {
        # Menu
        'title': 'ALIEN INVASION',
        'settings': 'SETTINGS',
        'instructions': 'INSTRUCTIONS',
        'back': 'Back',
        'start': 'START',
        'quit': 'QUIT',
        
        # Game modes
        'classic': 'CLASSIC',
        'endless': 'ENDLESS',
        'select_ship': 'SELECT SHIP',
        'ranking': 'RANKING',
        'high_score': 'HIGH SCORE',
        
        # Settings
        'volume': 'Volume:',
        'language': 'Language:',
        'vietnamese': 'Tiếng Việt',
        'english': 'English',
        'toggle_language': 'Toggle Language',
        'controls': 'Controls',
        'change_controls': 'Change Controls',
        
        # Instructions
        'goal': 'Goal: Destroy all aliens and pass levels.',
        'move_right': 'Move: {0} (right), {1} (left)',
        'shoot': 'Shoot: {0}',
        'quit_game': 'Quit: {0}',
        'powerup': 'Power-up: Collect items to speed up, multi-bullet, heal.',
        'ranking_desc': 'Ranking: Save score and name, top 5 players.',
        'control_desc': 'Control settings: Press C in menu to change keys.',
        'esc_menu': 'Press ESC to return to menu.',
        'pause': 'Pause',
        'resume': 'Resume',
        'restart': 'Restart',
        'menu': 'Menu',
        
        # Game Over
        'game_over': 'GAME OVER',
        'final_score': 'FINAL SCORE: ',
        'play_again': 'Play Again',
        
        # HUD
        'score': 'Score:',
        'ships': 'Ships:',
        'best': 'Best:',
        'dmg': 'DMG:',
        'rof': 'ROF:',
        'spd': 'SPD:',
        'nrg': 'NRG:',
        
        # Control menu
        'control_settings': 'CONTROL SETTINGS',
        'right_key': 'Right Key:',
        'left_key': 'Left Key:',
        'fire_key': 'Fire Key:',
        'quit_key': 'Quit Key:',
        'press_key': 'Press a key...',
        
        # Messages
        'level_up': 'LEVEL UP!',
        'wave': 'WAVE',
    }
}

class Translator:
    """Lớp dịch - quản lý dịch vụ dịch ngôn ngữ"""
    
    def __init__(self, language='vi'):
        self.language = language
    
    def set_language(self, language):
        """Thay đổi ngôn ngữ"""
        if language in TRANSLATIONS:
            self.language = language
    
    def get(self, key, *args):
        """Lấy chuỗi dịch từ từ khóa"""
        if self.language not in TRANSLATIONS:
            self.language = 'vi'
        
        translation_dict = TRANSLATIONS[self.language]
        text = translation_dict.get(key, key)
        
        # Format string with arguments if provided
        if args:
            try:
                return text.format(*args)
            except (IndexError, KeyError):
                return text
        
        return text
    
    def __call__(self, key, *args):
        """Cho phép gọi translator như một hàm"""
        return self.get(key, *args)
