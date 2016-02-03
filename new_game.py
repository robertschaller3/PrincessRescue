#Save The Princess
#By Robert Schaller

import random
import time
import sys
import os
import pygame

from pygame.locals import *

#Initalizations
WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 600 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
CURRENTROOM = 0;
PLAYER_ITEMS = list();

#Colors
BLACK =(0,0,0)
WHITE =(255,255,255)
RED =(255,0,0)
GREEN =(0,255,0)
BLUE =(0,0,255)

#Enemy stats as a dictionary
ENEMY_LIST = {
    'guard':{'health':100,'damage':15,'armour':0},
    'skeleton':{'health':50,'damage':10,'armour':40},
    'dragon':{'health':300,'damage':30,'armour':100}
    }

#layout of rooms
ROOMS = {
    0:{"name":"Courtyard",
       "north":1},
    1:{"name":"Great Hall",
       "south":0,
       "down":2,
       "west":3,
       "east":4},
    2:{"name":"Dungeon",
       "up":1},
    3:{"name":"West Hall",
       "east":1,
       "up":6},
    4:{"name":"East Hall",
       "west":1,
       "north":5},
    5:{"name":"Treasury",
       "south":4},
    6:{"name":"Tower Lvl 1",
       "down":3,
       "up":7},
    7:{"name":"Tower Lvl 2",
       "down":6},
    }

#Text prompt for each room
courtyard_text = ['You see a large imposing castle. ',
                  'The gate is left ominously open. ' ]
great_hall_text = ['You are in what appears to be a great hall. ',
                  'A throne sized for a giant fills the room. ' ]
east_hall_text = ['You see a dank and dirty hallway. '
                  ]
west_hall_text = ['You see a dusty old hallway. Footsteps',
                  'in the dust lead to an old ladder.' ]
dungeon_text = ['The dungeon is smelly and wet. ',
                'You hear a sweet voice call out ',
                '"Ser Robert! Save Me!"']
treasury_text = ['Amid the piles of silver and gold',
                 ' you see a sturdy old chest. ']
tower_one_text = ['You see ladders leading higher and lower. '
                  ]
tower_two_text = ['The is a golden chest on a pedastal. '
                  ]

#Amount of interactable objects
courtyard_items = [1]
great_hall_items = [1, 1]
east_hall_items = []
west_hall_items = [1]
dungeon_items = [1]
treasury_items = [1]
tower_one_items = [1]
tower_two_items = [1]

#List that combinds room items & text
courtyard_info = [courtyard_text, courtyard_items]
great_hall_info = [great_hall_text, great_hall_items]
east_hall_info = [east_hall_text, east_hall_items]
west_hall_info = [west_hall_text, west_hall_items]
dungeon_info = [dungeon_text, dungeon_items]
treasury_info = [treasury_text, treasury_items]
tower_one_info = [tower_one_text, tower_one_items]
tower_two_info = [tower_two_text, tower_two_items]

#list that combinds all rooms
ROOMS_INFO =[courtyard_info, great_hall_info, dungeon_info, west_hall_info,
             east_hall_info, treasury_info, tower_one_info, tower_two_info]

#dot position
DOTPOS =[200,200]

#plays background music
def backGroundMusic():
    pygame.mixer.music.load('music/come_and_find_me.mp3')
    pygame.mixer.music.play(-1, 0.0)

#draws interactable items
def objectDraw(item, x, y):
    opening_rect = IMAGESDICT[item].get_rect()
    top_cord = y
    opening_rect.top = top_cord
    opening_rect.centerx = x
    top_cord += opening_rect.height
    DISPLAYSURF.blit(IMAGESDICT[item], opening_rect)

#draws room backdrop
def roomDraw(room, info):
    opening_rect = IMAGESDICT[room].get_rect()
    top_cord = 50
    opening_rect.top = top_cord
    opening_rect.centerx = HALF_WINWIDTH
    top_cord += opening_rect.height
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(IMAGESDICT[room], opening_rect)

#draws text descriptions
def textDraw(text_list):
    opening_rect = IMAGESDICT['courtyard_back'].get_rect()
    top_cord = 50
    opening_rect.top = top_cord
    opening_rect.centerx = HALF_WINWIDTH
    top_cord += opening_rect.height
    FONT = pygame.font.Font('freesansbold.ttf', 18);
    for i in range(len(text_list)):
        instSurf = FONT.render(text_list[i], 1, BLACK)
        instRect = instSurf.get_rect()
        top_cord += 10 # 10 pixels will go in between each line of text.
        instRect.top = top_cord
        instRect.centerx = HALF_WINWIDTH -150
        top_cord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

#draws player item list
def itemDraw():
    opening_rect = IMAGESDICT['item_box'].get_rect()
    top_cord = 467
    opening_rect.top = top_cord
    opening_rect.centerx = 650
    DISPLAYSURF.blit(IMAGESDICT['item_box'], opening_rect)
    #Text Info
    FONT = pygame.font.Font('freesansbold.ttf', 14);
    for i in range(len(PLAYER_ITEMS)):
        instSurf = FONT.render(PLAYER_ITEMS[i], 1, BLACK)
        instRect = instSurf.get_rect()
        top_cord += 5 # 10 pixels will go in between each line of text.
        instRect.top = top_cord+28
        instRect.centerx = opening_rect.centerx
        top_cord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

#main function that asseses room interaction
#one loop for each room
def runRoom(mousex, mousey):
    global CURRENTROOM, ROOMS_INFO, PLAYER_ITEMS
    result = "not_done"
    
    if ROOMS[CURRENTROOM]["name"] == "Courtyard":
        if 'princess' not in PLAYER_ITEMS:
            roomDraw('courtyard_back',ROOMS_INFO[0][0])
            textDraw(ROOMS_INFO[0][0])
        if 'princess' in PLAYER_ITEMS:
            if ROOMS_INFO[0][0].count('You must defeat me to escape! ')==0:
                ROOMS_INFO[0][0].pop(0)
                ROOMS_INFO[0][0].pop(0)
                ROOMS_INFO[0][0].insert(0,'You must defeat me to escape! ')
            roomDraw('final_boss_back',ROOMS_INFO[0][0])
            objectDraw('dragon', 400, 200)
            textDraw(ROOMS_INFO[0][0])
            ROOMS_INFO[0][1][0] = 0
        for event in pygame.event.get(): # event handling loop
            if ROOMS_INFO[0][1][0] == 0 and event.type == MOUSEBUTTONUP and mousex >=360 and mousex <=445 and mousey >= 205 and mousey <= 330:
               ROOMS_INFO[0][1][0] = runBattle('dragon', 'final_boss_back', ROOMS_INFO[0][0], mousex, mousey)
            if event.type == MOUSEBUTTONUP and mousex >=375 and mousex <=420 and mousey >= 335 and mousey <= 390 and ROOMS_INFO[0][1][0] == 1:
                CURRENTROOM = 1
            if ROOMS_INFO[0][1][0] == 2:
                result = 'victory'
        return result
    
    if ROOMS[CURRENTROOM]["name"] == "Great Hall":
        roomDraw('great_hall_back',ROOMS_INFO[1][0])
        textDraw(ROOMS_INFO[1][0])
        for event in pygame.event.get(): # event handling loop
            if 'princess' in PLAYER_ITEMS and 'dragon punching gloves' not in PLAYER_ITEMS and ROOMS_INFO[1][1][1] == 1 :
                ROOMS_INFO[1][1][1] = 0
                ROOMS_INFO[1][0].insert(0,'I see something under the throne!" ')
                ROOMS_INFO[1][0].insert(0,'Princess Terra states "I think ')
            if event.type == MOUSEBUTTONUP and mousex >=285 and mousex <=490 and mousey >= 120 and mousey <= 300 and 'princess' in PLAYER_ITEMS:
                ROOMS_INFO[1][1][0] = 0
                if 'dragon punching gloves' not in PLAYER_ITEMS:
                    PLAYER_ITEMS.append('dragon punching gloves')
            if 'dragon punching gloves' in PLAYER_ITEMS:
                if ROOMS_INFO[1][0].count('I see something under the throne!" ')!=0:
                    ROOMS_INFO[1][0].remove('I see something under the throne!" ')
                if ROOMS_INFO[1][0].count('Princess Terra states "I think ')!=0:
                    ROOMS_INFO[1][0].remove('Princess Terra states "I think ')
            if event.type == MOUSEBUTTONUP and mousex >=395 and mousex <=470 and mousey >= 410 and mousey <= 465:
                CURRENTROOM = 0
                if ROOMS_INFO[1][0].count('You need a crowbar to open that. ')!=0:
                    ROOMS_INFO[1][0].remove('You need a crowbar to open that. ')
            if event.type == MOUSEBUTTONUP and mousex >=595 and mousex <=660 and mousey >= 130 and mousey <= 175:
                if 'crowbar' in PLAYER_ITEMS:
                    CURRENTROOM = 2
                    if ROOMS_INFO[1][0].count('You need a crowbar to open that. ')!=0:
                        ROOMS_INFO[1][0].remove('You need a crowbar to open that. ')
                else:
                    if ROOMS_INFO[1][0].count('You need a crowbar to open that. ')==0:
                        ROOMS_INFO[1][0].insert(0,'You need a crowbar to open that. ')
                        textDraw(ROOMS_INFO[1][0])                    
            if event.type == MOUSEBUTTONUP and mousex >=25 and mousex <=100 and mousey >= 225 and mousey <= 335:
                CURRENTROOM = 3
                if ROOMS_INFO[1][0].count('You need a crowbar to open that. ')!=0:
                    ROOMS_INFO[1][0].remove('You need a crowbar to open that. ')
            if event.type == MOUSEBUTTONUP and mousex >=700 and mousex <=775 and mousey >= 225 and mousey <= 335:
                CURRENTROOM = 4
                if ROOMS_INFO[1][0].count('You need a crowbar to open that. ')!=0:
                    ROOMS_INFO[1][0].remove('You need a crowbar to open that. ')
        return result
    
    if ROOMS[CURRENTROOM]["name"] == "Dungeon":
        roomDraw('dungeon_back',ROOMS_INFO[2][0])
        textDraw(ROOMS_INFO[2][0])
        if ROOMS_INFO[2][1][0] == 1:
            objectDraw('cage', 273, 155)
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and mousex >=240 and mousex <=305 and mousey >= 160 and mousey <= 255:
                ROOMS_INFO[2][1][0] = 0
                if 'princess' not in PLAYER_ITEMS:
                    PLAYER_ITEMS.append('princess')
                if ROOMS_INFO[2][0].count('You hear a sweet voice call out ')!=0:
                    ROOMS_INFO[2][0].remove('You hear a sweet voice call out ')
                if ROOMS_INFO[2][0].count('"Ser Robert! Save Me!"')!=0:
                    ROOMS_INFO[2][0].remove('"Ser Robert! Save Me!"')
            if event.type == MOUSEBUTTONUP and mousex >=95 and mousex <=140 and mousey >= 50 and mousey <= 430:
                CURRENTROOM = 1
        return result
    
    if ROOMS[CURRENTROOM]["name"] == "West Hall":
        roomDraw('west_hall_back',ROOMS_INFO[3][0])
        textDraw(ROOMS_INFO[3][0])
        if ROOMS_INFO[3][1][0] == 1:
            objectDraw('guard', 400, 200)
        for event in pygame.event.get(): # event handling loop
            if ROOMS_INFO[3][1][0] == 1 and event.type == MOUSEBUTTONUP and mousex >=360 and mousex <=445 and mousey >= 205 and mousey <= 330:
               ROOMS_INFO[3][1][0] = runBattle('guard', 'west_hall_back', ROOMS_INFO[3][0], mousex, mousey)
            if event.type == MOUSEBUTTONUP and mousex >=700 and mousex <=775 and mousey >= 225 and mousey <= 335:
                CURRENTROOM = 1
                if ROOMS_INFO[3][0].count('The guard is blocking your way. ')!=0:
                    ROOMS_INFO[3][0].remove('The guard is blocking your way. ')
            if event.type == MOUSEBUTTONUP and mousex >=160 and mousex <=210 and mousey >= 50 and mousey <= 320:
                if ROOMS_INFO[3][1][0] == 1:
                    if ROOMS_INFO[3][0].count('The guard is blocking your way. ')==0:
                        ROOMS_INFO[3][0].insert(0,'The guard is blocking your way. ')
                else:
                    CURRENTROOM = 6
                    if ROOMS_INFO[3][0].count('The guard is blocking your way. ')!=0:
                        ROOMS_INFO[3][0].remove('The guard is blocking your way. ')
        return result
    
    if ROOMS[CURRENTROOM]["name"] == "East Hall":
        roomDraw('east_hall_back',ROOMS_INFO[4][0])
        textDraw(ROOMS_INFO[4][0])
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and mousex >=25 and mousex <=100 and mousey >= 225 and mousey <= 335:
                CURRENTROOM = 1
                if ROOMS_INFO[4][0].count('You need a key to open that. ')!=0:
                        ROOMS_INFO[4][0].remove('You need a key to open that. ')
            if event.type == MOUSEBUTTONUP and mousex >=395 and mousex <=470 and mousey >= 50 and mousey <= 115:
                if 'key' in PLAYER_ITEMS:
                    CURRENTROOM = 5
                    if ROOMS_INFO[4][0].count('You need a key to open that. ')!=0:
                        ROOMS_INFO[4][0].remove('You need a key to open that. ')
                else:
                    if ROOMS_INFO[4][0].count('You need a key to open that. ')==0:
                        ROOMS_INFO[4][0].insert(0,'You need a key to open that. ')
                    textDraw(ROOMS_INFO[4][0])                    
        return result
    
    if ROOMS[CURRENTROOM]["name"] == "Treasury":
        roomDraw('treasury_back',ROOMS_INFO[5][0])
        textDraw(ROOMS_INFO[5][0])
        if ROOMS_INFO[5][1][0] == 1:
            objectDraw('item_chest', 400, 200)
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and mousex >=360 and mousex <=440 and mousey >= 200 and mousey <= 280:
                ROOMS_INFO[5][1][0] = 0
                if 'crowbar' not in PLAYER_ITEMS:
                    PLAYER_ITEMS.append('crowbar')
            if event.type == MOUSEBUTTONUP and mousex >=395 and mousex <=470 and mousey >= 400 and mousey <= 465:
                CURRENTROOM = 4
        return result

    if ROOMS[CURRENTROOM]["name"] == "Tower Lvl 1":
        roomDraw('tower_one_back',ROOMS_INFO[6][0])
        textDraw(ROOMS_INFO[6][0])
        if ROOMS_INFO[6][1][0] == 1:
            objectDraw('skeleton', 400, 200)
        for event in pygame.event.get(): # event handling loop
            if ROOMS_INFO[6][1][0] == 1 and event.type == MOUSEBUTTONUP and mousex >=360 and mousex <=445 and mousey >= 205 and mousey <= 330:
               ROOMS_INFO[6][1][0] = runBattle('skeleton', 'tower_one_back', ROOMS_INFO[6][0], mousex, mousey)
            if event.type == MOUSEBUTTONUP and mousex >=160 and mousex <=210 and mousey >= 230 and mousey <= 370:
                CURRENTROOM = 3
                if ROOMS_INFO[6][0].count('The skeleton is blocking your way. ')!=0:
                    ROOMS_INFO[6][0].remove('The skeleton is blocking your way. ')
            if event.type == MOUSEBUTTONUP and mousex >=580 and mousex <=630 and mousey >= 50 and mousey <= 280:
                if ROOMS_INFO[6][1][0] == 1:
                    if ROOMS_INFO[6][0].count('The skeleton is blocking your way. ')==0:
                        ROOMS_INFO[6][0].insert(0,'The skeleton is blocking your way. ')
                else:
                    CURRENTROOM = 7
                    if ROOMS_INFO[6][0].count('The skeleton is blocking your way. ')!=0:
                        ROOMS_INFO[6][0].remove('The skeleton is blocking your way. ')
        return result

    if ROOMS[CURRENTROOM]["name"] == "Tower Lvl 2":
        roomDraw('tower_two_back',ROOMS_INFO[7][0])
        textDraw(ROOMS_INFO[7][0])
        if ROOMS_INFO[7][1][0] == 1:
            objectDraw('item_chest', 400, 200)
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP and mousex >=360 and mousex <=440 and mousey >= 200 and mousey <= 280:
                ROOMS_INFO[7][1][0] = 0
                if 'key' not in PLAYER_ITEMS:
                    PLAYER_ITEMS.append('key')
            if event.type == MOUSEBUTTONUP and mousex >=590 and mousex <=640 and mousey >= 230 and mousey <= 370:
                CURRENTROOM = 6
        return result

def runTest(mousex, mousey):
    global CURRENTROOM, ROOMS_INFO, PLAYER_ITEMS, DOTPOS
    result = "not_done"
    
    if ROOMS[CURRENTROOM]["name"] == "Courtyard":
        roomDraw('great_hall_back',ROOMS_INFO[1][0])
        textDraw(ROOMS_INFO[1][0])
        objectDraw('dot', DOTPOS[0], DOTPOS[1])
    for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP and event.key == K_RIGHT:
                DOTPOS[0] = DOTPOS[0]+1
            if event.type == KEYDOWN and event.key == K_LEFT:
                DOTPOS[0] = DOTPOS[0]-1
            if event.type == KEYDOWN and event.key == K_UP:
                DOTPOS[1] = DOTPOS[1]-1
            if event.type == KEYDOWN and event.key == K_DOWN:
                DOTPOS[1] = DOTPOS[1]+1
    return result

#battle simulator
def runBattle(enemy, prev_room, prev_info, mousex, mousey):
    global ENEMY_LIST
    player_health=100
    enemy_health=ENEMY_LIST[enemy]['health']
    player_start_health=0
    enemy_start_health=0
    fight_info = []
    attackchoice=0
    while player_health>0 and enemy_health>0:
        player_start_health=player_health
        enemy_start_health=enemy_health
        roomDraw('battle_screen',ROOMS_INFO[0][0])
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
            if event.type == MOUSEBUTTONUP and mousex >=95 and mousex <=220 and mousey >= 205 and mousey <= 240:
                #stab
                fight_info[:] = []
                attackchoice=1
                player_health-=ENEMY_LIST[enemy]['damage']
                if 40-ENEMY_LIST[enemy]['armour'] >0:
                    enemy_health-=40-ENEMY_LIST[enemy]['armour'];
            if event.type == MOUSEBUTTONUP and mousex >=95 and mousex <=220 and mousey >= 250 and mousey <= 280:
                #shieldbash
                fight_info[:] = []
                attackchoice=2
                player_health-=ENEMY_LIST[enemy]['damage']
                enemy_health-=10;
            if event.type == MOUSEBUTTONUP and mousex >=95 and mousex <=220 and mousey >= 290 and mousey <= 330:
                #punch
                fight_info[:] = []
                attackchoice=3
                player_health-=ENEMY_LIST[enemy]['damage']
                if 'dragon punching gloves' in PLAYER_ITEMS:
                    enemy_health-=200;
                else:
                    if 5-ENEMY_LIST[enemy]['armour'] >0:
                        enemy_health-=5-ENEMY_LIST[enemy]['armour'];
        if attackchoice == 1 or attackchoice == 2 or attackchoice == 3:
            fight_info.insert(0,'You hit the {} for {} damage. '.format(enemy, enemy_start_health-enemy_health))
            fight_info.insert(0,'The {} his you for {} damage. '.format(enemy, player_start_health-player_health))
            if enemy == 'skeleton' and attackchoice == 1:
                fight_info.insert(0,'Stabbing skeletons isn\'t very effective')
            attackchoice = 0
        healthDraw(player_health, enemy_health)
        objectDraw(enemy, 475, 200)
        textDraw(fight_info)
        pygame.display.update()
    if enemy == 'skeleton':
        if ROOMS_INFO[6][0].count('The skeleton is blocking your way. ')!=0:
                    ROOMS_INFO[6][0].remove('The skeleton is blocking your way. ')
    if enemy == 'guard':
        if ROOMS_INFO[3][0].count('The guard is blocking your way. ')!=0:
                    ROOMS_INFO[3][0].remove('The guard is blocking your way. ')
    roomDraw(prev_room,prev_info)
    textDraw(prev_info)
    if player_health<=0:
        lossScreen()
    pygame.display.update()
    if enemy == 'dragon':
        return 2
    return 0

#displays health stats
def healthDraw(player, enemy):
    health_text = [str(player),'','','', str(enemy)]
    opening_rect = IMAGESDICT['courtyard_back'].get_rect()
    top_cord = 200
    opening_rect.top = top_cord
    opening_rect.centerx = 650
    FONT = pygame.font.Font('freesansbold.ttf', 18);
    for i in range(len(health_text)):
        instSurf = FONT.render(health_text[i], 1, BLACK)
        instRect = instSurf.get_rect()
        top_cord += 10 # 10 pixels will go in between each line of text.
        instRect.top = top_cord
        instRect.centerx = opening_rect.centerx
        top_cord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

#manages into screens
def openingScreen(open_screen):
    if open_screen == 0:
        roomDraw('title',0)
    if open_screen == 1:
        roomDraw('backstory',0)
    if open_screen == 2:
        roomDraw('instructions',0)
    pygame.display.update()

#manages loss screen
def lossScreen():
    roomDraw('end_title',0)
    pygame.display.update()
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP and event.key == K_RETURN:
                restartProgram()
            if event.type == KEYUP and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

#manages victory screen
def closingScreen(closing_screen):
    if closing_screen == 0:
        roomDraw('closing_story',0)
    if closing_screen == 1:
        roomDraw('end_title',0)
    pygame.display.update()

#restarts program if needed
def restartProgram():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def main():
    global CURRENTROOM, FPSCLOCK, DISPLAYSURF, IMAGESDICT

#Initalizations
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Princess Rescue!')
    IMAGESDICT = {'title': pygame.image.load('art/princess_rescue_big.png'),
                  'dot': pygame.image.load('art/dot.png'),
                  'backstory': pygame.image.load('art/backstory.png'),
                  'closing_story': pygame.image.load('art/closing_story.png'),
                  'end_title': pygame.image.load('art/end_title.png'),
                  'instructions': pygame.image.load('art/instructions.png'),
                  'courtyard_back': pygame.image.load('art/courtyard_back.png'),
                  'great_hall_back': pygame.image.load('art/great_hall_back.png'),
                  'dungeon_back': pygame.image.load('art/dungeon_back.png'),
                  'west_hall_back': pygame.image.load('art/west_hall_back.png'),
                  'east_hall_back': pygame.image.load('art/east_hall_back.png'),
                  'treasury_back': pygame.image.load('art/treasury_back.png'),
                  'tower_one_back': pygame.image.load('art/tower_one_back.png'),
                  'tower_two_back': pygame.image.load('art/tower_two_back.png'),
                  'item_chest': pygame.image.load('art/item_chest.png'),
                  'item_box': pygame.image.load('art/item_box.png'),
                  'cage': pygame.image.load('art/cage.png'),
                  'battle_screen': pygame.image.load('art/battle_screen.png'),
                  'guard': pygame.image.load('art/guard.png'),
                  'dragon': pygame.image.load('art/dragon.png'),
                  'skeleton': pygame.image.load('art/skeleton.png'),
                  'final_boss_back': pygame.image.load('art/final_boss_back.png')
                }                  
    mousex = 0 # x coordinate of mouse
    mousey = 0 # y coordinate of mouse
    open_screen = 0; # intro screen loop initalization
    closing_screen = 0; # closing screen loop initalization

#Actual Program Starts here

#Main game loop
    while True: 
        mousex, mousey = pygame.mouse.get_pos()
        ending = runTest(mousex, mousey)
#Victory screen if player wins
        if ending == "victory":
            while True:
                closingScreen(closing_screen)
                for event in pygame.event.get(): # event handling loop
                    if event.type == KEYUP and event.key == K_RETURN:
                        pygame.quit()
                        sys.exit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True
        itemDraw()
        pygame.display.update()
        
main()
