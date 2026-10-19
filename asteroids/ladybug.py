import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Ladybug(pygame.sprite.Sprite):
    def __init__(self):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.radius = 12
        self.position = pygame.Vector2(
            random.randint(50, SCREEN_WIDTH - 50),
            random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.rect = pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        self.type = random.choice(["BACKWARD", "TRIPLE", "QUAD"])

    def update(self, dt):
        pass

    def draw(self, screen):
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, "red", center, self.radius)
        
        head_pos = (int(self.position.x), int(self.position.y - self.radius + 3))
        pygame.draw.circle(screen, "black", head_pos, 4)

        spot_offsets = [(-4, -2), (4, -2), (-4, 4), (4, 4)]
        for ox, oy in spot_offsets:
            pygame.draw.circle(screen, "black", (int(self.position.x + ox), int(self.position.y + oy)), 2)

        pygame.draw.line(
            screen,
            "black",
            (int(self.position.x), int(self.position.y - self.radius + 6)),
            (int(self.position.x), int(self.position.y + self.radius)),
            2
        )

    def collides_with(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius