import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors for cyberpunk aesthetic
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DARK_BG = (10, 10, 20)
ROBO_STEEL = (100, 100, 100, 200)  # Semi-transparent metal
AI_EYE_RED = (255, 0, 0, 180)
BEAM_BLUE = (0, 100, 255, 128)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)  # For price tag

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Premium Bobsled 8: AI Overlord ($2.99 USD)")

# Fonts
font = pygame.font.SysFont('couriernew', 20, bold=True)
small_font = pygame.font.SysFont('couriernew', 12)

# Bobsled parameters
SLED_LENGTH = 115  # Pixels for visualization
SLED_WIDTH = 48
SLED_COLOR = ROBO_STEEL

# Robotic arm and scan beam
arm_timer = 0
beam_particles = []

def add_beam_particles(x, y):
    for _ in range(4):
        beam_particles.append([x, y, random.randint(1, 3), random.randint(40, 80), BEAM_BLUE])

def update_beam_particles():
    global arm_timer
    arm_timer += 1
    for p in beam_particles[:]:
        p[0] += random.randint(-1, 1)
        p[1] -= 1  # Beam upward
        p[4] = list(p[4])
        p[4][3] -= 3  # Fade
        if p[4][3] <= 0:
            beam_particles.remove(p)

# Track simulation for auto-call (chicane-heavy path for adaptive demo)
track_points = []
start_x = SCREEN_WIDTH //
