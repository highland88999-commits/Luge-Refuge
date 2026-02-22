import pygame
import sys
import importlib  # For auto-calling sled previews

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

# Fonts
title_font = pygame.font.SysFont('couriernew', 32, bold=True)
body_font = pygame.font.SysFont('couriernew', 20)
small_font = pygame.font.SysFont('couriernew', 16)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyberpunk Luge: Premium Bobsled Store")

# Placeholder unlock state (e.g., load from file in full game)
unlocked_sleds = set()  # e.g., add 'premium1' if unlocked

# Tier data (for display)
tiers = [
    {"name": "Tier 1 ($0.99 each)", "sleds": range(1, 6), "price": 0.99},
    {"name": "Tier 2 ($2.99 each)", "sleds": range(6, 16), "price": 2.99},
    {"name": "Tier 3 ($9.99 each)", "sleds": range(16, 21), "price": 9.99},
    {"name": "Tier 4 ($13.99 each)", "sleds": range(21, 26), "price": 13.99},
    {"name": "Tier 5 ($49.99 - Ultra)", "sleds": [26], "price": 49.99},
]

buy_all_price = 102.00  # 50% bundle

def draw_store():
    screen.fill(DARK_BG)
    
    # Title
    title_text = title_font.render("Premium Bobsled Store", True, GOLD)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
    
    # Buy All button
    pygame.draw.rect(screen, NEON_BLUE, (SCREEN_WIDTH // 2 - 150, 70, 300, 50))
    buy_all_text = body_font.render(f"Buy All (26 Sleds) - $102 USD", True, DARK_BG)
    screen.blit(buy_all_text, (SCREEN_WIDTH // 2 - buy_all_text.get_width() // 2, 80))
    
    y_offset = 140
    for tier in tiers:
        tier_text = body_font.render(tier["name"], True, WHITE)
        screen.blit(tier_text, (50, y_offset))
        y_offset += 40
        for sled_num in tier["sleds"]:
            status = "Unlocked" if f'premium{sled_num}' in unlocked_sleds else "Locked - Buy for ${tier['price']}"
            color = GLOW_GREEN if "Unlocked" in status else LOCKED_GRAY
            sled_text = small_font.render(f"Bobsled Premium {sled_num}: {status}", True, color)
            screen.blit(sled_text, (70, y_offset))
            # Auto-call preview (import and draw mini version if unlocked)
            if "Unlocked" in status:
                try:
                    module = importlib.import_module(f'bobsleds.bobsled_premium{sled_num}')
                    # Assume each sled has a draw_bobsled function; scale small
                    module.draw_bobsled(SCREEN_WIDTH - 150, y_offset + 10, scale=0.5)  # Pseudo-call, adjust as needed
                except:
                    pass
            y_offset += 30
        y_offset += 20
    
    # Instructions
    instr_text = small_font.render("Purchase to unlock - Email confirmation for codes on Ultra", True, GOLD)
    screen.blit(instr_text, (50, SCREEN_HEIGHT - 40))

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Placeholder click handling (e.g., for Buy All - integrate payment API here)
                if SCREEN_WIDTH // 2 - 150 < event.pos[0] < SCREEN_WIDTH // 2 + 150 and 70 < event.pos[1] < 120:
                    print("Buy All clicked - Process $102 payment and unlock all!")  # Replace with actual payment call
    
        draw_store()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
