import random
import pygame
from circleshape import CircleShape

class Particle(CircleShape):
    def __init__(self, x: float, y: float, velocity: pygame.Vector2, lifetime: float = 0.3) -> None:
        super().__init__(x, y, radius=random.uniform(1.5, 3.0))
        self.velocity = velocity
        self.lifetime = lifetime
        self.timer = lifetime

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        alpha_ratio = max(0.0, self.timer / self.lifetime)
        radius = max(1, int(self.radius * alpha_ratio))
        
        # Color transitions from orange/yellow to faint grey
        color = (255, int(150 * alpha_ratio), int(50 * alpha_ratio))
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), radius)
