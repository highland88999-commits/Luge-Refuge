import pygame

# AI Teammate: Neon Hacker
# Lore: Neon-veined prodigy who hacks reality's code, turning ice to lightning. A digital demigod born from the megacity's undergrid, wielding code like Zeus's bolt to slice through obstacles.
# Visual: Green visor hat, blue circuit hair (circle head with accents).
# Gestures:
# - Idle: Subtle glow pulse.
# - Cheer: Code rain upward burst.
# - Glitch: Screen static flicker.
# Stats: Speed +3%, Grip +1%
# Hoodie Match: "Neon Glow Hoodie" (inspired by Neon Phantom sled - cyber-blue with glowing circuits).
# Unlock Level: 1 (starting)

class NeonHacker:
    def __init__(self):
        self.stats = {'speed': 3, 'grip': 1, 'jump': 0, 'chaos': 0}  # % boosts
        self.lore = "Neon-veined prodigy who hacks reality's code, turning ice to lightning."
        self.hoodie_match = "Neon Glow Hoodie (cyber-blue with glowing circuits)"

    def draw(self, screen, x, y, state='idle'):
        # Base head (circle)
        pygame.draw.circle(screen, (0, 0, 255), (x, y), 16)  # Blue hair base
        
        # Green visor hat
        pygame.draw.rect(screen, (0, 255, 0), (x - 14, y - 18, 28, 8))  # Visor
        
        # Gestures
        if state == 'idle':
            # Glow pulse
            alpha = int(128 * (math.sin(pygame.time.get_ticks() / 500) + 1))
            glow_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (0, 255, 0, alpha), (16, 16), 18)
            screen.blit(glow_surf, (x - 16, y - 16))
        elif state == 'cheer':
            # Code rain burst
            for i in range(5):
                rain_y = y + i * 4
                pygame.draw.line(screen, (0, 255, 0), (x - 5, rain_y - 10), (x - 5, rain_y), 2)
                pygame.draw.line(screen, (0, 255, 0), (x + 5, rain_y - 10), (x + 5, rain_y), 2)
        elif state == 'glitch':
            # Static flicker
            for _ in range(10):
                sx = random.randint(x - 16, x + 16)
                sy = random.randint(y - 16, y + 16)
                pygame.draw.line(screen, (255, 255, 255), (sx, sy), (sx + random.randint(-4, 4), sy), 1)

# Example usage (for testing - remove in integration)
if __name__ == "__main__":
    screen = pygame.display.set_mode((100, 100))
    clock = pygame.time.Clock()
    running = True
    ai = NeonHacker()
    state = 'idle'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    state = 'idle'
                elif event.key == pygame.K_2:
                    state = 'cheer'
                elif event.key == pygame.K_3:
                    state = 'glitch'
        
        screen.fill(DARK_BG)
        ai.draw(screen, 50, 50, state)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()
