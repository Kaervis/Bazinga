import sys
import os
from asteroid import Asteroid
import random
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS,
    ASTEROID_SPAWN_RATE_SECONDS,
)
from asteroid import Asteroid
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle

HIGHSCORE_FILE = "highscore.txt"

def load_highscore() -> int:
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 0
    return 0

def save_highscore(score: int) -> None:
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

def generate_starfield(width: int, height: int, count: int) -> pygame.Surface:
    starfield = pygame.Surface((width, height), pygame.SRCALPHA)
    for _ in range(count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        alpha = random.randint(80, 255)
        size = random.choice([2, 2, 2, 3])
        pygame.draw.rect(starfield, (255, 255, 255, alpha), (x, y, size, size))
    return starfield

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    font = pygame.font.Font("freesansbold.ttf", 20)
    large_font = pygame.font.Font("freesansbold.ttf", 52)
    bg_stars = generate_starfield(SCREEN_WIDTH, SCREEN_HEIGHT, 200)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)

    STATE_TITLE = "title"
    STATE_PLAYING = "playing"
    STATE_CONTROLS = "controls"
    STATE_POWERUPS = "powerups"

    current_state = STATE_TITLE
    menu_options = ["PLAY", "CONTROLS", "POWERUPS"]
    selected_option = 0

    score = 0
    high_score = load_highscore()
    lives = 3
    game_over = False
    player = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if current_state == STATE_TITLE:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        choice = menu_options[selected_option]
                        if choice == "PLAY":
                            current_state = STATE_PLAYING
                            score = 0
                            lives = 3
                            game_over = False
                            updatable.empty()
                            drawable.empty()
                            asteroids.empty()
                            shots.empty()
                            player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            AsteroidField()
                        elif choice == "CONTROLS":
                            current_state = STATE_CONTROLS
                        elif choice == "POWERUPS":
                            current_state = STATE_POWERUPS

                elif current_state in (STATE_CONTROLS, STATE_POWERUPS):
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        current_state = STATE_TITLE

                elif current_state == STATE_PLAYING and game_over:
                    if event.key == pygame.K_RETURN:
                        current_state = STATE_TITLE

        if current_state == STATE_PLAYING and not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        if asteroid.radius <= ASTEROID_MIN_RADIUS:
                            points = 300
                        elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                            points = 200
                        else:
                            points = 100

                        score += points
                        if score > high_score:
                            high_score = score
                            save_highscore(high_score)

                        shot.kill()
                        asteroid.split()

            if player is not None and player.alive():
                for asteroid in asteroids:
                    if asteroid.collides_with(player):
                        lives -= 1
                        asteroid.kill()

                        if lives > 0:
                            player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            player.velocity = pygame.Vector2(0, 0)
                        else:
                            game_over = True
                            player.kill()

        screen.fill("black")
        screen.blit(bg_stars, (0, 0))

        if current_state == STATE_TITLE:
            title_surf = large_font.render("ASTEROIDS", False, "white")
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120))
            screen.blit(title_surf, title_rect)

            for i, option in enumerate(menu_options):
                color = "yellow" if i == selected_option else "white"
                prefix = "> " if i == selected_option else "  "
                opt_surf = font.render(f"{prefix}{option}", False, color)
                opt_rect = opt_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + (i * 45)))
                screen.blit(opt_surf, opt_rect)

        elif current_state == STATE_CONTROLS:
            title_surf = large_font.render("CONTROLS", False, "white")
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 120))
            screen.blit(title_surf, title_rect)

            ctrl_lines = [
                "W  - MOVE FORWARD",
                "A  - ROTATE LEFT",
                "S  - MOVE BACKWARD",
                "D  - ROTATE RIGHT",
                "SPACE - FIRE SHOT",
                "",
                "PRESS ENTER OR ESC TO RETURN",
            ]
            for i, line in enumerate(ctrl_lines):
                line_surf = font.render(line, False, "white" if i < 5 else "yellow")
                line_rect = line_surf.get_rect(center=(SCREEN_WIDTH / 2, 240 + (i * 35)))
                screen.blit(line_surf, line_rect)

        elif current_state == STATE_POWERUPS:
            title_surf = large_font.render("POWERUPS", False, "white")
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 120))
            screen.blit(title_surf, title_rect)

            msg_surf = font.render("COMING SOON...", False, "yellow")
            sub_surf = font.render("PRESS ENTER OR ESC TO RETURN", False, "white")
            screen.blit(msg_surf, msg_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
            screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60)))

        elif current_state == STATE_PLAYING:
            for obj in drawable:
                obj.draw(screen)

            score_surf = font.render(f"SCORE: {score}", False, "white")
            high_score_surf = font.render(f"HIGH SCORE: {high_score}", False, "white")
            lives_surf = font.render(f"LIVES: {lives}", False, "white")

            screen.blit(score_surf, (20, 20))
            screen.blit(high_score_surf, (20, 55))
            screen.blit(lives_surf, (SCREEN_WIDTH - 140, 20))

            if game_over:
                go_surf = large_font.render("GAME OVER", False, "red")
                restart_surf = font.render("PRESS ENTER FOR MENU", False, "white")

                go_rect = go_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30))
                restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))

                screen.blit(go_surf, go_rect)
                screen.blit(restart_surf, restart_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

if __name__ == "__main__":
    main()