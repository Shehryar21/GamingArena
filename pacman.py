from pygame import *
from random import *
import math
#######################################################################VARiABLES
init()
steps=1
level = 1
size=(560,660)
screen=display.set_mode(size)
#######################################################################iMAGES
pacman=image.load("images/pacman.png")
background=image.load("images/background.jpg")
pacmanLives=transform.scale(pacman,(25,25))
background=transform.scale(background,(560,284))
score=0
menuRect=Rect(0,0,50,50)
display.set_caption("Pacman - NingTai")
#######################################################################SOUND EFFECTS
mixer.pre_init(44100,16,2,4096)
mixer.init()
eatScore=mixer.music.load("soundEffect/eat.mp3")
mixer.music.set_volume(0.5)
#######################################################################FUNCTiONS
def initialize_vars(mapFile):
    global screen,mazeList,direction,pacX,pacY,running,myClock,moves,moveCount,keyBuffer,keyBufferValid,mouseDown,enemyX,enemyY,enemyDirection,live,enemyStopTime
    screen.fill((0,0,0))
    mazeFile=open(mapFile,"r")
    mazeLines=mazeFile.readlines()
    mazeList=[]
    count=0
    live=3
    direction="NONE"
    pacX,pacY=270,470
    running=True
    myClock=time.Clock()
    enemyStopTime=time.get_ticks()-4000
    moves=["NONE"]
    moveCount=0
    keyBuffer=None
    keyBufferValid=0
    mouseDown=False
    enemyY=[330,330,290,290,330,330,290,290]
    enemyX=[250,310,250,310,250,310,250,310]
    enemyDirection=["LEFT","RIGHT","LEFT","RIGHT","LEFT","RIGHT","LEFT","RIGHT"]    
    for aLine in mazeLines:
        mazeList.append([])
        for aChar in aLine.strip():
            mazeList[count].append(aChar)
        count=count+1
#Check for collision with special one direction wall
#To prevent pacman/enemy enter the enemy vault once they are out
#This returns True if collision with special wall and false if not
def collideWithOneWayWall(xPos,yPos,direction):
    if xPos in range(191,193) and yPos == 310 and direction == "RIGHT":
        return True
    elif xPos in range(368,370) and yPos == 310 and direction == "LEFT":
        return True
    else:
        return False
# Check if for given x and y position, there is a collision
# Returns true or false
def collideWithWall(xPos,yPos,direction,radius=9.5,pacMan=True):
    global mazeList,score,eatScore,enemyStopTime
    if collideWithOneWayWall(xPos,yPos,direction):
        return True
    #make a list of 4 corner coords and 4 mid-length coords 
    coords=[[math.ceil((xPos-radius)/20),math.ceil((yPos-radius)/20)],
            [math.ceil((xPos+radius)/20),math.ceil((yPos-radius)/20)],
            [math.ceil((xPos-radius)/20),math.ceil((yPos+radius)/20)],
            [math.ceil((xPos+radius)/20),math.ceil((yPos+radius)/20)]]
        #eating score
    for coordinate in coords:
        if pacMan and mazeList[coordinate[1]-1][coordinate[0]-1]=="2":
            mazeList[coordinate[1]-1][coordinate[0]-1]="0"
            score+=10
            mixer.music.play(1)
        if pacMan and mazeList[coordinate[1]-1][coordinate[0]-1]=="3":
            mazeList[coordinate[1]-1][coordinate[0]-1]="0"
            score+=50
            mixer.music.play(1)
            enemyStopTime=time.get_ticks()
        if mazeList[coordinate[1]-1][coordinate[0]-1]=="1":
            return True
    return False
def reDrawCharacters():
    global pacX,pacY,enemyX,enemy,pics,frame
    draw.circle(screen,(255,255,0),(pacX,pacY),10,0)
    for i in range(len(enemyX)):
        draw.circle(screen,(255,0,0),(enemyX[i],enemyY[i]),10,0)
def moveEnemy(radius=9.5):
    global enemyX,enemyY,enemyDirection,enemyStopTime
    elapsedSeconds=time.get_ticks()-enemyStopTime
    if(elapsedSeconds>4000):
        steps=1
        for i in range(len(enemyX)):
            validDirections=[]
            if enemyDirection[i]=="LEFT":
                if collideWithWall(enemyX[i]-steps,enemyY[i],"LEFT",radius,False):
                    validDirections.append("RIGHT")
                else:
                    validDirections.append("LEFT")
                validDirections.append("UP")
                validDirections.append("DOWN")
            if enemyDirection[i]=="RIGHT":
                if collideWithWall(enemyX[i]+steps,enemyY[i],"RIGHT",radius,False):
                    validDirections.append("LEFT")
                else:
                    validDirections.append("RIGHT")
                validDirections.append("UP")
                validDirections.append("DOWN")
            if enemyDirection[i]=="UP":
                if collideWithWall(enemyX[i],enemyY[i]-steps,"UP",radius,False):
                    validDirections.append("DOWN")
                else:
                    validDirections.append("UP")
                validDirections.append("LEFT")
                validDirections.append("RIGHT")
            if enemyDirection[i]=="DOWN":
                if collideWithWall(enemyX[i],enemyY[i]+steps,"DOWN",radius,False):
                    validDirections.append("UP")
                else:
                    validDirections.append("DOWN")
                validDirections.append("LEFT")
                validDirections.append("RIGHT")
            realValidList=[]
            for j in range(len(validDirections)):
                if validDirections[j]=="LEFT":
                    if not collideWithWall(enemyX[i]-steps,enemyY[i],"LEFT",radius,False):
                        realValidList.append("LEFT")
                if validDirections[j]=="RIGHT":
                    if not collideWithWall(enemyX[i]+steps,enemyY[i],"RIGHT",radius,False):
                        realValidList.append("RIGHT")
                if validDirections[j]=="UP":
                    if not collideWithWall(enemyX[i],enemyY[i]-steps,"UP",radius,False):
                        realValidList.append("UP")
                if validDirections[j]=="DOWN":
                    if not collideWithWall(enemyX[i],enemyY[i]+steps,"DOWN",radius,False):
                        realValidList.append("DOWN")   
            index=randint(0,len(realValidList)-1)
            enemyDirection[i] =  realValidList[index]
            if enemyDirection[i]=="LEFT":
                enemyX[i]-=1
            if enemyDirection[i]=="RIGHT":
                enemyX[i]+=1
            if enemyDirection[i]=="UP":
                enemyY[i]-=1
            if enemyDirection[i]=="DOWN":
                enemyY[i]+=1
def collideWithEnemy():
    global enemyX,enemyY,enemyDirection,live,pacX,pacY,direction
    for i in range(len(enemyX)):
        if abs(enemyX[i]-pacX)<=10 and abs(enemyY[i]-pacY)<=10:
            pacX,pacY=270,470
            live=live-1
            direction="NONE"
            enemyY=[330,330,290,290,330,330,290,290]
            enemyX=[250,310,250,310,250,310,250,310]
            enemyDirection=["LEFT","RIGHT","LEFT","RIGHT","LEFT","RIGHT","LEFT","RIGHT"]
        if live<=0:
            pacX,pacY=0,0
def drawMap():
    global mazeList
    colCount=0
    for row in mazeList:
        rowCount=0
        for element in row:
            #draw wall
            if element=='0':
                draw.rect(screen,(0,0,0),Rect(rowCount*20,colCount*20,20,20),0)
            elif element=='1':
                draw.rect(screen,(0,0,255),Rect(rowCount*20,colCount*20,20,20),0)
            #draw score
            elif element=='2':
                draw.rect(screen,(0,0,0),Rect(rowCount*20,colCount*20,20,20),0)
                draw.circle(screen,(255,255,255),(rowCount*20+10,colCount*20+10),3,0)
            #draw boosters
            elif element=='3':
                draw.rect(screen,(0,0,0),Rect(rowCount*20,colCount*20,20,20),0)
                draw.circle(screen,(255,255,255),(rowCount*20+10,colCount*20+10),7,0)
            elif element=='4':
                draw.rect(screen,(255,255,255),Rect(rowCount*20,colCount*20,20,20),0)
            rowCount+=1
        colCount+=1
def tunnelTeleportation():
    global pacX,enemyX,pacY,direction
    if pacX>=550:
        pacX=11
    if pacX<=10:
        pacX=549
    for i in range(8):
        if enemyX[i]>=550:
            enemyX[i]=11
        if enemyX[i]<=10:
            enemyX[i]=549
initialize_vars("maze1.txt")
#######################################################################WHiLE LOOP STARTS HERE
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        elif evt.type==KEYDOWN:
            keyBufferValid=30
            if evt.key==K_LEFT:
                direction="LEFT"
                keyBuffer="LEFT"
            elif evt.key==K_RIGHT:
                direction="RIGHT"
                keyBuffer="RIGHT"
            elif evt.key==K_UP:
                direction="UP"
                keyBuffer="UP"
            elif evt.key==K_DOWN:
                direction="DOWN"
                keyBuffer="DOWN"
    newX,newY=pacX,pacY
    if evt.type==MOUSEBUTTONDOWN:
        mouseDown=True
    if evt.type==MOUSEBUTTONUP:
        mouseDown=False
    mx,my=mouse.get_pos()
#######################################################################DRAW MAP
    drawMap()
#######################################################################ENEMY DiRECTiON
    if direction=="LEFT" or (keyBuffer == "LEFT" and keyBufferValid > 0):
        pacX=pacX-steps
        if(collideWithWall(pacX,pacY,"LEFT")):
            pacX=pacX+steps
            direction=moves[moveCount]
            keyBufferValid -=1
        else:
            moves.append("LEFT")
            moveCount+=1
            if direction == keyBuffer:
                keyBufferValid = 0
                direction="LEFT"
    if direction=="RIGHT" or (keyBuffer == "RIGHT" and keyBufferValid > 0):
        pacX=pacX+steps
        if(collideWithWall(pacX,pacY,"RIGHT")):
            pacX=pacX-steps
            direction=moves[moveCount]
            keyBufferValid -=1
        else:
            moves.append("RIGHT")
            moveCount+=1
            if direction == keyBuffer:
                keyBufferValid = 0
                direction="RIGHT"
    if direction=="UP" or (keyBuffer == "UP" and keyBufferValid > 0):
        pacY=pacY-steps
        if(collideWithWall(pacX,pacY,"UP")):
            pacY=pacY+steps
            direction=moves[moveCount]
            keyBufferValid -=1
        else:
            moves.append("UP")
            moveCount+=1
            if direction == keyBuffer: 
                keyBufferValid = 0
                direction="UP"
    if direction=="DOWN" or (keyBuffer == "DOWN" and keyBufferValid > 0):
        pacY=pacY+steps  
        if(collideWithWall(pacX,pacY,"DOWN")):
            pacY=pacY-steps
            direction=moves[moveCount]
            keyBufferValid -=1
        else:
            moves.append("DOWN")
            moveCount+=1
            if direction == keyBuffer:
                keyBufferValid = 0
                direction="DOWN"
#######################################################################FUNCTION LOAD
    moveEnemy()
    reDrawCharacters()
    tunnelTeleportation()
    collideWithEnemy()
#######################################################################TEXT
    completeText=font.SysFont("Comic Sans MS",15)
    comicFont=font.SysFont("Comic Sans MS",25)
    scoreText=comicFont.render("SCORE",True,(255,255,255))
    scoreNumber=comicFont.render(str(score),True,(255,255,0))
    liveText=comicFont.render("LiVES",True,(255,255,255))
    complete=completeText.render("LEVEL "+str(level)+" COMPLETE!",True,(255,255,0))
    over=completeText.render("GAME OVER",True,(255,255,0))
    overScore=completeText.render("SCORE:",True,(255,255,255))
    overScoreNum=completeText.render(str(score),True,(255,255,0))
    overRestart=completeText.render("> RESTART",True,(255,255,0))
    overQuit=completeText.render("> QUIT",True,(255,255,0))
    nextLevel=completeText.render("> NEXT LEVEL",True,(255,255,0))
    gameCompleted=completeText.render("CONGRATULATIONS, YOU COMPLETED THE GAME!", True,(255,255,0))
    returnMenu=completeText.render("> MENU",True,(255,255,0))
    start=completeText.render("READY!",True,(255,255,0))
    levelText=comicFont.render("LEVEL:",True,(255,255,255))
    levelNumber=comicFont.render(str(level)+"/3",True,(255,255,0))
    ###
    screen.blit(liveText,(350,620))
    screen.blit(scoreNumber,(110,620))
    screen.blit(scoreText,(20,620))
    screen.blit(pacmanLives,(430,626))
    screen.blit(pacmanLives,(460,626))
    screen.blit(levelText,(20,15))
    screen.blit(levelNumber,(120,15))
#######################################################################SCORE/LEVEL COMPLETION
    if score<=20:
        screen.blit(start,(255,360))
    if score%2500==0 and score!=0 and live>0:
        pacX,pacY=0,0
        draw.rect(screen,(0,0,0),Rect(0,0,560,660),0)
        screen.blit(background,(0,100))
        draw.rect(screen,(130,130,130),Rect(230,440,100,23),0)
        draw.rect(screen,(130,130,130),Rect(230,480,100,23),0)
        draw.rect(screen,(130,130,130),Rect(230,400,100,23),0)
        draw.rect(screen,(100,100,100),Rect(225,395,109,32),2)
        draw.rect(screen,(100,100,100),Rect(225,435,109,32),2)
        draw.rect(screen,(100,100,100),Rect(225,475,109,32),2)
        screen.blit(complete,(215,360))
        screen.blit(nextLevel,(230,400))
        screen.blit(overRestart,(239,440))
        screen.blit(overQuit,(249,480))
        nextRect=Rect(235,400,90,20)
        restartRect=Rect(245,440,70,20)
        quitRect=Rect(255,480,48,20)
        if level==3:
            draw.rect(screen,(0,0,0),Rect(215,360,200,20),0)
            screen.blit(gameCompleted,(100,360))
            draw.rect(screen,(130,130,130),Rect(230,400,100,23),0)
            screen.blit(returnMenu,(250,400))
            if nextRect.collidepoint(mx,my) and mouseDown==True:
                import menu
                break
        if nextRect.collidepoint(mx,my) and mouseDown==True:
            score=0
            if level==1:
                level=2
                initialize_vars("maze2.txt")
            elif level==2:
                level=3
                initialize_vars("maze3.txt")
            elif level==3:
                level=1
                initialize_vars("maze1.txt")
            draw.rect(screen,(255,255,0),Rect(230,440,100,23),2)
        if restartRect.collidepoint(mx,my) and mouseDown==True:
            score=0
            level=1 
            initialize_vars("maze1.txt")
        if quitRect.collidepoint(mx,my) and mouseDown==True:
            import menu
            break
        if nextRect.collidepoint(mx,my):
            draw.rect(screen,(255,255,0),Rect(230,400,100,23),2)
        if restartRect.collidepoint(mx,my):
            draw.rect(screen,(255,255,0),Rect(230,440,100,23),2)
        if quitRect.collidepoint(mx,my):
            draw.rect(screen,(255,255,0),Rect(230,480,100,23),2)
#######################################################################LiVES
    if live==2:
        draw.rect(screen,(0,0,0),Rect(460,626,25,25),0)
    if live==1:
        draw.rect(screen,(0,0,0),Rect(430,626,25,25),0)
        draw.rect(screen,(0,0,0),Rect(460,626,25,25),0)
    if live<=0:
        draw.rect(screen,(0,0,0),Rect(430,626,25,25),0)
        draw.rect(screen,(0,0,0),Rect(460,626,25,25),0)
        draw.rect(screen,(0,0,0),Rect(0,0,560,660),0)
        draw.rect(screen,(130,130,130),Rect(230,440,100,23),0)
        draw.rect(screen,(130,130,130),Rect(230,480,100,23),0)
        draw.rect(screen,(100,100,100),Rect(225,435,109,32),2)
        draw.rect(screen,(100,100,100),Rect(225,475,109,32),2)
        screen.blit(over,(235,360))
        screen.blit(overScore,(235,400))
        screen.blit(overScoreNum,(295,400))
        screen.blit(overRestart,(239,440))
        screen.blit(overQuit,(249,480))
        restartRect=Rect(245,440,70,20)
        quitRect=Rect(255,480,48,20)
        if restartRect.collidepoint(mx,my) and mouseDown==True:
            score=0
            initialize_vars("maze1.txt")
        if quitRect.collidepoint(mx,my) and mouseDown==True:
            import menu
            break
        if restartRect.collidepoint(mx,my):
            draw.rect(screen,(255,255,0),Rect(230,440,100,23),2)
        if quitRect.collidepoint(mx,my):
            draw.rect(screen,(255,255,0),Rect(230,480,100,23),2)
#######################################################################END
    display.flip()
    myClock.tick(120)
import menu
quit()
