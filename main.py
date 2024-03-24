import pygame
import math
from planet import Planet

pygame.init()

# Used to set our screen size
WIDTH, HEIGHT = 800, 800

# Set Window Size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set Title
pygame.display.set_caption("Solar System Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (165, 145, 134)
DARK_BLUE = (0, 0, 255)

# Initial zoom scale and panning offset
scale = 1.0
offset_x = 400
offset_y = 400

def main():
    global scale, offset_x, offset_y, dragging, last_mouse_pos

    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 3, DARK_GREY, 3.30 * 10**23)
    mercury.vy = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 6, WHITE, 4.8685 * 10**24)
    venus.vy = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 8, BLUE, 5.9742 * 10**24)
    earth.vy = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 5, RED, 6.39 * 10**23)
    mars.vy = 24.077 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 25, BROWN, 1.898 * 10**27)
    jupiter.vy = -13.06 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 20, YELLOW, 568.32 * 10**24)
    saturn.vy = -9.67 * 1000

    uranus = Planet(19 * Planet.AU, 0, 17, BLUE, 86.811 * 10**24)
    uranus.vy = -6.79 * 1000

    neptune = Planet(30 * Planet.AU, 0, 19, DARK_BLUE, 102.409 * 10**24)
    neptune.vy = -5.45 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    dragging = False

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll up
                    scale *= 1.1
                elif event.button == 5:  # scroll down
                    scale /= 1.1
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, scale, (offset_x, offset_y))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
