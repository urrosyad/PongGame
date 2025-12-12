
📋 Deskripsi Project
Game Pong klasik yang diimplementasikan menggunakan Python dan Tkinter dengan penerapan konsep Object-Oriented Programming (OOP) yang lengkap. Game ini menampilkan dua paddle yang dikontrol oleh dua pemain untuk memantulkan bola dan mencetak skor.

Tujuan Pembelajaran
Menerapkan prinsip Encapsulation (pembungkusan data)
Menerapkan prinsip Inheritance (pewarisan class)
Menerapkan prinsip Polymorphism (banyak bentuk)
Mengimplementasikan game loop dan collision detection
Membuat aplikasi interaktif dengan GUI

🎯 Fitur Utama
Gameplay
✅ Player vs Player Mode: Dua pemain dapat bermain secara bersamaan
✅ Scoring System: Sistem skor dengan target kemenangan 5 poin
✅ Power-ups:
Speed Boost (⚡): Mempercepat bola
Size Boost (⬆): Memperbesar paddle
✅ Collision Detection: Deteksi tabrakan akurat untuk bola, paddle, dan dinding
Visual Effects
✅ Particle Effects: Efek partikel saat collision dan scoring
✅ Modern UI: Desain dengan warna gradasi modern
✅ Smooth Animation: 60 FPS gameplay yang smooth
Audio

✅ Sound Effects:
Suara pantulan paddle
Suara pantulan dinding
Suara scoring
Suara power-up collection

Menu & Controls
✅ Main Menu: Menu awal dengan instruksi
✅ Pause System: Sistem pause/resume
✅ Game Over Screen: Layar game over dengan pemenang
🎮 Cara Bermain

Kontrol
Player 1 (Kiri - Merah):
W: Gerak ke atas
S: Gerak ke bawah
Player 2 (Kanan - Cyan):
↑ (Arrow Up): Gerak ke atas
↓ (Arrow Down): Gerak ke bawah

Kontrol Game
ENTER: Mulai game / Main lagi setelah game over
SPACE: Pause/Resume game
ESC: Kembali ke menu utama
M: Toggle sound on/off

Aturan
Pemain menggerakkan paddle untuk memantulkan bola
Jika bola melewati paddle lawan, pemain mendapat 1 poin
Pemain pertama yang mencapai 5 poin menang
Power-up muncul secara random - ambil dengan bola untuk efek khusus

🏗️ Struktur Project
pong-game/
├── main.py                 # Entry point aplikasi
├── pong_game.py           # Game manager utama
├── game_object.py         # Base class untuk semua objek
├── ball.py                # Class Ball
├── paddle.py              # Class Paddle
├── powerup.py             # Class PowerUp
├── particle.py            # Class Particle & ParticleSystem
├── sound_manager.py       # Class SoundManager
└──  README.md              # Dokumentasi ini

💻 Cara Menjalankan
Requirements
Python 3.7 atau lebih tinggi
Tkinter (sudah included dalam Python)
Windows OS (untuk sound effects optimal)
Langkah-langkah
Clone atau Download project
bash
   # Jika menggunakan git
   git clone [URL_REPOSITORY_ANDA]
   cd pong-game

Pastikan semua file ada
Periksa bahwa semua 8 file Python ada di folder yang sama
Jalankan game
bash
   python main.py

Mulai bermain!
Tekan ENTER untuk mulai
Gunakan kontrol sesuai panduan di atas
Troubleshooting
Problem: "ModuleNotFoundError: No module named 'tkinter'"

Solusi: Install tkinter
bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  
  # Fedora
  sudo dnf install python3-tkinter
  
  # Windows/Mac: Tkinter sudah included
Problem: Sound tidak berbunyi

Solusi: Tekan M untuk toggle sound atau pastikan volume sistem tidak mute
🎓 Konsep OOP yang Diterapkan
1. Encapsulation (Pembungkusan) ✅
Semua class menggunakan private attributes dengan prefix __
Akses ke attributes dilakukan melalui getter dan setter methods
Contoh di GameObject, Ball, Paddle
2. Inheritance (Pewarisan) ✅
Ball, Paddle, dan PowerUp mewarisi dari GameObject
Child class mendapat semua attributes dan methods dari parent
Child class dapat menambahkan fitur spesifik mereka
3. Polymorphism (Banyak Bentuk) ✅
Method update() dan draw() di-override oleh setiap child class
Setiap objek memiliki implementasi berbeda untuk method yang sama
Demonstrasi di Ball.update(), Paddle.update(), PowerUp.update()
📊 Class Diagram
Lihat file class_diagram.png untuk diagram lengkap.

Struktur Inheritance:

GameObject (parent)
├── Ball (child)
├── Paddle (child)
└── PowerUp (child)

PongGame (manager)
├── uses: Ball
├── uses: Paddle (2 instances)
├── uses: PowerUp
├── uses: ParticleSystem
└── uses: SoundManager
