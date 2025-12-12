import tkinter as tk
from pong_game import PongGame

def main():
    """
    Fungsi utama untuk menjalankan game
    """
    # Buat Tkinter root window
    root = tk.Tk()
    
    # Buat instance PongGame
    game = PongGame(root)
    
    # Jalankan game
    game.run()

if __name__ == "__main__":
    main()