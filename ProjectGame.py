import random #For generating random numbers
import sys #We will use sys.exit to exit the program
import os
from typing import List, NewType
import pygame
from pygame import image
from pygame import transform
from pygame.locals import *

#Glabal variables for the game
FPS = 36
SCREENWIDTH = 389
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\bird.png.png'
BACKGROUND = 'C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\background.png.jpg'
PIPE = 'C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\pipe.png.png'

def welcomeScreen():
    """
    Shows welcome Image on the Screen 
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #If useer clicks on cross button, close the game etc, Main: all keyboad er khoj rakhe.
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['message'], (0, 0)) #(messagex, messagey likhte)
                #SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                GAME_SOUNDS['welcomeSound'].play()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    #Create 2 pipes for bitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #my List of Upper pipe
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 +(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]
    #my list of Lower pipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 +(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVely = -9
    playerMaxVely = 10
    playerMinVely = -8
    playerAccy = 1

    playerFlapAccv = -8 #Velocity while flapping
    playerFlapped  = False #It is true only when the bird is Flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type ==KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) #This is fuction will return true if the player is crashed
        if crashTest:
            return

        #Check for Score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVely < playerMaxVely and not playerFlapped:
            playerVely += playerAccy

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)
        
        #Move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2
        
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 40 or playery < 0:
        GAME_SOUNDS['hit'].play() 
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False
                


def getRandomPipe():
    """
    #generate positions of two pipes(one bottom straight and one top rotated) for bitting on the screen.
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #Upper Pipe tai minus.
        {'x': pipeX, 'y': y2} #Lower Pipe 
    ]
    return pipe
                

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's module
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Sayan07')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\0.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\1.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\2.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\3.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\4.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\5.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\6.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\7.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\8.png.png').convert_alpha(),
        pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\9.png.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\message.png.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\ImageGaming\\base.png.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\MusicGaming\\die.wav.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\MusicGaming\\hit.wav.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\MusicGaming\\point.wav.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\MusicGaming\\swoosh.wav.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\MusicGaming\\wing.wav.wav')
    GAME_SOUNDS['welcomeSound'] = pygame.mixer.Sound('C:\\Users\\DELL SSD\\PycharmProjects\\beginnersProg\\GamingProject_flaappyBird\\MusicGaming\\welcomeSound.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he press a button
        mainGame() # This is the function

