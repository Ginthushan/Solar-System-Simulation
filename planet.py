import pygame

class Planet:
    #Distance from the Sun to Earth in meters
    AU = 149.6e6 * 1000

    #Gravitational Constant
    G = 6.67428e-11

    #Scale compared to Real Life. (What 1 meters means in Pixels)
    SCALE = 250 / AU #1AU = 100 Pixels

    #Simulate how fast simulation moves
    TIMESTEP = 3600*24 

    #Constructor of our Planet
    def __init__(self, x, y, radius, image_path, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        #In KG
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.vx = 0
        self.vy = 0

    def draw(self, win, WIDTH, HEIGHT):
        x = self.x * self.SCALE + WIDTH / 2 - self.radius
        y = self.y * self.SCALE + HEIGHT / 2 - self.radius
        win.blit(self.image, (x, y))
        