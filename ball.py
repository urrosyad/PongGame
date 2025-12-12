"""
Class Ball - Mewarisi dari GameObject
Demonstrasi INHERITANCE dan POLYMORPHISM
"""

from game_object import GameObject
import random
import math

class Ball(GameObject):
    """
    Class Ball yang mewarisi dari GameObject (INHERITANCE)
    Menambahkan fitur khusus untuk bola seperti kecepatan dan pantulan
    """
    
    def __init__(self, x, y, radius, color, speed):
        """
        Constructor untuk Ball
        
        Args:
            x (float): Posisi x bola
            y (float): Posisi y bola
            radius (float): Jari-jari bola
            color (str): Warna bola
            speed (float): Kecepatan dasar bola
        """
        # Panggil constructor parent class (GameObject)
        super().__init__(x, y, radius * 2, radius * 2, color)
        
        # Private attributes khusus untuk Ball
        self.__radius = radius
        self.__speed = speed
        self.__base_speed = speed  # Simpan speed dasar untuk reset
        self.__velocity_x = 0
        self.__velocity_y = 0
        self.__speed_boost = 1.0  # Multiplier untuk power-up
        
        # Inisialisasi arah bola secara random
        self.reset_velocity()
    
    # GETTER methods khusus Ball
    def get_radius(self):
        """Mengambil radius bola"""
        return self.__radius
    
    def get_velocity_x(self):
        """Mengambil kecepatan horizontal bola"""
        return self.__velocity_x
    
    def get_velocity_y(self):
        """Mengambil kecepatan vertikal bola"""
        return self.__velocity_y
    
    def get_speed(self):
        """Mengambil kecepatan bola saat ini"""
        return self.__speed
    
    # SETTER methods khusus Ball
    def set_velocity_x(self, vx):
        """Mengatur kecepatan horizontal bola"""
        self.__velocity_x = vx
    
    def set_velocity_y(self, vy):
        """Mengatur kecepatan vertikal bola"""
        self.__velocity_y = vy
    
    def set_speed_boost(self, boost):
        """
        Mengatur multiplier kecepatan (untuk power-up)
        
        Args:
            boost (float): Multiplier kecepatan (1.0 = normal, 1.5 = 50% lebih cepat)
        """
        self.__speed_boost = boost
        self.__speed = self.__base_speed * boost
        # Update velocity dengan speed baru
        self.normalize_velocity()
    
    def reset_speed_boost(self):
        """Reset speed boost ke normal"""
        self.set_speed_boost(1.0)
    
    def reset_velocity(self):
        """
        Reset kecepatan bola dengan arah random
        Digunakan saat game start atau setelah skor
        """
        # Random sudut antara -45 hingga 45 derajat
        angle = random.uniform(-math.pi/4, math.pi/4)
        
        # Random arah kiri atau kanan
        direction = random.choice([-1, 1])
        
        self.__velocity_x = direction * self.__speed * math.cos(angle)
        self.__velocity_y = self.__speed * math.sin(angle)
    
    def normalize_velocity(self):
        """
        Normalisasi velocity agar kecepatan tetap konsisten
        Berguna setelah pantulan atau perubahan kecepatan
        """
        # Hitung magnitude velocity saat ini
        magnitude = math.sqrt(self.__velocity_x**2 + self.__velocity_y**2)
        
        if magnitude > 0:
            # Normalisasi dan kalikan dengan speed
            self.__velocity_x = (self.__velocity_x / magnitude) * self.__speed
            self.__velocity_y = (self.__velocity_y / magnitude) * self.__speed
    
    def reverse_x(self):
        """Balik arah horizontal (pantulan di paddle)"""
        self.__velocity_x = -self.__velocity_x
    
    def reverse_y(self):
        """Balik arah vertikal (pantulan di atas/bawah)"""
        self.__velocity_y = -self.__velocity_y
    
    def update(self):
        """
        Override method update dari GameObject (POLYMORPHISM)
        Update posisi bola berdasarkan velocity
        """
        if not self.is_active():
            return
        
        # Update posisi berdasarkan velocity
        self.set_x(self.get_x() + self.__velocity_x)
        self.set_y(self.get_y() + self.__velocity_y)
    
    def draw(self, canvas):
        """
        Override method draw dari GameObject (POLYMORPHISM)
        Menggambar bola sebagai oval di canvas
        
        Args:
            canvas: Tkinter canvas object
        """
        if not self.is_active():
            return
        
        x = self.get_x()
        y = self.get_y()
        r = self.__radius
        
        # Gambar bola dengan efek gradasi (menggunakan oval)
        canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=self.get_color(),
            outline="white",
            width=2,
            tags="ball"
        )
        
        # Tambahkan highlight untuk efek 3D
        canvas.create_oval(
            x - r/2, y - r/2, x, y,
            fill="white",
            outline="",
            stipple="gray50",
            tags="ball"
        )
    
    def bounce_off_paddle(self, paddle):
        """
        Hitung pantulan bola dari paddle dengan sudut berdasarkan posisi impact
        
        Args:
            paddle: Objek Paddle yang ditabrak
        """
        # Hitung posisi relatif impact (0 = tengah, -1 = atas, 1 = bawah)
        ball_center = self.get_y()
        paddle_center = paddle.get_y() + paddle.get_height() / 2
        relative_impact = (ball_center - paddle_center) / (paddle.get_height() / 2)
        
        # Batasi relative_impact antara -1 dan 1
        relative_impact = max(-1, min(1, relative_impact))
        
        # Hitung sudut pantulan (maksimal 60 derajat)
        bounce_angle = relative_impact * (math.pi / 3)  # 60 derajat = pi/3
        
        # Tentukan arah horizontal berdasarkan posisi paddle
        direction = 1 if paddle.get_x() < 400 else -1  # 400 adalah tengah layar (asumsi)
        
        # Set velocity baru berdasarkan sudut
        self.__velocity_x = direction * self.__speed * math.cos(bounce_angle)
        self.__velocity_y = self.__speed * math.sin(bounce_angle)
    
    def increase_speed(self, increment=0.2):
        """
        Tingkatkan kecepatan bola secara gradual
        
        Args:
            increment (float): Jumlah peningkatan kecepatan
        """
        self.__speed += increment
        self.normalize_velocity()
    
    def reset_position(self, x, y):
        """
        Reset posisi bola ke koordinat tertentu
        
        Args:
            x (float): Posisi x baru
            y (float): Posisi y baru
        """
        self.set_x(x)
        self.set_y(y)
        self.reset_velocity()
        self.reset_speed_boost()