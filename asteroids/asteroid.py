import math
import random
import pygame
from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        self.points = self._generate_rock_points()

    def _generate_rock_points(self) -> list[pygame.Vector2]:
        points = []
        num_vertices = random.randint(8, 12)
        
        for i in range(num_vertices):

            angle = (2 * math.pi / num_vertices) * i

            distance = self.radius * random.uniform(0.7, 1.1)
            
            px = math.cos(angle) * distance
            py = math.sin(angle) * distance
            points.append(pygame.Vector2(px, py))
            
        return points

    def draw(self, screen: pygame.Surface) -> None:

        transformed_points = [self.position + p for p in self.points]

        pygame.draw.polygon(screen, "black", transformed_points)
        
        pygame.draw.polygon(screen, "white", transformed_points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)

        vel1 = self.velocity.rotate(random_angle)
        vel2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vel1 * 1.2

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vel2 * 1.2
