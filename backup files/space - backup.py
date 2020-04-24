from pygame import * 
from tkinter import *
from math import *
from random import *
root=Tk()
root.withdraw() #hiding the extra window
size=(1000,600)
BLACK=(0,0,0)
display.set_caption("Space Battle - Shehryar Suleman")
GREEN=(0,255,0)
####
WHITE = (255, 255, 255)
screen = display.set_mode(size)
x=0
enemy=image.load("pictures/enemy.png")
enemy=transform.scale(enemy,(80,80))

enemy2=image.load("pictures/enemy2.png")
enemy2=transform.scale(enemy2,(80,80))
score=0
font.init()
scoreFont=font.SysFont("Comic Sans MS",20)
levelFont=font.SysFont("Comic Sans MS",20)
endFont=font.SysFont("Comic Sans MS",40)
background1=image.load("Backgrounds/spaceBackground.jpg")
background2=image.load("Backgrounds/background2.png")
background3=image.load("Backgrounds/background3.jpg")
background3=transform.scale(background3,(1000,600))
background1=transform.scale(background1,(1000,600))
b1rect = background1.get_rect()
player=image.load("pictures/player.png")
player=transform.scale(player,(100,100))
playAgain=image.load("pictures/playagain.png")
playAgainRect=Rect(350,400,200,200)
bosshealth=0
myClock=time.Clock()
sbpic=image.load("pictures/specialbullet.png")
sbpic=transform.scale(sbpic,(30,30))
sbrect=Rect(200,10,30,30)
sbrect2=Rect(240,10,30,30)
sblimit=0
px=500
py=400
prect = [px,py,80,80]
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
rotateLeft= False
rotateRight= False
speed=8
angle=0
sRect=Rect(0,0,1000,60)
s = screen.subsurface(sRect)
copy=s.copy()
rapid = 10
erapid = 10
eerapid=10
bullets = [] #list for the bullets
specialBullets = [] #list for the bullets
badGuys = [[0,0,0], [200,500,0], [400,0,0], [600, 500,0],[800, 300,0],[1000, 0,0]]    # 6 x,y pairs
badGuys2=[[900,500,0],[100,100,0]]
crect=[10,10,148,20]
espeed=1
badBulletList=[]
badBulletList2=[]
level=1
bulletRectList=[]
healthRectList=[]
pics=[]
frame=0
#for i in range(5):
#    pics.append(image.load("ExplosionPics\\tile00"+str(i)+".png"))

def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5 

def badMove(guy, x,y):
    ''' The Bad Guy will now B-Line towards the player. Draw a similar
        triangle to get the x,y components of the move and use trig to 
        get the angle. The angle is needed to rotate the picture.
        returns (x,y,ang)
    '''

    dist = max(1,distance(guy[0], guy[1], x, y))
    moveX = (x- guy[0])*espeed/dist
    moveY = (y- guy[1])*espeed/dist
    ang = atan2(-moveY, moveX)
    
    return moveX, moveY, degrees(ang)

def badMove2(guy, x,y):
    ''' The Bad Guy will now B-Line towards the player. Draw a similar
        triangle to get the x,y components of the move and use trig to 
        get the angle. The angle is needed to rotate the picture.
        returns (x,y,ang)
    '''

    dist = max(1,distance(guy[0], guy[1], x, y))
    moveX = (x- guy[0])*espeed/dist
    moveY = (y- guy[1])*espeed/dist
    ang = atan2(-moveY, moveX)
    
    return moveX, moveY, degrees(ang)

def checkHits(badGuys, goodX, goodY):
    ''' Both good and bad guys are circles, so to check hits we just need to check if the
        distance from center to center is < 20.
        For this simple example when they do collide we re-set the bad guy
    '''
    for i, guy in enumerate(badGuys):
        if ((goodX-guy[0])**2 + (goodY-guy[1])**2)**0.5 < 20:
            if crect[2]>0:
                crect[2]-=0.5
    
    
def moveBadGuys(badGuys, px, py):
    ''' The AI for the badGuys is real simple. If the goodGuy is left/right
        they move left/right. Same with up/down.
        badGuys - A list of bad guy positions ([x,y] lists)
        goodX, goodY - good guy position
    '''
    for guy in badGuys:
        mx, my, ang = badMove(guy, px, py)
        guy[0] += mx
        guy[1]+=my
        guy[2] = ang

def moveBadGuys2(badGuys2, px, py):
    ''' The AI for the badGuys is real simple. If the goodGuy is left/right
        they move left/right. Same with up/down.
        badGuys - A list of bad guy positions ([x,y] lists)
        goodX, goodY - good guy position
    '''
    for guy in badGuys2:
        mx, my, ang = badMove2(guy, px, py)
        guy[0] += mx
        guy[1]+=my
        guy[2] = ang


def drawScene(screen, badGuys, px, py, goodAng,bullets,badBulletList,badGuys2,badBulletList2):
    ''' 
    '''
    if crect[2]>0:
        if level==1:
            screen.blit(background1,(0,0))
        if level==2:
            screen.blit(background2,(0,0))
        if level==3:
            screen.blit(background3,(0,0))
        for guy in badGuys:
            pic = transform.rotate(enemy, guy[2])
            screen.blit(pic, guy[:2])
        for guy in badGuys2:
            pic = transform.rotate(enemy2, guy[2])
            screen.blit(pic, guy[:2])
            draw.rect(screen,BLACK,[guy[0],guy[1],50,8],2)
            draw.rect(screen,GREEN,[guy[0]+2,guy[1],48-bosshealth,8])


        for b in bullets:
            draw.circle(screen,GREEN,(int(b[0]),int(b[1])),4)
        for x in badBulletList:
            draw.circle(screen,(255,0,0),(int(x[0]),int(x[1])),4)
        for xx in badBulletList2:
            draw.circle(screen,(255,0,0),(int(xx[0]),int(xx[1])),4)
        for d in specialBullets:
            draw.circle(screen,GREEN,(int(d[0]),int(d[1])),4)
        rotPlayerPic=transform.rotate(player,degrees(goodAng))
        hw=rotPlayerPic.get_width() #width (imaginary rectangle)
        hh=rotPlayerPic.get_height()#height (imaginary rectangle)
        screen.blit(rotPlayerPic, (px-hw//2,py-hh//2))
        draw.rect(screen,BLACK,[10,10,150,20],2)
        draw.rect(screen,GREEN,crect)
        scoreText=scoreFont.render("Score: "+str(score),True,GREEN)
        scoreBar=Surface((1000,1000),SRCALPHA)#infoBar is our "sticky note"
        scoreBar.blit(scoreText,(0,0))
        screen.blit(scoreBar,(850,0))
        levelText=levelFont.render("Level "+str(level),True,GREEN)
        levelBar=Surface((1000,1000),SRCALPHA)#infoBar is our "sticky note"
        levelBar.blit(levelText,(0,0))
        screen.blit(levelBar,(852,25))
        if sblimit<1:
            screen.blit(sbpic,sbrect)
        if sblimit<2:
            screen.blit(sbpic,sbrect2)
    
    display.flip()
    myClock.tick(200)

running = True
while running:


    for evt in event.get():  
        if evt.type == QUIT: 
            running = False
        if evt.type == KEYDOWN:
            if evt.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if evt.key == K_RIGHT:
                moveLeft = False
                moveRight = True
            if evt.key == K_UP:
                moveDown = False
                moveUp = True
            if evt.key == K_DOWN:
                moveUp = False
                moveDown = True
           	
            if evt.key == K_s:
                rotateRight = True
                rotateLeft = False
            if evt.key == K_d:
                rotateRight = False
                rotateLeft = True
			
        if evt.type == KEYUP:

            if evt.key == K_LEFT:
                moveLeft = False
            if evt.key == K_RIGHT:
                moveRight = False
            if evt.key == K_UP:
                moveUp = False
            if evt.key == K_DOWN:
                moveDown = False
            if evt.key == K_s:
                rotateRight = False
        
            if evt.key == K_d:
                rotateLeft = False
         
	            	
    if moveRight and px<1000:
        px+=speed #move rigth
    if moveLeft and px>0:
        px-=speed
    if moveDown and py<600:
        py+=speed
    if moveUp and py>0:
        py-=speed
    
    if rotateRight:
    	angle+=0.05
    if rotateLeft:
    	angle-=0.05

    keys = key.get_pressed()
    mb=mouse.get_pressed()
    mx,my=mouse.get_pos() #getting mouse position
    #print((40*cos(90-angle)))
    if mb[0]==1:
        if level==0 and playAgainRect.collidepoint(mx,my):
            score=0
            level=1
            crect[2]=148
            badGuys = [[0,0,0], [200,500,0], [400,0,0], [600, 500,0],[800, 300,0],[1000, 0,0]]    # 6 x,y pairs

    if rapid<30:
        rapid+=1
    if erapid<60:
        if level==1:

            erapid+=1
        if level==2:
            erapid+=1.1
    if eerapid<60:
        eerapid+=1
    if score==15  and crect[2]>0:
        if len(badGuys)<8:
            badGuys.append([100,900,0])
            badGuys.append([800,100,0])        
        level=2
        sblimit=0
    if score==35 and crect[2]>0:
        level=3
        sblimit=0

    if keys[K_a] and rapid==30 and sblimit<2: #32 is the SPACE key
        sblimit+=1
        rapid = 0
        for i in range(20):
            vx = 5*sin(0+i) #move right five pixels
            vy = 5*cos(0+i)
            lx=px
            ly=py

        #               0   1  2  3
            specialBullets.append([lx,ly,vx,vy])

########## SHOOTING SPECIAL 360 BULLETS ##################
    for b in specialBullets[:]:
       
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        specialbulletRect=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        for i in badGuys:
            if specialbulletRect.colliderect([i[0],i[1],80,80]):
                print("Hit")
                try:
                    specialBullets.remove(b)
                except:
                    pass
                
                d=i[0]
                badGuys.remove(i)
                if d>500:
                    badGuys.append([randint(900,1100),randint(0,600),0])
                if d<500:
                    badGuys.append([randint(-100,100),randint(0,600),0])
                score+=1

        for ii in badGuys2:
            if specialbulletRect.colliderect(ii[0],ii[1],80,80):
                try:
                    specialBullets.remove(b)
                except:
                    pass

                if bosshealth!=48:
                    bosshealth+=12
                if bosshealth==48:
                    score+=5
                    badGuys2.remove(ii)
                    bosshealth=0
                    direction=[randint(900,1100),randint(-100,100)]
                    place=direction[randint(0,1)]
                    badGuys2.append([place,randint(0,600),0])

        for d in badBulletList:    
            if specialbulletRect.colliderect([d[0],d[1],10,10]):
                badBulletList.remove(d)
                try:
                    specialBullets.remove(b)
                except:
                    pass
        if max(b) > 1050 or min(b) < -50:
            try:
                bullets.remove(b)
            except:
                pass
####################################################################



    if keys[K_w] and rapid==30: #32 is the SPACE key
        rapid = 0

        vx = 5*sin(angle) #move right five pixels
        vy = 5*cos(angle)
        lx=px
        ly=py

        #               0   1  2  3
        bullets.append([lx,ly,vx,vy])
        
########################## SHOOTING NORMAL BULLETS ###############################

    for b in bullets[:]:
        #b[2]*=1.1
        #b[3]*=1.1
        
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        bulletRect=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        bulletRectList.append(bulletRect)
        for i in badGuys:
            if bulletRect.colliderect([i[0],i[1],80,80]):
                print("Hit")
                #screen.blit(pics[frame],(i[0],i[1]))
                frame+=1 
                try:
                    bullets.remove(b)
                except:
                    pass
                d=i[0]
                

                badGuys.remove(i)
                direction=[randint(900,1100),randint(-100,100)]
                place=direction[randint(0,1)]
                badGuys.append([place,randint(0,600),0])
                
                score+=1
        for ii in badGuys2:
            draw.rect(screen,BLACK,[ii[0],ii[1],50,8],2)
            draw.rect(screen,GREEN,[ii[0]+2,ii[1],48-bosshealth,8])
            if bulletRect.colliderect(ii[0],ii[1],80,80):
                try:
                    bullets.remove(b)
                except:
                    pass
            
                if bosshealth!=48:
                    bosshealth+=12
                    
                if bosshealth==48:
                    
                    score+=5
                    badGuys2.remove(ii)
                    bosshealth=0
                    direction=[randint(900,1100),randint(-100,100)]
                    place=direction[randint(0,1)]
                    badGuys2.append([place,randint(0,600),0])

        #print(bosshealth)
        for d in badBulletList:
            if bulletRect.colliderect([d[0],d[1],10,10]):
                badBulletList.remove(d)
                try:
                    bullets.remove[b]
                except:
                    pass

        if max(b) > 1050 or min(b) < -50:
            bullets.remove(b)

######################################################################

    
    if erapid>60 or erapid==60:
        erapid=0
        for i in badGuys:
            vx = 5*sin(i[2]) #move right five pixels
            vy = 5*cos(i[2])
            lx=i[0] +40
            ly=i[1]+40

                #               0   1  2  3
            badBulletList.append([lx,ly,vx,vy])
        
############################## ENEMY BULLETS #############################
    for b in badBulletList[:]:
            #b[2]*=1.1
            #b[3]*=1.1
            
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        badBulletRect=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        if badBulletRect.colliderect([px,py,80,80]):
            #print("Hit")
            
            badBulletList.remove(b)
            if crect[2]>0:
                crect[2]-=0.5
            
        if max(b) > 1050 or min(b) < -50:
            badBulletList.remove(b)
##########################################################################

############################ BOSS BULLETS ##################################
    if eerapid>60 or eerapid==60:
        eerapid=0
        for i in badGuys2:
            vx = 5*sin(135+i[2]) #move right five pixels
            vy = 5*cos(135+i[2])
            lx=i[0] +40
            ly=i[1]+40

                #               0   1  2  3
            badBulletList2.append([lx,ly,vx,vy])
        
############################## BOSS BULLETS MOVEMENT #############################
    for b in badBulletList2[:]:
            #b[2]*=1.1
            #b[3]*=1.1
            
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        badBulletRect2=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        if badBulletRect2.colliderect([px,py,80,80]):
            #print("Hit")
            
            badBulletList2.remove(b)
            if crect[2]>0:
                crect[2]-=0.5
            
        if max(b) > 1050 or min(b) < -50:
            badBulletList2.remove(b)

    

    #goodAng = degrees(atan2(oldY-py, px-oldX))
    moveBadGuys(badGuys, px, py)
    moveBadGuys2(badGuys2, px, py)
    #badbullet(badGuys,px,py,screen)
    checkHits(badGuys, px, py)
    drawScene(screen, badGuys, px, py, angle,bullets,badBulletList,badGuys2,badBulletList2)
    
    if crect[2]==0:
        level=0
        #print("DONE")
    if level==0:
        sblimit=0
        badGuys=[]
        screen.fill(BLACK)
        #print(score)
        endText=endFont.render("You DIED!!!. Your Score: "+str(score),True,WHITE)
        endBar=Surface((1000,200),SRCALPHA)#infoBar is our "sticky note"
        endBar.blit(endText,(0,0))
        screen.blit(endBar,(250,300))
        screen.blit(playAgain,playAgainRect)
import menu    
quit() 
