"""
Base class untuk semua objek dalam game (GameObject)
Ini adalah parent class yang akan diwarisi oleh Ball, Paddle, dan PowerUp
Demonstrasi INHERITANCE dan ENCAPSULATION
"""

class GameObject:
    """
    Base class untuk semua objek game
    Menggunakan ENCAPSULATION dengan private attributes
    """
    
    def __init__(self, x, y, width, height, color):
        """
        Constructor untuk GameObject
        
        Args:
            x (float): Posisi x objek
            y (float): Posisi y objek
            width (float): Lebar objek
            height (float): Tinggi objek
            color (str): Warna objek
        """
        # Private attributes (Encapsulation) - gunakan __ untuk private
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__color = color
        self.__active = True  # Status objek apakah masih aktif
    
    # GETTER methods (Encapsulation) - akses ke private attributes
    def get_x(self):
        """Mengambil posisi x objek"""
        return self.__x
    
    def get_y(self):
        """Mengambil posisi y objek"""
        return self.__y
    
    def get_width(self):
        """Mengambil lebar objek"""
        return self.__width
    
    def get_height(self):
        """Mengambil tinggi objek"""
        return self.__height
    
    def get_color(self):
        """Mengambil warna objek"""
        return self.__color
    
    def is_active(self):
        """Mengecek apakah objek masih aktif"""
        return self.__active
    
    # SETTER methods (Encapsulation) - memodifikasi private attributes
    def set_x(self, x):
        """Mengatur posisi x objek"""
        self.__x = x
    
    def set_y(self, y):
        """Mengatur posisi y objek"""
        self.__y = y
    
    def set_width(self, width):
        """Mengatur lebar objek"""
        self.__width = width
    
    def set_height(self, height):
        """Mengatur tinggi objek"""
        self.__height = height
    
    def set_color(self, color):
        """Mengatur warna objek"""
        self.__color = color
    
    def set_active(self, active):
        """Mengatur status aktif objek"""
        self.__active = active
    
    # Method yang akan di-override oleh child classes (Polymorphism)
    def update(self):
        """
        Method untuk update logika objek setiap frame
        Method ini akan di-OVERRIDE oleh child classes
        """
        pass
    
    def draw(self, canvas):
        """
        Method untuk menggambar objek di canvas
        Method ini akan di-OVERRIDE oleh child classes
        
        Args:
            canvas: Tkinter canvas object
        """
        pass
    
    def get_bounds(self):
        """
        Mengambil batas-batas objek untuk collision detection
        
        Returns:
            tuple: (left, top, right, bottom)
        """
        return (
            self.__x,
            self.__y,
            self.__x + self.__width,
            self.__y + self.__height
        )
    
    def collides_with(self, other):
        """
        Mengecek apakah objek ini bertabrakan dengan objek lain
        
        Args:
            other (GameObject): Objek lain yang dicek
            
        Returns:
            bool: True jika bertabrakan, False jika tidak
        """
        left1, top1, right1, bottom1 = self.get_bounds()
        left2, top2, right2, bottom2 = other.get_bounds()
        
        # Collision detection menggunakan AABB (Axis-Aligned Bounding Box)
        return not (right1 < left2 or left1 > right2 or bottom1 < top2 or top1 > bottom2)