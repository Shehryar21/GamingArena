from pygame import *

##########################################################image load
pacmanMenu=image.load("images/pacmanMenu.png")
marioMenu=image.load("images/marioMenu.png")
spaceMenu=image.load("images/spaceMenu.jpg")
spaceRule=image.load("images/spaceRule.png")
pacmanRule=image.load("images/pacmanRule.png")
marioRule=image.load("images/marioRule.png")
background=image.load("images/wallpaper.jpg")
border=image.load("images/border.png")
spaceMenuTransformed=transform.scale(spaceMenu,(250,450))
pacmanMenuTransformed=transform.scale(pacmanMenu,(250,450))
marioMenuTransformed=transform.scale(marioMenu,(250,450))
pacmanRuleTransformed=transform.scale(pacmanRule,(250,450))
marioRuleTransformed=transform.scale(marioRule,(250,450))
spaceRuleTransformed=transform.scale(spaceRule,(250,450))
backgroundTransformed=transform.scale(background,(1000,600))
borderTransformed=transform.scale(border,(250,450))
#################################################################
click=False
screen=display.set_mode((1000,600))
running=True
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONDOWN:
            click=True
        if evt.type==MOUSEBUTTONUP:
            click=False
    mx,my=mouse.get_pos()
########################################################colide
    pacmanRect=Rect(675,75,250,450)
    spaceRect=Rect(375,75,250,450)
    marioRect=Rect(75,75,250,450)
    screen.blit(backgroundTransformed,(0,0))
    screen.blit(pacmanMenuTransformed,pacmanRect)
    screen.blit(marioMenuTransformed,marioRect)
    screen.blit(spaceMenuTransformed,spaceRect)
########################################################hover
    if pacmanRect.collidepoint(mx,my):
        screen.blit(pacmanRuleTransformed,pacmanRect)
    if spaceRect.collidepoint(mx,my):
        screen.blit(spaceRuleTransformed,spaceRect)
    if marioRect.collidepoint(mx,my):
        screen.blit(marioRuleTransformed,marioRect)
########################################################press
    if pacmanRect.collidepoint(mx,my) and click==True:
        import pacman
    if spaceRect.collidepoint(mx,my) and click==True:
        import space
    if marioRect.collidepoint(mx,my) and click==True:
        import mario
    screen.blit(borderTransformed,pacmanRect)
    screen.blit(borderTransformed,spaceRect)
    screen.blit(borderTransformed,marioRect)
    display.flip()
quit()
