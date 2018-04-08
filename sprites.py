import pygame as pg
from tilemap import collide_hit_rect
from settings import *
import random
# Loading pygame vector class
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    '''
        My nifty little collision checker.
        Having TWO checks ensures that in event of one x or y value collision,
        Movement the other way still works, thus we can slide down walls.
        If direction is x, detect collisions.

        rect HIT_RECT is used for collisions instead of the normal rectangle
        as it provides more consistent collisions as it is a static rectangle
        unlike the rectangle surrounding the player sprite that's used to track
        movement

        This function is not a method of any class, which means that this function
        will work with any sprite, give the sprite, the group the collision checker
        must check with, and the direction.

    '''

    # If direction is x, perform collision checking for x axis
    if dir == 'x':
        # Detects collision between player and walls.
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        # If hits == True.
        if hits:
            # If velocity is right,
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            # If velocity is left
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    # If direction is y, perform collision checking for y axis
    if dir == 'y':
        # Detects collision between player and walls.
        hits = pg.sprite.spritecollide(sprite, sprite.game.walls, False, collide_hit_rect)
        # If hits == True
        if hits:
            # If velocity is down
            if hits[0].rect.centery > sprite.hit_rect.centery > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            # If velocity is up
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y




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
        self.pos = vec(x,y)

        self.rot = 0

        self.last_shot = 0

        # Set health
        self.health = PLAYER_HEALTH

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

        # Shoot when space is pressed
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)


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
        collide_with_walls(self,self.game.walls,'x')

        # Update y value
        self.hit_rect.centery = self.pos.y

        # Calls collide_with_walls('y') every frame
        collide_with_walls(self,self.game.walls,'y')


        self.rect.center = self.hit_rect.center

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
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 100
        self.speed = MOB_SPEED

        # Vectors
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def avoid_mobs(self):
        # For each mob in mobs
        for mob in self.game.mobs:
            # Ignore current mob
            if mob != self:
                # Get the distance between current mob and mob in group
                dist = self.pos - mob.pos
                # If the distance between them is less than 50
                if 0 < dist.length() < AVOID_RADIUS:
                    # Spread them throughout a radius to avoid them clumping up
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # Unit vector
        self.acc = vec(1,0).rotate(-self.rot)

        # Mechanism to prevent mobs from clumping. Refer to avoid_mobs for documentation
        self.avoid_mobs()

        # Use self.speed as MOB_SPEEDS has a bunch of varying speeds, meaning
        # zombies will have different speeds, instead of all them being statically
        # moving together
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self,self.game.walls,'y')

        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0,0, width, 7)
        if self.health < 100:
            pg.draw.rect(self.image, col, self.health_bar)



# Mob sprite class
class Bullet(pg.sprite.Sprite):
    def __init__(self,game,pos,dir):

        # Defines which groups the sprite should be in
        self.groups = game.all_sprites, game.bullets

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos

        # Add some randomness to the bullets being shot
        # This will make the bullets shoot on a slightly different offset every Bullet
        spread =  random.uniform(-GUN_SPREAD, GUN_SPREAD)

        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        # If bullet hits any wall, it stops.
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()

# Wall sprite class (obselete - unless using walls instead of a TiledMap)
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

# Obstacle class
class Obstacle(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h):

        # Defines which groups the sprite should be in
        self.groups = game.walls

        # Initalizes into groups (defined above)
        pg.sprite.Sprite.__init__(self,self.groups)

        # Attributes of the Obstacle
        self.game = game
        self.rect = pg.Rect (x,y,w,h)

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y
