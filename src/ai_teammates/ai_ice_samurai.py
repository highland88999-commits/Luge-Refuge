import pygame
import math

# AI Teammate: Ice Samurai
# Lore: Honorable blade-master forged in the frozen underbelly of the megacity, wielding a katana of pure synth-ice that carves victory from chaos. A stoic warrior whose precision cuts through any turn, channeling ancestral fury for unyielding grip in the face of the gods' trials.
# Visual: Red scarf, katana topknot (circle head with blade hat and scarf accent).
# Gestures:
# - Idle: Subtle scarf flutter like wind-swept banner.
# - Cheer: Katana slash arc with ice trail.
# - Glitch: Ice crack shatter with fragments.
# Stats: Grip +4%, Chaos +2%
# Hoodie Match: "Ice Blade Hoodie" (red/black with katana embroidery, inspired by Street Samurai sled).
# Unlock Level: 1 (starting)

class IceSamurai:
    def __init__(self):
        self.stats = {'speed': 0, 'grip': 4, 'jump': 0, 'chaos': 2}  # % boosts
        self.lore = "Honorable blade-master forged in the frozen underbelly of the megacity, wielding a katana of pure synth-ice that carves victory from chaos."
        self.hoodie_match = "Ice Blade Hoodie (red/black with katana embroidery)"

    def draw(self, screen, x, y, state='idle'):
        # Base head (circle)
        pygame.draw.circle(screen, (200, 0, 0), (x, y), 16)  # Red base for warrior vibe
        
        # Red scarf
        pygame.draw.rect(screen, (255, 0, 0), (x - 16, y + 8, 32, 8))  # Scarf
        
        # Katana topknot (blade hat)
        pygame.draw.line(screen, (192, 192, 192), (x, y - 16), (x, y - 24), 4)  # Handle
        pygame.draw.line(screen, (192, 192, 192), (x, y - 24), (x + 10, y - 28), 3)  # Blade tip
        
        # Gestures
        if state == 'idle':
            # Scarf flutter
            flutter_offset = int(4 * math.sin(pygame.time.get_ticks() / 500))
            pygame.draw.rect(screen, (255, 0, 0), (x - 16 + flutter_offset, y + 8, 32, 8))
        elif state == 'cheer':
            # Katana slash arc with ice trail
            for i in range(5):
                arc_x = x + i * 4
                arc_y = y - i * 2
                pygame.draw.line(screen, (0, 255, 255), (x, y - 10), (arc_x, arc_y), 3)  # Ice blue trail
        elif state == 'glitch':
            # Ice crack shatter
            for _ in range(5):
                sx = random.randint(x - 16, x + 16)
                sy = random.randint(y - 16, y + 16)
                end_x = sx + random.randint(-6, 6)
                end_y = sy + random.randint(-6, 6)
                pygame.draw.line(screen, (0, 255, 255), (sx, sy), (end_x, end_y), 2)

# Example usage (for testing - remove in integration)
if __name__ == "__main__":
    screen = pygame.display.set_mode((100, 100))
    clock = pygame.time.Clock()
    running = True
    ai = IceSamurai()
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
