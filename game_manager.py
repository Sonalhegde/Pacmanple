import pygame
import pacman
import json
import os
import sys
import math

# Initialize Pygame (pacman already does this, but good to be sure)
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
        pygame.draw.rect(screen, (30, 120, 180), input_box, border_radius=8)
        pygame.draw.rect(screen, (100, 220, 255), input_box, 3, border_radius=8)
        
        name_font = pygame.font.Font('freesansbold.ttf', 45)
        name_text = name_font.render(self.input_name + "_" * (3 - len(self.input_name)), True, YELLOW)
        name_rect = name_text.get_rect(center=input_box.center)
        screen.blit(name_text, name_rect)
        
        # Submit hint
        hint = small_font.render("Press ENTER to save", True, (150, 200, 255))
        hint_rect = hint.get_rect(center=(WIDTH // 2, 550))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()

    def start_game(self):
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
            board_index = (self.current_level - 1) % 5  # Cycle through 5 boards
            
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
                            {"y": 360, "action": "start"},
                            {"y": 455, "action": "instructions"},
                            {"y": 550, "action": "highscores"},
                            {"y": 645, "action": "quit"}
                        ]
                        for btn in buttons:
                            btn_rect = pygame.Rect(WIDTH // 2 - 190, btn["y"], 380, 65)
                            if btn_rect.collidepoint(mouse_pos):
                                if btn["action"] == "start":
                                    self.start_game()
                                    if self.state != STATE_NEW_HIGHSCORE:
                                        self.state = STATE_MENU
                                elif btn["action"] == "instructions":
                                    self.state = STATE_INSTRUCTIONS
                                elif btn["action"] == "highscores":
                                    self.state = STATE_HIGHSCORES
                                elif btn["action"] == "quit":
                                    self.running = False
                    # Keep keyboard support as backup
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.start_game()
                            if self.state != STATE_NEW_HIGHSCORE:
                                self.state = STATE_MENU
                        elif event.key == pygame.K_2:
                            self.state = STATE_INSTRUCTIONS
                        elif event.key == pygame.K_3:
                            self.state = STATE_HIGHSCORES
                        elif event.key == pygame.K_4:
                            self.running = False
                            
            elif self.state == STATE_INSTRUCTIONS:
                self.draw_instructions()
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
                            
            elif self.state == STATE_HIGHSCORES:
                self.draw_high_scores()
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
                            if len(self.input_name) < 3 and event.unicode.isalnum():
                                self.input_name += event.unicode.upper()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameManager()
    game.run()
