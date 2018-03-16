import pygame as pg
from settings import *

# Player sprite class
class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Initalize an instance of Player in group all_sprites
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        # Sets attributes of class Player, sets a reference to the game class
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx,self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    # Function to get key presses, and move character in direction in event of keypress
    def get_keys(self):
        # If statements allow diagonal movement. Elif disables.
        # Set vx and vy to 0 unless a key is pressed.
        self.vx,self.vy = 0,0
        # Event handling of keyboard input
        # I used if statements instead of elif in order to allow diagonal
        # movement.
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        # Regulation of diagonal movement speed through pythag theorem
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071 # 1 / sqrt2
            self.vy *= 0.7071 # 1 / sqrt2

    # Function to test if next movement of the Player object will collide with an instance of a wall.
    # If the next movement collides, the function will return True.


    # Function that executes at every frame of the game.
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # Updates x value
        self.rect.x = self.x
        # Calls collide_with_walls('x') every frame
        self.collide_with_walls('x')
        # Update y value
        self.rect.y = self.y
        # Calls collide_with_walls('y') every frame
        self.collide_with_walls('y')
        # in the event of the player sprite colliding with a wall, reverse
        # the movement, effectively stopping movement.
        # if pg.sprite.spritecollideany(self,self.game.walls):
        #     self.x -= self.vx * self.game.dt
        #     self.y -= self.vy * self.game.dt
        #     self.rect.topleft = (self.x, self.y)
        # If sprite collides with ANY sprite in group walls, reverse the movement.

    def collide_with_walls(self,dir):
        # My nifty little collision checker.
        # Having TWO checks ensures that in event of one x or y value collision,
        # Movement the other way still works, thus we can slide down walls.
        # If direction is x, detect collisions
        if dir == 'x':
            # Detects collision between player and walls.
            hits = pg.sprite.spritecollide(self,self.game.walls,False)
            # If hits == True.
            if hits:
                # If velocity is right,
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                # If velocity is left
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        # If direction is y, detect collisions

        if dir == 'y':
            # Detects collision between player and walls.
            hits = pg.sprite.spritecollide(self,self.game.walls,False)
            # If hits == True.
            if hits:
                # If velocity is down
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                # If velocity is up
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

# Wall sprite class
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.walls
        # Initalizes into groups
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # Makes the wall the size of a tile
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE