#Import Statements
import pygame
import random
from os import path

#Game display dimensions
WIDTH = 1000
HEIGHT = 600
FPS = 200
#Number of enemy and leaves to start with
ENEMY= 3
LEAVES = 6

#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Game initialisation
# mixer is used for sound processing in pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
loading = pygame.display.set_mode((WIDTH, HEIGHT))
#Display game title
pygame.display.set_caption("Zombiee Rush")
clock = pygame.time.Clock()

#Global variables are used to store score and counter respectively
#NOTE - try using less GLOBAL VARIABLES rather create class and pass variables as a method argument
score=0
c=0

#Game images all images in res/images folder #making rect variables of all images which returns the image's W,H
background = pygame.image.load("res/images/bg1.jpg")
loadingbg = pygame.image.load("res/images/bg2.jpg")
menupad = pygame.image.load("res/images/pad.png")
health = pygame.image.load("res/images/health.png")
gamename = pygame.image.load("res/images/gamename.png")
inst = pygame.image.load("res/images/inst.png")
health_icon = pygame.transform.scale(health,(60,60))
background_rect = background.get_rect()
pad_rect=menupad.get_rect()
loading_rect = loadingbg.get_rect()
name_rect = gamename.get_rect()
inst_rect = inst.get_rect()

#Load sound effects
gunshots = pygame.mixer.Sound('res/gunshots.wav')
growl = pygame.mixer.Sound('res/growl.wav')
pygame.mixer.music.load('res/bm.mp3')
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True

#Lists to store the name of the images
run=[]
slide=[]
gun=[]
zombie=[]
death=[]
attack=[]

#Loops for appending  the image's name to the list NOTE - Do not use extend
#Different loop length due to varying number of images of each type

for x in range(9):
    run.append('Run ('+str(x)+').png')
for x in range(5):
    slide.append('Slide ('+str(x)+').png')
for x in range(11):
    zombie.append('Walk ('+str(x)+').png')
for x in range(3):
    gun.append('Shoot ('+str(x)+').png')
for x in range(10):
    death.append('Dead ('+str(x+1)+').png')
for x in range(8):
    attack.append('Attack ('+str(x+1)+').png')

#Character -------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Variable c to load the default/sequential image in list
        self.c=0
        #Variable q to load the default/sequential image in reverse list
        self.q=0
        #Load run's first image (standing stance)
        self.normal()
        self.image.set_colorkey(BLACK)
        #Define Character's spawn position and speed
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 10
        self.rect.centery = HEIGHT-(115)
        self.lives=2
        self.radius = 25
        self.speedx = 0
        self.speedy = 0
        
    def normal(self):
        #Load run's first image (standing stance)
        p = pygame.image.load("res/images/"+run[0])
        self.image=pygame.transform.scale(p,(200,190))

    def update(self):
        #Variables to store speed of character
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:

            #Move Character left
            #Load the flipped images of run
            #We use original image for right movement and flipped images for left movement
            self.c=self.c+1
            self.c=self.c%len(run)
            p = pygame.image.load("res/images/"+run[self.c])
            prev= pygame.transform.flip(p,True,False)
            #All images hitherto are resized to best fit on window dimensions
            self.image=pygame.transform.scale(prev,(200,190))
            self.speedx = -8
            
            
        if keystate[pygame.K_RIGHT]:
            #Load the images of run 
            self.c=self.c+1
            self.c=self.c%len(run)
            #Load the images of run
            p = pygame.image.load("res/images/"+run[self.c])
            self.image=pygame.transform.scale(p,(200,190))
            self.speedx = 8
            
        if keystate[pygame.K_DOWN]:
            #Load the images of slide
            self.speedx = 3
            self.c=self.c+1
            self.c=self.c%len(slide)
            p = pygame.image.load("res/images/"+slide[self.c])
            self.image=pygame.transform.scale(p,(200,190))
            
        if keystate[pygame.K_SPACE]:
            #Load the images of shoot
            self.speedx = 0
            self.c=self.c%len(gun)
            p = pygame.image.load("res/images/"+gun[self.c])
            self.image=pygame.transform.scale(p,(200,190))
            self.c=self.c+1

        for event in pygame.event.get():
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT):
                    #Load the images of normal stance and halt the character
                    self.speedx = 0
                    self.normal()
                           
        self.rect.x += self.speedx
        #Check player do not goes off the screen and reposition
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        #Create bullet object and passing bullet origin as a function of character's position
        bullet = Bullet(self.rect.centerx + 20, self.rect.centery+20)
        #add bullet to all_sprites
        all_sprites.add(bullet)
        bullets.add(bullet)

    '''def die(self):
        self.q=0
        #Load the death list images
        while(self.q<9):
            self.q=self.q%len(gun)
            p = pygame.image.load("res/images/"+death[self.q])
            self.image=pygame.transform.scale(p,(200,190))
            self.q+=1
            '''
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #Load bullet image

        p = pygame.image.load("res/images/bullet.png")
        self.image=pygame.transform.scale(p,(30,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        #Use a rect_surface instead of image
        ''' rect yellow
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        '''
        #Orient bullet and project them
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = +10

    def update(self):
        #Destroy bullet when moved out of screen
        self.rect.x += self.speedx
        if self.rect.x >=WIDTH-100:
            self.kill()
        

#Leaves -------------------------------------------------------------------------------------------------

class Leaves(pygame.sprite.Sprite):
    def __init__(self):
        #Similar varibles like character for positioning
        pygame.sprite.Sprite.__init__(self)
        p = pygame.image.load("res/images/leaves.png")
        self.image=pygame.transform.scale(p,(30,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #Origin of leaves and their speed is assigned randomly
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        #Update leaves position
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Recreate leaves if moved out of screen
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

#Trolls---------------------------------------------------------------------------------------------------------THE ENEMY

class Troll(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
         #Similar varibles like character for positioning
        self.c=0
        p = pygame.image.load("res/images/"+zombie[self.c])
        self.image=pygame.transform.scale(p,(157,190))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH-100
        self.rect.centery = HEIGHT-(115)

        #Assigning radius smaller than image size for precise looking collisions
        #We do this because often object acutally dont collide but
        #their image rectangle overlaps each-other and for code that's collision
        self.radius = int(self.rect.width * .85 / 2)

        #Spawn enemy anywhere between the given range
        self.rect.x = random.randrange(500,WIDTH)
        self.speedx = (random.randrange(-9, -1))
        

    def normal(self):
        #Normal enemy standing stance
        p = pygame.image.load("res/images/"+zombie[0])
        self.image=pygame.transform.scale(p,(157,190))

    def update(self):
        #moving enemy and updating images
        self.rect.x += self.speedx
        self.c=self.c+1
        self.c=self.c%len(zombie)
        p = pygame.image.load("res/images/"+zombie[self.c])
        self.image=pygame.transform.scale(p,(157,190))
        if self.rect.centerx < WIDTH/20 :
            self.kill()
            
    def spawnenemy(n):
        #Play the enemy 'shout' sound effect at random times
        x=random.randrange(0,5,1)
        if(x>=5):
            growl.play(1,4000,4000)
            growl.set_volume(0.7)
        #Spawn n number of enemy
        for i in range(n):
            m = Troll()
            all_sprites.add(m)
            Trolls.add(m)

def score_display(surf, text, size, x, y,color):
    #Use system font named arial
    font = pygame.font.SysFont('arial', size)
    #Set aliasing true (smooth rendering)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    #Align and blit surface
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def progress_bar(surf, x, y, val):
    #Display progress bar can be used for any purposes
    if val < 0:
        val = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (val / 100) * BAR_LENGTH
    if(fill>100):
        fill=100
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def lives(surf, x, y, lives, img):
    #Display lives of player left currently
    for i in range(lives):
        img_rect = img.get_rect()
        #Each image is displayed 30px apart
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def check(n):
    #Message for certain score 
    txt=("CONGRATULATIONS LEVEL 1 CLEARED")

    if(n>=100):
        score_display(screen,txt,30,WIDTH / 2, 50,BLUE)
        
def loadscreen():
    #First-most Screen to be loaded stating instructions and menu
    global c
    load = True
    while load:

        for event in pygame.event.get():
                # Check for closing window
                if event.type == pygame.QUIT:
                    load = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameloop()
                    
        loading.fill(BLACK)
        loading.blit(loadingbg, loading_rect)
        
        #Display surfaces like instructions and menu
        p = pygame.image.load("res/images/"+attack[c])
        prev= pygame.transform.flip(p,True,False)
        loading.blit(menupad,(WIDTH/3.25,HEIGHT/2),pad_rect)
        loadimage = pygame.transform.scale(prev,(90,120))
        loading.blit(loadimage,(WIDTH/1.75,HEIGHT/2.5))
        #For animating synch purposes
        pygame.time.wait(30)

        #Loop over the image list
        c+=1
        c=c%(len(attack)-1)
            
        
        loading.blit(gamename,(WIDTH/5,HEIGHT/12),name_rect)
        loading.blit(inst,(WIDTH/7.5,HEIGHT-125),inst_rect)
        
        pygame.display.flip()

def gameloop():
    global score
    running = True
    while running:
        
        pygame.display.flip()
        # Keep loop running at the right speed
        clock.tick(FPS)
        
        # Handle event requests
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                running = False

            #Shoot
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gunshots.play()
                    player.shoot()

        all_sprites.update()

        #When a character hits an enemy update score and spawn an enemy (Reinforcements ?? )
        kills = pygame.sprite.groupcollide(Trolls, bullets, True, True)
        for n in kills:
            score+=10
            Troll.spawnenemy(1)
        
        #When an enemy hits character deduct lives 
        damage = pygame.sprite.spritecollide(player, Trolls, True, pygame.sprite.collide_circle)
        for n in damage:
            if(player.lives>0):
                player.lives -= 1
            else:
                player.lives =0
        #If no lives left Exit game loop
        if player.lives ==0:
            screen.fill(BLACK)
            pygame.display.flip()
            pygame.time.delay(500)
            running=False
           
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        score_display(screen, str(score), 36, WIDTH / 2, 100,WHITE)
        progress_bar(screen, 15, 15, score)
        lives(screen, WIDTH - 300, 5, player.lives,health_icon )

        #For displaying level clear messages
        check(score)
        pygame.display.flip()
        clock.tick(FPS)

#Make a Sprite group object
all_sprites = pygame.sprite.Group()
leaves = pygame.sprite.Group()
bullets = pygame.sprite.Group()
Trolls= pygame.sprite.Group()

#Single character so don't make a group
player = Player()
all_sprites.add(player)

#Add n enemy for Start
for i in range(ENEMY):
    m = Troll()
    all_sprites.add(m)
    Trolls.add(m)

#Add n leaves for Start
for i in range(LEAVES):
    l = Leaves()
    all_sprites.add(l)
    leaves.add(m)
    
loadscreen()
pygame.quit()
