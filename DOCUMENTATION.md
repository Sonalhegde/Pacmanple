# Pac-Man Cyberpunk Edition - Technical Documentation

## 1. Project Overview
**Pac-Man Cyberpunk Edition** is a modern reimagining of the classic arcade game, built using Python and the Pygame library. It features a distinct "Cyberpunk" visual style with neon colors, glitch effects, and chamfered UI elements. The game includes a complete menu system, multiple levels, high score persistence, and sophisticated ghost AI.

### Technology Stack
*   **Language**: Python 3.x
*   **Library**: Pygame (for rendering, input handling, and audio)
*   **Data Format**: JSON (for high scores)

---

## 2. System Architecture
The project is structured into three main modules:

1.  **`game_manager.py`**: The application controller. It manages the global game state (menus, transitions), UI rendering, and the main application loop.
2.  **`pacman.py`**: The game engine. It contains the core gameplay logic, physics, collision detection, AI, and level rendering.
3.  **`board.py`**: The data layer. It stores the level layouts as 2D integer arrays.

---

## 3. Module Details

### 3.1 Game Manager (`game_manager.py`)
This module is responsible for the "meta-game" experience.

#### Class: `GameManager`
*   **State Management**: Uses an integer-based state machine (`STATE_MENU`, `STATE_PLAYING`, etc.) to switch between different screens.
*   **`__init__`**: Initializes Pygame, loads high scores from `high_scores.json`, and initializes the background particle system.
*   **`run()`**: The main entry point. It contains the primary event loop that delegates drawing and input handling to specific methods based on the current state.

#### Key Functions:
*   **`draw_background()`**: Renders the dynamic Cyberpunk background.
    *   **Logic**: Draws a grid, moving floating particles (with alpha fading), and pulsing concentric circles in the center.
*   **`draw_cyber_panel(rect, ...)`**: A helper function to draw UI panels.
    *   **Style**: Uses `pygame.draw.polygon` to create chamfered (cut) corners and adds "tech" accent lines for a futuristic look.
*   **`start_game()`**: Transitions from the menu to gameplay.
    *   **Logic**: Calls `pacman.play_level()` and waits for a return value.
    *   **Return Handling**:
        *   `"QUIT"`: Exits the application.
        *   `"GAMEOVER"`: Shows Game Over screen (handled in `pacman.py`), then checks high scores.
        *   `"VICTORY"`: Increments level and loops to start the next level.
        *   `"RESTART"`: Restarts the current level immediately.
        *   `"MENU"`: Returns to the main menu.

### 3.2 Game Engine (`pacman.py`)
This module handles the actual gameplay.

#### Core Loop: `play_level()`
This function runs the game frame-by-frame (60 FPS).
1.  **Initialization**: Resets player/ghost positions and randomizes bonus points (`randomize_bonuses`).
2.  **Event Handling**: Listens for Quit, Pause, and Movement inputs.
3.  **Update Phase**:
    *   Updates Player position (`move_player`).
    *   Updates Ghost positions (`move_blinky`, etc.) based on their AI.
    *   Checks collisions (`check_collisions`).
4.  **Render Phase**: Draws the board, player, ghosts, and HUD (`draw_misc`).
5.  **Pause Menu**: Renders a semi-transparent overlay with Resume, Restart, Menu, and Quit options when paused.

#### Ghost AI & Algorithms
The ghosts use a target-tile pathfinding system. They calculate the Euclidean distance to their target from all available neighboring tiles and choose the one with the shortest distance. They cannot reverse direction unless entering "Frightened" mode.

*   **Blinky (Red)**:
    *   **Target**: The player's current tile.
    *   **Behavior**: Aggressive chase.
*   **Pinky (Pink)**:
    *   **Target**: 4 tiles *in front* of the player's current direction.
    *   **Behavior**: Ambush / Intercept.
*   **Inky (Blue)**:
    *   **Target**: Calculated using a vector. It takes the vector from Blinky to 2 tiles in front of the player, and doubles it.
    *   **Behavior**: Unpredictable / Flanking.
*   **Clyde (Orange)**:
    *   **Target**: The player, *unless* Clyde is within 8 tiles of the player, in which case his target becomes his "scatter corner" (bottom-left).
    *   **Behavior**: Chase and Retreat.

#### Bonus Randomization: `randomize_bonuses()`
*   **Goal**: Shuffle Power Pellet positions to add variety.
*   **Algorithm**:
    1.  Identifies all valid "Dot" and "Power Pellet" positions.
    2.  Shuffles the list of valid spots.
    3.  Selects new spots for Power Pellets, enforcing a **minimum Euclidean distance of 10 tiles** between them to ensure even distribution.
    4.  Updates the `level` grid.

### 3.3 Board Data (`board.py`)
*   **Structure**: A list of lists (2D array) representing the grid.
*   **Encoding**:
    *   `0`: Empty Space
    *   `1`: Small Dot
    *   `2`: Power Pellet (Big Dot)
    *   `3`: Vertical Wall
    *   `4`: Horizontal Wall
    *   `5-8`: Corner Walls
    *   `9`: Ghost House Gate

---

## 4. Game Rules & Logic

### Movement & Physics
*   **Grid-Based**: Movement is constrained to the grid. Entities can only turn if the center of their sprite aligns with the center of a tile and the target tile is not a wall.
*   **Speed**:
    *   Player: Constant base speed.
    *   Ghosts: Base speed increases slightly with each level (`speed_mult`).
    *   Frightened Mode: Ghosts slow down significantly.
    *   Dead Mode: Ghosts move very fast (4x) to return to the ghost house.

### Scoring System
*   **Small Dot**: 10 points.
*   **Power Pellet**: 50 points.
*   **Ghost (eaten)**: 200, 400, 800, 1600 points (doubles for each consecutive ghost eaten per power pellet).

### Game States
*   **Power Mode**: Activated when eating a Power Pellet. Lasts for 600 frames (10 seconds). Ghosts turn blue and flee.
*   **Game Over**: Occurs when Lives reach 0.
*   **Victory**: Occurs when all dots (1s and 2s) are cleared from the board.

---

## 5. UI/UX Design (Cyberpunk Edition)
The UI was overhauled to match a Cyberpunk aesthetic.

*   **Colors**: High-contrast palette.
    *   Cyber Yellow (`#FCEE0A`)
    *   Cyber Blue (`#00F0FF`)
    *   Cyber Pink (`#FF003C`)
    *   Dark Background (`#05050A`)
*   **Visual Elements**:
    *   **Chamfered Panels**: UI boxes have cut corners instead of rounded ones.
    *   **Glitch Text**: The main title features a layered offset effect.
    *   **Particles**: Floating digital bits in the background.
    *   **Scanlines**: Subtle horizontal lines to simulate a CRT monitor.
