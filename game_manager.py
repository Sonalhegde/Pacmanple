import pygame
import pacman
import json
import os
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 900
HEIGHT = 950
screen = pacman.screen
font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 20)
title_font = pygame.font.Font('freesansbold.ttf', 90)
sub_font = pygame.font.Font('freesansbold.ttf', 30)
btn_font = pygame.font.Font('freesansbold.ttf', 32)
footer_font = pygame.font.Font('freesansbold.ttf', 16)
version_font = pygame.font.Font('freesansbold.ttf', 13)
info_font = pygame.font.Font('freesansbold.ttf', 28)
credit_font = pygame.font.Font('freesansbold.ttf', 22)
desc_font = pygame.font.Font('freesansbold.ttf', 20)
section_font = pygame.font.Font('freesansbold.ttf', 24)
inst_font = pygame.font.Font('freesansbold.ttf', 18)
score_font = pygame.font.Font('freesansbold.ttf', 32)
large_score_font = pygame.font.Font('freesansbold.ttf', 40)
prompt_font = pygame.font.Font('freesansbold.ttf', 28)
input_font = pygame.font.Font('freesansbold.ttf', 45)
level_font = pygame.font.Font('freesansbold.ttf', 80)
header_font = pygame.font.Font('freesansbold.ttf', 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
CYBER_YELLOW = (252, 238, 10)
CYBER_BLUE = (0, 240, 255)
CYBER_PINK = (255, 0, 60)
DARK_BG = (5, 5, 10)

# States
STATE_MENU = 1
STATE_PLAYING = 2
STATE_INSTRUCTIONS = 3
STATE_HIGHSCORES = 4
STATE_GAMEOVER = 5
STATE_NEW_HIGHSCORE = 6
STATE_LEVELS = 7
STATE_ABOUT = 8

HIGH_SCORE_FILE = "high_scores.json"

class GameManager:
    def __init__(self):
        self.state = STATE_MENU
        self.running = True
        self.high_scores = self.load_high_scores()
        self.current_score = 0
        self.current_level = 1
        self.current_lives = 3
        self.input_name = ""
        
        # Background Particles
        self.particles = []
        for i in range(50):
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.2, 1.5),
                'size': random.randint(2, 4),
                'color': random.choice([CYBER_BLUE, CYBER_PINK, CYBER_YELLOW, (50, 50, 50)])
            })

    def load_high_scores(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_high_scores(self):
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump(self.high_scores, f)

    def draw_background(self):
        screen.fill(DARK_BG)
        
        # Animated Cyber Circles
        time_ticks = pygame.time.get_ticks()
        center = (WIDTH // 2, HEIGHT // 2)
        
        # Outer pulsing ring
        radius1 = 350 + math.sin(time_ticks * 0.001) * 10
        pygame.draw.circle(screen, (15, 20, 30), center, int(radius1), 2)
        
        # Inner rotating gaps ring (simulated with arcs)
        radius2 = 280
        angle_offset = time_ticks * 0.0005
        for i in range(0, 360, 45):
            start_angle = math.radians(i) + angle_offset
            end_angle = math.radians(i + 30) + angle_offset
            pygame.draw.arc(screen, (20, 30, 40), 
                          (center[0] - radius2, center[1] - radius2, radius2 * 2, radius2 * 2), 
                          start_angle, end_angle, 4)

        # Cyber Grid
        grid_color = (20, 25, 35)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y), 1)
            
        # Draw Particles
        for p in self.particles:
            p['y'] -= p['speed']
            if p['y'] < 0:
                p['y'] = HEIGHT
                p['x'] = random.randint(0, WIDTH)
                
            # Draw particle with alpha
            # Since pygame.draw doesn't support alpha directly on screen, use a temp surface
            s = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            alpha = int(100 + 155 * (p['y'] / HEIGHT)) # Fade out at top
            s.fill((*p['color'], alpha))
            screen.blit(s, (p['x'], p['y']))

        # Scanlines
        for y in range(0, HEIGHT, 4):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y), 1)

    def draw_cyber_panel(self, rect, color=(20, 20, 30), alpha=240, border_color=CYBER_BLUE, border_width=2):
        # Chamfered corners
        cut = 20
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        
        points = [
            (x + cut, y), (x + w, y), (x + w, y + h - cut),
            (x + w - cut, y + h), (x, y + h), (x, y + cut)
        ]
        
        # Background
        shape_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        local_points = [
            (cut, 0), (w, 0), (w, h - cut),
            (w - cut, h), (0, h), (0, cut)
        ]
        pygame.draw.polygon(shape_surf, (*color, alpha), local_points)
        screen.blit(shape_surf, (x, y))
        
        # Border
        pygame.draw.polygon(screen, border_color, points, border_width)
        
        # Tech accents
        pygame.draw.line(screen, border_color, (x + cut, y + 5), (x + w // 3, y + 5), 1)
        pygame.draw.line(screen, border_color, (x + w - cut, y + h - 5), (x + w - w // 3, y + h - 5), 1)

    def draw_text_centered(self, text, font, color, y_offset):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
        # Drop shadow
        shadow = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, y_offset + 2))
        screen.blit(shadow, shadow_rect)
        screen.blit(text_surface, text_rect)

    def draw_menu(self):
        self.draw_background()
        
        # Glitch Title
        title_text = "PAC-MAN"
        
        # Glitch layers
        offset_x = 4
        screen.blit(title_font.render(title_text, True, CYBER_PINK), (WIDTH//2 - 200 + offset_x, 100))
        screen.blit(title_font.render(title_text, True, CYBER_BLUE), (WIDTH//2 - 200 - offset_x, 100))
        
        # Main Title
        title_surf = title_font.render(title_text, True, CYBER_YELLOW)
        screen.blit(title_surf, (WIDTH//2 - 200, 100))
        
        # Subtitle
        sub_text = sub_font.render("CLASSIC EDITION", True, CYBER_BLUE)
        screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, 200))

        # Menu Buttons
        buttons = [
            {"text": "START GAME", "y": 300, "icon": "▶"},
            {"text": "LEVELS", "y": 390, "icon": "☰"},
            {"text": "INSTRUCTIONS", "y": 480, "icon": "ℹ"},
            {"text": "HIGH SCORES", "y": 570, "icon": "★"},
            {"text": "ABOUT US", "y": 660, "icon": "👥"},
            {"text": "EXIT GAME", "y": 750, "icon": "✕"}
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in buttons:
            rect = pygame.Rect(WIDTH // 2 - 200, btn["y"], 400, 70)
            is_hover = rect.collidepoint(mouse_pos)
            
            # Button Style
            if is_hover:
                self.draw_cyber_panel(rect, color=(252, 238, 10), alpha=255, border_color=WHITE)
                text_color = BLACK
            else:
                self.draw_cyber_panel(rect, color=(20, 20, 30), border_color=CYBER_BLUE)
                text_color = CYBER_BLUE
                
            # Text
            text_surf = btn_font.render(f"{btn['icon']}  {btn['text']}", True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

        # Footer
        footer = footer_font.render("v2.0 | Remastered UI", True, (100, 100, 150))
        screen.blit(footer, (WIDTH//2 - footer.get_width()//2, 900))
        
        pygame.display.flip()

    def draw_about(self):
        self.draw_background()
        
        # Title
        self.draw_text_centered("ABOUT US", header_font, CYBER_YELLOW, 80)
        
        # Content Panel
        panel_rect = pygame.Rect(WIDTH // 2 - 350, 150, 700, 550)
        self.draw_cyber_panel(panel_rect, border_color=CYBER_PINK)
        
        # Team info
        y_pos = 200
        
        # Project title
        project_title = info_font.render("PAC-MAN CYBERPUNK", True, CYBER_BLUE)
        screen.blit(project_title, (WIDTH//2 - project_title.get_width()//2, y_pos))
        y_pos += 60
        
        # Team section
        team_title = info_font.render("DEVELOPMENT TEAM", True, CYBER_YELLOW)
        screen.blit(team_title, (WIDTH//2 - team_title.get_width()//2, y_pos))
        y_pos += 50
        
        # Team members
        credits = [
            "SIDDHARTH R - NNM24AC049",
            "SONAL HEGDE - NNM24AC050",
            "SOUMYA SM - NNM24AC051"
        ]
        
        for credit in credits:
            credit_text = credit_font.render(credit, True, (200, 200, 255))
            screen.blit(credit_text, (WIDTH//2 - credit_text.get_width()//2, y_pos))
            y_pos += 40
        
        y_pos += 80
        
        # Description
        descriptions = [
            "A modern recreation of the classic arcade game",
            "Built with Python and Pygame",
            "Features multiple levels, high scores, and smooth gameplay"
        ]
        
        for desc in descriptions:
            desc_text = desc_font.render(desc, True, (180, 180, 200))
            screen.blit(desc_text, (WIDTH//2 - desc_text.get_width()//2, y_pos))
            y_pos += 35
        
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 750, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        if is_hover:
            self.draw_cyber_panel(back_btn_rect, color=CYBER_YELLOW, alpha=255, border_color=WHITE)
            text_color = BLACK
        else:
            self.draw_cyber_panel(back_btn_rect, color=(20, 20, 30), border_color=CYBER_PINK)
            text_color = WHITE
            
        back_text = font.render("BACK", True, text_color)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_levels(self):
        self.draw_background()
        
        # Title
        self.draw_text_centered("SELECT LEVEL", header_font, CYBER_YELLOW, 100)
        
        # Level Buttons
        levels = [
            {"text": "LEVEL 1 (Classic)", "y": 300, "level": 1},
            {"text": "LEVEL 2 (Open)", "y": 450, "level": 2}
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for lvl in levels:
            btn_rect = pygame.Rect(WIDTH // 2 - 200, lvl["y"], 400, 80)
            is_hover = btn_rect.collidepoint(mouse_pos)
            
            if is_hover:
                self.draw_cyber_panel(btn_rect, color=CYBER_BLUE, alpha=255, border_color=WHITE)
                text_color = BLACK
            else:
                self.draw_cyber_panel(btn_rect, color=(20, 20, 30), border_color=CYBER_YELLOW)
                text_color = CYBER_YELLOW
                
            text = sub_font.render(lvl["text"], True, text_color)
            text_rect = text.get_rect(center=btn_rect.center)
            screen.blit(text, text_rect)
            
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 700, 200, 50)
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        if is_hover:
            self.draw_cyber_panel(back_btn_rect, color=CYBER_YELLOW, alpha=255, border_color=WHITE)
            text_color = BLACK
        else:
            self.draw_cyber_panel(back_btn_rect, color=(20, 20, 30), border_color=CYBER_PINK)
            text_color = WHITE
            
        back_text = font.render("BACK", True, text_color)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_instructions(self):
        self.draw_background()
        
        # Title
        self.draw_text_centered("HOW TO PLAY", header_font, CYBER_YELLOW, 60)
        
        # Instructions Panel
        panel_rect = pygame.Rect(50, 120, WIDTH - 100, 700)
        self.draw_cyber_panel(panel_rect, border_color=CYBER_BLUE)
        
        # Instructions sections
        y_pos = 150
        
        sections = [
            ("OBJECTIVE", [
                "• Eat all the dots to complete each level",
                "• Avoid the ghosts or you'll lose a life",
                "• Clear all levels to win the game"
            ]),
            ("CONTROLS", [
                "• Arrow Keys: Move Pac-Man (Up, Down, Left, Right)",
                "• ESC: Pause or return to menu",
                "• Mouse Click: Navigate menus"
            ]),
            ("POWER-UPS", [
                "• Small Dots: 10 points each",
                "• Power Pellets (Big Dots): 50 points + Ghost Hunt Mode",
                "• During Power Mode: Eat blue ghosts for bonus points!"
            ]),
            ("GHOSTS", [
                "• Red Ghost (Blinky): Chases you directly",
                "• Pink Ghost (Pinky): Tries to ambush you",
                "• Blue Ghost (Inky): Unpredictable movement",
                "• Orange Ghost (Clyde): Patrols and chases"
            ])
        ]
        
        for title, lines in sections:
            # Section Title
            title_surf = section_font.render(title, True, CYBER_PINK)
            screen.blit(title_surf, (100, y_pos))
            y_pos += 35
            
            # Lines
            for line in lines:
                line_surf = inst_font.render(line, True, (200, 200, 220))
                screen.blit(line_surf, (120, y_pos))
                y_pos += 25
            y_pos += 20
        
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 850, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        if is_hover:
            self.draw_cyber_panel(back_btn_rect, color=CYBER_YELLOW, alpha=255, border_color=WHITE)
            text_color = BLACK
        else:
            self.draw_cyber_panel(back_btn_rect, color=(20, 20, 30), border_color=CYBER_PINK)
            text_color = WHITE
            
        back_text = font.render("BACK", True, text_color)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_high_scores(self):
        self.draw_background()
        
        # Title
        self.draw_text_centered("HIGH SCORES", header_font, CYBER_YELLOW, 80)
        
        # Sort scores
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Score Panel
        panel_rect = pygame.Rect(WIDTH // 2 - 300, 150, 600, 450)
        self.draw_cyber_panel(panel_rect, border_color=CYBER_BLUE)
        
        # Score entries
        y_start = 200
        
        if len(self.high_scores) == 0:
            no_scores = score_font.render("No high scores yet!", True, (150, 200, 255))
            no_rect = no_scores.get_rect(center=(WIDTH // 2, 350))
            screen.blit(no_scores, no_rect)
        else:
            for i, entry in enumerate(self.high_scores[:5]):
                # Rank
                rank_colors = [CYBER_YELLOW, (192, 192, 192), (205, 127, 50), CYBER_BLUE, CYBER_BLUE]
                rank_text = score_font.render(f"#{i+1}", True, rank_colors[i])
                screen.blit(rank_text, (WIDTH // 2 - 250, y_start + i * 70))
                
                # Name
                name_text = score_font.render(entry['name'], True, WHITE)
                screen.blit(name_text, (WIDTH // 2 - 150, y_start + i * 70))
                
                # Score
                score_text = score_font.render(str(entry['score']), True, CYBER_PINK)
                score_rect = score_text.get_rect(right=WIDTH // 2 + 250, top=y_start + i * 70)
                screen.blit(score_text, score_rect)
        
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 650, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        if is_hover:
            self.draw_cyber_panel(back_btn_rect, color=CYBER_YELLOW, alpha=255, border_color=WHITE)
            text_color = BLACK
        else:
            self.draw_cyber_panel(back_btn_rect, color=(20, 20, 30), border_color=CYBER_PINK)
            text_color = WHITE
            
        back_text = font.render("BACK", True, text_color)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_new_highscore(self):
        self.draw_background()
        
        # Celebration title
        self.draw_text_centered("NEW HIGH SCORE!", header_font, CYBER_YELLOW, 150)
        
        # Panel
        panel_rect = pygame.Rect(WIDTH // 2 - 300, 220, 600, 400)
        self.draw_cyber_panel(panel_rect, border_color=CYBER_PINK)
        
        # Score display
        score_text = large_score_font.render(f"Score: {self.current_score}", True, CYBER_BLUE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 280))
        screen.blit(score_text, score_rect)
        
        # Name entry prompt
        prompt = prompt_font.render("Enter Your Name (Max 10 chars):", True, WHITE)
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, 380))
        screen.blit(prompt, prompt_rect)
        
        # Name input box
        input_box = pygame.Rect(WIDTH // 2 - 150, 430, 300, 70)
        self.draw_cyber_panel(input_box, color=(0, 0, 0), border_color=CYBER_YELLOW)
        
        # Display name with blinking cursor effect
        display_name = self.input_name
        if pygame.time.get_ticks() % 1000 < 500:
            display_name += "_"
        
        name_text = input_font.render(display_name, True, CYBER_YELLOW)
        name_rect = name_text.get_rect(center=input_box.center)
        screen.blit(name_text, name_rect)
        
        # Submit hint
        hint = small_font.render("Press ENTER to save", True, (150, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH // 2, 550))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()

    def start_game(self):
        # Don't reset level if coming from level select
        if self.state != STATE_LEVELS:
            self.current_level = 1
        
        self.current_lives = 3
        self.current_score = 0
        
        while True:
            # Setup level
            pacman.init_globals()
            pacman.lives = self.current_lives
            pacman.score = self.current_score
            
            # Determine difficulty and board
            speed_mult = 1.0 + (self.current_level - 1) * 0.15
            
            # Map level to board: Level 1 -> board1, Level 2 -> board2
            if self.current_level == 1:
                board_index = 0  # board1
            elif self.current_level == 2:
                board_index = 1  # board2
            else:
                # For levels 3+, cycle through boards
                board_index = (self.current_level - 1) % 2
            
            # Show Level Screen only for levels 2+
            if self.current_level > 1:
                self.draw_background()
                self.draw_text_centered(f"LEVEL {self.current_level}", level_font, CYBER_YELLOW, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
            
            # Play Level
            result = pacman.play_level(speed_mult=speed_mult, board_index=board_index, level_num=self.current_level)
            
            # Update stats from pacman module
            self.current_score = pacman.score
            self.current_lives = pacman.lives
            
            if result == "QUIT":
                self.running = False
                return
            elif result == "GAMEOVER":
                # Pacman.py handles the game over screen now
                self.check_high_score()
                return
            elif result == "VICTORY":
                self.current_level += 1
                # Loop continues to next level
            elif result == "RESTART":
                # Loop continues, restarting the level
                pass
            elif result == "MENU":
                return
            else:
                # Should not happen
                return

    def check_high_score(self):
        # Check if score is in top 5
        is_high = False
        if len(self.high_scores) < 5:
            is_high = True
        else:
            min_score = min(s['score'] for s in self.high_scores)
            if self.current_score > min_score:
                is_high = True
        
        if is_high:
            self.state = STATE_NEW_HIGHSCORE
            self.input_name = ""
        else:
            self.state = STATE_MENU

    def run(self):
        while self.running:
            if self.state == STATE_MENU:
                self.draw_menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        # Check which button was clicked
                        buttons = [
                            {"y": 300, "action": "start"},
                            {"y": 390, "action": "levels"},
                            {"y": 480, "action": "instructions"},
                            {"y": 570, "action": "highscores"},
                            {"y": 660, "action": "about"},
                            {"y": 750, "action": "quit"}
                        ]
                        for btn in buttons:
                            btn_rect = pygame.Rect(WIDTH // 2 - 200, btn["y"], 400, 70)
                            if btn_rect.collidepoint(mouse_pos):
                                if btn["action"] == "start":
                                    self.start_game()
                                    if self.state != STATE_NEW_HIGHSCORE:
                                        self.state = STATE_MENU
                                elif btn["action"] == "levels":
                                    self.state = STATE_LEVELS
                                elif btn["action"] == "instructions":
                                    self.state = STATE_INSTRUCTIONS
                                elif btn["action"] == "highscores":
                                    self.state = STATE_HIGHSCORES
                                elif btn["action"] == "about":
                                    self.state = STATE_ABOUT
                                elif btn["action"] == "quit":
                                    self.running = False
                    # Keep keyboard support as backup
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.start_game()
                            if self.state != STATE_NEW_HIGHSCORE:
                                self.state = STATE_MENU
                        elif event.key == pygame.K_2:
                            self.state = STATE_LEVELS
                        elif event.key == pygame.K_3:
                            self.state = STATE_INSTRUCTIONS
                        elif event.key == pygame.K_4:
                            self.state = STATE_HIGHSCORES
                        elif event.key == pygame.K_5:
                            self.state = STATE_ABOUT
                        elif event.key == pygame.K_6:
                            self.running = False
            
            elif self.state == STATE_LEVELS:
                self.draw_levels()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Level 1 Button
                        lvl1_rect = pygame.Rect(WIDTH // 2 - 200, 300, 400, 80)
                        if lvl1_rect.collidepoint(mouse_pos):
                            self.current_level = 1
                            self.start_game()
                            if self.state != STATE_NEW_HIGHSCORE:
                                self.state = STATE_MENU
                            
                        # Level 2 Button
                        lvl2_rect = pygame.Rect(WIDTH // 2 - 200, 450, 400, 80)
                        if lvl2_rect.collidepoint(mouse_pos):
                            self.current_level = 2
                            self.start_game()
                            if self.state != STATE_NEW_HIGHSCORE:
                                self.state = STATE_MENU
                            
                        # Back Button
                        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 700, 200, 50)
                        if back_btn_rect.collidepoint(mouse_pos):
                            self.state = STATE_MENU
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATE_MENU

            elif self.state == STATE_INSTRUCTIONS:
                self.draw_instructions()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 850, 200, 50)
                        if back_btn_rect.collidepoint(mouse_pos):
                            self.state = STATE_MENU
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATE_MENU
                            
            elif self.state == STATE_HIGHSCORES:
                self.draw_high_scores()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 650, 200, 50)
                        if back_btn_rect.collidepoint(mouse_pos):
                            self.state = STATE_MENU
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATE_MENU

            elif self.state == STATE_ABOUT:
                self.draw_about()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 750, 200, 50)
                        if back_btn_rect.collidepoint(mouse_pos):
                            self.state = STATE_MENU
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATE_MENU

            elif self.state == STATE_NEW_HIGHSCORE:
                self.draw_new_highscore()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            # Save score
                            self.high_scores.append({"name": self.input_name, "score": self.current_score})
                            self.high_scores.sort(key=lambda x: x['score'], reverse=True)
                            self.high_scores = self.high_scores[:5]
                            self.save_high_scores()
                            self.state = STATE_HIGHSCORES
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_name = self.input_name[:-1]
                        else:
                            if len(self.input_name) < 10 and event.unicode.isalnum():
                                self.input_name += event.unicode.upper()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameManager()
    game.run()
