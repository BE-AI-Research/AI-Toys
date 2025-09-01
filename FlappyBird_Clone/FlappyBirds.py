# BE-AI-Research - System 2 Trial Test: Qwen2.5 Code 30b-A3B 1-shot script.
# August 31st, 2025 (AMD Ryzen 5600, Dual RTX 3050 16GB GPUs, 256GB NVME, Xubuntu OS)

import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors
SKY_BLUE = (113, 197, 255)
GREEN = (111, 196, 69)
DARK_GREEN = (76, 145, 65)
BROWN = (160, 120, 40)
YELLOW = (255, 221, 45)
RED = (231, 76, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1800  # milliseconds
GROUND_HEIGHT = 100
FONT_SIZE = 32
SMALL_FONT_SIZE = 24

# Create clock object
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont(None, FONT_SIZE)
small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)

class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 20
        self.alive = True
        self.flap_count = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.flap_count += 1

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Keep bird on screen
        if self.y < self.radius:
            self.y = self.radius
            self.velocity = 0

        if self.y > HEIGHT - GROUND_HEIGHT - self.radius:
            self.y = HEIGHT - GROUND_HEIGHT - self.radius
            self.alive = False

    def draw(self):
        # Draw bird body
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)

        # Draw bird eye
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y - 5), 6)
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 7), 2)

        # Draw bird beak
        beak_points = [(self.x + 15, self.y), (self.x + 30, self.y - 5), (self.x + 30, self.y + 5)]
        pygame.draw.polygon(screen, RED, beak_points)

        # Draw wing
        wing_y_offset = math.sin(pygame.time.get_ticks() / 100) * 5
        wing_points = [
            (self.x - 10, self.y),
            (self.x - 20, self.y - 10 + wing_y_offset),
            (self.x, self.y + 5 + wing_y_offset)
        ]
        pygame.draw.polygon(screen, (200, 170, 0), wing_points)

    def get_mask(self):
        # Simple collision detection rectangle
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, HEIGHT - GROUND_HEIGHT - 150)
        self.x = WIDTH
        self.width = 70
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y - PIPE_GAP // 2))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, self.width, self.gap_y - PIPE_GAP // 2),
3)

        # Draw pipe cap (top)
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.gap_y - PIPE_GAP // 2 - 20, self.width +
10, 20))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.gap_y - PIPE_GAP // 2 - 20,
self.width + 10, 20), 3)

        # Draw bottom pipe
        bottom_pipe_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, GREEN, (self.x, bottom_pipe_y, self.width, HEIGHT -
bottom_pipe_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, bottom_pipe_y, self.width,
HEIGHT - bottom_pipe_y), 3)

        # Draw pipe cap (bottom)
        pygame.draw.rect(screen, GREEN, (self.x - 5, bottom_pipe_y, self.width + 10, 20))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, bottom_pipe_y, self.width + 10, 20), 3)

    def collide(self, bird):
        bird_mask = bird.get_mask()

        # Top pipe collision
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP // 2)
        if bird_mask.colliderect(top_pipe_rect):
            return True

        # Bottom pipe collision
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, self.width, HEIGHT)
        if bird_mask.colliderect(bottom_pipe_rect):
            return True

        return False

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_state = "start"  # start, playing, game_over
        self.last_pipe = pygame.time.get_ticks()
        self.high_score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "start":
                        self.game_state = "playing"
                    elif self.game_state == "playing":
                        self.bird.flap()
                    elif self.game_state == "game_over":
                        self.__init__()  # Reset game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "start" or self.game_state == "playing":
                    self.bird.flap()
                elif self.game_state == "game_over":
                    self.__init__()  # Reset game

        return True

    def update(self):
        if self.game_state != "playing":
            return

        # Update bird
        self.bird.update()

        # Generate new pipes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe > PIPE_FREQUENCY:
            self.pipes.append(Pipe())
            self.last_pipe = current_time

        # Update pipes and check for collisions
        for pipe in self.pipes[:]:
            pipe.update()

            # Check if bird passed the pipe
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1

            # Check collision
            if pipe.collide(self.bird):
                self.bird.alive = False

            # Remove pipes that are off screen
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)

        # Check if bird is dead
        if not self.bird.alive:
            self.game_state = "game_over"
            if self.score > self.high_score:
                self.high_score = self.score

    def draw(self):
        # Draw sky
        screen.fill(SKY_BLUE)

        # Draw clouds
        for i in range(5):
            x = (pygame.time.get_ticks() // 50 + i * 200) % (WIDTH + 400) - 200
            y = 100 + i * 30
            pygame.draw.circle(screen, WHITE, (x, y), 30)
            pygame.draw.circle(screen, WHITE, (x + 20, y - 10), 25)
            pygame.draw.circle(screen, WHITE, (x + 40, y), 30)

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()

        # Draw ground
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # Draw grass
        pygame.draw.rect(screen, GREEN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, 20))

        # Draw grass details
        for i in range(0, WIDTH, 20):
            pygame.draw.line(screen, DARK_GREEN, (i, HEIGHT - GROUND_HEIGHT + 10),
                            (i + 10, HEIGHT - GROUND_HEIGHT + 10), 3)

        # Draw bird
        self.bird.draw()

        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        high_score_text = small_font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(high_score_text, (20, 60))

        # Draw game state messages
        if self.game_state == "start":
            start_text = font.render("Press SPACE or Click to Start", True, WHITE)
            screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 - 50))

            title_text = font.render("FLAPPY BIRD", True, YELLOW)
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))

        elif self.game_state == "game_over":
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))

            final_score = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2))

            restart_text = font.render("Press SPACE or Click to Restart", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

# Create game instance
game = Game()

# Main game loop
running = True
while running:
    # Handle events
    running = game.handle_events()

    # Update game state
    game.update()

    # Draw everything
    game.draw()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
