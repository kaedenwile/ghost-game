import pygame, math, random

SCREEN_SIZE = 800
FPS = 60
GHOST_SPEED = 2
GHOST_ACCELERATION = 1.0006
MAX_ANGLE = ANGLE = math.pi / 4
FLASHLIGHT_SHRINK = 0.999995
SCORE, DIRECTION, IS_GAME_OVER = 0, 0, False

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("GHOST GAME")
game_clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
ghosts = pygame.sprite.Group()
font = pygame.font.SysFont("", 36)

def polar_coords(distance, direction):
    return (SCREEN_SIZE / 2 + distance * math.cos(direction), SCREEN_SIZE / 2 + distance * math.sin(direction))

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_ghost = random.randint(1, 100) < 90
        self.image = pygame.image.load("./ghost.png" if self.is_ghost else "./power.png")
        self.direction = random.random() * 2 * math.pi
        self.distance = SCREEN_SIZE / math.sqrt(2)
        self.update()
    def update(self):
        global SCORE, GHOST_SPEED, IS_GAME_OVER, ANGLE
        self.distance -= GHOST_SPEED
        self.rect = self.image.get_rect(center=polar_coords(self.distance, self.direction))
        if screen.get_rect().colliderect(self.rect) and self.direction > DIRECTION - ANGLE and self.direction < DIRECTION + ANGLE:
            self.kill()
            if self.is_ghost:
                SCORE += 1
            else:
                GHOST_SPEED *= 1.1
        elif self.distance < 20:
            if self.is_ghost:
                IS_GAME_OVER = True
            else:
                ANGLE = MAX_ANGLE
                self.kill()
      
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif not IS_GAME_OVER and event.type == pygame.USEREVENT:
            Ghost().add(ghosts)

    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, (255, 175, 175), [
        (SCREEN_SIZE / 2, SCREEN_SIZE / 2),
        polar_coords(SCREEN_SIZE, DIRECTION - ANGLE),
        polar_coords(SCREEN_SIZE, DIRECTION + ANGLE),
    ])
    ghosts.draw(screen)
    screen.blit(font.render(f"Score: {SCORE}", True, (255, 0, 0)), (0, 0))

    if IS_GAME_OVER:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_SIZE/2, SCREEN_SIZE/2))
        screen.blit(game_over_text, text_rect)
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            DIRECTION -= math.pi / 50
        elif keys[pygame.K_RIGHT]:
            DIRECTION += math.pi / 50
        DIRECTION = (DIRECTION + 2 * math.pi) % (2 * math.pi)
        GHOST_SPEED *= GHOST_ACCELERATION
        ANGLE *= FLASHLIGHT_SHRINK
        ghosts.update()
        
    pygame.display.update()
    game_clock.tick(FPS)
