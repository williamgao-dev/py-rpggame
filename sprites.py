import pygame as pg
from settings import *
# Loading pygame vector class
vec = pg.math.Vector2

# Player sprite class
class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Initalize an instance of Player in group all_sprites
        self.groups = game.all_sprites

        pg.sprite.Sprite.__init__(self,self.groups)

        # Sets an image in the dimensions of tilesize*tilesize for the player
        # sprite
        self.image = pg.Surface((TILESIZE,TILESIZE))

        # Sets attributes of class Player, sets a reference to the game class
        self.game = game

        # Sets the image that will be used for the player sprite to
        # the player image loaded in game.load_data
        self.image = game.player_img
        self.rect = self.image.get_rect()

        # Velocity vector
        self.vel = vec(0,0)
        # Position vector
        self.pos = vec(x,y) * TILESIZE

    # Function to get key presses, and move character in direction in event of keypress
    def get_keys(self):

        # If statements allow diagonal movement. Elif disables.
        # Set vx and vy to 0 unless a key is pressed.

        self.vel = vec(0,0)

        # Event handling of keyboard input
        # I used if statements instead of elif in order to allow diagonal
        # movement.

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED

        # Regulation of diagonal movement speed through pythag theorem

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071 # 1 / sqrt2


    # Function that WILL executes at every frame of the game.
    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt

        # Updates x value
        self.rect.x = self.pos.x

        # Calls collide_with_walls('x') every frame, checking if theres a collision
        self.collide_with_walls('x')

        # Update y value
        self.rect.y = self.pos.y

        # Calls collide_with_walls('y') every frame
        self.collide_with_walls('y')

    def collide_with_walls(self,dir):
        '''
            My nifty little collision checker.
            Having TWO checks ensures that in event of one x or y value collision,
            Movement the other way still works, thus we can slide down walls.
            If direction is x, detect collisions.
        '''

        if dir == 'x':
            # Detects collision between player and walls.
            hits = pg.sprite.spritecollide(self,self.game.walls,False)
            # If hits == True.
            if hits:
                # If velocity is right,
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                # If velocity is left
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        # If direction is y, detect collisions

        if dir == 'y':
            # Detects collision between player and walls.
            hits = pg.sprite.spritecollide(self,self.game.walls,False)
            # If hits == True.
            if hits:
                # If velocity is down
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                # If velocity is up
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

# Wall sprite class
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):

        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.walls

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Attributes of the wall
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # Makes the wall the size of a tile
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
