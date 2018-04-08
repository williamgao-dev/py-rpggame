import pygame as pg
from tilemap import collide_hit_rect
from settings import *
# Loading pygame vector class
vec = pg.math.Vector2

# Player sprite class
class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Initalize an instance of Player in group all_sprites
        self.groups = game.all_sprites

        pg.sprite.Sprite.__init__(self,self.groups)

        # Sets attributes of class Player, sets a reference to the game class
        self.game = game

        # Sets the image that will be used for the player sprite to
        # the player image loaded in game.load_data
        self.image = game.player_img
        self.rect = self.image.get_rect()

        # Different rectangle for collision detection
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        # VECTORS
        # Velocity vector
        self.vel = vec(0,0)

        # Position vector
        self.pos = vec(x,y) * TILESIZE

        self.rot = 0

    # Function to get key presses, and move character in direction in event of keypress
    def get_keys(self):

        self.rot_speed = 0

        # Set vx and vy to 0 unless a key is pressed.

        self.vel = vec(0,0)

        # Event handling of keyboard input

        keys = pg.key.get_pressed()

        # If left or right, make the character rotate at player_rot_speed
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED

        # If up or down, move up or down
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED,0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2,0).rotate(-self.rot)


    # Function that WILL executes at every frame of the game.
    def update(self):
        self.get_keys()

        # Transform the image of the player so it rotates
        # Rotates image around the centre to ensure consistent movement
        self.image = pg.transform.rotate(self.game.player_img, self.rot)

        self.pos += self.vel * self.game.dt
        self.rect = self.image.get_rect()

        # Updating rotation (mod 360 means that we will always go back to 0 at 360 degrees)
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360

        # Note that I use hit_rect instead of the normal rectangle to ensure consistent collision
        # as the normal rect changes in proportion of the image in the middle, but this new one
        # is a constant rectangle thus the hitbox of the rectangle remains constant as well.

        # Updates x value
        self.hit_rect.centerx = self.pos.x

        # Calls collide_with_walls('x') every frame, checking if theres a collision
        self.collide_with_walls('x')

        # Update y value
        self.hit_rect.centery = self.pos.y

        # Calls collide_with_walls('y') every frame
        self.collide_with_walls('y')


        self.rect.center = self.hit_rect.center

    def collide_with_walls(self,dir):
        '''
            My nifty little collision checker.
            Having TWO checks ensures that in event of one x or y value collision,
            Movement the other way still works, thus we can slide down walls.
            If direction is x, detect collisions.

            rect HIT_RECT is used for collisions instead of the normal rectangle
            as it provides more consistent collisions as it is a static rectangle
            unlike the rectangle surrounding the player sprite that's used to track
            movement
        '''

        # If direction is x, perform collision checking for x axis
        if dir == 'x':
            # Detects collision between player and walls.
            hits = pg.sprite.spritecollide(self,self.game.walls,False, collide_hit_rect)
            # If hits == True.
            if hits:
                # If velocity is right,
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2.0
                # If velocity is left
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2.0
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x

        # If direction is y, perform collision checking for y axis
        if dir == 'y':
            # Detects collision between player and walls.
            hits = pg.sprite.spritecollide(self,self.game.walls,False, collide_hit_rect)
            # If hits == True
            if hits:
                # If velocity is down
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2.0
                # If velocity is up
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2.0
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

# Wall sprite class
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):


        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.walls

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Attributes of the wall
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # Makes the wall the size of a tile
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Mob sprite class
class Mob(pg.sprite.Sprite):
    def __init__(self,game,x,y):

        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.mobs
        self.game = game

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos



