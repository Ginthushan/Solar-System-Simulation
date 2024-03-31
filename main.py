import pygame
import math
from planet import Planet
from planet import Asteroid
from planet import AsteroidBelt
import random
import pygame_gui

pygame.init()

# Used to set our screen size
WIDTH, HEIGHT = 800, 800

# Set Window Size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set Title
pygame.display.set_caption("Solar System Simulation")

# Set Color Variables
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
    # Set variables for panning and zooming camera
    global scale, offset_x, offset_y

    run = True
    clock = pygame.time.Clock() 

    # Create Sun and planets in solar system with realistic values
    sun = Planet(0, 0, 70, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    # List of planets to be used in our Solar System
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

    #Add all to list of planets
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    
    #Moons, which are instances of larger asteroids with a reference to a planet instead of a star
    moon = Asteroid(0, 0, 7.0E9, DARK_GREY, 102.409, earth)
   
    #Create Asteroidbelt instance and have 700 asteroids in this belt and the sun as reference
    asteroidbelt = AsteroidBelt(700,sun = sun)

    # Create a UIManager
    ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Create a slider
    slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 10), (200, 20)),
                                                     start_value=1.0,
                                                     value_range=(0.1, 5.0),
                                                     manager=ui_manager)

    # Create a label next to the slider
    slider_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((230, 10), (130, 20)),
                                                text="Simulation Speed",
                                                manager=ui_manager)

    # Create Buttons
    draw_orbits = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((10, 40), (150, 30)),
                                                           text="Draw Orbits",
                                                           manager=ui_manager)
    draw_distance = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((10, 70), (150, 30)),
                                                             text="Draw Distance",
                                                             manager=ui_manager)
    
    # If button pressed or not
    d_o = False
    d_d = False

    # Inside your main function before the main loop
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    background_surface.fill((0, 0, 0))  # Fill background with black

    # Draw stars on the background surface
    num_stars = 200  # Adjust as needed
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.uniform(1, 2)
        pygame.draw.circle(background_surface, WHITE, (x, y), radius)

    while run:
        time_delta = clock.tick(60) / 1000.0
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Zooming Camera
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll up
                    scale *= 1.1
                elif event.button == 5:  # scroll down
                    scale /= 1.1
            # If arrow keys are hit, pan camera to the direction by 40 pixels
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    offset_x -= 40
                elif event.key == pygame.K_RIGHT:
                    offset_x += 40
                if event.key == pygame.K_UP:
                    offset_y += 40
                elif event.key == pygame.K_DOWN:
                    offset_y -= 40
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Update simulation speed based on slider value
                    if event.ui_element == slider:
                        simulation_speed = slider.get_current_value()
                        for planet in planets:
                            planet.TIMESTEP = 3600 * 24 * simulation_speed
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Draw orbits or Draw distance if button pressed
                    if event.ui_element == draw_distance:
                        d_d = not d_d
                    elif event.ui_element == draw_orbits:
                        d_o = not d_o

            ui_manager.process_events(event)

        WIN.blit(background_surface, (0, 0))

        # Create planets and update per tick going through all planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, scale, (offset_x, offset_y), d_o, d_d)
        
        # Create the astroid belt and update
        asteroidbelt.update_positions(planets)
        asteroidbelt.draw(WIN,scale, (offset_x,offset_y))

        # Update and draw moons
        moon.update_position(planets,0.08)
        moon.draw(WIN,scale,(offset_x,offset_y))
        
        # Update and Display UI
        ui_manager.update(time_delta)
        ui_manager.draw_ui(WIN)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
