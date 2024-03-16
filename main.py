import pygame
import math
from planet import Planet
pygame.init()

#Used to set our screen size
WIDTH, HEIGHT = 600, 600

#Set Window Size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#Set Title
pygame.display.set_caption("Solar System Simulation")

#Background image path
BACKGROUND_PATH = "images\Background.jpg"

YELLOW = (255, 255, 0)


def main():
    run = True

    #Used to set framerate of project
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, "images\Sun.png", 1.989e+30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, "images\Earth.png", 5.972e+24)

    planets = [sun, earth]

    # Load background image
    background_image = pygame.image.load(BACKGROUND_PATH)

    # Scale background image to match window size
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    WIN.blit(background_image, (0, 0))

    while run:
        #FPS = 60
        clock.tick(60)

        for planet in planets:
            planet.draw(WIN, WIDTH, HEIGHT)

        pygame.display.update()

        #If 'X' button is hit on the window, close the window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit

main()