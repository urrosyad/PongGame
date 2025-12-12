"""
Class PowerUp - Mewarisi dari GameObject
Demonstrasi INHERITANCE dan POLYMORPHISM
"""

from game_object import GameObject
import random

class PowerUp(GameObject):
    """
    Class PowerUp yang mewarisi dari GameObject (INHERITANCE)
    Menambahkan fitur khusus untuk power-up seperti tipe dan durasi
    """
    
    # Tipe-tipe power-up yang tersedia
    SPEED_BOOST = "speed_boost"  # Mempercepat bola
    SIZE_BOOST = "size_boost"    # Memperbesar paddle
    
    # Warna untuk setiap tipe power-up
    COLORS = {
        SPEED_BOOST: "#FF6B6B",  # Merah untuk speed
        SIZE_BOOST: "#4ECDC4"    # Cyan untuk size
    }
    
    def __init__(self, x, y, size, powerup_type):
        """
        Constructor untuk PowerUp
        
        Args:
            x (float): Posisi x power-up
            y (float): Posisi y power-up
            size (float): Ukuran power-up
            powerup_type (str): Tipe power-up (SPEED_BOOST atau SIZE_BOOST)
        """
        # Panggil constructor parent class dengan warna sesuai tipe
        color = self.COLORS.get(powerup_type, "#FFFFFF")
        super().__init__(x, y, size, size, color)
        
        # Private attributes khusus untuk PowerUp
        self.__type = powerup_type
        self.__size = size
        self.__rotation = 0  # Untuk animasi rotasi
        self.__pulse = 0     # Untuk animasi pulsing
        self.__lifetime = 300  # Durasi power-up muncul (dalam frame, ~10 detik)
        self.__collected = False
    
    # GETTER methods khusus PowerUp
    def get_type(self):
        """Mengambil tipe power-up"""
        return self.__type
    
    def get_size(self):
        """Mengambil ukuran power-up"""
        return self.__size
    
    def is_collected(self):
        """Mengecek apakah power-up sudah diambil"""
        return self.__collected
    
    def get_lifetime(self):
        """Mengambil sisa lifetime power-up"""
        return self.__lifetime
    
    # SETTER methods khusus PowerUp
    def collect(self):
        """Tandai power-up sebagai sudah diambil"""
        self.__collected = True
        self.set_active(False)
    
    def update(self):
        """
        Override method update dari GameObject (POLYMORPHISM)
        Update animasi dan lifetime power-up
        """
        if not self.is_active() or self.__collected:
            return
        
        # Update rotasi untuk animasi
        self.__rotation += 2
        if self.__rotation >= 360:
            self.__rotation = 0
        
        # Update pulse untuk animasi scale
        self.__pulse += 0.1
        
        # Kurangi lifetime
        self.__lifetime -= 1
        if self.__lifetime <= 0:
            self.set_active(False)
    
    def draw(self, canvas):
        """
        Override method draw dari GameObject (POLYMORPHISM)
        Menggambar power-up dengan animasi
        
        Args:
            canvas: Tkinter canvas object
        """
        if not self.is_active() or self.__collected:
            return
        
        import math
        
        x = self.get_x()
        y = self.get_y()
        size = self.__size
        
        # Hitung scale dari pulse effect
        pulse_scale = 1.0 + math.sin(self.__pulse) * 0.2
        current_size = size * pulse_scale
        
        # Gambar power-up sebagai diamond (rotated square)
        half_size = current_size / 2
        
        # Koordinat untuk diamond shape
        points = [
            x, y - half_size,              # Top
            x + half_size, y,              # Right
            x, y + half_size,              # Bottom
            x - half_size, y               # Left
        ]
        
        # Gambar diamond dengan glow effect
        # Outer glow
        canvas.create_polygon(
            points,
            fill=self.get_color(),
            outline="white",
            width=2,
            tags="powerup"
        )
        
        # Inner highlight
        inner_size = half_size * 0.5
        inner_points = [
            x, y - inner_size,
            x + inner_size, y,
            x, y + inner_size,
            x - inner_size, y
        ]
        canvas.create_polygon(
            inner_points,
            fill="white",
            outline="",
            stipple="gray50",
            tags="powerup"
        )
        
        # Gambar icon sesuai tipe
        self._draw_icon(canvas, x, y, size * 0.4)
    
    def _draw_icon(self, canvas, x, y, size):
        """
        Gambar icon untuk membedakan tipe power-up
        
        Args:
            canvas: Tkinter canvas object
            x (float): Posisi x center
            y (float): Posisi y center
            size (float): Ukuran icon
        """
        if self.__type == self.SPEED_BOOST:
            # Gambar panah untuk speed boost
            canvas.create_text(
                x, y,
                text="⚡",
                font=("Arial", int(size * 2)),
                fill="white",
                tags="powerup"
            )
        elif self.__type == self.SIZE_BOOST:
            # Gambar panah untuk size boost
            canvas.create_text(
                x, y,
                text="⬆",
                font=("Arial", int(size * 2)),
                fill="white",
                tags="powerup"
            )
    
    @staticmethod
    def spawn_random(canvas_width, canvas_height, size=20):
        """
        Static method untuk spawn power-up random
        
        Args:
            canvas_width (float): Lebar canvas
            canvas_height (float): Tinggi canvas
            size (float): Ukuran power-up
            
        Returns:
            PowerUp: Objek PowerUp baru dengan posisi dan tipe random
        """
        # Random posisi di tengah layar (hindari tepi)
        x = random.randint(int(canvas_width * 0.3), int(canvas_width * 0.7))
        y = random.randint(int(canvas_height * 0.2), int(canvas_height * 0.8))
        
        # Random tipe
        powerup_type = random.choice([PowerUp.SPEED_BOOST, PowerUp.SIZE_BOOST])
        
        return PowerUp(x, y, size, powerup_type)