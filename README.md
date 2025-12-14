# 🏓 Pong Game OOP – Python Tkinter
Game Pong klasik yang diimplementasikan menggunakan Python dan Tkinter dengan penerapan konsep **Object-Oriented Programming (OOP)** secara lengkap. Game ini menghadirkan dua paddle yang saling berkompetisi memantulkan bola dan mencetak skor dengan berbagai efek visual dan power-up menarik.
---

## 📋 Deskripsi Project
Proyek ini merupakan implementasi game Pong yang dibangun dengan pendekatan OOP menggunakan Python. Seluruh fitur utama permainan seperti movement, collision, score system, power-up, dan visual effect diatur melalui sistem class yang modular serta mudah dikembangkan.
---

## 🎯 Tujuan Pembelajaran
* Menerapkan **Encapsulation** (pembungkusan data)
* Menerapkan **Inheritance** (pewarisan class)
* Menerapkan **Polymorphism** (banyak bentuk)
* Mengimplementasikan game loop dan collision detection
* Membangun aplikasi interaktif dengan GUI Tkinter
---

## 🎮 Fitur Utama

### **Gameplay**
* ✔ Player vs Player mode
* ✔ Sistem skor dengan target kemenangan **5 poin**
* ✔ **Power-ups**

  * ⚡ *Speed Boost*: meningkatkan kecepatan bola
  * ⬆ *Size Boost*: memperbesar paddle
* ✔ Collision detection untuk paddle, bola, dan dinding

### **Visual Effects**
* ✔ Particle Effects saat collision dan scoring
* ✔ Modern UI dengan warna gradasi
* ✔ Smooth animation (60 FPS)

### **Audio**   
* ✔ Efek suara pantulan
* ✔ Efek suara dinding
* ✔ Efek suara scoring
* ✔ Efek suara power-up

### **Menu & Controls**
* ✔ Main Menu
* ✔ Pause System
* ✔ Game Over Screen
* ✔ Sound Toggle

---

## 🎮 Cara Bermain

### **Kontrol Pemain**
| Player                      | Gerak Up       | Gerak Down       |
| --------------------------- | -------------- | ---------------- |
| **Player 1 (Kiri - Merah)** | **W**          | **S**            |
| **Player 2 (Kanan - Cyan)** | **↑ Arrow Up** | **↓ Arrow Down** |

### **Kontrol Game**
| Tombol    | Fungsi                 |
| --------- | ---------------------- |
| **ENTER** | Mulai game / Main lagi |
| **SPACE** | Pause / Resume         |
| **ESC**   | Kembali ke menu        |
| **M**     | Toggle sound           |

### **Aturan Main**
* Bola harus dipantulkan menggunakan paddle
* Jika bola melewati sisi musuh, pemain mendapat **1 poin**
* Pemain pertama yang mencapai **5 poin** adalah pemenang
* Power-up akan muncul secara acak dan memberikan efek khusus

---

## 🏗 Struktur Project

```
pong-game/
├── main.py                 # Entry point aplikasi
├── pong_game.py           # Game manager utama
├── game_object.py         # Base class untuk semua objek
├── ball.py                # Class Ball
├── paddle.py              # Class Paddle
├── powerup.py             # Class PowerUp
├── particle.py            # Class Particle & ParticleSystem
├── sound_manager.py       # Class SoundManager
└── README.md              # Dokumentasi ini
```

---

## 💻 Cara Menjalankan

### **Requirements**
* Python **3.7 atau lebih tinggi**
* Tkinter (sudah termasuk di Python)
* Windows OS untuk dukungan sound optimal

### **Langkah Menjalankan**
```bash
# Clone repository
git clone [URL_REPOSITORY_ANDA]
cd pong-game
```

Periksa semua file sudah ada, kemudian jalankan:
```bash
python main.py
```

Mulai bermain dengan **ENTER**.
---

## 🔧 Troubleshooting

### ❌ *ModuleNotFoundError: No module named 'tkinter'*
Solusi:
* Pastikan Python sudah terinstall lengkap
* Gunakan Python dari website resmi (python.org)
* Pada Linux, install Tkinter secara manual:

  ```bash
  sudo apt install python3-tk
  ```

### ❌ Tidak ada suara?
* Tekan **M** untuk toggle sound
* Periksa volume sistem

---

## 🎓 Konsep OOP yang Diterapkan

### **1. Encapsulation (Pembungkusan)**
* Menggunakan atribut privat `__attribute`
* Akses melalui getter dan setter
* Digunakan pada class: `GameObject`, `Ball`, `Paddle`

### **2. Inheritance (Pewarisan)**
* `Ball`, `Paddle`, dan `PowerUp` mewarisi dari `GameObject`
* Child class memiliki sifat parent class + perilaku khusus

### **3. Polymorphism (Banyak Bentuk)**
* Method `update()` dan `draw()` di-override di setiap child class
* Tiap objek memiliki perilaku berbeda walaupun method-nya sama
---

## 📊 Class Diagram
Lihat file **class_diagram.png** untuk visual lengkap.
Struktur inheritance utama:
```
GameObject
├── Ball
├── Paddle
└── PowerUp
```

Sedangkan `PongGame` bertindak sebagai manager yang menggunakan:
* Ball
* Dua Paddle
* PowerUp
* ParticleSystem
* SoundManager
---
