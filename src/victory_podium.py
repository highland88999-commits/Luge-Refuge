import pygame
import sys
import random  # For subtle animations like confetti or lights

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors for cyberpunk aesthetic with Olympus theme (golden accents)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
DARK_BG = (10, 10, 20)
GLOW_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
HOLO_PURPLE = (200, 0, 255)
AI_RED = (255, 50, 50)
ENERGY_YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
OLYMPUS_BG = (20, 20, 40)  # Slightly brighter for podium
CONFETTI_COLORS = [NEON_BLUE, NEON_PINK, ENERGY_YELLOW, GOLD]

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge: Olympus Victory Podium")

# Fonts
title_font = pygame.font.SysFont('couriernew', 32, bold=True)
body_font = pygame.font.SysFont('couriernew', 20)
small_font = pygame.font.SysFont('couriernew', 16)

# Animation variables
fade_alpha = 255  # For initial fade-in from black
elevator_y = SCREEN_HEIGHT  # Starts off-screen bottom, moves up
podium_phase = False  # Switch to podium after elevator
confetti = []  # List for confetti particles
timer = 0

# Player ID (placeholder; incorporate from main game)
player_id = "PLAYER-ID-12345"  # This will be shown at the top; replace with actual from game state

def generate_confetti():
    return [random.randint(0, SCREEN_WIDTH), random.randint(-SCREEN_HEIGHT, 0), random.choice(CONFETTI_COLORS), random.randint(3, 6)]

for _ in range(100):  # Pre-generate confetti
    confetti.append(generate_confetti())

def draw_scene():
    global fade_alpha, elevator_y, podium_phase, timer
    timer += 1
    
    # Background fade from black (initial faze in)
    if fade_alpha > 0:
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill(DARK_BG)
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha -= 5
    
    if not podium_phase:
        # Elevator scene: Boarding and riding up
        # Draw megacity building interior (tallest building)
        screen.fill(OLYMPUS_BG)
        # Windows with city view (neon lights)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.rect(screen, NEON_BLUE, (50, y - elevator_y % 50, 100, 30), 2)  # Left windows
            pygame.draw.rect(screen, NEON_PINK, (650, y - elevator_y % 50, 100, 30), 2)  # Right windows
        
        # Elevator car (moving up)
        elevator_height = 200
        pygame.draw.rect(screen, GOLD, (SCREEN_WIDTH // 2 - 150, elevator_y - elevator_height, 300, elevator_height), 5)
        # Player silhouette in elevator
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 50, elevator_y - 150, 100, 150))
        
        # Move elevator up
        if elevator_y > SCREEN_HEIGHT // 2:
            elevator_y -= 2  # Slow ascent
        else:
            podium_phase = True  # Transition to podium
        
        # Text: Boarding elevator
        boarding_text = body_font.render("Boarding Elevator in Megacity's Tallest Tower...", True, WHITE)
        screen.blit(boarding_text, (SCREEN_WIDTH // 2 - boarding_text.get_width() // 2, 50))
    else:
        # Podium scene at Olympus
        screen.fill(OLYMPUS_BG)
        # Podium platform
        pygame.draw.rect(screen, GOLD, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 200, 400, 150), 0)
        pygame.draw.rect(screen, ENERGY_YELLOW, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 200, 400, 150), 5)
        
        # Holographic gods/titans awarding prize
        for x in [SCREEN_WIDTH // 2 - 150, SCREEN_WIDTH // 2 + 150]:
            pygame.draw.ellipse(screen, HOLO_PURPLE, (x - 50, 200, 100, 200), 0)
        
        # Confetti animation
        for c in confetti:
            pygame.draw.circle(screen, c[2], (c[0], c[1]), c[3])
            c[1] += 2  # Fall down
            if c[1] > SCREEN_HEIGHT:
                c[1] = random.randint(-50, 0)  # Respawn top
        
        # Victory text
        victory_text = title_font.render("Congratulations! You've Conquered All 20 Courses!", True, GOLD)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 50))
        
        # Prize info
        prize_text1 = body_font.render("Your Prize: A Free Hoodie of Your Choosing!", True, WHITE)
        screen.blit(prize_text1, (50, 150))
        
        prize_text2 = small_font.render("Visit: https://olympus-lac.vercel.app/", True, NEON_BLUE)
        screen.blit(prize_text2, (50, 180))
        
        instr_text1 = small_font.render("To Claim:", True, WHITE)
        screen.blit(instr_text1, (50, 220))
        
        instr_text2 = small_font.render("- Email screenshot of your Player ID: " + player_id, True, WHITE)
        screen.blit(instr_text2, (50, 240))
        
        instr_text3 = small_font.render("- Screenshot of the hoodie you choose", True, WHITE)
        screen.blit(instr_text3, (50, 260))
        
        instr_text4 = small_font.render("- Your mailing address", True, WHITE)
        screen.blit(instr_text4, (50, 280))
        
        instr_text5 = small_font.render("The Gods Cover the Cost!", True, GOLD)
        screen.blit(instr_text5, (50, 320))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_scene()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
