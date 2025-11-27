import pygame
import pacman
import json
import os
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 900
HEIGHT = 950
screen = pacman.screen
font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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

    def draw_text_centered(self, text, font, color, y_offset):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)

    def draw_menu(self):
        # Dark theme background - deep black
        screen.fill((10, 10, 15))
        
        # Animated grid pattern for depth
        time_offset = pygame.time.get_ticks() * 0.001
        for i in range(0, WIDTH, 60):
            alpha = int(abs(math.sin(time_offset + i * 0.01)) * 30 + 20)
            pygame.draw.line(screen, (alpha, alpha, alpha + 5), (i, 0), (i, HEIGHT), 1)
        for j in range(0, HEIGHT, 60):
            alpha = int(abs(math.cos(time_offset + j * 0.01)) * 30 + 20)
            pygame.draw.line(screen, (alpha, alpha, alpha + 5), (0, j), (WIDTH, j), 1)
        
        # Animated Pac-Man character
        pac_time = pygame.time.get_ticks() * 0.003
        pac_x = int((math.sin(pac_time * 0.5) + 1) * (WIDTH - 100) / 2 + 50)
        pac_y = 60
        pac_size = 35
        
        # Pac-Man body
        pygame.draw.circle(screen, (255, 255, 0), (pac_x, pac_y), pac_size)
        
        # Animated mouth
        mouth_angle = abs(math.sin(pac_time * 3)) * 40
        mouth_points = [
            (pac_x, pac_y),
            (int(pac_x + pac_size * math.cos(math.radians(mouth_angle))), 
             int(pac_y - pac_size * math.sin(math.radians(mouth_angle)))),
            (int(pac_x + pac_size * math.cos(math.radians(-mouth_angle))), 
             int(pac_y + pac_size * math.sin(math.radians(mouth_angle))))
        ]
        pygame.draw.polygon(screen, (10, 10, 15), mouth_points)
        
        # Main title "PAC-MAN" with pulsing glow effect
        title_font = pygame.font.Font('freesansbold.ttf', 95)
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.002)) * 10 + 5
        
        # Animated glow layers
        for offset in [int(pulse), int(pulse * 0.7), int(pulse * 0.4)]:
            glow_alpha = int(60 - offset * 3)
            glow_text = title_font.render("PAC-MAN", True, (glow_alpha, glow_alpha, glow_alpha + 20))
            glow_rect = glow_text.get_rect(center=(WIDTH // 2 + offset, 160 + offset))
            screen.blit(glow_text, glow_rect)
        
        # Main title with gradient effect
        title_colors = [(255, 255, 100), (255, 220, 50), (255, 180, 0)]
        title_text = "PAC-MAN"
        title_x_start = WIDTH // 2 - 270
        
        # Animated letter bounce
        for i, letter in enumerate(title_text):
            bounce = math.sin(pygame.time.get_ticks() * 0.003 + i * 0.5) * 5
            if letter != "-":
                color = title_colors[i % len(title_colors)]
                letter_surface = title_font.render(letter, True, color)
                screen.blit(letter_surface, (title_x_start + i * 75, 150 + bounce))
            else:
                letter_surface = title_font.render(letter, True, (220, 220, 220))
                screen.blit(letter_surface, (title_x_start + i * 75, 150 + bounce))
        
        # Subtitle "CLASSIC EDITION" with better font
        subtitle_font = pygame.font.Font('freesansbold.ttf', 26)
        subtitle = subtitle_font.render("CLASSIC EDITION", True, (120, 170, 255))
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 260))
        screen.blit(subtitle, subtitle_rect)
        
        # Animated decorative line
        line_width = int(abs(math.sin(pygame.time.get_ticks() * 0.002)) * 50 + 150)
        pygame.draw.line(screen, (70, 120, 220), (WIDTH // 2 - line_width, 290), 
                        (WIDTH // 2 + line_width, 290), 3)
        
        # Menu buttons with floating animation
        button_font = pygame.font.Font('freesansbold.ttf', 28)
        buttons = [
            {"text": "START GAME", "y": 340, "icon": "▶"},
            {"text": "LEVELS", "y": 425, "icon": "☰"},
            {"text": "INSTRUCTIONS", "y": 510, "icon": "ℹ"},
            {"text": "HIGH SCORES", "y": 595, "icon": "★"},
            {"text": "ABOUT US", "y": 680, "icon": "👥"},
            {"text": "EXIT GAME", "y": 765, "icon": "✕"}
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for idx, btn in enumerate(buttons):
            # Floating animation
            float_offset = math.sin(pygame.time.get_ticks() * 0.002 + idx * 0.8) * 3
            btn_y = btn["y"] + float_offset
            btn_rect = pygame.Rect(WIDTH // 2 - 190, int(btn_y), 380, 65)
            is_hover = btn_rect.collidepoint(mouse_pos)
            
            # Button background with gradient effect
            if is_hover:
                # Brighter on hover with pulse
                pulse_color = int(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 40 + 80)
                pygame.draw.rect(screen, (50, pulse_color, 160), btn_rect, border_radius=12)
                pygame.draw.rect(screen, (70, pulse_color + 40, 220), btn_rect.inflate(-6, -6), border_radius=10)
            else:
                pygame.draw.rect(screen, (28, 38, 55), btn_rect, border_radius=12)
                pygame.draw.rect(screen, (38, 48, 70), btn_rect.inflate(-6, -6), border_radius=10)
            
            # Button border glow
            border_color = (100, 170, 255) if is_hover else (55, 75, 110)
            pygame.draw.rect(screen, border_color, btn_rect, 3, border_radius=12)
            
            # Icon with animation on hover
            icon_font = pygame.font.Font('freesansbold.ttf', 32)
            icon_color = (255, 220, 100) if is_hover else (160, 160, 190)
            icon_surface = icon_font.render(btn["icon"], True, icon_color)
            icon_x = btn_rect.left + 25
            if is_hover:
                icon_x += int(math.sin(pygame.time.get_ticks() * 0.01) * 3)
            screen.blit(icon_surface, (icon_x, btn_rect.centery - 16))
            
            # Button text
            text_color = (255, 255, 255) if is_hover else (190, 200, 220)
            text_surface = button_font.render(btn["text"], True, text_color)
            text_rect = text_surface.get_rect(center=(btn_rect.centerx + 25, btn_rect.centery))
            screen.blit(text_surface, text_rect)
        
        # Footer text with better font
        footer_font = pygame.font.Font('freesansbold.ttf', 15)
        footer = footer_font.render("Click to select or press 1-6", True, (90, 100, 120))
        footer_rect = footer.get_rect(center=(WIDTH // 2, 860))
        screen.blit(footer, footer_rect)
        
        # Version info
        version_font = pygame.font.Font('freesansbold.ttf', 13)
        version = version_font.render("v1.0 | Enhanced Edition", True, (70, 80, 100))
        version_rect = version.get_rect(center=(WIDTH // 2, 920))
        screen.blit(version, version_rect)
        
        pygame.display.flip()

    def draw_about(self):
        screen.fill((10, 10, 15))
        
        # Title
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        title = title_font.render("ABOUT US", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Decorative line
        pygame.draw.line(screen, (70, 120, 220), (WIDTH // 2 - 150, 150), (WIDTH // 2 + 150, 150), 3)
        
        # Team info
        info_font = pygame.font.Font('freesansbold.ttf', 24)
        credit_font = pygame.font.Font('freesansbold.ttf', 20)
        
        y_pos = 220
        
        # Project title
        project_title = info_font.render("PAC-MAN CLASSIC EDITION", True, (100, 200, 255))
        project_rect = project_title.get_rect(center=(WIDTH // 2, y_pos))
        screen.blit(project_title, project_rect)
        y_pos += 60
        
        # Team section
        team_title = info_font.render("DEVELOPMENT TEAM", True, (150, 180, 255))
        team_rect = team_title.get_rect(center=(WIDTH // 2, y_pos))
        screen.blit(team_title, team_rect)
        y_pos += 60
        
        # Team members
        credits = [
            "SIDDHARTH R - NNM24AC049",
            "SONAL HEGDE - NNM24AC050",
            "SOUMYA SM - NNM24AC051"
        ]
        
        for i, credit in enumerate(credits):
            credit_text = credit_font.render(credit, True, (200, 210, 230))
            credit_rect = credit_text.get_rect(center=(WIDTH // 2, y_pos + i * 50))
            screen.blit(credit_text, credit_rect)
        
        y_pos += 200
        
        # Description
        desc_font = pygame.font.Font('freesansbold.ttf', 18)
        descriptions = [
            "A modern recreation of the classic arcade game",
            "Built with Python and Pygame",
            "Features multiple levels, high scores, and smooth gameplay"
        ]
        
        for i, desc in enumerate(descriptions):
            desc_text = desc_font.render(desc, True, (150, 170, 200))
            desc_rect = desc_text.get_rect(center=(WIDTH // 2, y_pos + i * 35))
            screen.blit(desc_text, desc_rect)
        
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 750, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        btn_color = (50, 180, 220) if is_hover else (30, 120, 180)
        pygame.draw.rect(screen, btn_color, back_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 220, 255), back_btn_rect, 3, border_radius=8)
        
        back_text = font.render("BACK", True, WHITE)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_levels(self):
        screen.fill((10, 10, 15))
        
        # Title
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        title = title_font.render("SELECT LEVEL", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Level Buttons
        levels = [
            {"text": "LEVEL 1 (Classic)", "y": 300, "level": 1},
            {"text": "LEVEL 2 (Open)", "y": 450, "level": 2}
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for lvl in levels:
            btn_rect = pygame.Rect(WIDTH // 2 - 200, lvl["y"], 400, 80)
            is_hover = btn_rect.collidepoint(mouse_pos)
            
            # Button style
            if is_hover:
                pygame.draw.rect(screen, (50, 100, 180), btn_rect, border_radius=15)
                pygame.draw.rect(screen, (80, 150, 255), btn_rect, 3, border_radius=15)
            else:
                pygame.draw.rect(screen, (30, 50, 80), btn_rect, border_radius=15)
                pygame.draw.rect(screen, (50, 80, 120), btn_rect, 3, border_radius=15)
                
            text_font = pygame.font.Font('freesansbold.ttf', 30)
            text = text_font.render(lvl["text"], True, 'white')
            text_rect = text.get_rect(center=btn_rect.center)
            screen.blit(text, text_rect)
            
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 700, 200, 50)
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        btn_color = (50, 180, 220) if is_hover else (30, 120, 180)
        pygame.draw.rect(screen, btn_color, back_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 220, 255), back_btn_rect, 3, border_radius=8)
        
        back_text = font.render("BACK", True, WHITE)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_instructions(self):
        screen.fill((10, 10, 15))
        
        # Title
        title_font = pygame.font.Font('freesansbold.ttf', 48)
        title = title_font.render("HOW TO PLAY", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 60))
        screen.blit(title, title_rect)
        
        # Decorative line
        pygame.draw.line(screen, (70, 120, 220), (WIDTH // 2 - 150, 100), (WIDTH // 2 + 150, 100), 3)
        
        # Instructions sections
        section_font = pygame.font.Font('freesansbold.ttf', 24)
        inst_font = pygame.font.Font('freesansbold.ttf', 18)
        
        y_pos = 140
        
        # OBJECTIVE Section
        objective_title = section_font.render("OBJECTIVE", True, (100, 200, 255))
        screen.blit(objective_title, (100, y_pos))
        y_pos += 35
        
        objective_text = [
            "• Eat all the dots to complete each level",
            "• Avoid the ghosts or you'll lose a life",
            "• Clear all levels to win the game"
        ]
        for text in objective_text:
            line = inst_font.render(text, True, (200, 210, 230))
            screen.blit(line, (120, y_pos))
            y_pos += 28
        
        y_pos += 15
        
        # CONTROLS Section
        controls_title = section_font.render("CONTROLS", True, (100, 200, 255))
        screen.blit(controls_title, (100, y_pos))
        y_pos += 35
        
        controls_text = [
            "• Arrow Keys: Move Pac-Man (Up, Down, Left, Right)",
            "• ESC: Pause or return to menu",
            "• Mouse Click: Navigate menus"
        ]
        for text in controls_text:
            line = inst_font.render(text, True, (200, 210, 230))
            screen.blit(line, (120, y_pos))
            y_pos += 28
        
        y_pos += 15
        
        # POWER-UPS Section
        powerup_title = section_font.render("POWER-UPS", True, (100, 200, 255))
        screen.blit(powerup_title, (100, y_pos))
        y_pos += 35
        
        powerup_text = [
            "• Small Dots: 10 points each",
            "• Power Pellets (Big Dots): 50 points + Ghost Hunt Mode",
            "• During Power Mode: Eat blue ghosts for bonus points!"
        ]
        for text in powerup_text:
            line = inst_font.render(text, True, (200, 210, 230))
            screen.blit(line, (120, y_pos))
            y_pos += 28
        
        y_pos += 15
        
        # GHOSTS Section
        ghosts_title = section_font.render("GHOSTS", True, (100, 200, 255))
        screen.blit(ghosts_title, (100, y_pos))
        y_pos += 35
        
        ghosts_text = [
            "• Red Ghost (Blinky): Chases you directly",
            "• Pink Ghost (Pinky): Tries to ambush you",
            "• Blue Ghost (Inky): Unpredictable movement",
            "• Orange Ghost (Clyde): Patrols and chases"
        ]
        for text in ghosts_text:
            line = inst_font.render(text, True, (200, 210, 230))
            screen.blit(line, (120, y_pos))
            y_pos += 28
        
        y_pos += 15
        
        # LEVELS Section
        levels_title = section_font.render("LEVELS", True, (100, 200, 255))
        screen.blit(levels_title, (100, y_pos))
        y_pos += 35
        
        levels_text = [
            "• Each level increases speed by 15%",
            "• Different maze layouts every level",
            "• You start with 3 lives - use them wisely!"
        ]
        for text in levels_text:
            line = inst_font.render(text, True, (200, 210, 230))
            screen.blit(line, (120, y_pos))
            y_pos += 28
        
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 850, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        btn_color = (50, 180, 220) if is_hover else (30, 120, 180)
        pygame.draw.rect(screen, btn_color, back_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 220, 255), back_btn_rect, 3, border_radius=8)
        
        back_text = font.render("BACK", True, WHITE)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_high_scores(self):
        screen.fill((20, 40, 80))
        
        # Title
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        title = title_font.render("HIGH SCORES", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Sort scores
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Score entries
        score_font = pygame.font.Font('freesansbold.ttf', 28)
        y_start = 200
        
        if len(self.high_scores) == 0:
            no_scores = score_font.render("No high scores yet!", True, (150, 200, 255))
            no_rect = no_scores.get_rect(center=(WIDTH // 2, 350))
            screen.blit(no_scores, no_rect)
        else:
            for i, entry in enumerate(self.high_scores[:5]):
                # Rank
                rank_colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (100, 200, 255), (100, 200, 255)]
                rank_text = score_font.render(f"#{i+1}", True, rank_colors[i])
                screen.blit(rank_text, (200, y_start + i * 70))
                
                # Name
                name_text = score_font.render(entry['name'], True, WHITE)
                screen.blit(name_text, (300, y_start + i * 70))
                
                # Score
                score_text = score_font.render(str(entry['score']), True, (100, 255, 150))
                score_rect = score_text.get_rect(right=700, top=y_start + i * 70)
                screen.blit(score_text, score_rect)
        
        # Back button
        back_btn_rect = pygame.Rect(WIDTH // 2 - 100, 650, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = back_btn_rect.collidepoint(mouse_pos)
        
        btn_color = (50, 180, 220) if is_hover else (30, 120, 180)
        pygame.draw.rect(screen, btn_color, back_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 220, 255), back_btn_rect, 3, border_radius=8)
        
        back_text = font.render("BACK", True, WHITE)
        back_rect = back_text.get_rect(center=back_btn_rect.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

    def draw_new_highscore(self):
        screen.fill((20, 40, 80))
        
        # Celebration title
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        title = title_font.render("NEW HIGH SCORE!", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        # Score display
        score_font = pygame.font.Font('freesansbold.ttf', 40)
        score_text = score_font.render(f"Score: {self.current_score}", True, (100, 255, 150))
        score_rect = score_text.get_rect(center=(WIDTH // 2, 250))
        screen.blit(score_text, score_rect)
        
        # Name entry prompt
        prompt_font = pygame.font.Font('freesansbold.ttf', 28)
        prompt = prompt_font.render("Enter Your Name (Max 10 chars):", True, WHITE)
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, 350))
        screen.blit(prompt, prompt_rect)
        
        # Name input box
        input_box = pygame.Rect(WIDTH // 2 - 150, 420, 300, 60)
        pygame.draw.rect(screen, (30, 120, 180), input_box, border_radius=8)
        pygame.draw.rect(screen, (100, 220, 255), input_box, 3, border_radius=8)
        
        name_font = pygame.font.Font('freesansbold.ttf', 45)
        # Display name with blinking cursor effect
        display_name = self.input_name
        if pygame.time.get_ticks() % 1000 < 500:
            display_name += "_"
        
        name_text = name_font.render(display_name, True, YELLOW)
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
                screen.fill(BLACK)
                self.draw_text_centered(f"LEVEL {self.current_level}", font, YELLOW, HEIGHT // 2)
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
                screen.fill(BLACK)
                self.draw_text_centered("GAME OVER", font, RED, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(2000)
                self.check_high_score()
                return
            elif result == "VICTORY":
                self.current_level += 1
                # Loop continues to next level
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
                            {"y": 340, "action": "start"},
                            {"y": 425, "action": "levels"},
                            {"y": 510, "action": "instructions"},
                            {"y": 595, "action": "highscores"},
                            {"y": 680, "action": "about"},
                            {"y": 765, "action": "quit"}
                        ]
                        for btn in buttons:
                            btn_rect = pygame.Rect(WIDTH // 2 - 190, btn["y"], 380, 65)
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
