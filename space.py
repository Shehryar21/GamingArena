from pygame import * 
from tkinter import *
from math import *
from random import *
root=Tk()
root.withdraw() #hiding the extra window
size=(1000,600)
BLACK=(0,0,0)
GREEN=(0,255,0)
####
WHITE = (255, 255, 255)
screen = display.set_mode(size)

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
background4=image.load("Backgrounds/background4.jpg")
background5=image.load("Backgrounds/background5.png")
playpic=image.load("music/play.png")
pausepic=image.load("music/pause.png")
playpic=transform.scale(playpic,(30,30))#resizing the picture
pausepic=transform.scale(pausepic,(30,30))#resizing the picture
background3=transform.scale(background3,(1000,600))
background1=transform.scale(background1,(1000,600))
player=image.load("pictures/player.png")
player=transform.scale(player,(100,100))
playAgain=image.load("pictures/playagain.png")
playAgainRect=Rect(350,400,200,200)
myClock=time.Clock()
sbpic=image.load("pictures/specialbullet.png")
sbpic=transform.scale(sbpic,(30,30))
sbrect=Rect(200,10,30,30)
sbrect2=Rect(240,10,30,30)
sblimit=0
px=500
py=400
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
rotateLeft= False
rotateRight= False
speed=8 #speed of player
angle=0 #angle of player
rapid = 10 #
erapid = 10
eerapid=10
bullets = [] #list for the bullets
specialBullets = [] #list for the 360 degree bullets
badGuys = [[0,0,0], [200,500,0], [400,0,0], [600, 500,0],[800, 300,0],[1000, 0,0]]    # List of normal enemies
badGuys2=[[900,500,0,0],[100,100,0,0]] #list of enemy boss
crect=[10,10,148,20] #enemy health
espeed=1
badBulletList=[]
badBulletList2=[]
level=1
pics=[]
frame=0

playRect=Rect(800,10,30,30)
pauseRect=Rect(750,10,30,30)

###### MUSIC ##########
mixer.pre_init(44100,-16,1,512)
init()
mixer.init()
mixer.music.load("music/music.mp3")#loads the song

mixer.music.play(-1)
###################################





def distance(x1,y1,x2,y2): #This function finds the distance between the player and the enemy
    return ((x1-x2)**2 + (y1-y2)**2)**0.5 

def badMove(guy, x,y): #guy is enemy, x is player x position, y is player y position. FOR NORMAL ENEMIES

    dist = max(1,distance(guy[0], guy[1], x, y)) #this finds the dist between player and enemy, the function above is used for that
    moveX = (x- guy[0])*espeed/dist #this is the movement of x direction of enemy and how fast it is going to approach the player
    moveY = (y- guy[1])*espeed/dist #this is the movement of y direction of enemy and how fast it is going to approach the player
    ang = atan2(-moveY, moveX) #this finds the angle between player and enemy
    
    return moveX, moveY, degrees(ang)

def badMove2(guy, x,y): #same thing as above function, just the difference is that this is for the boss enemy, where as the above one is for normal enemies

    dist = max(1,distance(guy[0], guy[1], x, y))
    moveX = (x- guy[0])*espeed/dist
    moveY = (y- guy[1])*espeed/dist
    ang = atan2(-moveY, moveX)
    
    return moveX, moveY, degrees(ang)

def checkHits(badGuys, goodX, goodY): #This function finds if an enemy is touching the player
    for i, guy in enumerate(badGuys):
        if ((goodX-guy[0])**2 + (goodY-guy[1])**2)**0.5 < 20: #checking the distance between normal enemies and player. IF less than 20, then decrease health.
                                                                #less than 20 would mean that the enemy is touching the player, becuase player itself is 80 by 80
            if crect[2]>0: #this is the health bar rect, so if there is health remaining, then decrease it
                crect[2]-=0.5

def checkHits2(badGuys2, goodX, goodY): #This function finds if the boss enemy is touching the player. DOES the same thing as above function, just for the boss enemy
    for i, guy in enumerate(badGuys2):
        if ((goodX-guy[0])**2 + (goodY-guy[1])**2)**0.5 < 20: 
            if crect[2]>0:
                crect[2]-=0.5
    
    
def moveBadGuys(badGuys, px, py): #for the normal enemies
    ''' .
        badGuys - A list of bad guy positions ([x,y,ang] lists)
        px, py - good guy position
    '''
    for guy in badGuys: #become each enemy position in the enemy list named badGuys
        mx, my, ang = badMove(guy, px, py) #this goes in the function bad move which gets the movement of enemy towards the player
        guy[0] += mx #mx which is founded in  badmove is added to the x position of enemy
        guy[1]+=my #my which is founded in  badmove is added to the y position of enemy
        guy[2] = ang #angle between the enemy and the player is added 

def moveBadGuys2(badGuys2, px, py): # same as above function. Just for the enemy boss
    ''' 
        badGuys2 - A list of bad enemy boss positions ([x,y,ang] lists)
        px, py - player position
    '''
    for guy in badGuys2:
        mx, my, ang = badMove2(guy, px, py)
        guy[0] += mx
        guy[1]+=my
        guy[2] = ang

def movingBullets(bullets): #movin p
    global score,bosshealth
    for b in bullets[:]: #bullets is the location rect of each bullet that is shot when the player presses w
        #b[2]*=1.1
        #b[3]*=1.1
        
        b[0]-=b[2] #horizontal movement, b[0] is original x location, and the b[2] is added to the original location, so this keeps on changing
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
                direction=[randint(900,1100),randint(-100,100)] #these are two x location that the new enemy would have, so its going to come either from left or right side
                place=direction[randint(0,1)] # can be either between 900 and 100 or -100 and 100
                badGuys.append([place,randint(0,600),0]) #new enemy list position is appended to enemy list
                
                score+=1 #score added
        for ii in badGuys2: #same thing as above, but this is for boss enemy
            
            if bulletRect.colliderect(ii[0],ii[1],80,80):
                try:
                    bullets.remove(b)
                except:
                    pass
            
                if ii[3]!=48: #ii[3] is health of boss enemy, so if health is remaining, then the health would decrease.
                    ii[3]+=12
                    
                if ii[3]==48: #when health is finished
                    
                    score+=5
                    ii[3]=0
                    badGuys2.remove(ii)
                    
                    direction=[randint(900,1100),randint(-100,100)]
                    place=direction[randint(0,1)]
                    badGuys2.append([place,randint(0,600),0,0])

        
        for d in badBulletList: #checking if bullet collides with the bullet of enemies
            if bulletRect.colliderect([d[0],d[1],10,10]):
                badBulletList.remove(d) #both bullets are removed if they collide with each other
                try:
                    bullets.remove[b]
                except:
                    pass

        if max(b) > 1050 or min(b) < -50: #if goes off screen, bullet is removed
            bullets.remove(b)
    return score


def movingspecialBullets(specialBullets): #same as the function movingbullets, but this is for special 360 degrees bullets
    global score, bosshealth
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
                direction=[randint(900,1100),randint(-100,100)]
                place=direction[randint(0,1)]
                badGuys.append([place,randint(0,600),0,0])
                score+=1

        for ii in badGuys2:
            if specialbulletRect.colliderect(ii[0],ii[1],80,80):
                try:
                    specialBullets.remove(b)
                except:
                    pass

                if ii[3]<=48:
                    ii[3]+=12
                if ii[3]==48:
                    score+=5
                    ii[3]=0
                    badGuys2.remove(ii)
                    
                    direction=[randint(900,1100),randint(-100,100)]
                    place=direction[randint(0,1)]
                    badGuys2.append([place,randint(0,600),0,0])

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

def movingEnemyBullet(badBulletList,crect): #this function is for moving normal enemy bullets

    for b in badBulletList[:]: #bad bullet list is the list of normal enemy bullets, bullets is appended in list in the game running loop
            #b[2]*=1.1
            #b[3]*=1.1
            
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        badBulletRect=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        if badBulletRect.colliderect([px,py,80,80]): #checking if enemy bullet collides with player
            print("Hit")
            
            badBulletList.remove(b) #enemy bullet is removed
            if crect[2]>0: #if player health is remaing
                crect[2]-=0.5 #then decrease the health
            
        if max(b) > 1050 or min(b) < -50:
            badBulletList.remove(b) #removing the enemy bullet if it goes off screen
    
def movingBossBullet(badBulletList2,crect): #same idea as above function, but this is for boss bullets
    for b in badBulletList2[:]:
            #b[2]*=1.1
            #b[3]*=1.1
            
        b[0]-=b[2] #horizontal movement
        b[1]-=b[3] #vertical movement

        badBulletRect2=Rect(b[0]-5,b[1]-5,10,10)# #bullet's rect is 10x10
        if badBulletRect2.colliderect([px,py,80,80]):
            print("Hit")
            
            badBulletList2.remove(b)
            if crect[2]>0:
                crect[2]-=0.5
            
        if max(b) > 1050 or min(b) < -50:
            badBulletList2.remove(b)



def drawScene(screen, badGuys, px, py, goodAng,bullets,badBulletList,badGuys2,badBulletList2):
    ''' 
    '''

    if crect[2]>0: #if player health is remaining
        ########### BLITTING BACKGROUNDS FOR DIFFERENT LEVELS #############
        if level==1: 
            screen.blit(background1,(0,0))
        elif level==2:
            screen.blit(background2,(0,0))
        elif level==3:
            screen.blit(background3,(0,0))
        elif level==4:
            screen.blit(background4,(0,0))
        elif level==5:
            screen.blit(background5,(0,0))
        for guy in badGuys:
            pic = transform.rotate(enemy, guy[2]) #guy[2] is the angle of the enemy with the player, so it is transformed so that it points toward player
            screen.blit(pic, guy[:2]) #guy[0] and guy[1] is the x and y position, so the rotated player is blitted there
        for guy in badGuys2: #same thing as above, but this is for enemy boss
            pic = transform.rotate(enemy2, guy[2])
            screen.blit(pic, guy[:2])
            draw.rect(screen,BLACK,[guy[0],guy[1],50,8],2) #Outline rect of health bar of enemy boss
            draw.rect(screen,GREEN,[guy[0]+2,guy[1],48-guy[3],8]) #health rect of enemy boss, guy[3] was the amount of health it lost, so the health it is decreased over on screen


        for b in bullets: # blitting the player bullets on screen
            draw.circle(screen,GREEN,(int(b[0]),int(b[1])),4)
        for x in badBulletList: #blitting normal enemy bullets
            draw.circle(screen,(255,0,0),(int(x[0]),int(x[1])),4)
        for xx in badBulletList2: #blitting enemy boss bullets
            draw.circle(screen,(255,0,0),(int(xx[0]),int(xx[1])),4)
        for d in specialBullets: #blitting the player 360 bullets
            draw.circle(screen,GREEN,(int(d[0]),int(d[1])),4)
        rotPlayerPic=transform.rotate(player,degrees(goodAng)) # good ang is the rotation of player when pressed d or s, so player is rotated according to that ang
        hw=rotPlayerPic.get_width() #width (imaginary rectangle)
        hh=rotPlayerPic.get_height()#height (imaginary rectangle)
        screen.blit(rotPlayerPic, (px-hw//2,py-hh//2)) #blitting the rotated player on screen
        draw.rect(screen,BLACK,[10,10,150,20],2) #outline health rect of player
        draw.rect(screen,GREEN,crect) #health rect of player
        scoreText=scoreFont.render("Score: "+str(score),True,GREEN) # showing score on screen
        scoreBar=Surface((1000,1000),SRCALPHA)#infoBar is our "sticky note"
        scoreBar.blit(scoreText,(0,0))
        screen.blit(scoreBar,(850,0)) #blitting the score
        levelText=levelFont.render("Level "+str(level),True,GREEN)
        levelBar=Surface((1000,1000),SRCALPHA)#infoBar is our "sticky note"
        levelBar.blit(levelText,(0,0))
        screen.blit(levelBar,(852,25)) #blitting the level
        if sblimit<1: #sblimit is the amount of 360 bullets left in a level, as the player can only do twice in a level
            screen.blit(sbpic,sbrect) #blitting the bomb type pic on screen as that dipicts the 360 bullets. sblimit is 0 at start and increased when the player uses it
                                        #this is why when it is 0, both pics are shown
        if sblimit<2:
            screen.blit(sbpic,sbrect2)
        screen.blit(playpic,playRect) #blittin the play and pause pic to stop and play music
        screen.blit(pausepic,pauseRect)
    
    display.flip()
    myClock.tick(2000)

running = True
while running:


    for evt in event.get():  
        if evt.type == QUIT: 
            running = False
        if evt.type == KEYDOWN: #WHen key is pressed down
            ############## Below is  what happens when arrow keys is pressed ###### 
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
           	############ THis is for rotation #######
            if evt.key == K_s:
                rotateRight = True
                rotateLeft = False
            if evt.key == K_d:
                rotateRight = False
                rotateLeft = True
			
        if evt.type == KEYUP: #when key is released and goes back up, everything becomes false, as we dont want anything to happen when the keys are not pressed by players

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
        px+=speed #move right when moveRight is true from the above section of code, and that only happens when right key is pressed. Speed is how fast player would move
    if moveLeft and px>0:
        px-=speed #same thing as the above if statement
    if moveDown and py<600:
        py+=speed
    if moveUp and py>0:
        py-=speed
    
    if rotateRight:
    	angle+=0.05 #when rotate right is true and that happens when key d is pressed
    if rotateLeft: #when key s is pressed and rotate left becomes true
    	angle-=0.05

    keys = key.get_pressed() #when keys pressed
    mb=mouse.get_pressed()
    mx,my=mouse.get_pos() #getting mouse position
    
    if mb[0]==1: #when left clicked
        if level==0 and playAgainRect.collidepoint(mx,my): #when playagain rect is pressed at the end of game and game is restarted
            score=0 #score goees back to 0 and level goes back to 0
            level=1
            crect[2]=148 #health renewed
            badGuys = [[0,0,0], [200,500,0], [400,0,0], [600, 500,0],[800, 300,0],[1000, 0,0]]    # 6 x,y pairs # bacGuys normal enemy list made again as when player dies it becomes empty
            badGuys2=[[900,500,0,0],[100,100,0,0]] #list of enemy boss
        elif playRect.collidepoint(mx,my): #plays the music if player pauses the music first
            mixer.music.unpause()
            draw.rect(screen,GREEN,playRect,4)
        elif pauseRect.collidepoint(mx,my): #pauses the music when pause button is pressed
            mixer.music.pause()
            draw.rect(screen,GREEN,pauseRect,4)

    if rapid<30: #this is to limit the player shooting, so that player cannot infinitely shoot, and so that there is gap between bullets
        rapid+=1
    if erapid<60: #this is to limit the ememy bullet shooting
        if level==1:

            erapid+=1 #in level one, bullets are shot with a greater interval time, but as level would increase, the erapid would increase faster so that enemy can shoot faster
        elif level==2:
            erapid+=1.5

        elif level==3:
            erapid+=2
        elif level==4:
            erapid+=2.5
        elif level==5:
            erapid+=3
            espeed=2

    if eerapid<60: #this is to limit enemy boss shooting
        if level==1:
            eerapid+=1
        elif level==2:
            eerapid+=1.5
        elif level==3:
            eerapid+=2
        elif level==4:
            eerapid+=2.5
        elif level==5:
            eerapid+=3
    if 25<=score<=29 and crect[2]>0: # level is changed when player still has health (crect) and score is above 25. 
    #                           I did 25 to 29 because to kill enemy boss, we get 5 points, so if i did equal to 25, 
                                #and player shot enemy when he had score of 24, then the level would not have changed. 
        if len(badGuys)<8:
            badGuys.append([100,900,0]) #as level increased, so to add difficulty, more enemies are appended to make it more challenging
            badGuys.append([800,100,0])        
        level=2
        sblimit=0 #as level increases, the allowance of shooting 360 degree bullets is also renewed
    elif 50<=score<=54 and crect[2]>0: #same thing as above, changing level when score comes within a range
        level=3
        sblimit=0
    elif 75<=score<=79 and crect[2]>0:
        level=4
        sblimit=0
    elif 100<=score<=104 and crect[2]>0:
        if len(badGuys2)<4:
            badGuys2.append([100,900,0,0]) #as level increased, so to add difficulty, more enemies are appended to make it more challenging
            badGuys2.append([800,100,0,0])

        level=5
        sblimit=0


    if keys[K_a] and rapid==30 and sblimit<2: #this is for shooting special bullets (360 degree bullets), and sblimit has to be less than 2 because this is only allowed twice per level
        sblimit+=1 #increases when it is shot by player
        rapid = 0 #rapid becomes 0 so that there is time between the next time player shoots
        for i in range(20): # there would be 20 bullets all around the player that would go, and below is the code of their movement
            vx = 5*sin(i) #5 is how fast they will go 
            vy = 5*cos(i)
            lx=px #starting x position same as player
            ly=py #starting y position

        #               0   1  2  3
            specialBullets.append([lx,ly,vx,vy]) 

########## SHOOTING SPECIAL 360 BULLETS ##################
    
####################################################################



    if keys[K_w] and rapid==30: #When w key is pressed
        rapid = 0

        vx = 5*sin(angle) # for x movement. angle is the angle of rotation, so the bullets are moved according to the angle so that the bullets go where player is pointing
        vy = 5*cos(angle) # for y movement.
        lx=px
        ly=py

        #               0   1  2  3
        bullets.append([lx,ly,vx,vy])
        
########################## SHOOTING NORMAL BULLETS ###############################

    

######################################################################

    
    if erapid>60 or erapid==60: #enemy bullets movement
        erapid=0 # so that there is time in between shooting enemy bullets
        for i in badGuys: # for each enemy
            vx = 5*sin(i[2]) # The x and y movement of enemy bullet is sort of randomized, because i[2] is angle of enemy and player, so sometimes it goes to direction of player and sometime it doesnt
            vy = 5*cos(i[2]) 
            lx=i[0] +40 # is the starting position of bullet, same as the location of enemy
            ly=i[1]+40

                #               0   1  2  3
            badBulletList.append([lx,ly,vx,vy])
        
############################## ENEMY BULLETS #############################
    
##########################################################################

############################ BOSS BULLETS ##################################
    if eerapid>60 or eerapid==60: #same as above, but this is for boss enemy
        eerapid=0
        for i in badGuys2:
            vx = 5*sin(135+i[2]) 
            vy = 5*cos(135+i[2])
            lx=i[0] +40
            ly=i[1]+40

                #               0   1  2  3
            badBulletList2.append([lx,ly,vx,vy])
        
    
    
    ######## FUNCTION INPUTS ###########
    moveBadGuys(badGuys, px, py)
    moveBadGuys2(badGuys2, px, py)
    #badbullet(badGuys,px,py,screen)
    checkHits(badGuys, px, py)
    checkHits2(badGuys2, px, py)
    movingspecialBullets(specialBullets)
    movingBullets(bullets)
    movingEnemyBullet(badBulletList,crect)
    movingBossBullet(badBulletList2,crect)
    drawScene(screen, badGuys, px, py, angle,bullets,badBulletList,badGuys2,badBulletList2)
    
    
    if crect[2]==0: # when health of player is finished
        level=0
        print("DONE")
    if level==0: # when game is finished
        sblimit=0
        badGuys=[] #enemies list is emptied, so that enemies are removed from screen
        badGuys2=[]
        screen.fill(BLACK)
        print(score)
        endText=endFont.render("You DIED!!!. Your Score: "+str(score),True,WHITE) # score is shown on screen
        endBar=Surface((1000,200),SRCALPHA)#infoBar is our "sticky note"
        endBar.blit(endText,(0,0))
        screen.blit(endBar,(250,300))
        screen.blit(playAgain,playAgainRect) # play again pic is blitted
        

    
quit() 
