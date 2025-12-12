"""
Pong Game Manager - Class utama yang mengelola seluruh game
Demonstrasi penggunaan COMPOSITION dan orchestration berbagai class OOP
"""

import tkinter as tk
from ball import Ball
from paddle import Paddle
from powerup import PowerUp
from particle import ParticleSystem
from sound_manager import SoundManager
import random

class PongGame:
    """
    Main Game Manager yang mengatur semua komponen game
    Menggunakan COMPOSITION: menggabungkan objek Ball, Paddle, PowerUp, dll
    """
    
    # Konstanta game
    WIDTH = 800
    HEIGHT = 600
    FPS = 60  # Frame per second
    WINNING_SCORE = 5
    POWERUP_SPAWN_CHANCE = 0.003  # 0.3% chance per frame
    
    # Warna tema modern dengan gradasi
    BG_COLOR = "#0a0e27"
    ACCENT_COLOR = "#00d4ff"
    
    def __init__(self, root):
        """
        Constructor untuk PongGame
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("PONG GAME - OOP Project")
        self.root.resizable(False, False)
        
        # Setup canvas dengan warna modern
        self.canvas = tk.Canvas(
            root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Game state
        self.__game_state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER
        self.__player1_score = 0
        self.__player2_score = 0
        self.__winner = None
        
        # Inisialisasi game objects
        self._init_game_objects()
        
        # Sound manager
        self.sound_manager = SoundManager()
        
        # Particle system untuk efek visual
        self.particle_system = ParticleSystem()
        
        # Power-up system
        self.__current_powerup = None
        self.__powerup_timer = 0
        self.__powerup_duration = 180  # 3 detik (60 fps * 3)
        self.__powerup_active_player = None  # 1 atau 2
        
        # Key bindings
        self._setup_controls()
        
        # UI Elements
        self._create_ui()
        
        # Game loop
        self.__game_running = False
        self.__update_id = None
    
    def _init_game_objects(self):
        """Inisialisasi semua game objects (Ball dan Paddle)"""
        # Buat Ball di tengah layar
        self.ball = Ball(
            x=self.WIDTH / 2,
            y=self.HEIGHT / 2,
            radius=10,
            color=self.ACCENT_COLOR,
            speed=5
        )
        
        # Buat Paddle 1 (kiri)
        self.paddle1 = Paddle(
            x=30,
            y=self.HEIGHT / 2 - 50,
            width=15,
            height=100,
            color="#FF6B6B",
            speed=7
        )
        self.paddle1.set_screen_height(self.HEIGHT)
        
        # Buat Paddle 2 (kanan)
        self.paddle2 = Paddle(
            x=self.WIDTH - 45,
            y=self.HEIGHT / 2 - 50,
            width=15,
            height=100,
            color="#4ECDC4",
            speed=7
        )
        self.paddle2.set_screen_height(self.HEIGHT)
    
    def _setup_controls(self):
        """Setup keyboard controls untuk kedua pemain"""
        # Player 1 controls (W/S) - support both lowercase and uppercase
        self.root.bind('<w>', lambda e: self.paddle1.move_up())
        self.root.bind('<W>', lambda e: self.paddle1.move_up())
        self.root.bind('<s>', lambda e: self.paddle1.move_down())
        self.root.bind('<S>', lambda e: self.paddle1.move_down())
        self.root.bind('<KeyRelease-w>', lambda e: self.paddle1.stop())
        self.root.bind('<KeyRelease-W>', lambda e: self.paddle1.stop())
        self.root.bind('<KeyRelease-s>', lambda e: self.paddle1.stop())
        self.root.bind('<KeyRelease-S>', lambda e: self.paddle1.stop())
        
        # Player 2 controls (Up/Down arrows)
        self.root.bind('<Up>', lambda e: self.paddle2.move_up())
        self.root.bind('<Down>', lambda e: self.paddle2.move_down())
        self.root.bind('<KeyRelease-Up>', lambda e: self.paddle2.stop())
        self.root.bind('<KeyRelease-Down>', lambda e: self.paddle2.stop())
        
        # Game controls
        self.root.bind('<space>', lambda e: self._toggle_pause())
        self.root.bind('<Return>', lambda e: self._handle_enter())
        self.root.bind('<Escape>', lambda e: self._back_to_menu())
        self.root.bind('<m>', lambda e: self.sound_manager.toggle())
    
    def _create_ui(self):
        """Buat UI elements (scores, menu, dll)"""
        # Title untuk menu
        self.title_text = self.canvas.create_text(
            self.WIDTH / 2, 150,
            text="PONG",
            font=("Arial", 80, "bold"),
            fill=self.ACCENT_COLOR,
            tags="menu"
        )
        
        # Subtitle
        self.subtitle_text = self.canvas.create_text(
            self.WIDTH / 2, 250,
            text="Player vs Player",
            font=("Arial", 24),
            fill="white",
            tags="menu"
        )
        
        # Instructions
        self.instructions_text = self.canvas.create_text(
            self.WIDTH / 2, 350,
            text="Player 1: W/S | Player 2: ↑/↓\n\nPress ENTER to Start\nSPACE to Pause | ESC to Menu | M to Toggle Sound",
            font=("Arial", 16),
            fill="gray",
            justify="center",
            tags="menu"
        )
        
        # Score displays (hidden di menu)
        self.score1_text = self.canvas.create_text(
            self.WIDTH / 4, 50,
            text="0",
            font=("Arial", 48, "bold"),
            fill="#FF6B6B",
            state="hidden"
        )
        
        self.score2_text = self.canvas.create_text(
            self.WIDTH * 3 / 4, 50,
            text="0",
            font=("Arial", 48, "bold"),
            fill="#4ECDC4",
            state="hidden"
        )
        
        # Center line
        for i in range(0, self.HEIGHT, 20):
            self.canvas.create_rectangle(
                self.WIDTH / 2 - 2, i,
                self.WIDTH / 2 + 2, i + 10,
                fill="white",
                outline="",
                stipple="gray50",
                tags="game_ui"
            )
        self.canvas.itemconfig("game_ui", state="hidden")
        
        # Pause text
        self.pause_text = self.canvas.create_text(
            self.WIDTH / 2, self.HEIGHT / 2,
            text="PAUSED\n\nPress SPACE to Resume",
            font=("Arial", 36, "bold"),
            fill="white",
            justify="center",
            state="hidden"
        )
        
        # Game over text
        self.gameover_text = self.canvas.create_text(
            self.WIDTH / 2, self.HEIGHT / 2,
            text="",
            font=("Arial", 48, "bold"),
            fill=self.ACCENT_COLOR,
            justify="center",
            state="hidden"
        )
    
    def _handle_enter(self):
        """Handle tombol ENTER"""
        if self.__game_state == "MENU":
            self.start_game()
        elif self.__game_state == "GAME_OVER":
            self._reset_game()
            self.__game_state = "PLAYING"
            self.__game_running = True
            self._hide_menu()
            self.canvas.itemconfig(self.gameover_text, state="hidden")
            self.sound_manager.play_game_start()
            self._game_loop()  # Restart game loop
    
    def _toggle_pause(self):
        """Toggle pause game"""
        if self.__game_state == "PLAYING":
            self.__game_state = "PAUSED"
            self.canvas.itemconfig(self.pause_text, state="normal")
        elif self.__game_state == "PAUSED":
            self.__game_state = "PLAYING"
            self.canvas.itemconfig(self.pause_text, state="hidden")
    
    def _back_to_menu(self):
        """Kembali ke menu utama"""
        self.__game_running = False
        if self.__update_id:
            self.root.after_cancel(self.__update_id)
        self.__game_state = "MENU"
        self._reset_game()
        self._show_menu()
    
    def _show_menu(self):
        """Tampilkan menu utama"""
        self.canvas.itemconfig("menu", state="normal")
        self.canvas.itemconfig("game_ui", state="hidden")
        self.canvas.itemconfig(self.score1_text, state="hidden")
        self.canvas.itemconfig(self.score2_text, state="hidden")
        self.canvas.itemconfig(self.pause_text, state="hidden")
        self.canvas.itemconfig(self.gameover_text, state="hidden")
    
    def _hide_menu(self):
        """Sembunyikan menu utama"""
        self.canvas.itemconfig("menu", state="hidden")
        self.canvas.itemconfig("game_ui", state="normal")
        self.canvas.itemconfig(self.score1_text, state="normal")
        self.canvas.itemconfig(self.score2_text, state="normal")
    
    def start_game(self):
        """Mulai game"""
        self.__game_state = "PLAYING"
        self.__game_running = True
        self._hide_menu()
        self.sound_manager.play_game_start()
        self._game_loop()
    
    def _reset_game(self):
        """Reset game ke kondisi awal"""
        # Cancel existing game loop jika ada
        if self.__update_id:
            self.root.after_cancel(self.__update_id)
            self.__update_id = None
        
        self.__player1_score = 0
        self.__player2_score = 0
        self.__winner = None
        
        # Reset ball position
        self.ball.reset_position(self.WIDTH / 2, self.HEIGHT / 2)
        
        # Reset paddle positions
        self.paddle1.reset_position(30, self.HEIGHT / 2 - 50)
        self.paddle2.reset_position(self.WIDTH - 45, self.HEIGHT / 2 - 50)
        
        # Clear power-up
        self.__current_powerup = None
        self.__powerup_timer = 0
        self.__powerup_active_player = None
        
        # Clear particles
        self.particle_system.clear()
        
        # Update score display
        self._update_score_display()
    
    def _reset_ball(self):
        """Reset ball ke tengah setelah score"""
        self.ball.reset_position(self.WIDTH / 2, self.HEIGHT / 2)
        # Set ball inactive sementara
        self.ball.set_active(False)
        
        # Pause sebentar sebelum ball bergerak lagi (tapi loop tetap jalan)
        def reactivate_ball():
            self.ball.set_active(True)
        
        self.root.after(1000, reactivate_ball)
    
    def _update_score_display(self):
        """Update tampilan score"""
        self.canvas.itemconfig(self.score1_text, text=str(self.__player1_score))
        self.canvas.itemconfig(self.score2_text, text=str(self.__player2_score))
    
    def _check_scoring(self):
        """Cek apakah ada yang score"""
        ball_x = self.ball.get_x()
        
        # Player 2 scores (ball keluar kiri)
        if ball_x < 0:
            self.__player2_score += 1
            self._update_score_display()
            self.sound_manager.play_score()
            self._create_score_particles(0, self.HEIGHT / 2, "#4ECDC4")
            self._reset_ball()
            self._check_game_over()
            return True
        
        # Player 1 scores (ball keluar kanan)
        if ball_x > self.WIDTH:
            self.__player1_score += 1
            self._update_score_display()
            self.sound_manager.play_score()
            self._create_score_particles(self.WIDTH, self.HEIGHT / 2, "#FF6B6B")
            self._reset_ball()
            self._check_game_over()
            return True
        
        return False
    
    def _check_game_over(self):
        """Cek apakah game sudah selesai"""
        if self.__player1_score >= self.WINNING_SCORE:
            self.__winner = 1
            self._game_over()
        elif self.__player2_score >= self.WINNING_SCORE:
            self.__winner = 2
            self._game_over()
    
    def _game_over(self):
        """Handle game over"""
        self.__game_state = "GAME_OVER"
        self.__game_running = False
        
        winner_color = "#FF6B6B" if self.__winner == 1 else "#4ECDC4"
        self.canvas.itemconfig(
            self.gameover_text,
            text=f"PLAYER {self.__winner} WINS!\n\nPress ENTER to Play Again\nESC for Menu",
            fill=winner_color,
            state="normal"
        )
        
        self.sound_manager.play_game_over()
    
    def _create_score_particles(self, x, y, color):
        """Buat particle effect saat score"""
        self.particle_system.emit(x, y, color, count=30)
    
    def _check_wall_collision(self):
        """Cek collision dengan dinding atas/bawah"""
        ball_y = self.ball.get_y()
        ball_radius = self.ball.get_radius()
        
        # Collision dengan dinding atas
        if ball_y - ball_radius < 0:
            self.ball.set_y(ball_radius)
            self.ball.reverse_y()
            self.sound_manager.play_wall_hit()
            self.particle_system.emit(self.ball.get_x(), 0, self.ACCENT_COLOR, count=8)
            return True
        
        # Collision dengan dinding bawah
        if ball_y + ball_radius > self.HEIGHT:
            self.ball.set_y(self.HEIGHT - ball_radius)
            self.ball.reverse_y()
            self.sound_manager.play_wall_hit()
            self.particle_system.emit(self.ball.get_x(), self.HEIGHT, self.ACCENT_COLOR, count=8)
            return True
        
        return False
    
    def _check_paddle_collision(self):
        """Cek collision dengan paddle"""
        # Collision dengan paddle 1
        if self.ball.collides_with(self.paddle1) and self.ball.get_velocity_x() < 0:
            self.ball.bounce_off_paddle(self.paddle1)
            self.sound_manager.play_paddle_hit()
            self.particle_system.emit(
                self.paddle1.get_x() + self.paddle1.get_width(),
                self.ball.get_y(),
                "#FF6B6B",
                count=10
            )
            return True
        
        # Collision dengan paddle 2
        if self.ball.collides_with(self.paddle2) and self.ball.get_velocity_x() > 0:
            self.ball.bounce_off_paddle(self.paddle2)
            self.sound_manager.play_paddle_hit()
            self.particle_system.emit(
                self.paddle2.get_x(),
                self.ball.get_y(),
                "#4ECDC4",
                count=10
            )
            return True
        
        return False
    
    def _spawn_powerup(self):
        """Spawn power-up secara random"""
        if self.__current_powerup is None and random.random() < self.POWERUP_SPAWN_CHANCE:
            self.__current_powerup = PowerUp.spawn_random(self.WIDTH, self.HEIGHT)
    
    def _check_powerup_collection(self):
        """Cek apakah ada yang mengambil power-up"""
        if self.__current_powerup is None or not self.__current_powerup.is_active():
            return
        
        # Cek collision dengan ball
        if self.ball.collides_with(self.__current_powerup):
            powerup_type = self.__current_powerup.get_type()
            self.__current_powerup.collect()
            self.sound_manager.play_powerup_collect()
            
            # Tentukan siapa yang dapat power-up berdasarkan arah bola
            if self.ball.get_velocity_x() > 0:
                # Bola ke kanan, player 2 dapat power-up
                self.__powerup_active_player = 2
                if powerup_type == PowerUp.SPEED_BOOST:
                    self.ball.set_speed_boost(1.5)
                elif powerup_type == PowerUp.SIZE_BOOST:
                    self.paddle2.set_size_boost(1.5)
            else:
                # Bola ke kiri, player 1 dapat power-up
                self.__powerup_active_player = 1
                if powerup_type == PowerUp.SPEED_BOOST:
                    self.ball.set_speed_boost(1.5)
                elif powerup_type == PowerUp.SIZE_BOOST:
                    self.paddle1.set_size_boost(1.5)
            
            self.__powerup_timer = self.__powerup_duration
            
            # Particle effect
            self.particle_system.emit(
                self.__current_powerup.get_x(),
                self.__current_powerup.get_y(),
                self.__current_powerup.get_color(),
                count=20
            )
    
    def _update_powerup(self):
        """Update power-up timer dan reset jika habis"""
        if self.__powerup_timer > 0:
            self.__powerup_timer -= 1
            if self.__powerup_timer == 0:
                # Reset power-up effects
                self.ball.reset_speed_boost()
                self.paddle1.reset_size_boost()
                self.paddle2.reset_size_boost()
                self.__powerup_active_player = None
    
    def _game_loop(self):
        """Main game loop yang berjalan setiap frame"""
        # Cek apakah game masih running dan dalam state PLAYING
        if not self.__game_running:
            return
            
        if self.__game_state != "PLAYING":
            # Jika paused atau state lain, schedule ulang dan return
            self.__update_id = self.root.after(1000 // self.FPS, self._game_loop)
            return
        
        # Update game objects
        self.ball.update()
        self.paddle1.update()
        self.paddle2.update()
        
        # Update power-up
        if self.__current_powerup and self.__current_powerup.is_active():
            self.__current_powerup.update()
        
        self._update_powerup()
        self._spawn_powerup()
        self._check_powerup_collection()
        
        # Update particle system
        self.particle_system.update()
        
        # Check collisions
        self._check_wall_collision()
        self._check_paddle_collision()
        self._check_scoring()
        
        # Render everything
        self._render()
        
        # Schedule next frame
        self.__update_id = self.root.after(1000 // self.FPS, self._game_loop)
    
    def _render(self):
        """Render semua objek ke canvas"""
        # Clear canvas (hapus semua objek game, kecuali UI)
        self.canvas.delete("ball", "paddle", "powerup", "particle")
        
        # Draw game objects
        self.ball.draw(self.canvas)
        self.paddle1.draw(self.canvas)
        self.paddle2.draw(self.canvas)
        
        # Draw power-up
        if self.__current_powerup and self.__current_powerup.is_active():
            self.__current_powerup.draw(self.canvas)
        
        # Draw particles
        self.particle_system.draw(self.canvas)
    
    def run(self):
        """Jalankan aplikasi"""
        self.root.mainloop()