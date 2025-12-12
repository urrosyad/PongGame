"""
Sound Manager untuk mengelola efek suara game
Menggunakan winsound untuk Windows atau fallback untuk OS lain
"""

import sys
import threading

class SoundManager:
    """
    Class untuk mengelola sound effects dalam game
    Menggunakan beep sounds sebagai alternatif yang cross-platform
    """
    
    def __init__(self):
        """Constructor untuk SoundManager"""
        self.__enabled = True
        self.__sound_available = False
        
        # Cek apakah winsound tersedia (Windows only)
        try:
            if sys.platform == 'win32':
                import winsound
                self.__winsound = winsound
                self.__sound_available = True
            else:
                # Untuk Mac/Linux, kita akan gunakan print sebagai fallback
                self.__sound_available = False
        except ImportError:
            self.__sound_available = False
    
    def enable(self):
        """Enable sound effects"""
        self.__enabled = True
    
    def disable(self):
        """Disable sound effects"""
        self.__enabled = False
    
    def is_enabled(self):
        """Mengecek apakah sound enabled"""
        return self.__enabled
    
    def toggle(self):
        """Toggle sound on/off"""
        self.__enabled = not self.__enabled
        return self.__enabled
    
    def _play_beep(self, frequency, duration):
        """
        Helper method untuk play beep sound
        
        Args:
            frequency (int): Frekuensi suara dalam Hz
            duration (int): Durasi dalam milliseconds
        """
        if not self.__enabled:
            return
        
        if self.__sound_available and sys.platform == 'win32':
            # Play sound di thread terpisah agar tidak blocking
            threading.Thread(
                target=lambda: self.__winsound.Beep(frequency, duration),
                daemon=True
            ).start()
    
    def play_paddle_hit(self):
        """
        Play sound saat bola kena paddle
        Suara pendek dengan frekuensi sedang
        """
        self._play_beep(800, 50)
    
    def play_wall_hit(self):
        """
        Play sound saat bola kena dinding atas/bawah
        Suara pendek dengan frekuensi tinggi
        """
        self._play_beep(600, 50)
    
    def play_score(self):
        """
        Play sound saat ada yang score
        Suara yang lebih panjang dan rendah
        """
        if not self.__enabled:
            return
        
        if self.__sound_available and sys.platform == 'win32':
            # Sequence of beeps untuk score
            def play_sequence():
                self.__winsound.Beep(400, 100)
                self.__winsound.Beep(300, 150)
            
            threading.Thread(target=play_sequence, daemon=True).start()
    
    def play_powerup_collect(self):
        """
        Play sound saat mengambil power-up
        Suara ascending untuk efek positif
        """
        if not self.__enabled:
            return
        
        if self.__sound_available and sys.platform == 'win32':
            # Ascending beeps
            def play_sequence():
                self.__winsound.Beep(500, 50)
                self.__winsound.Beep(700, 50)
                self.__winsound.Beep(900, 50)
            
            threading.Thread(target=play_sequence, daemon=True).start()
    
    def play_game_start(self):
        """
        Play sound saat game mulai
        Suara yang energetic
        """
        if not self.__enabled:
            return
        
        if self.__sound_available and sys.platform == 'win32':
            def play_sequence():
                self.__winsound.Beep(600, 100)
                self.__winsound.Beep(800, 150)
            
            threading.Thread(target=play_sequence, daemon=True).start()
    
    def play_game_over(self):
        """
        Play sound saat game over
        Suara descending untuk efek ending
        """
        if not self.__enabled:
            return
        
        if self.__sound_available and sys.platform == 'win32':
            def play_sequence():
                self.__winsound.Beep(800, 100)
                self.__winsound.Beep(600, 100)
                self.__winsound.Beep(400, 200)
            
            threading.Thread(target=play_sequence, daemon=True).start()