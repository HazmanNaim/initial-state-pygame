import pygame
import sys
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60
G = 6.67430e-11  # Gravitational constant
SCALE = 1e8  # Scale factor for visualization (1 pixel = 1e9 meters)
TIME_STEP = 3600 * 24  # Time step in seconds (1 day)
YEARS_TO_WIN = 10
SECONDS_PER_YEAR = 365.25 * 24 * 3600

# Increase gravitational effect for better gameplay
GRAVITY_MULTIPLIER = 5000  # Amplify gravity for better visual effect

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TRAIL_COLOR = (100, 100, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)

# Game states
MENU = 0
PLACING = 1
DRAGGING = 2
SIMULATING = 3
GAME_OVER = 4
WIN = 5

# Goldilocks zone (in millions of km)
MIN_SAFE_DISTANCE = 10
MAX_SAFE_DISTANCE = 100
DANGER_CLOSE = 20
DANGER_FAR = 200

class Star:
    def __init__(self):
        self.pos = CENTER
        self.mass = 1.989e30
        self.radius = 20
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.pos, self.radius)
        for r in range(self.radius + 5, self.radius + 20, 5):
            intensity = max(0, min(255, 100 - r * 5))
            pygame.draw.circle(screen, (255, 165, intensity), self.pos, r, 1)

class Colony:
    def __init__(self, pos, vel=(0, 0)):
        self.pos = pos
        self.vel = vel
        self.mass = 1e6
        self.radius = 5
        self.trail = []
        self.max_trail_length = 500
        self.stability = 100
        self.temperature = 0
    def update(self, star, dt):
        dx = star.pos[0] - self.pos[0]
        dy = star.pos[1] - self.pos[1]
        distance_pixels = math.hypot(dx, dy)
        r = distance_pixels * SCALE
        if r <= (star.radius + self.radius) * SCALE:
            return False
        force = G * self.mass * star.mass / (r * r) * GRAVITY_MULTIPLIER
        angle = math.atan2(dy, dx)
        ax = force * math.cos(angle) / self.mass
        ay = force * math.sin(angle) / self.mass
        self.vel = (self.vel[0] + ax * dt / SCALE, self.vel[1] + ay * dt / SCALE)
        self.pos = (self.pos[0] + self.vel[0] * dt / SCALE,
                    self.pos[1] + self.vel[1] * dt / SCALE)
        self.trail.append(self.pos)
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        if (self.pos[0] < -50 or self.pos[0] > WIDTH + 50 or self.pos[1] < -50 or self.pos[1] > HEIGHT + 50):
            return False
        distance_mkm = distance_pixels * SCALE / 1e9
        if distance_mkm < DANGER_CLOSE:
            self.stability -= 0.5 * (DANGER_CLOSE - distance_mkm) / DANGER_CLOSE
            self.temperature = 1
        elif distance_mkm > DANGER_FAR:
            self.stability -= 0.3 * (distance_mkm - DANGER_FAR) / DANGER_FAR
            self.temperature = -1
        else:
            if MIN_SAFE_DISTANCE <= distance_mkm <= MAX_SAFE_DISTANCE:
                self.stability = min(100, self.stability + 0.01)
            self.temperature = 0
        self.stability = max(0, min(100, self.stability))
        return self.stability > 0
    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, TRAIL_COLOR, False, self.trail, 2)
        pygame.draw.circle(screen, BLUE, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Initial State - EON-1 Orbital Mission")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.reset_game()
    def reset_game(self):
        self.star = Star()
        self.colony = None
        self.state = MENU
        self.start_pos = None
        self.current_pos = None
        self.elapsed_time = 0
        self.years_survived = 0
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if self.state == MENU:
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if WIDTH//2 - 100 < x < WIDTH//2 + 100 and HEIGHT//2 + 50 < y < HEIGHT//2 + 100:
                        self.state = PLACING
            else:
                if event.type == KEYDOWN:
                    if event.key == K_r or (self.state in [GAME_OVER, WIN] and event.key == K_SPACE):
                        self.reset_game()
                if self.state == PLACING and event.type == MOUSEBUTTONDOWN:
                    self.start_pos = pygame.mouse.get_pos()
                    self.colony = Colony(self.start_pos)
                    self.state = DRAGGING
                if self.state == DRAGGING:
                    if event.type == MOUSEMOTION:
                        self.current_pos = pygame.mouse.get_pos()
                    elif event.type == MOUSEBUTTONUP:
                        end_pos = pygame.mouse.get_pos()
                        dx, dy = end_pos[0] - self.start_pos[0], end_pos[1] - self.start_pos[1]
                        self.colony.vel = (-dx * 5, -dy * 5)
                        self.state = SIMULATING
                        self.current_pos = None
    def update(self):
        if self.state == SIMULATING:
            if not self.colony.update(self.star, TIME_STEP):
                self.state = GAME_OVER
                return
            self.elapsed_time += TIME_STEP
            self.years_survived = self.elapsed_time / SECONDS_PER_YEAR
            if self.years_survived >= YEARS_TO_WIN:
                self.state = WIN
    def draw(self):
        self.screen.fill(BLACK)
        if self.state == MENU:
            title_surf = self.title_font.render("Initial State", True, WHITE)
            title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            self.screen.blit(title_surf, title_rect)
            desc = "Pilot a small colony through gravity to find a stable orbit & survive 10 years"
            desc_surf = self.font.render(desc, True, WHITE)
            desc_rect = desc_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(desc_surf, desc_rect)
            mx, my = pygame.mouse.get_pos()
            btn_color = BUTTON_HOVER if WIDTH//2 - 100 < mx < WIDTH//2 + 100 and HEIGHT//2 + 50 < my < HEIGHT//2 + 100 else BUTTON_COLOR
            pygame.draw.rect(self.screen, btn_color, (WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50))
            play_surf = self.font.render("Play", True, WHITE)
            play_rect = play_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 75))
            self.screen.blit(play_surf, play_rect)
            pygame.display.flip()
            return
        # Non-menu drawing
        self.star.draw(self.screen)
        if self.colony:
            self.colony.draw(self.screen)
            if self.state == DRAGGING and self.current_pos:
                pygame.draw.line(self.screen, WHITE, self.start_pos, self.current_pos, 2)
        if self.state == PLACING:
            inst = self.font.render("Click to place the EON-1 colony", True, WHITE)
            self.screen.blit(inst, (20, 20))
        else:
            if self.colony:
                dx = self.star.pos[0] - self.colony.pos[0]
                dy = self.star.pos[1] - self.colony.pos[1]
                dist = math.hypot(dx, dy) * SCALE / 1e9
                self.screen.blit(self.font.render(f"Years: {self.years_survived:.2f}/{YEARS_TO_WIN}", True, WHITE), (20,20))
                self.screen.blit(self.font.render(f"Dist: {dist:.2f}Mkm", True, WHITE), (20,50))
                self.screen.blit(self.font.render(f"Stability: {self.colony.stability:.1f}%", True, WHITE), (20,80))
                if self.colony.temperature > 0:
                    self.screen.blit(self.font.render("WARNING: Too close to star!", True, RED), (20,110))
                elif self.colony.temperature < 0:
                    self.screen.blit(self.font.render("WARNING: Too far from star!", True, BLUE), (20,110))
        if self.state == GAME_OVER:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,128)); self.screen.blit(overlay,(0,0))
            go = self.title_font.render("MISSION FAILED", True, RED)
            self.screen.blit(go, go.get_rect(center=(WIDTH//2,HEIGHT//2-50)))
            reason = self.font.render("Game Over", True, WHITE)
            self.screen.blit(reason, reason.get_rect(center=(WIDTH//2,HEIGHT//2)))
            self.screen.blit(self.font.render("Press R/SPACE to restart", True, WHITE), (WIDTH//2-100, HEIGHT//2+50))
        if self.state == WIN:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,128)); self.screen.blit(overlay,(0,0))
            ws = self.title_font.render("MISSION SUCCESSFUL!", True, GREEN)
            self.screen.blit(ws, ws.get_rect(center=(WIDTH//2,HEIGHT//2-50)))
            msg = self.font.render(f"Survived {YEARS_TO_WIN} years!", True, WHITE)
            self.screen.blit(msg, msg.get_rect(center=(WIDTH//2,HEIGHT//2)))
            self.screen.blit(self.font.render("Press R/SPACE to restart", True, WHITE), (WIDTH//2-100, HEIGHT//2+50))
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    Game().run()
