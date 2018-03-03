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
        # If statements allow diagonal movement
        self.vx,self.vy = 0,0
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
            self.vx *= 0.7071
            self.vy *= 0.7071

    def move(self,dx=0,dy=0):
        if not self.collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy

    # Function to test if next movement of the Player object will collide with an instance of a wall.
    # If the next movement collides, the function will return True.
    def collide_with_walls(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    # Function that executes at every frame of the game.
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.x -= self.vx * self.game.dt
            self.y -= self.vy * self.game.dt
            self.rect.x = self.x
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