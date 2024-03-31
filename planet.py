import pygame
import math
import random

#Planet class which takes realistic values, and uses them for update function
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

        #if other.sun:
            #self.distance_to_sun = distance

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

#Asteroid class, child to planet which uses its initialization to make simple circle objects.
class Asteroid(Planet):
    def __init__(self, x, y, radius, color, mass, star_ref):
        super().__init__(x, y, radius, color, mass)
        #Asteroid size means the size of an asteroid, all instances are 3 in this case. In planet, radius refers to the size of planet.
        #Radius for asteroid child class refers to radius of orbit around the parent star/planet
        self.size = 3
        #Angle is the angle that is used to complete a full orbit and incremented per update.
        self.angle = 0
        #Reference to star
        self.star_ref = star_ref

    def draw(self, win, scale, offset):
        scaled_x = self.x * self.SCALE * scale + offset[0]
        scaled_y = self.y * self.SCALE * scale + offset[1]
        pygame.draw.circle(win, self.color, (int(scaled_x), int(scaled_y)), max(int(self.size * scale), 1))

    #Use the angle, increment it by a value- determines how fast the angular velocity is essentially per step.
    def update_position(self, planets,val):
        self.angle -= val
        #Get x and y component based on new angle
        x = self.radius*math.cos(self.angle)
        y = self.radius*math.sin(self.angle)

        #Set position to x and y from the reference star/planet.
        self.x = x+self.star_ref.x
        self.y = y+ self.star_ref.y

        



#Asteroid belt class used to form asteroid belts in solar system.
class AsteroidBelt:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 300 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day
    COLOR = (169, 169, 169)
    #Create list of asteroid objects, and their reference point.
    def __init__(self, num_asteroids, sun):
        self.asteroids = []
        self.sun = sun  # Assuming the sun is a Planet object

        #Create this asteroid belt on instantiation
        self.create_asteroid_belt(num_asteroids)

    def create_asteroid_belt(self, num_asteroids):
        #Angle initially is 0, and increases so each star placed around uniformly.
        angle = 0.001
        for _ in range(num_asteroids):
            #Radius, bandwith of asteroid belt in solar system(Width), to pick a random value in for the radius of their orbits. 
            #Each asteroid will have random in this range.
            ranradius = random.uniform(self.AU * 2.2, self.AU *3.9)
            #X and Y Components from this radius
            x = ranradius * math.cos(angle)
            y = ranradius * math.sin(angle)
            #Random mass per asteroid
            mass = random.uniform(1E12,1E14)
            #Create the object
            asteroid = Asteroid(x, y,ranradius,self.COLOR, mass,self.sun)
            #Increment the angle, so that it spawns in a new area around the belt.
            asteroid.angle += angle
            #Increment this angle so we have a new one for next asteroid creation further around circle.
            angle += 0.022421 
            self.asteroids.append(asteroid)
            

    def draw(self, win, scale, offset):
        for asteroid in self.asteroids:
            asteroid.draw(win, scale, offset)

    def update_positions(self,planets):
        for asteroid in self.asteroids:
            asteroid.update_position(planets,0.002)
        


        
        