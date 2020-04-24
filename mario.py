#MarioGame.py

from pygame import *
from random import *

X=0
Y=1
VY=2
ONGROUND=3
##LOADING IMAGES 
backpic=image.load("background2.png")
maskPic=image.load("maskkk.png")
coinPic=image.load("co.png")
enemy=image.load("e3.png")
enemy=transform.scale(enemy,(800,800))

screen = display.set_mode((1000,600))#SCREEN
##DEFINING COLOURS
WHITE=(255,255,255)
YELLOW=(255,255,0)
SGREEN=(0,255,194)
BLACK=(0,0,0)
COLOR=(198,255,0)
GREEN=(0,255,0)
init()
font.init()#Initializing font
arialFont=font.SysFont("Arial",40)#Font Style and size
##MUSIC
mixer.pre_init(44100,16,2,4096)
mixer.music.load("song.mp3")
mixer.music.set_volume(1)
mixer.music.play(-1)



##RECTS
TextRect=Rect(100,100,20,20)
badGuys = [[900,440,0], [1190,440,0], [1390,440,0],[1590,440,0],[1790,440,0],  [2000,440,0]]    # 6 x,y pairs
badGuysX=[900,1190]
##VARIABLES
enemy1=900
score=0
count=0
erapid=0
##LISTS
badBulletList=[]
bullets=[]
rapid=0
crect=[10,10,148,20] #enemy health
def moveBadGuys(badGuys,mario,badGuysX,count):##Moving Bad guys 
    move=""
    for i in range(len(badGuys)):
        badGuys[i][0]-=2
        print(badGuys[i][0])
        print(count)
def getPixel(mask,x,y):##Getting pixel of the image
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        #print( mask.get_at((int(x),int(y)))[:3])
        return maskPic.get_at((int(x),int(y)))[:3]
   
    else:
        return (-1,-1,-1)
        
def moveRight(guy,vx):#Moving the mario right if there is no white colour
    for i in range(vx):
        if getPixel(maskPic,guy[X]+430,guy[Y]) != WHITE and getPixel(maskPic,guy[X]+430,guy[Y]+27) != WHITE and mario[X]<8300:
            guy[X] += 1
        

def moveLeft(guy,vx):#Movinf left if there is no white colour
    for i in range(vx):              #head                                           #feet
        if getPixel(maskPic,guy[X]+405 ,guy[Y]) != WHITE and getPixel(maskPic,guy[X]+405,guy[Y]+27) != WHITE and mario[X]>0:
            guy[X] -= 1

def moveGuy(guy):
    keys = key.get_pressed()
        
    if keys[K_LEFT]:
        moveLeft(guy,5)#moving guy  5 pixels left
    if keys[K_RIGHT]:
        moveRight(guy,5)#moving guy 5 pixels right
    

def moveMario():
    ''' moveMario controls the location of Mario as well as adjusts the move and frame
        variables to ensure the right 5picture is drawn.
    '''
    global move, frame
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_RIGHT] and mario[X]<8300:#changing the moves of mario to blit pictures according
        newMove = RIGHT
        
    elif keys[K_LEFT] and mario[X]>0:
        newMove = LEFT
        
    else:
        frame=0
    #Mario Jumping
    if keys[K_SPACE] and mario[ONGROUND]:
        mario[VY] = -15
        mario[ONGROUND]=False
    

    mario[Y]+=mario[VY]     # add current speed to Y - jumping or falling down 
    if mario[Y] >= 485:#ground
        mario[Y] = 485
        mario[ONGROUND] = True #stop falling down 
    mario[VY]+=0.7     # add current speed to Y


    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
def movingEnemyBullet(badBulletList,crect): #this function is for moving normal enemy bullets

    for b in badBulletList[:]: #bad bullet list is the list of normal enemy bullets, bullets is appended in list in the game running loop
            #b[2]*=1.1
            #b[3]*=1.1
            
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        badBulletRect=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        if badBulletRect.colliderect([400,450,20,40]): #checking if enemy bullet collides with player
            print("Hit")
            
            badBulletList.remove(b) #enemy bullet is removed
            if crect[2]>0: #if player health is remaing
                crect[2]-=0.5 #then decrease the health
            
        if max(b) > 1050 or min(b) < -50:
            badBulletList.remove(b) #removing the enemy bullet if it goes off screen



def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):#folder File
##        i=transform.scale(i,(40,40))
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
        
    return move
def movingBullets(bullets): #movin p
    
    for b in bullets[:]: #bullets is the location rect of each bullet that is shot when the player presses w
        #b[2]*=1.1
        #b[3]*=1.1
        
        b[0]+=b[2] #horizontal movement, b[0] is original x location, and the b[2] is added to the original location, so this keeps on changing
        b[1]-=b[3] #vertical movement, b[1] is original y location, and the b[3] is added to the original location, so this keeps on changing

        bulletRect=Rect(b[0]-5,b[1]-5,10,10)# #making a bullet rect
        
        for i in badGuys: # i become each enemy 
            if bulletRect.colliderect([i[0],i[1],80,80]): #checking if bullet collides with enemy
                print("Hit")
                #screen.blit(pics[frame],(i[0],i[1]))
                #frame+=1 
                try:
                    bullets.remove(b) #bullet is removed
                except:
                    pass
                d=i[0]
                

                badGuys.remove(i) #enemy is removed
    
offset=0
rec=Rect(400,0,0,0)
def drawScene():

    global offset,rec,score,c1,eRec
    offset=400-mario[X]
    screen.blit(backpic,(-mario[X],0))#Blitting background
    pic = pics[move][int(frame)]#mario Pics
    
    screen.blit(pic,(rec))#blitting mario
    
    TextPic1=arialFont.render("Score:"+str(score),True,YELLOW)
    scoreBar=Surface((1000,1000),SRCALPHA)#ScoreBAr is our "sticky note"
    scoreBar.blit(TextPic1,(0,0))
    screen.blit(scoreBar,(20,20))
    for guy in badGuys:
            pic = transform.rotate(enemy, guy[2]) 
            screen.blit(pic, guy[:2])
    for x in badBulletList: #blitting normal enemy bullets
            draw.circle(screen,(255,0,0),(int(x[0]),int(x[1])),4)
    for b in bullets: # blitting the player bullets on screen
            draw.circle(screen,GREEN,(int(b[0]),int(b[1])),4)
    #Blitting coins
    for c1 in coinRects:
        c=c1.move(offset,0)
        screen.blit(coinPic,c)
    #When game is complete
    if getPixel(maskPic,mario[X]+430,mario[Y]) == SGREEN and getPixel(maskPic,mario[X]+430,mario[Y]+27) == SGREEN and mario[X]<8300:
            score+=5
            screen.fill((0,0,0))
            TextPic2=arialFont.render("Game Completed!!",True,WHITE)
            scoreBar=Surface((1000,1000),SRCALPHA)#infoBar is our "sticky note"
            scoreBar.blit(TextPic2,(0,0))
            screen.blit(scoreBar,(300,300))
            


    rec = Rect(mario[X]+offset,mario[Y]-27,29,54)#rectangle around the player
    draw.rect(screen,BLACK,crect) #health rect of player
    draw.rect(screen,(255,255,255),[10,10,150,20],2) #health rect of player
    for c1 in coinRects:
        c=c1.move(offset,0)
        if rec.colliderect(c):
            score+=5
            coinRects.remove(c1)
            mixer.music.play(1)    
    
    for pl in plats:
        p = pl.move(offset,0)#move horizontally only
    
        
    display.flip()

def checkCollide(guy,plats):
    global offset,rec

#Checking collisions for plats to stand on top
    for p in plats:
        p2=p.move(offset,0)
        if rec.colliderect(p2):
                #he is falling down
            if mario[VY]>0 and rec.move(0,-mario[VY]).colliderect(p2)==False:

                mario[ONGROUND]=True
                mario[VY] =0
                mario[Y] = p2.y - 26 #54 is the size of the player #p.y is the p            

RIGHT = 0 # These are just the indices of the moves
DOWN = 1  
UP = 2
LEFT = 3
#RECTS
plats=[Rect(289,344,41,7),Rect(456,344,217,7),Rect(801,429,86,7),Rect(1229,387,86,7),Rect(1572,344,86,7),Rect(2044,344,86,7),Rect(2900,344,129,7),Rect(3028,172,344,7),Rect(3500,172,172,7),Rect(3628,344,42,7),Rect(3884,344,42,7),Rect(4144,344,42,7),Rect(4271,344,42,7),Rect(4401,344,42,7),Rect(4657,344,42,7),Rect(4272,172,42,7),Rect(4785,172,130,7),Rect(5085,172,175,7),Rect(5128,344,88,7),Rect(6587,430,84,7),Rect(6800,344,173,7),Rect(7273,430,84,7),Rect(5346,471,40,7),Rect(5386,430,40,7),Rect(5426,388,40,7),Rect(5470,345,40,7),Rect(5603,343,40,7),Rect(5644,386,40,7),Rect(5685,428,40,7),Rect(5729,469,40,7),Rect(7358,470,40,7),Rect(7400,430,40,7),Rect(7440,386,40,7),Rect(7485,344,40,7),Rect(7530,300,40,7),Rect(7572,257,40,7),Rect(7614,214,40,7),
       Rect(7658,171,83,7),Rect(5942,470,40,7),Rect(5986,428,40,7),Rect(6029,386,40,7),Rect(6073,344,83,7),Rect(6243,344,40,7),Rect(6286,386,40,7),Rect(6329,430,40,7),Rect(6372,470,40,7),Rect(544,171,41,7),Rect(8086,470,38,2)]
coinRects=[Rect(289,344,41,49),Rect(503,344,41,49),Rect(544,173,41,49),Rect(588,344,41,49),Rect(2945,344,41,49),Rect(3630,173,41,49),Rect(4144,344,41,49),Rect(4273,173,41,49),Rect(4273,344,41,49),Rect(4401,344,41,49),Rect(5131,173,41,49),Rect(5172,173,41,49),Rect(6887,344,41,49)]

pics = [] #2d list
pics.append(makeMove("Mario",1,6))      # RIGHT
pics.append(makeMove("Mario",7,12))     # DOWN
pics.append(makeMove("Mario",13,18))    # UP
pics.append(makeMove("Mario",19,24))    # LEFT

frame=0     # current frame within the move
move=0      # current move being performed (right, down, up, left)

mario=[400,500,0,True]

running = True
myClock = time.Clock()

while running:
    keys = key.get_pressed()
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
    
    
    mx,my=mouse.get_pos()
    if erapid<60: #this is to limit enemy boss shooting
        erapid+=1
    if rapid<30: #this is to limit enemy boss shooting
        rapid+=1
    if erapid>60 or erapid==60: #enemy bullets movement
        erapid=0 # so that there is time in between shooting enemy bullets
        for i in badGuys: # for each enemy
            vx = 5 # The x and y movement of enemy bullet is sort of randomized, because i[2] is angle of enemy and player, so sometimes it goes to direction of player and sometime it doesnt
            vy = 0 
            lx=i[0] +40 # is the starting position of bullet, same as the location of enemy
            ly=i[1]+40

                #               0   1  2  3
            badBulletList.append([lx,ly,vx,vy])

    if keys[K_w] and rapid==30: #When w key is pressed
        rapid = 0

        vx = 2 # for x movement. angle is the angle of rotation, so the bullets are moved according to the angle so that the bullets go where player is pointing
        vy = 0 # for y movement.
        lx=420
        ly=470

        #               0   1  2  3
        bullets.append([lx,ly,vx,vy])

    movingEnemyBullet(badBulletList,crect)
    movingBullets(bullets)
    moveGuy(mario)
    moveMario()          
    checkCollide(mario,plats)
    drawScene()
    
myClock.tick(500)
 
    
quit()
