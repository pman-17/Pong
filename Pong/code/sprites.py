from settings import *
from random import choice, uniform

class Paddel(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        #image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0,0), SIZE['paddle']), 0, 10)
       

        #rectangle and movement
        self.rect = self.image.get_frect(center = POS['player'])   
        self.old_rect = self.rect.copy()
        self.direction = 0
        self.speed = SPEED['player']

    def move(self, dt):
            self.rect.centery += self.direction * self.speed *dt
            self.rect.top = 0 if self.rect.top < 0 else self.rect.top
            self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom
    
    def update(self, dt):
            self.old_rect = self.rect.copy()
            self.get_direction()
            self.move(dt)    


class Player(Paddel): #the player class inherits image, rectangle, movement and upddate logic from the paddel class
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = SPEED['player']

    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  

class Opponent(Paddel):
    def __init__(self, groups, ball):
        super().__init__(groups)#calls all the logic for iages, rectangles and movement in the paddel sprite
        self.speed = SPEED['opponent']
        self.rect.center = POS['opponent'] # set opponents position ot their side of the window
        self.ball = ball #pass ball as an argument into this class at init so create the ball variable t
    
    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1
        #if the ball is lower than the opponent then the opponent will move down, otherwise the opponent will move up to meet the ball

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score  = update_score


        #image
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0]/ 2, SIZE['ball'][1]/2), SIZE['ball'][0]/ 2)#drawing a circular ball on the image for the ball
        #self.image.fill(COLORS['ball'])

        #rect and movement
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy() #get a rectangle of same size and pos and store 
        self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8) *choice((-1, 1)))

    def move(self, dt):
        self.rect.x += self.direction.x * SPEED['ball'] * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * SPEED['ball'] * dt
        self.collision('vertical')


    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect): #is there overlap between player and the ball
                if direction == 'horizontal': #is direction horizontal
                    #first check is there any overlap between pbject and player, then check if old rectangle is to the left pf the sprite in the previous frame
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left 
                        self.direction.x *= -1 #bounce the ball of the paddel following collision by changing x direciton
                        SPEED["ball"] += 50
                    #back of padel
                    if self.rect.left <= sprite.rect.top and self.old_rect.left <= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                        SPEED["ball"] += 50
                        
                    else:
                        #chekcing if bottom of ball collides with the top of the player in current and old frame
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top #moves the ball up with the paddel ie can collide with side or top of paddel
                            self.direction.y *= -1 #bounces the ball up away from the paddel
                        #same logic for bottom of padel
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top  = sprite.rect.bottom 
                            self.direction *= -1



    def wall_collision(self):
        #ensures ball stays within limits of window
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        if self.rect.right >= WINDOW_WIDTH or self.rect.left <=0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH/2 else 'opponent') #if ball is on left hand side of screen then player will selected in dictionary if not the opponenet
            self.reset()

    def reset(self):
        self.rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2) # WHEN BALL LEAVES THE WINDOW IT IS RESET TO THE MIDDLE OF THE SCREEN
        self.direction = pygame.Vector2(choice((1, -1))    , uniform(0.7, 0.8) *choice((-1, 1)))# ball moves in random direction
        pygame.time.delay(2000)
    def update(self, dt): 
        self.old_rect = self.rect.copy() #store the old position of the rectangle before moving it in next frame
        self.move(dt)
        self.wall_collision()