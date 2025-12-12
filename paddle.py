"""
Class Paddle - Mewarisi dari GameObject
Demonstrasi INHERITANCE dan POLYMORPHISM
"""

from game_object import GameObject

class Paddle(GameObject):
    """
    Class Paddle yang mewarisi dari GameObject (INHERITANCE)
    Menambahkan fitur khusus untuk paddle seperti movement dan size boost
    """
    
    def __init__(self, x, y, width, height, color, speed):
        """
        Constructor untuk Paddle
        
        Args:
            x (float): Posisi x paddle
            y (float): Posisi y paddle
            width (float): Lebar paddle
            height (float): Tinggi paddle
            color (str): Warna paddle
            speed (float): Kecepatan gerak paddle
        """
        # Panggil constructor parent class (GameObject)
        super().__init__(x, y, width, height, color)
        
        # Private attributes khusus untuk Paddle
        self.__speed = speed
        self.__base_height = height  # Simpan tinggi dasar untuk reset
        self.__velocity_y = 0  # Kecepatan vertikal saat ini
        self.__size_boost = 1.0  # Multiplier untuk power-up ukuran
        self.__screen_height = 600  # Default screen height, akan di-set dari game
    
    # GETTER methods khusus Paddle
    def get_speed(self):
        """Mengambil kecepatan paddle"""
        return self.__speed
    
    def get_velocity_y(self):
        """Mengambil velocity vertikal paddle"""
        return self.__velocity_y
    
    def get_base_height(self):
        """Mengambil tinggi dasar paddle"""
        return self.__base_height
    
    # SETTER methods khusus Paddle
    def set_screen_height(self, height):
        """
        Set tinggi layar untuk boundary checking
        
        Args:
            height (float): Tinggi layar
        """
        self.__screen_height = height
    
    def set_size_boost(self, boost):
        """
        Mengatur multiplier ukuran paddle (untuk power-up)
        
        Args:
            boost (float): Multiplier ukuran (1.0 = normal, 1.5 = 50% lebih besar)
        """
        self.__size_boost = boost
        new_height = self.__base_height * boost
        
        # Update tinggi paddle
        self.set_height(new_height)
        
        # Adjust posisi agar paddle tidak keluar layar
        if self.get_y() + new_height > self.__screen_height:
            self.set_y(self.__screen_height - new_height)
    
    def reset_size_boost(self):
        """Reset ukuran paddle ke normal"""
        self.set_size_boost(1.0)
    
    def move_up(self):
        """Gerakkan paddle ke atas"""
        self.__velocity_y = -self.__speed
    
    def move_down(self):
        """Gerakkan paddle ke bawah"""
        self.__velocity_y = self.__speed
    
    def stop(self):
        """Hentikan gerakan paddle"""
        self.__velocity_y = 0
    
    def update(self):
        """
        Override method update dari GameObject (POLYMORPHISM)
        Update posisi paddle berdasarkan velocity dan boundary checking
        """
        if not self.is_active():
            return
        
        # Update posisi y berdasarkan velocity
        new_y = self.get_y() + self.__velocity_y
        
        # Boundary checking - pastikan paddle tidak keluar layar
        if new_y < 0:
            new_y = 0
        elif new_y + self.get_height() > self.__screen_height:
            new_y = self.__screen_height - self.get_height()
        
        self.set_y(new_y)
    
    def draw(self, canvas):
        """
        Override method draw dari GameObject (POLYMORPHISM)
        Menggambar paddle sebagai rectangle dengan efek gradasi
        
        Args:
            canvas: Tkinter canvas object
        """
        if not self.is_active():
            return
        
        x = self.get_x()
        y = self.get_y()
        width = self.get_width()
        height = self.get_height()
        
        # Gambar paddle dengan rounded corners
        canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=self.get_color(),
            outline="white",
            width=2,
            tags="paddle"
        )
        
        # Tambahkan highlight untuk efek 3D
        canvas.create_rectangle(
            x + 2, y + 2, x + width - 2, y + height / 2,
            fill="white",
            outline="",
            stipple="gray50",
            tags="paddle"
        )
    
    def reset_position(self, x, y):
        """
        Reset posisi paddle ke koordinat tertentu
        
        Args:
            x (float): Posisi x baru
            y (float): Posisi y baru
        """
        self.set_x(x)
        self.set_y(y)
        self.stop()
        self.reset_size_boost()