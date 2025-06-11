import pygame
import numpy as np
import math
import random

class SnakeAndLadderVisualizer:
    def __init__(self, board_size=100):
        pygame.init()
        self.board_size = board_size
        self.cell_size = 70
        self.margin = 30
        self.width = self.cell_size * 10 + self.margin * 2
        self.height = self.cell_size * 10 + self.margin * 2 + 150  # Increased height for buttons
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BOARD_COLOR = (245, 222, 179)  # Wheat color
        self.CELL_COLOR1 = (255, 255, 255)
        self.CELL_COLOR2 = (240, 240, 240)
        self.SNAKE_COLOR = (0, 100, 0)
        self.SNAKE_HEAD_COLOR = (0, 150, 0)
        self.LADDER_COLOR = (139, 69, 19)  # Brown
        self.PLAYER_COLOR = (0, 0, 255)
        self.TEXT_COLOR = (50, 50, 50)
        self.START_COLOR = (0, 255, 0)
        self.END_COLOR = (255, 0, 0)
        self.BUTTON_COLOR = (100, 100, 255)
        self.BUTTON_HOVER_COLOR = (150, 150, 255)
        self.BUTTON_PRESSED_COLOR = (50, 50, 200)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.BUTTON_SHADOW_COLOR = (50, 50, 50)
        self.DICE_COLOR = (255, 255, 255)
        self.DICE_SHADOW = (200, 200, 200)
        
        # Initialize screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake and Ladder Game")
        
        # Fonts
        self.cell_font = pygame.font.Font(None, 28)
        self.stats_font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.dice_font = pygame.font.Font(None, 36)
        
        # Load dice images
        self.dice_images = []
        for i in range(1, 7):
            dice = pygame.Surface((40, 40))
            dice.fill(self.WHITE)
            pygame.draw.rect(dice, self.BLACK, (0, 0, 40, 40), 2)
            dots = self._get_dice_dots(i)
            for dot in dots:
                pygame.draw.circle(dice, self.BLACK, dot, 4)
            self.dice_images.append(dice)
        
        # Button positions and states
        self.button_height = 40
        self.button_width = 120
        self.button_margin = 20
        self.button_radius = 10
        self.button_pressed = None
        
        # Create buttons
        self.start_button = pygame.Rect(
            self.margin,
            self.height - self.button_height - self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.reset_button = pygame.Rect(
            self.margin + self.button_width + self.button_margin,
            self.height - self.button_height - self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.roll_button = pygame.Rect(
            self.margin + 2 * (self.button_width + self.button_margin),
            self.height - self.button_height - self.button_margin,
            self.button_width,
            self.button_height
        )
        
        # Dice properties
        self.dice_size = 60
        self.dice_margin = 10
        self.dice_animation_frames = 10
        self.dice_rotation_angle = 0
        
        # Create dice surface
        self.dice_surface = pygame.Surface((self.dice_size, self.dice_size))
        self.dice_surface.fill(self.DICE_COLOR)
        
        # Game state indicators
        self.state_colors = {
            "idle": (200, 200, 200),
            "auto": (0, 200, 0),
            "roll": (0, 0, 200)
        }
    
    def _get_dice_dots(self, number):
        """Return positions of dots for dice face"""
        positions = {
            1: [(20, 20)],
            2: [(10, 10), (30, 30)],
            3: [(10, 10), (20, 20), (30, 30)],
            4: [(10, 10), (10, 30), (30, 10), (30, 30)],
            5: [(10, 10), (10, 30), (20, 20), (30, 10), (30, 30)],
            6: [(10, 10), (10, 20), (10, 30), (30, 10), (30, 20), (30, 30)]
        }
        return positions[number]
    
    def get_cell_center(self, cell_num):
        """Get the pixel coordinates of a cell's center"""
        # Convert cell number to row and column
        row = (cell_num - 1) // 10
        col = (cell_num - 1) % 10
        
        # For odd rows, reverse the column order
        if row % 2 == 1:
            col = 9 - col
            
        x = col * self.cell_size + self.margin + self.cell_size // 2
        y = (9 - row) * self.cell_size + self.margin + 30 + self.cell_size // 2  # Added offset for title
        return (x, y)
    
    def draw_snake(self, start_pos, end_pos):
        """Draw a realistic snake between two positions"""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Calculate control points for the curve
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.sqrt(dx*dx + dy*dy)
        
        # Create a wavy snake body
        points = []
        segments = 20
        for i in range(segments + 1):
            t = i / segments
            # Base curve
            x = start_x + dx * t
            y = start_y + dy * t
            
            # Add wave effect
            if 0 < t < 1:
                wave = math.sin(t * math.pi * 4) * (length / 20)
                perp_x = -dy / length
                perp_y = dx / length
                x += wave * perp_x
                y += wave * perp_y
            
            points.append((int(x), int(y)))
        
        # Draw snake body with gradient
        for i in range(len(points) - 1):
            color = self.SNAKE_COLOR
            if i > len(points) * 0.8:  # Make head portion lighter
                color = self.SNAKE_HEAD_COLOR
            pygame.draw.line(self.screen, color, points[i], points[i+1], 6)
        
        # Draw snake head
        pygame.draw.circle(self.screen, self.SNAKE_HEAD_COLOR, points[-1], 8)
        # Draw eyes
        eye_offset = 3
        pygame.draw.circle(self.screen, self.WHITE, 
                         (points[-1][0] - eye_offset, points[-1][1] - eye_offset), 2)
        pygame.draw.circle(self.screen, self.WHITE, 
                         (points[-1][0] + eye_offset, points[-1][1] - eye_offset), 2)
    
    def draw_ladder(self, start_pos, end_pos):
        """Draw a realistic ladder between two positions"""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Calculate perpendicular vector for ladder width
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return
        
        perpx = -dy * 8 / length
        perpy = dx * 8 / length
        
        # Draw side rails with wood texture
        for i in range(2):
            offset = i * 2 - 1
            pygame.draw.line(self.screen, 
                           self.LADDER_COLOR,
                           (start_x + perpx * offset, start_y + perpy * offset),
                           (end_x + perpx * offset, end_y + perpy * offset),
                           4)
        
        # Draw rungs with wood texture
        num_rungs = int(length / 25)
        for i in range(1, num_rungs):
            t = i / num_rungs
            x1 = start_x + dx * t
            y1 = start_y + dy * t
            pygame.draw.line(self.screen,
                           self.LADDER_COLOR,
                           (x1 + perpx, y1 + perpy),
                           (x1 - perpx, y1 - perpy),
                           3)
    
    def draw_button(self, button, text, hover=False, pressed=False):
        """Draw a modern button with shadow and hover effects"""
        # Draw shadow
        shadow_offset = 3
        shadow_rect = button.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen, self.BUTTON_SHADOW_COLOR, shadow_rect, 
                        border_radius=self.button_radius)
        
        # Draw button
        color = self.BUTTON_PRESSED_COLOR if pressed else (
            self.BUTTON_HOVER_COLOR if hover else self.BUTTON_COLOR
        )
        pygame.draw.rect(self.screen, color, button, border_radius=self.button_radius)
        
        # Draw border
        pygame.draw.rect(self.screen, self.BUTTON_TEXT_COLOR, button, 
                        2, border_radius=self.button_radius)
        
        # Draw text
        text_surface = self.button_font.render(text, True, self.BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button.center)
        self.screen.blit(text_surface, text_rect)
    
    def check_button_click(self, pos):
        """Check if a button was clicked and handle button states"""
        for button_name, button_rect in [
            ("start", self.start_button),
            ("reset", self.reset_button),
            ("roll", self.roll_button)
        ]:
            if button_rect.collidepoint(pos):
                self.button_pressed = button_name
                return button_name
        return None
    
    def draw_dice(self, number, x, y, rotation=0):
        """Draw an animated dice with rotation"""
        # Create a new surface for the dice
        dice = pygame.Surface((self.dice_size, self.dice_size), pygame.SRCALPHA)
        dice.fill((0, 0, 0, 0))
        
        # Draw dice shadow
        shadow = pygame.Surface((self.dice_size, self.dice_size))
        shadow.fill(self.DICE_SHADOW)
        dice.blit(shadow, (2, 2))
        
        # Draw dice body
        pygame.draw.rect(dice, self.DICE_COLOR, (0, 0, self.dice_size, self.dice_size))
        pygame.draw.rect(dice, self.BLACK, (0, 0, self.dice_size, self.dice_size), 2)
        
        # Draw dots
        dots = self._get_dice_dots(number)
        for dot in dots:
            # Scale dot positions to dice size
            scaled_x = int(dot[0] * self.dice_size / 40)
            scaled_y = int(dot[1] * self.dice_size / 40)
            pygame.draw.circle(dice, self.BLACK, (scaled_x, scaled_y), 4)
        
        # Rotate the dice
        rotated_dice = pygame.transform.rotate(dice, rotation)
        
        # Draw the rotated dice
        self.screen.blit(rotated_dice, (x - rotated_dice.get_width()//2, 
                                      y - rotated_dice.get_height()//2))
    
    def draw_board(self, current_position, snakes, ladders, steps=0, current_dice=0, game_state="idle"):
        # Draw background
        self.screen.fill(self.BOARD_COLOR)
        
        # Draw title with shadow
        title = self.title_font.render("Snake and Ladder Game", True, self.TEXT_COLOR)
        title_shadow = self.title_font.render("Snake and Ladder Game", True, self.BUTTON_SHADOW_COLOR)
        self.screen.blit(title_shadow, (self.width//2 - title.get_width()//2 + 2, 12))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 10))
        
        # Draw game state indicator
        state_color = self.state_colors.get(game_state, (200, 200, 200))
        pygame.draw.circle(self.screen, state_color, (self.width - 20, 20), 8)
        
        # Draw instructions for roll mode
        if game_state == "roll":
            instructions = self.stats_font.render("Click 'Roll Dice' to roll!", True, self.TEXT_COLOR)
            self.screen.blit(instructions, (self.width//2 - instructions.get_width()//2, 40))
        
        # Draw grid
        for i in range(10):
            for j in range(10):
                x = j * self.cell_size + self.margin
                y = i * self.cell_size + self.margin + 30
                
                # Calculate cell number (1-100)
                row = 9 - i
                if row % 2 == 0:
                    cell_num = row * 10 + j + 1
                else:
                    cell_num = row * 10 + (9 - j) + 1
                
                # Draw cell with gradient
                cell_color = self.CELL_COLOR1 if (i + j) % 2 == 0 else self.CELL_COLOR2
                pygame.draw.rect(self.screen, cell_color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, self.BLACK, (x, y, self.cell_size, self.cell_size), 1)
                
                # Special colors for start and end
                if cell_num == 1:
                    pygame.draw.rect(self.screen, self.START_COLOR, (x, y, self.cell_size, self.cell_size), 3)
                elif cell_num == 100:
                    pygame.draw.rect(self.screen, self.END_COLOR, (x, y, self.cell_size, self.cell_size), 3)
                
                # Draw cell number
                text = self.cell_font.render(str(cell_num), True, self.TEXT_COLOR)
                text_rect = text.get_rect(center=(x + self.cell_size/2, y + self.cell_size/2))
                self.screen.blit(text, text_rect)
        
        # Draw snakes and ladders
        for start, end in snakes.items():
            self.draw_snake(self.get_cell_center(start), self.get_cell_center(end))
        
        for start, end in ladders.items():
            self.draw_ladder(self.get_cell_center(start), self.get_cell_center(end))
        
        # Draw current position
        if current_position > 0:
            pos = self.get_cell_center(current_position)
            # Draw shadow
            pygame.draw.circle(self.screen, (50, 50, 50), 
                             (pos[0] + 2, pos[1] + 2), self.cell_size/4)
            # Draw player
            pygame.draw.circle(self.screen, self.PLAYER_COLOR, pos, self.cell_size/4)
            # Draw highlight
            pygame.draw.circle(self.screen, self.WHITE, pos, self.cell_size/4, 2)
        
        # Draw statistics
        self.draw_stats(steps, current_dice, game_state)
        
        # Draw buttons with hover and pressed states
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.start_button, "Start", 
                        self.start_button.collidepoint(mouse_pos),
                        self.button_pressed == "start")
        self.draw_button(self.reset_button, "Reset", 
                        self.reset_button.collidepoint(mouse_pos),
                        self.button_pressed == "reset")
        self.draw_button(self.roll_button, "Roll Dice", 
                        self.roll_button.collidepoint(mouse_pos),
                        self.button_pressed == "roll")
        
        pygame.display.flip()
    
    def draw_stats(self, steps, current_dice, game_state):
        """Draw game statistics with enhanced visuals"""
        y_pos = self.height - 120
        
        # Draw stats background
        stats_bg = pygame.Rect(self.margin, y_pos - 10, 
                             self.width - 2 * self.margin, 100)
        pygame.draw.rect(self.screen, (240, 240, 240), stats_bg, 
                        border_radius=10)
        pygame.draw.rect(self.screen, self.BLACK, stats_bg, 2, 
                        border_radius=10)
        
        stats = [
            f"Steps taken: {steps}",
            f"Current dice: {current_dice}",
            f"Game state: {game_state}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.stats_font.render(stat, True, self.TEXT_COLOR)
            self.screen.blit(text, (self.margin + 10, y_pos + i * 25))
        
        # Draw current dice with animation
        if 1 <= current_dice <= 6:
            # Calculate dice position
            dice_x = self.width - self.margin - self.dice_size//2
            dice_y = y_pos + self.dice_size//2
            
            # Draw dice with rotation animation
            self.draw_dice(current_dice, dice_x, dice_y, 
                         self.dice_rotation_angle)
            
            # Update rotation angle for next frame
            self.dice_rotation_angle = (self.dice_rotation_angle + 5) % 360
    
    def close(self):
        pygame.quit() 