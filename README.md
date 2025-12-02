




# PAC-MAN CLASSIC EDITION - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation & Setup](#installation--setup)
3. [File Structure](#file-structure)
4. [Code Architecture](#code-architecture)
5. [Detailed Function Explanations](#detailed-function-explanations)
6. [Game Mechanics](#game-mechanics)
7. [Troubleshooting](#troubleshooting)

---

## Project Overview

**PAC-MAN CLASSIC EDITION** is a modern recreation of the classic arcade game built with Python and Pygame. This implementation features:

- **Multiple Levels**: Two distinct maze layouts with increasing difficulty
- **Smart AI Ghosts**: Four ghosts with unique movement patterns
- **High Score System**: Persistent storage of top 5 scores
- **Modern UI**: Animated menus, pause functionality, and responsive controls
- **Level Selection**: Choose your starting level
- **Power-ups**: Eat power pellets to turn the tables on ghosts

### Development Team

- **SONAL HEGDE** -<img width="751" height="760" alt="image" src="https://github.com/user-attachments/assets/f00c173e-0c6d-4bae-acce-d546c558e125" />

<img width="2378" height="1136" alt="image" src="https://github.com/user-attachments/assets/afe64397-f2c2-4021-8cee-27c8e9788ce6" />

---

## Installation & Setup

### Prerequisites
- **Python 3.7 or higher** (Tested on Python 3.13.2)
- **Pygame library** (Version 2.6.1 or higher)

### Step-by-Step Installation

#### 1. Install Python
Download and install Python from [python.org](https://www.python.org/downloads/)

**Verify installation:**
```bash
python --version
```

#### 2. Clone the Repository
```bash
git clone https://github.com/Sonalhegde/Pacmanple.git
cd Pacmanple
```

**OR Download ZIP:**
- Go to https://github.com/Sonalhegde/Pacmanple
- Click "Code" → "Download ZIP"
- Extract to your desired location

#### 3. Install Pygame
```bash
pip install pygame
```

**Verify Pygame installation:**
```bash
python -c "import pygame; print(pygame.version.ver)"
```

#### 4. Run the Game
```bash
python game_manager.py
```

### Alternative: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install pygame

# Run the game
python game_manager.py
```

---

## File Structure

```
PythonPacman/
│
├── game_manager.py      # Main game controller and menu system
├── pacman.py           # Core game logic, player, and ghost AI
├── board.py            # Maze layouts and board definitions
├── high_scores.json    # Persistent high score storage (auto-generated)
├── README.md           # Project overview
├── DOCUMENTATION.md    # This file
├── .gitignore         # Git ignore rules
│
└── assets/ (if present)
    └── (game assets like images)
```

### File Descriptions

#### **game_manager.py** (Main Controller)
- Manages game states (menu, playing, instructions, etc.)
- Handles all UI screens (homepage, levels, high scores, about)
- Controls game flow and level progression
- Manages high score persistence

#### **pacman.py** (Game Engine)
- Contains core game loop
- Player movement and collision detection
- Ghost AI and pathfinding
- Power-up mechanics
- Drawing functions for game entities

#### **board.py** (Level Data)
- Defines maze layouts using 2D arrays
- Contains two board configurations (Classic and Open)
- Board element encoding (walls, dots, power pellets, gates)

#### **high_scores.json** (Data Storage)
- Stores top 5 high scores
- JSON format: `[{"name": "ABC", "score": 1000}, ...]`
- Automatically created on first run

---

## Code Architecture

### State Management System

The game uses a **state machine** pattern with 8 distinct states:

```python
STATE_MENU = 1           # Main menu
STATE_PLAYING = 2        # Active gameplay
STATE_INSTRUCTIONS = 3   # How to play screen
STATE_HIGHSCORES = 4     # High score display
STATE_GAMEOVER = 5       # Game over state
STATE_NEW_HIGHSCORE = 6  # High score entry
STATE_LEVELS = 7         # Level selection
STATE_ABOUT = 8          # About us screen
```

### Game Flow Diagram

```
┌─────────────┐
│  Main Menu  │
└──────┬──────┘
       │
       ├──→ Start Game ──→ Level 1 ──→ Level 2 ──→ ...
       │                      │
       │                      ├──→ Game Over ──→ High Score Entry
       │                      └──→ Victory ──→ Next Level
       │
       ├──→ Level Select ──→ Choose Level ──→ Start Game
       │
       ├──→ Instructions ──→ View Controls ──→ Back
       │
       ├──→ High Scores ──→ View Top 5 ──→ Back
       │
       ├──→ About Us ──→ View Credits ──→ Back
       │
       └──→ Exit Game
```

---

## Detailed Function Explanations

### **game_manager.py**

#### Class: `GameManager`

**Purpose:** Central controller for the entire game application.

##### **`__init__(self)`**
```python
def __init__(self):
    self.state = STATE_MENU
    self.running = True
    self.high_scores = self.load_high_scores()
    self.current_score = 0
    self.current_level = 1
    self.current_lives = 3
    self.input_name = ""
```
**Explanation:**
- Initializes game state to main menu
- Loads existing high scores from JSON file
- Sets default values for score, level, and lives
- Prepares name input buffer for high score entry

##### **`load_high_scores(self)`**
```python
def load_high_scores(self):
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []
```
**Explanation:**
- Checks if `high_scores.json` exists
- Attempts to load and parse JSON data
- Returns empty list if file doesn't exist or is corrupted
- **Error Handling:** Catches JSON parse errors gracefully

##### **`save_high_scores(self)`**
```python
def save_high_scores(self):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump(self.high_scores, f)
```
**Explanation:**
- Writes current high scores to JSON file
- Overwrites existing file
- Called after new high score is added

##### **`draw_menu(self)`**
**Purpose:** Renders the main menu with animated elements.

**Key Features:**
- **Animated Grid Background:** Pulsing grid pattern using sine waves
- **Animated Pac-Man:** Floating character with chomping mouth animation
- **Glowing Title:** "PAC-MAN" with multi-layer glow effect
- **Interactive Buttons:** 6 buttons with hover effects and floating animation
- **Team Credits:** Version info at bottom

**Animation Math:**
```python
# Grid animation
time_offset = pygame.time.get_ticks() * 0.001
alpha = int(abs(math.sin(time_offset + i * 0.01)) * 30 + 20)

# Pac-Man floating
pac_x = int((math.sin(pac_time * 0.5) + 1) * (WIDTH - 100) / 2 + 50)

# Button floating
float_offset = math.sin(pygame.time.get_ticks() * 0.002 + idx * 0.8) * 3
```

##### **`draw_levels(self)`**
**Purpose:** Displays level selection screen.

**Features:**
- Two level options: "LEVEL 1 (Classic)" and "LEVEL 2 (Open)"
- Hover effects on buttons
- Back button to return to menu

##### **`draw_instructions(self)`**
**Purpose:** Shows game instructions and controls.

**Sections:**
1. **Objective:** Game goals
2. **Controls:** Keyboard mappings
3. **Power-ups:** Dot and pellet descriptions
4. **Ghosts:** Individual ghost behaviors
5. **Levels:** Difficulty progression

##### **`draw_high_scores(self)`**
**Purpose:** Displays top 5 high scores.

**Features:**
- Ranked display with colored medals (Gold, Silver, Bronze)
- Shows player name and score
- "No high scores yet!" message if empty
- Sorted by score (descending)

##### **`draw_new_highscore(self)`**
**Purpose:** Allows player to enter name for new high score.

**Features:**
- Displays achieved score
- Text input box with blinking cursor
- Max 10 alphanumeric characters
- Real-time input display

**Input Handling:**
```python
if event.key == pygame.K_RETURN:
    # Save score
elif event.key == pygame.K_BACKSPACE:
    # Delete character
else:
    if len(self.input_name) < 10 and event.unicode.isalnum():
        # Add character
```

##### **`draw_about(self)`**
**Purpose:** Shows team information and project details.

**Content:**
- Project title
- Development team members with IDs
- Project description
- Technology stack

##### **`start_game(self)`**
**Purpose:** Main game loop controller.

**Flow:**
1. Initialize game variables (lives, score)
2. Load appropriate board based on level
3. Calculate speed multiplier (increases 15% per level)
4. Call `pacman.play_level()` to run level
5. Handle result (VICTORY, GAMEOVER, QUIT)
6. Progress to next level or end game

**Level-to-Board Mapping:**
```python
if self.current_level == 1:
    board_index = 0  # board1 (Classic)
elif self.current_level == 2:
    board_index = 1  # board2 (Open)
else:
    board_index = (self.current_level - 1) % 2  # Cycle
```

**Speed Progression:**
```python
speed_mult = 1.0 + (self.current_level - 1) * 0.15
# Level 1: 1.0x speed
# Level 2: 1.15x speed
# Level 3: 1.30x speed
```

##### **`check_high_score(self)`**
**Purpose:** Determines if current score qualifies for high score board.

**Logic:**
```python
if len(self.high_scores) < 5:
    is_high = True  # Always qualifies if less than 5 scores
else:
    min_score = min(s['score'] for s in self.high_scores)
    if self.current_score > min_score:
        is_high = True  # Beats lowest score
```

##### **`run(self)`**
**Purpose:** Main application loop.

**Structure:**
```python
while self.running:
    if self.state == STATE_MENU:
        # Handle menu
    elif self.state == STATE_LEVELS:
        # Handle level selection
    elif self.state == STATE_INSTRUCTIONS:
        # Handle instructions
    # ... etc for all states
```

**Event Handling:**
- Mouse clicks for button interactions
- Keyboard shortcuts (1-6 for menu options)
- ESC key to return to menu from sub-screens

---

### **pacman.py**

#### Global Variables

```python
# Display
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Game State
score = 0
lives = 3
level = []  # Current board layout
powerup = False
game_over = False
game_won = False

# Player
player_x = 450
player_y = 663
direction = 0  # 0=right, 1=left, 2=up, 3=down

# Ghosts
blinky_x, blinky_y = 56, 58
inky_x, inky_y = 440, 388
pinky_x, pinky_y = 440, 438
clyde_x, clyde_y = 440, 438
```

#### Class: `Ghost`

**Purpose:** Represents a ghost enemy with AI movement.

##### **`__init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id)`**
```python
def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
    self.x_pos = x_coord
    self.y_pos = y_coord
    self.center_x = self.x_pos + 22
    self.center_y = self.y_pos + 22
    self.target = target
    self.speed = speed
    self.img = img
    self.direction = direct
    self.dead = dead
    self.in_box = box
    self.id = id
    self.turns, self.in_box = self.check_collisions()
    self.rect = self.draw()
```
**Parameters:**
- `x_coord, y_coord`: Starting position
- `target`: Target coordinates to move towards
- `speed`: Movement speed (pixels per frame)
- `img`: Ghost sprite image
- `direct`: Current direction (0-3)
- `dead`: Whether ghost is in "eaten" state
- `box`: Whether ghost is in spawn box
- `id`: Ghost identifier (0-3)

##### **`draw(self)`**
**Purpose:** Renders ghost sprite based on current state.

**States:**
1. **Normal:** Display ghost's color sprite
2. **Vulnerable:** Display blue "spooked" sprite (during power-up)
3. **Eaten:** Display eyes sprite (returning to spawn)

```python
if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup):
    screen.blit(self.img, (self.x_pos, self.y_pos))
elif powerup and not self.dead and not eaten_ghost[self.id]:
    screen.blit(spooked_img, (self.x_pos, self.y_pos))
else:
    screen.blit(dead_img, (self.x_pos, self.y_pos))
```

##### **`check_collisions(self)`**
**Purpose:** Determines valid movement directions for ghost.

**Returns:** `[right, left, up, down]` boolean array

**Logic:**
- Checks board tiles around ghost position
- Allows movement through empty spaces (0, 1, 2)
- Special handling for spawn gate (9) when dead or in box
- Considers ghost's current direction for smooth turning

##### **`move_blinky(self)`, `move_inky(self)`, `move_pinky(self)`, `move_clyde(self)`**
**Purpose:** Individual movement AI for each ghost.

**Blinky (Red) - The Chaser:**
- Directly targets Pac-Man's position
- Most aggressive ghost
- Uses shortest path algorithm

**Inky (Cyan) - The Ambusher:**
- Targets position ahead of Pac-Man
- Works in tandem with Blinky
- Unpredictable movement

**Pinky (Pink) - The Interceptor:**
- Targets 4 tiles ahead of Pac-Man
- Tries to cut off escape routes
- Strategic positioning

**Clyde (Orange) - The Random:**
- Alternates between chasing and fleeing
- Becomes unpredictable when close to Pac-Man
- Patrol behavior

**Movement Algorithm:**
```python
# Calculate distance to target
x_dist = abs(self.target[0] - self.center_x)
y_dist = abs(self.target[1] - self.center_y)

# Choose direction that reduces distance
if x_dist > y_dist and self.turns[0]:  # Move right
    self.direction = 0
elif y_dist > x_dist and self.turns[2]:  # Move up
    self.direction = 2
# ... etc
```

#### Core Functions

##### **`draw_board()`**
**Purpose:** Renders the maze layout.

**Board Encoding:**
```python
0 = Empty space (black)
1 = Small dot (10 points)
2 = Power pellet (50 points)
3 = Vertical wall
4 = Horizontal wall
5 = Top-right corner
6 = Top-left corner
7 = Bottom-left corner
8 = Bottom-right corner
9 = Ghost spawn gate
```

**Drawing Logic:**
```python
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == 1:  # Small dot
            pygame.draw.circle(screen, 'white', (j * num3 + (0.5 * num3), i * num1 + (0.5 * num1)), 4)
        elif level[i][j] == 2 and not flicker:  # Power pellet (animated)
            pygame.draw.circle(screen, 'white', (j * num3 + (0.5 * num3), i * num1 + (0.5 * num1)), 10)
        # ... wall drawing logic
```

##### **`draw_player()`**
**Purpose:** Renders Pac-Man with mouth animation.

**Animation:**
- Cycles through 4 sprite images
- Rotates based on direction
- Mouth opens and closes

```python
if direction == 0:  # Right
    screen.blit(player_images[counter // 5], (player_x, player_y))
elif direction == 1:  # Left
    screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
# ... etc
```

##### **`draw_misc()`**
**Purpose:** Renders HUD elements.

**Elements:**
- **Score:** Top-left, colorful cyan value
- **Lives:** Center-top, Pac-Man icons
- **Level:** Below score, yellow text
- **Power-up indicator:** Blue circle when active

```python
# Colorful Score
score_label = font.render('Score:', True, 'white')
score_value = font.render(f'{score}', True, (0, 255, 255))  # Cyan

# Lives (centered)
for i in range(lives):
    screen.blit(pygame.transform.scale(player_images[0], (30, 30)), 
                (WIDTH // 2 - 45 + i * 40, 10))

# Level Indicator
level_text = font.render(f'Lvl: {current_level_display}', True, (255, 255, 0))
```

##### **`check_position(centerx, centery)`**
**Purpose:** Determines valid movement directions for Pac-Man.

**Returns:** `[right, left, up, down]` boolean array

**Logic:**
- Checks tiles around Pac-Man's center position
- Allows movement through spaces < 3 (empty, dots, pellets)
- Prevents movement into walls
- Enables smooth turning at intersections

##### **`move_player(play_x, play_y)`**
**Purpose:** Updates Pac-Man's position based on direction.

**Movement:**
```python
if direction == 0 and turns_allowed[0]:  # Right
    play_x += player_speed
elif direction == 1 and turns_allowed[1]:  # Left
    play_x -= player_speed
elif direction == 2 and turns_allowed[2]:  # Up
    play_y -= player_speed
elif direction == 3 and turns_allowed[3]:  # Down
    play_y += player_speed
```

**Tunnel Wrapping:**
```python
if player_x > 900:
    player_x = -47  # Wrap to left
elif player_x < -50:
    player_x = 897  # Wrap to right
```

##### **`check_collisions(scor, power, power_count, eaten_ghosts, cx, cy)`**
**Purpose:** Detects Pac-Man eating dots and pellets.

**Logic:**
```python
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == 1:  # Small dot
            if circle.colliderect(objects[num]):
                level[i][j] = 0  # Remove dot
                scor += 10
        elif level[i][j] == 2:  # Power pellet
            if circle.colliderect(objects[num]):
                level[i][j] = 0
                scor += 50
                power = True
                power_count = 0
                eaten_ghosts = [False, False, False, False]
```

##### **`get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y)`**
**Purpose:** Calculates target positions for each ghost.

**Power-up Mode:**
- Ghosts flee to corners
- Eaten ghosts return to spawn box

**Normal Mode:**
- Each ghost targets Pac-Man or strategic positions
- Blinky: Direct chase
- Inky: Ambush from side
- Pinky: Intercept ahead
- Clyde: Random patrol

```python
if powerup:
    if not blinky.dead and not eaten_ghost[0]:
        blink_target = (runaway_x, runaway_y)  # Flee
    elif not blinky.dead and eaten_ghost[0]:
        blink_target = (400, 100)  # Return to spawn
else:
    blink_target = (player_x, player_y)  # Chase
```

##### **`play_level(speed_mult=1.0, extra_ghosts=0, board_index=0, level_num=1)`**
**Purpose:** Main game loop for a single level.

**Parameters:**
- `speed_mult`: Speed multiplier for difficulty
- `extra_ghosts`: (Unused) For future expansion
- `board_index`: Which board layout to use (0 or 1)
- `level_num`: Current level number for display

**Game Loop Structure:**
```python
while run:
    timer.tick(fps)  # 60 FPS
    
    # 1. Update counters and timers
    # 2. Draw board and entities
    # 3. Draw pause button
    # 4. Handle pause state
    # 5. Check win condition
    # 6. Move player and ghosts
    # 7. Check collisions
    # 8. Handle ghost-player collisions
    # 9. Process input events
    # 10. Update display
```

**Pause System:**
```python
if paused:
    # Draw overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 50, 200))
    
    # Draw pause menu
    # - PAUSED title
    # - RESUME button
    # - QUIT button
    
    # Handle pause events only
    continue  # Skip game logic
```

**Win Condition:**
```python
game_won = True
for i in range(len(level)):
    if 1 in level[i] or 2 in level[i]:
        game_won = False
        break

if game_won:
    return "VICTORY"
```

**Ghost-Player Collision:**
```python
if not powerup:
    if player_circle.colliderect(ghost.rect) and not ghost.dead:
        if lives > 0:
            lives -= 1
            # Reset positions
        else:
            return "GAMEOVER"
else:  # Power-up active
    if player_circle.colliderect(ghost.rect) and not ghost.dead:
        ghost_dead = True
        score += (2 ** eaten_ghost.count(True)) * 100
```

---

### **board.py**

#### Board Layouts

##### **board1 (Classic Maze)**
```python
board1 = [
    [6, 4, 4, 4, ...],  # 33 rows
    # ... 30 columns
]
```
**Features:**
- Traditional Pac-Man maze design
- Balanced difficulty
- Multiple pathways and corners
- Central ghost spawn area

##### **board2 (Open Maze)**
```python
board2 = [
    [6, 4, 4, 4, ...],  # 33 rows
    # ... 30 columns
]
```
**Features:**
- More open spaces
- Fewer walls
- Faster gameplay
- Strategic power pellet placement

**Modifications:**
```python
# Remove some inner walls for more open gameplay
board2[9] = [3, 3, 1, 1, 1, ...]  # More dots, fewer walls
board2[27] = [3, 3, 1, 1, 1, ...]
```

##### **all_boards**
```python
all_boards = [board1, board2, board1, board2, board1]
```
**Purpose:** Array of boards for level progression
- Cycles between two layouts
- Can be expanded for more variety

---

## Game Mechanics

### Scoring System

| Action | Points |
|--------|--------|
| Small Dot | 10 |
| Power Pellet | 50 |
| 1st Ghost (Power-up) | 200 |
| 2nd Ghost (Power-up) | 400 |
| 3rd Ghost (Power-up) | 800 |
| 4th Ghost (Power-up) | 1600 |

**Ghost Score Formula:**
```python
score += (2 ** eaten_ghost.count(True)) * 100
```

### Lives System

- **Starting Lives:** 3
- **Lose Life:** Collision with ghost (when not powered up)
- **Game Over:** When lives reach 0
- **No Extra Lives:** (Could be added as feature)

### Power-up Mechanics

**Duration:** 600 frames (~10 seconds at 60 FPS)

**Effects:**
1. Ghosts turn blue and flee
2. Pac-Man can eat ghosts
3. Eaten ghosts return to spawn
4. Score multiplier for consecutive ghost captures

**Timer:**
```python
if powerup and power_counter < 600:
    power_counter += 1
elif powerup and power_counter >= 600:
    power_counter = 0
    powerup = False
    eaten_ghost = [False, False, False, False]
```

### Level Progression

**Speed Increase:** 15% per level
```python
Level 1: 1.00x speed
Level 2: 1.15x speed
Level 3: 1.30x speed
Level 4: 1.45x speed
...
```

**Board Rotation:**
- Odd levels: Classic maze (board1)
- Even levels: Open maze (board2)

### Ghost AI Behavior

**States:**
1. **Chase:** Normal behavior, hunt Pac-Man
2. **Scatter:** Retreat to corners (during power-up)
3. **Eaten:** Return to spawn box
4. **In Box:** Wait before exiting

**Pathfinding:**
- Uses Manhattan distance to target
- Chooses direction that minimizes distance
- Avoids reversing direction when possible
- Special handling for spawn box gate

### Collision Detection

**Pac-Man vs Walls:**
```python
turns_allowed = check_position(center_x, center_y)
# Only move if turn is allowed
```

**Pac-Man vs Dots:**
```python
if circle.colliderect(dot_rect):
    level[i][j] = 0  # Remove dot
    score += 10
```

**Pac-Man vs Ghosts:**
```python
if player_circle.colliderect(ghost.rect):
    if powerup and not ghost.dead:
        # Eat ghost
    elif not powerup:
        # Lose life
```

---

## Controls

### Gameplay
- **Arrow Keys:** Move Pac-Man (Up, Down, Left, Right)
- **SPACE:** Pause/Resume game
- **ESC:** Pause/Resume game or return to menu

### Menu Navigation
- **Mouse Click:** Select buttons
- **Keyboard Shortcuts:**
  - `1` - Start Game
  - `2` - Level Select
  - `3` - Instructions
  - `4` - High Scores
  - `5` - About Us
  - `6` - Exit Game

### High Score Entry
- **Alphanumeric Keys:** Enter name (max 10 characters)
- **BACKSPACE:** Delete character
- **ENTER:** Save score

---

## Troubleshooting

### Common Issues

#### 1. **"ModuleNotFoundError: No module named 'pygame'"**
**Solution:**
```bash
pip install pygame
```

#### 2. **Game runs too fast/slow**
**Solution:** Check FPS setting in `pacman.py`
```python
fps = 60  # Adjust if needed
timer = pygame.time.Clock()
```

#### 3. **High scores not saving**
**Check:**
- File permissions in game directory
- `high_scores.json` is not read-only
- Sufficient disk space

**Manual fix:**
```bash
# Delete corrupted file
del high_scores.json

# Game will create new one on next run
```

#### 4. **Graphics not displaying correctly**
**Solution:**
- Update graphics drivers
- Try different display mode:
```python
# In pacman.py, change:
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
```

#### 5. **Game crashes on start**
**Debug steps:**
```bash
# Run with error output
python game_manager.py 2> error.log

# Check error.log for details
```

### Performance Optimization

**If game lags:**
1. Reduce FPS: `fps = 30`
2. Disable animations in menu
3. Close other applications
4. Check CPU usage

---

## Advanced Customization

### Adding New Levels

**1. Create new board in `board.py`:**
```python
board3 = [
    [6, 4, 4, ...],
    # Your custom layout
]

# Add to rotation
all_boards = [board1, board2, board3]
```

**2. Update level selection in `game_manager.py`:**
```python
levels = [
    {"text": "LEVEL 1 (Classic)", "y": 300, "level": 1},
    {"text": "LEVEL 2 (Open)", "y": 400, "level": 2},
    {"text": "LEVEL 3 (Custom)", "y": 500, "level": 3},
]
```

### Modifying Ghost Speed

**In `pacman.py`:**
```python
# Adjust base speed
base_speed = 2 * speed_mult  # Change 2 to desired value

# Adjust power-up speed
if powerup:
    ghost_speeds = [1 * speed_mult, ...]  # Change 1 to desired value
```

### Changing Colors

**Menu colors in `game_manager.py`:**
```python
# Background
screen.fill((10, 10, 15))  # RGB values

# Button colors
pygame.draw.rect(screen, (50, 80, 160), btn_rect)  # Change RGB
```

**Game colors in `pacman.py`:**
```python
# Pac-Man color
pygame.draw.circle(screen, (255, 255, 0), ...)  # Yellow

# Dot color
pygame.draw.circle(screen, 'white', ...)  # Can use color names
```

---

## Credits & License

### Development Team
- 
- **SONAL HEGDE** - NNM24AC050
-

### Technology Stack
- **Python 3.13.2**
- **Pygame 2.6.1**
- **JSON** for data storage
- **Math** for animations

### Repository
- **GitHub:** https://github.com/Sonalhegde/Pacmanple
- **Version:** 1.0 Enhanced Edition

### License
This project is created for educational purposes.

---

## Future Enhancements

### Planned Features
- [ ] Sound effects and background music
- [ ] Fruit bonuses
- [ ] More ghost AI patterns
- [ ] Multiplayer mode
- [ ] Mobile touch controls
- [ ] Web version using Pygbag
- [ ] Leaderboard with online sync
- [ ] Achievement system
- [ ] Custom maze editor

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Contact & Support

For questions, issues, or suggestions:
- **GitHub Issues:** https://github.com/Sonalhegde/Pacmanple/issues
- **Email:** Contact through GitHub profile

---

**Last Updated:** November 27, 2024
**Documentation Version:** 1.0
>>>>>>> d5dc95705f314893b1e392c0fd304574e950d057
