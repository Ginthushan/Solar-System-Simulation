import pygame
import math
import random
pygame.init()
FONT = pygame.font.SysFont("comicsans", 16)
WHITE = (255, 255, 255)

#Planet class which takes realistic values, and uses them for update function
class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 300 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day

    # Contrustor, take in x and y position, radius, color of planet and mass (kg)
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

    # Function used to draw the planet
    def draw(self, win, scale, offset, d_o, d_d):
        scaled_x = self.x * self.SCALE * scale + offset[0]
        scaled_y = self.y * self.SCALE * scale + offset[1]

        # If Draw Orbit (d_o) true, display orbit
        if d_o == True:
            if len(self.orbit) > 2:
                updated_points = []
                for point in self.orbit:
                    x, y = point
                    x = x * self.SCALE * scale + offset[0]
                    y = y * self.SCALE * scale + offset[1]
                    updated_points.append((x, y))
                if self.sun == False:
                    pygame.draw.lines(win, self.color, False, updated_points, 2)
        if d_o == False:
            self.orbit.clear()

        pygame.draw.circle(win, self.color, (scaled_x, scaled_y), int(self.radius * scale))

        # If Draw Distance (d_d) true, display distance (km)
        if d_d == True:
            if not self.sun:
                distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
                win.blit(distance_text, (scaled_x - distance_text.get_width()/2, scaled_y - distance_text.get_height()/2))

    #Calculates the gravitational force vector between two objects, considering their masses and distances
    def attraction(self, other):
        distance_vector = [other.x - self.x, other.y - self.y]
        distance = math.sqrt(distance_vector[0] ** 2 + distance_vector[1] ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force_magnitude = self.G * self.mass * other.mass / distance ** 2
        force_vector = [force_magnitude * distance_vector[0] / distance,  force_magnitude * distance_vector[1] / distance]

        return force_vector

    # Updates the position of a celestial object based on the gravitational forces exerted by other planets in the system
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
    def update_position(self, val):
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
    def __init__(self, num_asteroids, sun,range_start,range_end,angle_inc = 0.022421):
        self.asteroids = []
        self.sun = sun  # Assuming the sun is a Planet object
        self.angle_inc = angle_inc

        #Create this asteroid belt on instantiation
        self.create_asteroid_belt(num_asteroids,range_start,range_end)

    def create_asteroid_belt(self, num_asteroids,range_start, range_end):
        #Angle initially is 0, and increases so each star placed around uniformly.
        angle = 0.001
        for _ in range(num_asteroids):
            #Radius, bandwith of asteroid belt in solar system(Width), to pick a random value in for the radius of their orbits. 
            #Each asteroid will have random in this range.
            ranradius = random.uniform(range_start*self.AU, range_end * self.AU)
            #X and Y Components from this radius
            x = ranradius * math.cos(angle) + self.sun.x
            y = ranradius * math.sin(angle) + self.sun.y
            #Random mass per asteroid
            mass = random.uniform(1E12,1E14)
            #Create the object
            asteroid = Asteroid(x, y,ranradius,self.COLOR, mass,self.sun)
            #Increment the angle, so that it spawns in a new area around the belt.
            asteroid.angle += angle
            #Increment this angle so we have a new one for next asteroid creation further around circle.
            angle += self.angle_inc
            self.asteroids.append(asteroid)
            

    def draw(self, win, scale, offset):
        for asteroid in self.asteroids:
            asteroid.draw(win, scale, offset)

    def update_positions(self,val):
        for asteroid in self.asteroids:
            asteroid.update_position(val)
        


        
        