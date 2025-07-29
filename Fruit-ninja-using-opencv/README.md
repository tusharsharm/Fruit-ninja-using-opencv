🍉 Fruit Ninja - Webcam Edition (Python)
Control the game with your bare hands. Slice flying fruits using your webcam and finger tracking in real-time. It’s Fruit Ninja — but you are the controller.

📦 Overview
A real-time slicing game powered by:

Python

Pygame for rendering and sound

OpenCV for webcam handling

MediaPipe for hand tracking

NumPy for video frame processing

All you need is a webcam and ninja reflexes.

🎮 Features
- 🔪 Slice fruits with your fingers using your webcam

- 🎨 Motion-blurred blade trails (with alpha blending)
 
- 🍉 Fruits split into left/right halves when hit
 
- 💥 Bombs end the game — avoid them!
 
- 💫 Combo system — slice multiple fruits quickly to gain bonus points
 
- ⏸ Pause menu, game over screen, and restart option
 
- 🔊 Sound effects for slicing, combos, and explosions
 
- 📹 Webcam preview displayed in-game

🧠 Tech Stack
| Tool      | Purpose                         |
| --------- | ------------------------------- |
| Python    | Core logic and game engine      |
| Pygame    | Rendering, sound, main loop     |
| OpenCV    | Camera capture & image tweaks   |
| MediaPipe | Hand/finger landmark tracking   |
| NumPy     | Frame conversion and processing |


📁 Folder Structure
fruit-ninja/
├── assets/              # Game images
│   ├── apple.png
│   ├── apple-1.png
│   ├── apple-2.png
│   └── background.jpg
├── sounds/              # Sound effects
│   ├── slice.wav
│   ├── explode.wav
│   └── music.mp3
├── main.py  # Main game logic
├── fruit.py             # Fruit and fruit halves logic
├── hand_detector.py     # Hand tracking module
├── README.md            # This file


🧩 How It Works
1. OpenCV grabs webcam frames and enhances them

2. MediaPipe tracks your hand and fingertip positions

2. The tips of your fingers (index, middle, ring, pinky) become slicing blades

4. If a fruit collides with your fingers, it gets sliced in half

5. Combo streaks and missed fruits affect your score
All motion, slicing, scoring, trails, and physics are rendered live via Pygame.

🔧 Setup

1. Clone the Repository
` git clone https://github.com/yourusername/fruit-ninja-webcam.git `
` cd fruit-ninja-webcam`

` pip install pygame opencv-python mediapipe numpy`

2. Run the Game
` python main.py`

🎯 Controls
| Key     | Action                  |
| ------- | ----------------------- |
| `SPACE` | Start game from menu    |
| `P`     | Pause / Resume          |
| `R`     | Restart after game over |
| `ESC`   | Quit the game           |


📄 requirements.txt
pygame
opencv-python
mediapipe
numpy

