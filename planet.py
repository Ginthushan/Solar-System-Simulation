import pygame
import math
import random

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 300 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.vx = 0
        self.vy = 0

    def draw(self, win, scale, offset):
        scaled_x = self.x * self.SCALE * scale + offset[0]
        scaled_y = self.y * self.SCALE * scale + offset[1]

        pygame.draw.circle(win, self.color, (scaled_x, scaled_y), int(self.radius * scale))

    def attraction(self, other):
        distance_vector = [other.x - self.x, other.y - self.y]
        distance = math.sqrt(distance_vector[0] ** 2 + distance_vector[1] ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force_magnitude = self.G * self.mass * other.mass / distance ** 2
        force_vector = [force_magnitude * distance_vector[0] / distance,  force_magnitude * distance_vector[1] / distance]

        return force_vector

    def update_position(self, planets):
        total_force_x = 0
        total_force_y = 0

        # Calculate total force acting on the planet
        for planet in planets:
            if self != planet:
                force = self.attraction(planet)
                total_force_x += force[0]
                total_force_y += force[1]

        # Calculate acceleration
        acceleration_x = total_force_x / self.mass
        acceleration_y = total_force_y / self.mass

        # Update velocity
        self.vx += acceleration_x * self.TIMESTEP
        self.vy += acceleration_y * self.TIMESTEP

        # Update position
        self.x += self.vx * self.TIMESTEP
        self.y += self.vy * self.TIMESTEP

        # Append current position to orbit
        self.orbit.append((self.x, self.y))


class Asteroid(Planet):
    def __init__(self, x, y, radius, color, mass, sun_ref):
        super().__init__(x, y, radius, color, mass)
        self.sun_ref = sun_ref
        self.distance_to_sun = 0    

    def draw(self, win, scale, offset):
        scaled_x = self.x * self.SCALE * scale + offset[0]
        scaled_y = self.y * self.SCALE * scale + offset[1]
        pygame.draw.circle(win, self.color, (int(scaled_x), int(scaled_y)), max(int(self.radius * scale), 1))


    
class AsteroidBelt:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 300 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day
    def __init__(self, num_asteroids, sun):
        self.asteroids = []
        self.sun = sun  # Assuming the sun is a Planet object
        self.create_asteroid_belt(num_asteroids)

    def create_asteroid_belt(self, num_asteroids):
        for _ in range(num_asteroids):
            # Randomly generate asteroid properties within the belt's range
            x = random.uniform(self.AU * 2.2, self.AU * 3.2)  # Example range
            y = random.uniform(self.AU * 2.2, self.AU * 3.2)
            radius = random.uniform(2, 3)  # Simplified example
            color = (169, 169, 169)  # Grey color
            mass = random.uniform(1E12, 1E14)  # Example masses
            
            asteroid = Asteroid(x, y, radius, color, mass,self.sun)
            asteroid.vy = -20 * 1000
            self.asteroids.append(asteroid)

    def draw(self, win, scale, offset):
        for asteroid in self.asteroids:
            asteroid.draw(win, scale, offset)

    def update_positions(self,planets):
        for asteroid in self.asteroids:
            asteroid.update_position(planets)
        


        
        