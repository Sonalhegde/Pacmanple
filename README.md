# Pac-Man Enhanced Edition

A modern, animated Pac‑Man clone built with **Pygame**.

## ✨ Features
- Dark‑theme UI with black‑purple color scheme
- Animated homepage (pulsing grid, floating Pac‑Man, bouncing title)
- Multiple maze layouts (5 distinct boards, cycling each level)
- Level‑based speed increase (15 % per level)
- Touch‑sensitive navigation (mouse clicks) and keyboard fallback
- Detailed **Instructions** page with clear sections
- **ABOUT US** credits displayed on the home screen
- High‑score tracking (saved to `high_scores.json`, ignored by Git)

## 📦 Prerequisites
- Python 3.13+  
- Pygame 2.6.1 (`pip install pygame`)

## ▶️ Running the Game
```bash
cd c:\Users\sonal\P1\PythonPacman
python game_manager.py
```

## 📂 Project Structure
```
├─ board.py          # Maze definitions
├─ pacman.py         # Core game logic
├─ game_manager.py   # UI, state machine, level handling
├─ high_scores.json  # Persistent scores (git‑ignored)
├─ .gitignore        # Ignores high_scores.json & typical Python files
└─ README.md         # This file
```

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Ensure the UI follows the black‑purple theme.
5. Submit a pull request.

## 📜 License
MIT – feel free to remix and share!

---
Enjoy the game and happy coding! 🎮✨
