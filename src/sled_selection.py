import pygame
import sys
import importlib  # For auto-calling sled previews
import random  # For any menu effects if needed

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
DARK_BG = (10, 10, 20)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
NEON_BLUE = (0, 255, 255)
LOCKED_GRAY = (100, 100, 100)
SELECTED_GREEN = (0, 255, 0)

# Fonts
title_font = pygame.font.SysFont('couriernew', 32, bold=True)
body_font = pygame.font.SysFont('couriernew', 20)
small_font = pygame.font.SysFont('couriernew', 16)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge: Sled Selection Menu")

# Placeholder unlocked sleds (load from save file in full game, e.g., generics always unlocked)
unlocked_sleds = {'generic1', 'generic2', 'premium1'}  # Example; expand with all as unlocked

# Sled list (for display; generics + premiums)
sleds = [
    {"type": "generic", "num": 1, "name": "Standard Racer"},
    {"type": "generic", "num": 2, "name": "Urban Glider"},
    {"type": "premium", "num": 1, "name": "Neon Phantom"},
    {"type": "premium", "num": 2, "name": "Grid Runner"},
    {"type": "premium", "num": 3, "name": "Street Samurai"},
    {"type": "premium", "num": 4, "name": "Hacker's Glide"},
    {"type": "premium", "num": 5, "name": "Dysto Drifter"},
    {"type": "premium", "num": 6, "name": "Plasma Fury"},
    {"type": "premium", "num": 7, "name": "Void Whisper"},
    {"type": "premium", "num": 8, "name": "AI Overlord"},
    {"type": "premium", "num": 9, "name": "Cyber Zeus"},
    {"type": "premium", "num": 10, "name": "Neural Nightmare"},
    {"type": "premium", "num": 11, "name": "Rift Marauder"},
    {"type": "premium", "num": 12, "name": "Mech Titan"},
    {"type": "premium", "num": 13, "name": "Holo Mirage"},
    {"type": "premium", "num": 14, "name": "Entropy Beast"},
    {"type": "premium", "num": 15, "name": "Mega Hermes"},
    {"type": "premium", "num": 16, "name": "Quantum Leviathan"},
    {"type": "premium", "num": 17, "name": "Bio-Fusion Predator"},
    {"type": "premium", "num": 18, "name": "Ares Warlord"},
    {"type": "premium", "num": 19, "name": "Stellar Vortex"},
    {"type": "premium", "num": 20, "name": "Chrono Phantom"},
    {"type": "premium", "num": 21, "name": "Olympus Eternal"},
    {"type": "premium", "num": 22, "name": "Abyss Sovereign"},
    {"type": "premium", "num": 23, "name": "Neural Sovereign"},
    {"type": "premium", "num": 24, "name": "Entropy Emperor"},
    {"type": "premium", "num": 25, "name": "Multiversal Odin"},
    {"type": "premium", "num": 26, "name": "Merlin's Apex"},
]

selected_sled = None  # To store chosen sled

def draw_menu():
    screen.fill(DARK_BG)
    
    # Title
    title_text = title_font.render("Select Your Sled for the Level", True, GOLD)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
    
    # Scrollable list (simple, assume all fit or add scrolling later)
    y_offset = 80
    for sled in sleds:
        key = f'{sled["type"]}{sled["num"]}'
        status = "Unlocked" if key in unlocked_sleds else "Locked"
        color = SELECTED_GREEN if selected_sled == key else GLOW_GREEN if status == "Unlocked" else LOCKED_GRAY
        sled_text = body_font.render(f"{sled['name']} ({status})", True, color)
        screen.blit(sled_text, (50, y_offset))
        
        # Preview if unlocked
        if status == "Unlocked":
            try:
                module_name = f'bobsled_{sled["type"]}{sled["num"]}'
                module = importlib.import_module(module_name)
                # Assume draw_bobsled function; draw small preview
                module.draw_bobsled(SCREEN_WIDTH - 150, y_offset + 10, scale=0.5)  # Pseudo, adjust per sled code
            except:
                pass
        
        y_offset += 40
    
    # Confirm button
    pygame.draw.rect(screen, NEON_BLUE, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50))
    confirm_text = body_font.render("Select & Start Level", True, DARK_BG)
    screen.blit(confirm_text, (SCREEN_WIDTH // 2 - confirm_text.get_width() // 2, SCREEN_HEIGHT - 70))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check sled clicks (approx positions)
                for idx, sled in enumerate(sleds):
                    sled_y = 80 + idx * 40
                    if 50 < x < 400 and sled_y < y < sled_y + 30:
                        key = f'{sled["type"]}{sled["num"]}'
                        if key in unlocked_sleds:
                            global selected_sled
                            selected_sled = key
                            print(f"Selected: {sled['name']}")  # Placeholder; load level with this sled
                # Confirm button
                if SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT - 80 < y < SCREEN_HEIGHT - 30:
                    if selected_sled:
                        running = False  # Proceed to level
                        # Here, return or call level with selected_sled
    
        draw_menu()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
