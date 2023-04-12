import pygame
# import os
# import time
import random

pygame.font.init()


# making the display window
WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HIDDEN)

pygame.display.set_caption("Space Invaders")

# load images
RED_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_blue_small.png")
# player ship
YELLOW_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_yellow.png")
# here we are using the image.load() method of pygame module
# os.path.join is where the image is located, and we are mentioning the name of folder as well as the image file
# If we want to add folder name to a file name we use os.path.join

# Lasers
RED_LASER = pygame.image.load("./assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("./assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("./assets/pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("./assets/pixel_laser_yellow.png")

# Background, which we scale to fit the entire window
BG = pygame.transform.scale(pygame.image.load("./assets/background-black.png"), (WIDTH, HEIGHT))


# making the laser class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # drawing the laser on the window
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # moving the laser
    def move(self, vel):
        self.y += vel

    # tells whether the laser is off the screen
    def off_screen(self, height):
        return not self.y <= height and self.y >= 0

    # tells whether collision has occurred
    def collision(self, obj):
        return collide(self, obj)


# we are making an abstract class ship so that both player and enemy ships can be inherited from it
class Ship:
    COOLDOWN = 30

    # defining init method which is used to initialize objects and creating attributes of a ship
    def __init__(self, x, y, health=100):
        self.x = x  # setting up attributes for the class
        self.y = y
        self.health = health
        self.ship_img = None  # used to draw images of ship and lasers
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0  # creates delay between shooting consecutive lasers

    def draw(self, window):
        # to draw a proper ship
        window.blit(self.ship_img, (self.x, self.y))  # referencing attributes to the ship being currently drawn
        # pygame.draw.rect(window, (255, 0, 0,), (self.x, self.y, 50, 50))
        # using draw module of pygame to draw a rectangle on the window , we define the color and dimensions
        for laser in self.lasers:  # drawing the lasers
            laser.draw(window)

    # defining a function to move the lasers of player whilst also checking for collision of enemy laser with player
    def move_lasers(self, vel, obj):
        self.cooldown()  # increment the cooldown counter when we shoot the lasers
        for laser in self.lasers:
            laser.move(vel)  # defining the velocity of the laser
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)  # removing the laser if it is off the screen
            elif laser.collision(obj):  # if enemy laser collides with player ship decrement the health and delete laser
                obj.health -= 10
                self.lasers.remove(laser)

    # to handle the cool down that is time between shooting two lasers
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

# we are making the shoot method which creates new lasers as soon as the counter hits zero adding it to the lasers list
    # And then restarting the counter
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# class player inherited from class ship
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        # super is the parent class ship, whose initialization method is used inside the child class player
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        # using masking on ship_img surface to do pixel perfect collision
        # masks tells us where pixel are located
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health  # defining that the health 100 is max

    def move_lasers(self, vel, objs):
        self.cooldown()  # increment the cooldown counter when we shoot the lasers
        for laser in self.lasers:
            laser.move(vel)  # defining the velocity of the laser
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)  # removing the laser if it is off the screen
            else:
                # for each object in the object list, if the laser has collided with the object remove it and the laser
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

# drawing the healthbar
    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    # creating the health bar
    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width() * (self.health/self.max_health), 10))


# class enemy inherited from class ship
class Enemy(Ship):
    # creating a dictionary that maps colours to particular spaceships and lasers
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        # we are passing a color which will then return the images
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health  # defining that the health 100 is max

    # defining the move method for the ship which will only allow the ship to move downwards
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# The way this methods works is it determines if the masks of two objects are overlapping and then concludes that
# they are colliding. Masks indicate where the pixels of the object are located. Since surfaces are rectangular
# while objects are not , masks tell us where within the rectangle, the pixels of the objects are
# We are then determining if these masks overlap and if so collision has occurred
# the offset given the distance between the objects which is useful to calculate their point of intersection
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# main loops handles all events of the games like moving, exiting, collisions etc.
def main():
    run = True
    FPS = 60  # decides how fast or slow the game will run, higher the fps faster the game
    # shows 60 frames per second
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)  # creating the font object and defining the font to be used
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []  # stores where enemies are
    wave_length = 5
    enemy_vel = 1

    player_vel = 5  # defines how fast the player can move in pixels
    laser_vel = 6
    player = Player(300, 630)  # creating an instance of the ship class

    clock = pygame.time.Clock()  # checks events 60 times a second using clock

    lost = False
    lost_count = 0

    # in pygame we have surfaces which can be drawn on, which we will refresh 60 tps and thus all contents on it will
    # be redrawn
    def redraw_window():
        global WIN
        WIN.blit(BG, (0, 0))  # drawing a background image on the surface at the location mentioned (0,0) which
        # corresponds to top left, which we can draw other things on draw text by making a label, to put anything on
        # the screen it is by default a surface
        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))

        WIN.blit(lives_label, (20, 20))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 20, 20))

        # drawing enemies
        for e in enemies:
            e.draw(WIN)

        player.draw(WIN)  # calling the ship object, and draw method

        if lost:
            lost_label = lost_font.render("YOU LOST!!!", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()  # refresh display

    while run:
        clock.tick(FPS)  # we are ticking/timing clock according to the FPS which allows the game to be consistent
        # across all devices by setting a fixed clock speed Everytime we run while loop, we are looping through all
        # the events pygame knows, and we are going to check if an event has occurred and performing necessary action
        redraw_window()

        # if all our lives or player health is over
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1  # increment the timer of lost count

        # we are setting a 3 second timer and after that we quit the game
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # if there are no more enemies on the screen then increment the level and number of enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # after adding new enemies we have to start moving the entire new batch downwards
            # the entire batch will move at the same velocity but to make it seem as it they are moving at
            # different times we give them different inital positions above the screen and randomly choose their colours
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)  # adding ships to enemy list

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitting pygame by exiting loop
                run = False
                WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HIDDEN)
                pygame.display.flip()

        # defining keys function
        keys = pygame.key.get_pressed()  # checks if keys are pressed
        # moving the keys whilst also restricting them to the screen
        if keys[pygame.K_LEFT] and player.x + player_vel > 0:  # to move left
            player.x -= player_vel  # Subtracting from the x value of ship to move left
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:  # to move right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y + player_vel > 0:  # to move up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # to move down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            # if the enemies hit the bottom of the screen then we lose a life and we remove the object from screen

            # to make enemy shoot bullets every 2 seconds
            if random.randrange(0, 5 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # will check if laser has collided with any of the enemies
        player.move_lasers(-laser_vel, enemies)


# creating the main menu
def main_menu():
    global WIN
    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SHOWN)
    pygame.display.update()
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("PRESS THE MOUSE TO BEGIN....", True, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HIDDEN)
                pygame.display.flip()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                return
    pygame.quit()


main_menu()