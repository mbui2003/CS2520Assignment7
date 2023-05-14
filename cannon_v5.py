import numpy as np
import pygame as pg
# from random import randint, choice, random
import math
import random

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = (800, 600)


def rand_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class GameObject:
    def move(self):
        pass

    def draw(self, screen):
        pass


class CircleShell(GameObject):
    '''
    The ball class. Creates a ball, controls its movement, and implements its rendering.
    '''

    def __init__(self, coord, vel, rad=20, color=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.

        Parameters:
        - coord (tuple): The initial coordinates of the ball.
        - vel (tuple): The initial velocity of the ball.
        - rad (int): The radius of the ball (default: 20).
        - color (tuple): The color of the ball (default: None, random color will be generated).

        Returns:
        None
        '''
        self.coord = coord  # Ball's coordinates
        self.vel = vel  # Ball's velocity
        if color is None:
            color = rand_color()  # Randomly generate color if not provided
        self.color = color  # Ball's color
        self.rad = rad  # Ball's radius
        self.is_alive = True  # Flag indicating if the ball is alive

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implements inelastic rebound.

        Parameters:
        - refl_ort (float): Coefficient of restitution for the velocity parallel to the collision surface (default: 0.8).
        - refl_par (float): Coefficient of restitution for the velocity perpendicular to the collision surface (default: 0.9).

        Returns:
        None
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad  # Prevent ball from going out of bounds
                self.vel[i] = -int(self.vel[i] * refl_ort)  # Reflect velocity with a coefficient of restitution
                self.vel[1-i] = int(self.vel[1-i] * refl_par)  # Reduce velocity perpendicular to the collision
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad  # Prevent ball from going out of bounds
                self.vel[i] = -int(self.vel[i] * refl_ort)  # Reflect velocity with a coefficient of restitution
                self.vel[1-i] = int(self.vel[1-i] * refl_par)  # Reduce velocity perpendicular to the collision

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to its velocity and time step.
        Changes the ball's velocity due to gravitational force.

        Parameters:
        - time (float): The time step for the movement (default: 1).
        - grav (float): The gravitational force applied to the ball (default: 0).

        Returns:
        None
        '''
        self.vel[1] += grav  # Apply gravitational force to the ball's vertical velocity
        for i in range(2):
            self.coord[i] += time * self.vel[i]  # Update the ball's position based on velocity and time
        self.check_corners()  # Check for collisions with screen corners
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
            self.is_alive = False  # Ball is considered dead if its velocity is low and it's close to the bottom of the screen

    def draw(self, screen):
        '''
        Draws the ball on the appropriate surface.

        Parameters:
        - screen: The surface object where the ball will be drawn.

        Returns:
        None
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)


class EllipseShell(GameObject):
    '''
    The ball class. Creates a ball, controls its movement, and implements its rendering.
    '''

    def __init__(self, coord, vel, rad=20, color=None, size=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        
        Parameters:
        - coord (list): The coordinates of the ball's center as [x, y].
        - vel (list): The velocity of the ball as [vx, vy].
        - rad (int): The radius of the ball (default: 20).
        - color (str): The color of the ball (default: random color).
        - size (list): The size of the ellipse bounding box as [width, height] (default: [rad*2, rad*4]).

        Returns:
        None
        '''
        self.coord = coord
        self.vel = vel
        if color is None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True
        if size == None:
            size = [rad*2, rad*4]
        self.size = size

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implements inelastic rebound.
        
        Parameters:
        - refl_ort (float): The coefficient of restitution for the velocity component perpendicular to the collision surface (default: 0.8).
        - refl_par (float): The coefficient of restitution for the velocity component parallel to the collision surface (default: 0.9).
        
        Returns:
        None
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1 - i] = int(self.vel[1 - i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1 - i] = int(self.vel[1 - i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to its velocity and time step.
        Changes the ball's velocity due to gravitational force.
        
        Parameters:
        - time (int): The time step for the movement (default: 1).
        - grav (int): The gravitational force affecting the ball's velocity (default: 0).
        
        Returns:
        None
        '''
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 2 ** 2 and self.coord[1] > SCREEN_SIZE[1] - 2 * self.rad:
            self.is_alive = False

    def draw(self, screen):
        '''
        Draws the ball on the appropriate surface.
        
        Parameters:
        - screen: The surface object where the ball will be drawn.

        Returns:
        None
        '''
        rect = pg.Rect(self.coord[0]-self.size[0]/2, self.coord[1] -
                       self.size[1]/2, self.size[0], self.size[1])
        pg.draw.ellipse(screen, self.color, rect)



class Tank(GameObject):
    '''
    Tank class. Manages its rendering, movement, and striking.
    '''

    def __init__(self, coord=[SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 30], angle=0, max_pow=50, min_pow=10, color=RED):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power, and color of the tank.
        
        Parameters:
        - coord (list): The initial coordinates of the tank. Default is [SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 30].
        - angle (float): The initial angle of the tank in radians. Default is 0.
        - max_pow (int): The maximum power value for the tank's charge. Default is 50.
        - min_pow (int): The minimum power value for the tank's charge. Default is 10.
        - color: The color of the tank. Default is RED.

        Returns:
        None
        '''
        self.coord = coord  # Coordinate of the tank on the screen
        self.angle = angle  # Direction angle of the tank's barrel
        self.max_pow = max_pow  # Maximum power for the tank's striking
        self.min_pow = min_pow  # Minimum power for the tank's striking
        self.color = color  # Color of the tank
        self.active = False  # Flag indicating if the tank is active
        self.pow = min_pow  # Current power of the tank's strike

    def activate(self):
        '''
        Activates the tank's charge.

        Parameters:
        None

        Returns:
        None
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases the current power of the tank's charge.
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self):
        '''
        Creates a shell with the tank's direction and current charge power.

        Parameters:
        None
        
        Returns:
        - circle_shell: CircleShell object representing the created shell.
        '''
        vel = self.pow
        angle = self.angle
        circle_shell = CircleShell(list(self.coord), [
            int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        self.pow = self.min_pow
        self.active = False
        return circle_shell

    def set_angle(self, target_pos):
        '''
        Sets the tank's direction to the target position.
        
        Parameters:
        - target_pos: Target position as a tuple (x, y).

        Returns:
        None
        '''
        self.angle = np.arctan2(
            target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])

    def move_left(self, inc):
        '''
        Changes the horizontal position of the tank to the left.

        Parameters:
        - inc: Increment value for the movement.

        Returns:
        None
        '''
        if self.coord[0] > 30:
            self.coord[0] -= inc

    def move_right(self, inc):
        '''
        Changes the horizontal position of the tank to the right.

        Parameters:
        - inc: Increment value for the movement.

        Returns:
        None
        '''
        if self.coord[0] < SCREEN_SIZE[0] - 30:
            self.coord[0] += inc

    def handle_events(self):
        '''
        Handles Pygame events to control the tank's movement.

        Parameters:
        None

        Returns:
        None
        '''
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.move_left(5)
        elif keys[pg.K_RIGHT]:
            self.move_right(5)

    def draw(self, screen):
        '''
        Draws the tank on the screen.

        Parameters:
        - screen: Pygame screen object to draw on.
        
        Returns:
        None
        '''
        tank_shape = []
        tank_width = 40
        tank_height = 20
        wheel_width = 8
        wheel_height = 15
        barrel_len = 25
        tank_pos = np.array(self.coord)
        # draw wheels
        for i in range(4):
            wheel_pos = np.array([tank_pos[0] - tank_width // 2 + (i + 1)
                                 * tank_width // 5, tank_pos[1] + tank_height // 2])
            pg.draw.rect(screen, self.color, [
                         wheel_pos[0] - wheel_width // 2, wheel_pos[1] - wheel_height // 2, wheel_width, wheel_height])
        # draw tank body
        tank_shape.append(
            (tank_pos[0] - tank_width // 2, tank_pos[1] + tank_height // 2))
        tank_shape.append(
            (tank_pos[0] - tank_width // 2, tank_pos[1] - tank_height // 2))
        tank_shape.append(
            (tank_pos[0] + tank_width // 2, tank_pos[1] - tank_height // 2))
        tank_shape.append(
            (tank_pos[0] + tank_width // 2, tank_pos[1] + tank_height // 2))
        pg.draw.polygon(screen, self.color, tank_shape)
        # draw barrel
        barrel_end_pos = (tank_pos + np.array([barrel_len * np.cos(
            self.angle), barrel_len * np.sin(self.angle)])).astype(int)
        pg.draw.line(screen, self.color,
                     tank_pos.astype(int), barrel_end_pos, 5)


class Tank2(GameObject):
    '''
    Tank class. Manages its rendering, movement, and striking.
    '''

    def __init__(self, coord=[SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 30], angle=0, max_pow=50, min_pow=10, color=RED):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the tank.

        Parameters:
        - coord (list): The initial coordinates of the tank. Default is [SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 30].
        - angle (float): The initial angle of the tank in radians. Default is 0.
        - max_pow (int): The maximum power value for the tank's charge. Default is 50.
        - min_pow (int): The minimum power value for the tank's charge. Default is 10.
        - color: The color of the tank. Default is RED.

        Returns:
        None
        '''
        self.coord = coord
        self.angle = angle
        self.max_pow = max_pow
        self.min_pow = min_pow
        self.color = color
        self.active = False
        self.pow = min_pow

    def activate(self):
        '''
        Activates tank's charge.
        '''
        self.active = True

    def gain(self, inc=2):
        '''
        Increases current tank charge power.

        Parameters:
        - inc (int): The increment value for increasing the power. Default is 2.

        Returns:
        None
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self):
        '''
        Creates a shell, according to tank's direction and current charge power.

        Parameters:
        None

        Returns:
        - ellipse_shell (EllipseShell): The shell object created based on the tank's properties.
        '''
        vel = self.pow
        angle = self.angle
        ellipse_shell = EllipseShell(list(self.coord), [
            int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        self.pow = self.min_pow
        self.active = False
        return ellipse_shell

    def set_angle(self, target_pos):
        '''
        Sets tank's direction to target position.

        Parameters:
        - target_pos (list): The target position coordinates.

        Returns:
        None
        '''
        self.angle = np.arctan2(
            target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])

    def move_left(self, inc):
        '''
        Changes horizontal position of the tank to the left.

        Parameters:
        - inc (int): The increment value for moving left.

        Returns:
        None
        '''
        if self.coord[0] > 30:
            self.coord[0] -= inc

    def move_right(self, inc):
        '''
        Changes horizontal position of the tank to the right.

        Parameters:
        - inc (int): The increment value for moving right.

        Returns:
        None
        '''
        if self.coord[0] < SCREEN_SIZE[0] - 30:
            self.coord[0] += inc

    def handle_events(self):
        '''
        Handles Pygame events to control tank's movement.

        Parameters:
        None

        Returns:
        None
        '''
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.move_left(5)
        elif keys[pg.K_RIGHT]:
            self.move_right(5)

    def draw(self, screen):
        '''
        Draws the tank on the screen.

        Parameters:
        - screen: Pygame screen object to draw on.
        
        Returns:
        None
        '''
        tank_shape = []
        tank_width = 40
        tank_height = 20
        wheel_width = 8
        wheel_height = 15
        barrel_len = 25
        tank_pos = np.array(self.coord)
        # draw wheels
        for i in range(4):
            wheel_pos = np.array([tank_pos[0] - tank_width // 2 + (i + 1)
                                 * tank_width // 5, tank_pos[1] + tank_height // 2])
            pg.draw.rect(screen, self.color, [
                         wheel_pos[0] - wheel_width // 2, wheel_pos[1] - wheel_height // 2, wheel_width, wheel_height])
        # draw tank body
        tank_shape.append(
            (tank_pos[0] - tank_width // 2, tank_pos[1] + tank_height // 2))
        tank_shape.append(
            (tank_pos[0] - tank_width // 2, tank_pos[1] - tank_height // 2))
        tank_shape.append(
            (tank_pos[0] + tank_width // 2, tank_pos[1] - tank_height // 2))
        tank_shape.append(
            (tank_pos[0] + tank_width // 2, tank_pos[1] + tank_height // 2))
        pg.draw.polygon(screen, self.color, tank_shape)
        # draw barrel
        barrel_end_pos = (tank_pos + np.array([barrel_len * np.cos(
            self.angle), barrel_len * np.sin(self.angle)])).astype(int)
        pg.draw.line(screen, self.color,
                     tank_pos.astype(int), barrel_end_pos, 5)


class CircleTarget(GameObject):
    '''
    Target class. Creates target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets the coordinate, color, and radius of the target.

        Parameters:
        - coord (list): The coordinate of the target. If None, it will be randomly generated within the screen boundaries.
        - color (tuple): The color of the target. If None, a random color will be assigned.
        - rad (int): The radius of the target.

        Returns:
        None
        '''
        if coord is None:
            coord = [random.randint(rad, SCREEN_SIZE[0] - rad),
                     random.randint(rad, SCREEN_SIZE[1] - rad)]
        self.coord = coord
        self.rad = rad

        if color is None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into the target.

        Parameters:
        - ball (Ball): The ball object to check for collision.

        Returns:
        bool: True if the ball collides with the target, False otherwise.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.rad + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen.

        Parameters:
        - screen (Surface): The screen surface to draw on.

        Returns:
        None
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self):
        '''
        This type of target can't move at all.

        Returns:
        None
        '''
        pass


class MovingCircleTarget(CircleTarget):
    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets the coordinate, color, and radius of the moving circle target.

        Parameters:
        - coord (list): The coordinate of the target. If None, it will be randomly generated within the screen boundaries.
        - color (tuple): The color of the target. If None, a random color will be assigned.
        - rad (int): The radius of the target.

        Returns:
        None
        '''
        super().__init__(coord, color, rad)
        self.vx = random.randint(-2, +2)
        self.vy = random.randint(-2, +2)

    def move(self):
        '''
        Moves the moving circle target by updating its coordinates based on the velocity.

        Returns:
        None
        '''
        self.coord[0] += self.vx
        self.coord[1] += self.vy


class EllipseTarget(GameObject):
    '''
    Target class. Creates target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, rad=30, size=None):
        '''
        Constructor method. Initializes the target with specified parameters.
        
        Parameters:
        - coord (list): The coordinate of the target. If not provided, random coordinates within screen boundaries are generated.
        - color (tuple): The color of the target. If not provided, a random color is chosen.
        - rad (int): The radius of the target. Default is 30.
        - size (list): The size of the target as [width, height]. If not provided, it is calculated based on the radius.
        '''
        if coord == None:
            coord = [random.randint(rad, SCREEN_SIZE[0] - rad),
                     random.randint(rad, SCREEN_SIZE[1] - rad)]
        self.coord = coord
        self.rad = rad

        if size == None:
            size = [rad*2, rad*4]
        self.size = size

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball collides with the target.

        Parameters:
        - ball (Ball): The ball object to check collision with.

        Returns:
        - bool: True if the ball collides with the target, False otherwise.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = max(self.size)/2 + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen.

        Parameters:
        - screen: The screen to draw the target on.

        Returns:
        - None
        '''
        rect = pg.Rect(self.coord[0]-self.size[0]/2, self.coord[1] -
                       self.size[1]/2, self.size[0], self.size[1])
        pg.draw.ellipse(screen, self.color, rect)

    def move(self):
        """
        This type of target cannot move.

        Returns:
        - None
        """
        pass


class MovingEllipseTarget(EllipseTarget):
    '''
    Moving target class. Creates a moving target that oscillates vertically and horizontally.
    '''

    def __init__(self, coord=None, color=None, rad=30, size=None, speed=5):
        """
        Initializes a MovingEllipseTarget object.

        Parameters:
        - coord (list or None): The coordinates of the target's center. If None, defaults to the origin.
        - color (str or None): The color of the target. If None, defaults to the parent class's default color.
        - rad (int): The radius of the target's ellipse. Defaults to 30.
        - size (tuple or None): The size of the target's bounding box. If None, defaults to the parent class's default size.
        - speed (int): The speed at which the target moves. Defaults to 5.
        """
        super().__init__(coord, color, rad, size)
        self.speed = speed
        self.start_coord = self.coord.copy()
        self.direction = 1

    def move(self):
        '''
        Moves the target back and forth horizontally and vertically.
        '''
        if self.direction == 1:
            # Move target horizontally to the right
            self.coord[0] += self.speed
            if self.coord[0] >= self.start_coord[0] + self.rad:
                # Reverse direction if reached maximum horizontal position
                self.direction = 2
        elif self.direction == 2:
            # Move target vertically downward
            self.coord[1] += self.speed
            if self.coord[1] >= self.start_coord[1] + self.size[1] / 2:
                # Reverse direction if reached maximum vertical position
                self.direction = 3
        elif self.direction == 3:
            # Move target horizontally to the left
            self.coord[0] -= self.speed
            if self.coord[0] <= self.start_coord[0] - self.rad:
                # Reverse direction if reached minimum horizontal position
                self.direction = 4
        elif self.direction == 4:
            # Move target vertically upward
            self.coord[1] -= self.speed
            if self.coord[1] <= self.start_coord[1] - self.size[1] / 2:
                # Reverse direction if reached minimum vertical position
                self.direction = 1


class RectangleTarget(GameObject):
    '''
    RectangleTarget class. Creates rectangle target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, width=60, height=30):
        '''
        Constructor method. Sets coordinate, color, and dimensions of the target.

        '''
        if coord == None:
            coord = [random.randint(width, SCREEN_SIZE[0] - width),
                     random.randint(height, SCREEN_SIZE[1] - height)]
        self.coord = coord
        self.width = width
        self.height = height

        if color == None:
            color = rand_color()  # Assuming there's a function rand_color() that generates a random color.
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into the target.

        '''
        dx = abs(ball.coord[0] - self.coord[0])
        dy = abs(ball.coord[1] - self.coord[1])

        if dx > (self.width/2 + ball.rad):
            return False
        if dy > (self.height/2 + ball.rad):
            return False

        if dx <= (self.width/2):
            return True
        if dy <= (self.height/2):
            return True

        corner_dist_sq = (dx - self.width/2)**2 + (dy - self.height/2)**2

        return (corner_dist_sq <= ball.rad**2)

    def draw(self, screen):
        '''
        Draws the target on the screen.

        '''
        rect = pg.Rect(self.coord[0] - self.width/2,
                       self.coord[1] - self.height/2, self.width, self.height)
        pg.draw.rect(screen, self.color, rect)

    def move(self):
        """
        This type of target can't move at all.

        """
        pass


class MovingRectangleTarget(RectangleTarget):
    '''
    MovingRectangleTarget class. Creates moving rectangle target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, speed=2, **kwargs):
        '''
        Constructor method. Sets the speed and calls the parent constructor.

        '''
        super().__init__(**kwargs)
        self.speed = speed
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def move(self):
        '''
        Moves the target in a random direction.

        '''
        if self.direction == 'left':
            self.coord[0] -= self.speed
            if self.coord[0] < self.width/2:
                self.coord[0] = self.width/2
                self.direction = 'right'
        elif self.direction == 'right':
            self.coord[0] += self.speed
            if self.coord[0] > SCREEN_SIZE[0] - self.width/2:
                self.coord[0] = SCREEN_SIZE[0] - self.width/2
                self.direction = 'left'
        elif self.direction == 'up':
            self.coord[1] -= self.speed
            if self.coord[1] < self.height/2:
                self.coord[1] = self.height/2
                self.direction = 'down'
        elif self.direction == 'down':
            self.coord[1] += self.speed
            if self.coord[1] > SCREEN_SIZE[1] - self.height/2:
                self.coord[1] = SCREEN_SIZE[1] - self.height/2
                self.direction = 'up'


class PolygonTarget(GameObject):
    '''
    PolygonTarget class. Creates polygon target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, sides=5, size=30):
        '''
        Constructor method. Sets coordinate, color, and dimensions of the target.

        '''
        if coord == None:
            coord = [random.randint(size, SCREEN_SIZE[0] - size),
                     random.randint(size, SCREEN_SIZE[1] - size)]
        self.coord = coord
        self.sides = sides
        self.size = size

        if color == None:
            color = rand_color()  # Assuming there's a function rand_color() that generates a random color.
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into the target.

        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.size + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen.

        '''
        points = []
        for i in range(self.sides):
            angle = math.pi * 2 * i / self.sides
            x = self.coord[0] + self.size * math.cos(angle)
            y = self.coord[1] + self.size * math.sin(angle)
            points.append((x, y))

        pg.draw.polygon(screen, self.color, points)

    def move(self):
        '''
        This type of target can't move at all.

        '''
        pass


class MovingPolygonTarget(PolygonTarget):
    '''
    MovingPolygonTarget class. Creates a polygon target that moves, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, sides=5, size=30, vel=1):
        '''
        Constructor method. Sets coordinate, color, dimensions, and velocity of the target.

        '''
        super().__init__(coord=coord, color=color, sides=sides, size=size)
        self.vel = vel  # velocity in pixels per frame
        self.direction = random.uniform(0, 2 * math.pi)  # initial movement direction

    def move(self):
        '''
        Moves the target in its current direction with its set velocity.

        '''
        dx = self.vel * math.cos(self.direction)
        dy = self.vel * math.sin(self.direction)
        self.coord[0] += dx
        self.coord[1] += dy

        # Check if target hits screen edges, reverse direction if necessary
        if self.coord[0] < self.size or self.coord[0] > SCREEN_SIZE[0] - self.size:
            self.direction = math.pi - self.direction
        elif self.coord[1] < self.size or self.coord[1] > SCREEN_SIZE[1] - self.size:
            self.direction = -self.direction


class ScoreTable:
    '''
    Score table class.
    '''

    def __init__(self, t_destr=0, b_used=0):
        '''
        Constructor method. Initializes the score table with the total destroyed and balls used.

        '''
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pg.font.SysFont("dejavusansmono", 25)

    def score(self):
        '''
        Score calculation method. Calculates the score as the difference between the total destroyed and balls used.

        '''
        return self.t_destr - self.b_used

    def draw(self, screen):
        '''
        Draws the score table on the screen.

        '''
        score_surf = []
        score_surf.append(self.font.render("Destroyed: {}".format(self.t_destr), True, WHITE))
        score_surf.append(self.font.render("Balls used: {}".format(self.b_used), True, WHITE))
        score_surf.append(self.font.render("Total: {}".format(self.score()), True, RED))
        for i in range(3):
            screen.blit(score_surf[i], [10, 10 + 30*i])


class Manager:
    '''
    Class that manages events' handling, ball's motion and collision, target creation, etc.

    '''
    def __init__(self, n_targets=1):
        self.balls = []
        self.gun = [Tank(coord=[SCREEN_SIZE[0] - 100, SCREEN_SIZE[1] - 30], color=RED),
                    Tank2(coord=[100, SCREEN_SIZE[1] - 30], color=BLUE)]
        self.targets = []
        self.score_t = ScoreTable()
        self.n_targets = n_targets
        self.new_mission()

    def new_mission(self):
        '''
        Adds new targets.
        '''
        for i in range(self.n_targets):
            self.targets.append(MovingCircleTarget(rad=random.randint(max(1, 30 - 2*max(0, self.score_t.score())),
                                                                      30 - max(0, self.score_t.score())))),
            self.targets.append(MovingEllipseTarget(rad=random.randint(max(1, 30 - 2*max(0, self.score_t.score())),
                                                                       30 - max(0, self.score_t.score())))),
            self.targets.append(CircleTarget(rad=random.randint(max(1, 30 - 2*max(0, self.score_t.score())),
                                                                30 - max(0, self.score_t.score())))),
            self.targets.append(EllipseTarget(rad=random.randint(max(1, 30 - 2*max(0, self.score_t.score())),
                                                                 30 - max(0, self.score_t.score())))),
            self.targets.append(RectangleTarget(coord=[random.randint(200, SCREEN_SIZE[0] - 200), random.randint(200, SCREEN_SIZE[1] - 200)],
                                                color=rand_color(),
                                                width=random.randint(max(1, 30 - 2 * max(0, self.score_t.score())),
                                                                     30 - max(0, self.score_t.score())),
                                                height=random.randint(max(1, 30 - 2 * max(0, self.score_t.score())),
                                                                      30 - max(0, self.score_t.score()))))
            self.targets.append(MovingRectangleTarget(coord=[random.randint(200, SCREEN_SIZE[0] - 200), random.randint(200, SCREEN_SIZE[1] - 200)],
                                                      color=rand_color(),
                                                      width=random.randint(max(1, 30 - 2 * max(0, self.score_t.score())),
                                                                           30 - max(0, self.score_t.score())),
                                                      height=random.randint(max(1, 30 - 2 * max(0, self.score_t.score())),
                                                                            30 - max(0, self.score_t.score())))),
            self.targets.append(PolygonTarget(coord=[random.randint(100, SCREEN_SIZE[0] - 100), random.randint(100, SCREEN_SIZE[1] - 100)],
                                              color=rand_color(),
                                              sides=5,
                                              size=25)),
            self.targets.append(MovingPolygonTarget(coord=[random.randint(100, SCREEN_SIZE[0] - 100), random.randint(100, SCREEN_SIZE[1] - 100)],
                                                    color=rand_color(),
                                                    sides=5,
                                                    size=25))

    def process(self, events, screen):
        '''
        Runs all necessary methods for each iteration. Adds new targets if previous ones are destroyed.

        '''
        done = self.handle_events(events)

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun[0].set_angle(mouse_pos)
            self.gun[1].set_angle(mouse_pos)

        self.move()
        self.collide()
        self.draw(screen)

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from the keyboard, mouse, etc.

        '''
        done = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.gun[0].move_left(1)
            # self.gun[1].move_left(1)
        elif keys[pg.K_RIGHT]:
            self.gun[0].move_right(1)
            # self.gun[1].move_right(1)
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.gun[0].move_left(1)
                    # self.gun[1].move_left(1)
                elif event.key == pg.K_RIGHT:
                    self.gun[0].move_right(1)
                    # self.gun[1].move_right(1)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun[0].activate()
                    # self.gun[1].activate()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun[0].strike())
                    # self.balls.append(self.gun[1].strike())
                    self.score_t.b_used += 1

        if keys[pg.K_a]:
            # self.gun[0].move_left(1)
            self.gun[1].move_left(1)
        elif keys[pg.K_d]:
            # self.gun[0].move_right(1)
            self.gun[1].move_right(1)
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    # self.gun[0].move_left(1)
                    self.gun[1].move_left(1)
                elif event.key == pg.K_d:
                    # self.gun[0].move_right(1)
                    self.gun[1].move_right(1)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # self.gun[0].activate()
                    self.gun[1].activate()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    # self.balls.append(self.gun[0].strike())
                    self.balls.append(self.gun[1].strike())
                    self.score_t.b_used += 1
        return done


    def draw(self, screen):
        '''
        Runs the drawing method for balls, guns, targets, and the score table.

        '''
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.gun[0].draw(screen)
        self.gun[1].draw(screen)
        self.score_t.draw(screen)

    def move(self):
        '''
        Runs the movement method for balls and guns, and removes dead balls.

        '''
        dead_balls = []
        for i, ball in enumerate(self.balls):
            ball.move(grav=2)
            if not ball.is_alive:
                dead_balls.append(i)
        for i in reversed(dead_balls):
            self.balls.pop(i)
        for i, target in enumerate(self.targets):
            target.move()
        self.gun[0].gain()
        self.gun[1].gain()

    def collide(self):
        '''
        Checks whether balls bump into targets and sets balls' alive trigger.

        '''
        collisions = []
        targets_c = []
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check_collision(ball):
                    collisions.append([i, j])
                    targets_c.append(j)
        targets_c.sort()
        for j in reversed(targets_c):
            self.score_t.t_destr += 1
            self.targets.pop(j)


screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("The gun of Khiryanov")

done = False
clock = pg.time.Clock()

mgr = Manager(n_targets=1)

while not done:
    clock.tick(15)
    screen.fill(BLACK)

    done = mgr.process(pg.event.get(), screen)

    pg.display.flip()


pg.quit()