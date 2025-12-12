"""
Class Particle untuk efek visual
Tidak inherit dari GameObject karena lebih sederhana
"""

import random
import math

class Particle:
    """
    Class Particle untuk efek visual saat collision
    """
    
    def __init__(self, x, y, color):
        """
        Constructor untuk Particle
        
        Args:
            x (float): Posisi x awal particle
            y (float): Posisi y awal particle
            color (str): Warna particle
        """
        self.__x = x
        self.__y = y
        self.__color = color
        
        # Random velocity untuk setiap particle
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.__velocity_x = math.cos(angle) * speed
        self.__velocity_y = math.sin(angle) * speed
        
        # Properties untuk fade out effect
        self.__lifetime = random.randint(20, 40)  # Berapa frame particle bertahan
        self.__max_lifetime = self.__lifetime
        self.__size = random.uniform(2, 5)
        self.__active = True
    
    def is_active(self):
        """Mengecek apakah particle masih aktif"""
        return self.__active
    
    def update(self):
        """Update posisi dan lifetime particle"""
        if not self.__active:
            return
        
        # Update posisi
        self.__x += self.__velocity_x
        self.__y += self.__velocity_y
        
        # Apply gravity (opsional, untuk efek lebih natural)
        self.__velocity_y += 0.2
        
        # Kurangi lifetime
        self.__lifetime -= 1
        if self.__lifetime <= 0:
            self.__active = False
    
    def draw(self, canvas):
        """
        Gambar particle di canvas
        
        Args:
            canvas: Tkinter canvas object
        """
        if not self.__active:
            return
        
        # Hitung alpha (transparency) berdasarkan lifetime
        alpha_ratio = self.__lifetime / self.__max_lifetime
        
        # Size yang mengecil seiring waktu
        current_size = self.__size * alpha_ratio
        
        # Gambar particle sebagai oval kecil
        canvas.create_oval(
            self.__x - current_size,
            self.__y - current_size,
            self.__x + current_size,
            self.__y + current_size,
            fill=self.__color,
            outline="",
            tags="particle"
        )


class ParticleSystem:
    """
    Class untuk mengelola banyak particle sekaligus
    """
    
    def __init__(self):
        """Constructor untuk ParticleSystem"""
        self.__particles = []
    
    def emit(self, x, y, color, count=10):
        """
        Emit (keluarkan) particles dari posisi tertentu
        
        Args:
            x (float): Posisi x emisi
            y (float): Posisi y emisi
            color (str): Warna particles
            count (int): Jumlah particles yang dikeluarkan
        """
        for _ in range(count):
            particle = Particle(x, y, color)
            self.__particles.append(particle)
    
    def update(self):
        """Update semua particles"""
        # Update dan hapus particle yang tidak aktif
        self.__particles = [p for p in self.__particles if p.is_active()]
        
        for particle in self.__particles:
            particle.update()
    
    def draw(self, canvas):
        """
        Gambar semua particles
        
        Args:
            canvas: Tkinter canvas object
        """
        for particle in self.__particles:
            particle.draw(canvas)
    
    def clear(self):
        """Hapus semua particles"""
        self.__particles.clear()
    
    def get_particle_count(self):
        """Mengambil jumlah particles aktif"""
        return len(self.__particles)