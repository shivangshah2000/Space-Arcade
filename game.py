import pygame,random,math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")

icon= pygame.image.load('space-invaders.png').convert_alpha() # convert_alpha() increases
# the efficiency of the code also prevents the game from lagging as it pre-loads the images

pygame.display.set_icon(icon)
flag = True

player1=pygame.image.load('player.png').convert_alpha()
x=360
y=480
movx=0
inc_player_speed=0.5

bg_pic=pygame.image.load('new_bg1.jpg').convert_alpha()

file=open('highscore.txt','r+')
s=""
for i in file:
    s+=i[:-1]
s+=i[-1]
highscore=s.split(',')
highscore=list(map(int,highscore))
highscore.sort()

file.close()

bullet=pygame.image.load('bullet.png').convert_alpha()
bullet_flag=False
bullet_x=-9999
bullet_y=-9999
bullet_speed=2


enemies=[]
no_of_enemies = 6
enemy_movx = no_of_enemies*[0.5]
enemy_movy = no_of_enemies*[30]
x1=[]
y1=[]
for i in range(no_of_enemies):
    enemies.append(pygame.image.load('enemy.png').convert_alpha())
    xx = random.randint(0, 730)
    yy = random.randint(0, 70)
    x1.append(xx)
    y1.append(yy)

inc_enemy_speed=0.1
score=0
game_over=0
font =pygame.font.Font('freesansbold.ttf',32)
font2=pygame.font.Font('freesansbold.ttf',64)

#bg music
mixer.music.load('background.wav')
mixer.music.play(-1)

def show_high_score():
    score_dis= font.render("High Score : "+ str(highscore[-1]), True, (255,255,255) )
    screen.blit(score_dis,(540,10))

def show_game_over():
    score_dis = font2.render("Game Over", True, (255, 255, 255))
    screen.blit(score_dis, (250, 250))

def show_score():
    score_dis= font.render("Score : "+ str(score), True, (255,255,255) )
    screen.blit(score_dis,(10,10))

def drawPlayer(x,y):
    screen.blit(player1,(x,y))


def isCollision(a1,b1,a2,b2):
    if math.sqrt((a1-a2)**2+(b1-b2)**2)<=30:
        return 1
    else:
        return 0

while flag:
    screen.fill((0, 0, 0))
    screen.blit(bg_pic,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type== pygame.KEYDOWN:
            if event.key== pygame.K_LEFT:
                movx=-inc_player_speed
            if event.key == pygame.K_RIGHT:
                movx=inc_player_speed
            if event.key== pygame.K_SPACE:
                if bullet_flag==True:
                    pass
                else:
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_flag=True
                    bullet_x=x
                    bullet_y=y+10

        if event.type== pygame.KEYUP:
            movx=0
    if game_over==0:
        screen.blit(bullet, (bullet_x+15, bullet_y))
        if bullet_flag:
            bullet_y-=bullet_speed
            if bullet_y< -32:
                bullet_flag=False
        x+=movx
        if x>735 or x< 0:
            if x>735:
                x=735
            else:
                x=0
        for i in range(no_of_enemies):
            screen.blit(enemies[i],(x1[i],y1[i]))
            x1[i]+=enemy_movx[i]
            if x1[i]>735 or x1[i]< 0:
                if x1[i]>735:
                    x1[i]=735
                    enemy_movx[i] =-enemy_movx[i]
                    y1[i]+=enemy_movy[i]
                else:
                    x1[i]=0
                    enemy_movx[i] =-enemy_movx[i]
                    y1[i] += enemy_movy[i]
            if isCollision(x1[i], y1[i], bullet_x, bullet_y):
                score += 1
                if score%5==0:
                    bullet_speed+=0.1
                    inc_player_speed+=0.1

                col_sound = mixer.Sound('explosion.wav')
                col_sound.play()
                bullet_y = -100
                if enemy_movx[i]<0:
                    enemy_movx[i]+=-(inc_enemy_speed)
                else:
                    enemy_movx[i] += (inc_enemy_speed)
                x1[i] = random.randint(0, 730)
                y1[i] = random.randint(0, 70)
                bullet_flag = False
            if isCollision(x, y, x1[i], y1[i]):
                col_sound_player=mixer.Sound('Explosion+5.wav')
                col_sound_player.play()
                if score>highscore[-1]:
                    file.write(',')
                    file.write(str(score))
                    print("Congrats you beat the high score. New high score is "+ str(score))
                else:
                    print("Game over! Your score is " + str(score) + " High Score is " + str(highscore[-1]))
                game_over=1
                break
    else:
        show_game_over()
    drawPlayer(x,y)
    show_score()
    show_high_score()
    pygame.display.update()