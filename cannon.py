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

SCREEN_SIZE = (800, 600)


def rand_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class GameObject:
    def move(self):
        pass

    def draw(self, screen):
        pass


class Shell(GameObject):
    '''
    The ball class. Creates a ball, controls it's movement and implement it's rendering.
    '''

    def __init__(self, coord, vel, rad=20, color=None):
        '''
        Constructor method. Initializes ball's parameters and initial values.
        '''
        self.coord = coord
        self.vel = vel
        if color == None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        '''
        Reflects ball's velocity when ball bumps into the screen corners. Implemetns inelastic rebounce.
        '''
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1-i] = int(self.vel[1-i] * refl_par)

    def move(self, time=1, grav=0):
        '''
        Moves the ball according to it's velocity and time step.
        Changes the ball's velocity due to gravitational force.
        '''
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0]**2 + self.vel[1]**2 < 2**2 and self.coord[1] > SCREEN_SIZE[1] - 2*self.rad:
            self.is_alive = False

    def draw(self, screen):
        '''
        Draws the ball on appropriate surface.
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

class Tank(GameObject):
    '''
    Tank class. Manages its rendering, movement, and striking.
    '''

    def __init__(self, coord=[SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 30], angle=0, max_pow=50, min_pow=10, color=RED):
        '''
        Constructor method. Sets coordinate, direction, minimum and maximum power and color of the tank.
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
        '''
        if self.active and self.pow < self.max_pow:
            self.pow += inc

    def strike(self):
        '''
        Creates a shell, according to tank's direction and current charge power.
        '''
        vel = self.pow
        angle = self.angle
        shell = Shell(list(self.coord), [
            int(vel * np.cos(angle)), int(vel * np.sin(angle))])
        self.pow = self.min_pow
        self.active = False
        return shell

    def set_angle(self, target_pos):
        '''
        Sets tank's direction to target position.
        '''
        self.angle = np.arctan2(
            target_pos[1] - self.coord[1], target_pos[0] - self.coord[0])

    def move(self, inc):
        '''
        Changes horizontal position of the tank.
        '''
        if (self.coord[0] > 30 or inc > 0) and (self.coord[0] < SCREEN_SIZE[0] - 30 or inc < 0):
            self.coord[0] += inc

    def draw(self, screen):
        '''
        Draws the tank on the screen.
        '''
        tank_shape = []
        tank_width = 40
        tank_height = 20
        barrel_len = 25
        tank_pos = np.array(self.coord)
        # draw tank body
        tank_shape.append((tank_pos[0] - tank_width // 2, tank_pos[1] + tank_height // 2))
        tank_shape.append((tank_pos[0] - tank_width // 2, tank_pos[1] - tank_height // 2))
        tank_shape.append((tank_pos[0] + tank_width // 2, tank_pos[1] - tank_height // 2))
        tank_shape.append((tank_pos[0] + tank_width // 2, tank_pos[1] + tank_height // 2))
        pg.draw.polygon(screen, self.color, tank_shape)
        # draw barrel
        barrel_end_pos = (tank_pos + np.array([barrel_len * np.cos(self.angle), barrel_len * np.sin(self.angle)])).astype(int)
        pg.draw.line(screen, self.color, tank_pos.astype(int), barrel_end_pos, 5)

class CircleTarget(GameObject):
    '''
    Target class. Creates target, manages it's rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, rad=30):
        '''
        Constructor method. Sets coordinate, color and radius of the target.
        '''
        if coord == None:
            coord = [random.randint(rad, SCREEN_SIZE[0] - rad),
                     random.randint(rad, SCREEN_SIZE[1] - rad)]
        self.coord = coord
        self.rad = rad

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into target.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.rad + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen
        '''
        pg.draw.circle(screen, self.color, self.coord, self.rad)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass


class MovingCircleTarget(CircleTarget):
    def __init__(self, coord=None, color=None, rad=30):
        super().__init__(coord, color, rad)
        self.vx = random.randint(-2, +2)
        self.vy = random.randint(-2, +2)

    def move(self):
        self.coord[0] += self.vx
        self.coord[1] += self.vy


class EllipseTarget(GameObject):
    '''
    Target class. Creates target, manages it's rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, rad=30, size=None):
        '''
        Constructor method. Sets coordinate, color, radius and size of the target.
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
        Checks whether the ball bumps into target.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = max(self.size)/2 + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen
        '''
        rect = pg.Rect(self.coord[0]-self.size[0]/2, self.coord[1] -
                       self.size[1]/2, self.size[0], self.size[1])
        pg.draw.ellipse(screen, self.color, rect)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass


class MovingEllipseTarget(EllipseTarget):
    '''
    Moving target class. Creates a moving target that oscillates vertically and horizontally.
    '''

    def __init__(self, coord=None, color=None, rad=30, size=None, speed=5):
        super().__init__(coord, color, rad, size)
        self.speed = speed
        self.start_coord = self.coord.copy()
        self.direction = 1

    def move(self):
        '''
        Moves the target back and forth horizontally and vertically.
        '''
        if self.direction == 1:
            self.coord[0] += self.speed
            if self.coord[0] >= self.start_coord[0] + self.rad:
                self.direction = 2
        elif self.direction == 2:
            self.coord[1] += self.speed
            if self.coord[1] >= self.start_coord[1] + self.size[1] / 2:
                self.direction = 3
        elif self.direction == 3:
            self.coord[0] -= self.speed
            if self.coord[0] <= self.start_coord[0] - self.rad:
                self.direction = 4
        elif self.direction == 4:
            self.coord[1] -= self.speed
            if self.coord[1] <= self.start_coord[1] - self.size[1] / 2:
                self.direction = 1


class RectangleTarget(GameObject):
    '''
    RectangleTarget class. Creates rectangle target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, width=60, height=30):
        '''
        Constructor method. Sets coordinate, color and dimensions of the target.
        '''
        if coord == None:
            coord = [random.randint(width, SCREEN_SIZE[0] - width),
                     random.randint(height, SCREEN_SIZE[1] - height)]
        self.coord = coord
        self.width = width
        self.height = height

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into target.
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
        Draws the target on the screen
        '''
        rect = pg.Rect(self.coord[0] - self.width/2,
                       self.coord[1] - self.height/2, self.width, self.height)
        pg.draw.rect(screen, self.color, rect)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass


class MovingRectangleTarget(RectangleTarget):
    '''
    MovingRectangleTarget class. Creates moving rectangle target, manages its rendering and collision with a ball event.
    '''

    def __init__(self, speed=2, **kwargs):
        '''
        Constructor method. Sets speed and calls parent constructor.
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
        Constructor method. Sets coordinate, color and dimensions of the target.
        '''
        if coord == None:
            coord = [random.randint(size, SCREEN_SIZE[0] - size),
                     random.randint(size, SCREEN_SIZE[1] - size)]
        self.coord = coord
        self.sides = sides
        self.size = size

        if color == None:
            color = rand_color()
        self.color = color

    def check_collision(self, ball):
        '''
        Checks whether the ball bumps into target.
        '''
        dist = sum([(self.coord[i] - ball.coord[i])**2 for i in range(2)])**0.5
        min_dist = self.size + ball.rad
        return dist <= min_dist

    def draw(self, screen):
        '''
        Draws the target on the screen
        '''
        points = []
        for i in range(self.sides):
            angle = math.pi * 2 * i / self.sides
            x = self.coord[0] + self.size * math.cos(angle)
            y = self.coord[1] + self.size * math.sin(angle)
            points.append((x, y))

        pg.draw.polygon(screen, self.color, points)

    def move(self):
        """
        This type of target can't move at all.
        :return: None
        """
        pass

class MovingPolygonTarget(PolygonTarget):
    '''
    MovingPolygonTarget class. Creates a polygon target that moves, manages its rendering and collision with a ball event.
    '''

    def __init__(self, coord=None, color=None, sides=5, size=30, vel=1):
        '''
        Constructor method. Sets coordinate, color, dimensions and velocity of the target.
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
        self.t_destr = t_destr
        self.b_used = b_used
        self.font = pg.font.SysFont("dejavusansmono", 25)

    def score(self):
        '''
        Score calculation method.
        '''
        return self.t_destr - self.b_used

    def draw(self, screen):
        score_surf = []
        score_surf.append(self.font.render(
            "Destroyed: {}".format(self.t_destr), True, WHITE))
        score_surf.append(self.font.render(
            "Balls used: {}".format(self.b_used), True, WHITE))
        score_surf.append(self.font.render(
            "Total: {}".format(self.score()), True, RED))
        for i in range(3):
            screen.blit(score_surf[i], [10, 10 + 30*i])


class Manager:
    '''
    Class that manages events' handling, ball's motion and collision, target creation, etc.
    '''

    def __init__(self, n_targets=1):
        self.balls = []
        self.gun = Tank()
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
        Runs all necessary method for each iteration. Adds new targets, if previous are destroyed.
        '''
        done = self.handle_events(events)

        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)

        self.move()
        self.collide()
        self.draw(screen)

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return done

    def handle_events(self, events):
        '''
        Handles events from keyboard, mouse, etc.
        '''
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.move(-5)
                elif event.key == pg.K_DOWN:
                    self.gun.move(5)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.activate()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.score_t.b_used += 1
        return done

    def draw(self, screen):
        '''
        Runs balls', gun's, targets' and score table's drawing method.
        '''
        for ball in self.balls:
            ball.draw(screen)
        for target in self.targets:
            target.draw(screen)
        self.gun.draw(screen)
        self.score_t.draw(screen)

    def move(self):
        '''
        Runs balls' and gun's movement method, removes dead balls.
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
        self.gun.gain()

    def collide(self):
        '''
        Checks whether balls bump into targets, sets balls' alive trigger.
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
