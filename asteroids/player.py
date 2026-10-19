import random
import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    LINE_WIDTH,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)
from shot import Shot
from particle import Particle

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float):
        unit_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += unit_vector * PLAYER_SPEED * dt

        backward_vector = -unit_vector
        for _ in range(2):
            spread_angle = random.uniform(-25, 25)
            particle_vel = backward_vector.rotate(spread_angle) * random.uniform(80, 180)

            spawn_pos = self.position + (backward_vector *(self.radius * 0.8))
            Particle(spawn_pos.x, spawn_pos.y, particle_vel)
    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt: float):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
