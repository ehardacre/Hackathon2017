
import random, time, pygame, sys, Tkinter, pyautogui
import mainStart
from pygame.locals import *

FPS = 25
root = Tkinter.Tk()
root.withdraw()
WINDOWWIDTH = root.winfo_screenwidth()
WINDOWHEIGHT = root.winfo_screenheight()
BOXSIZE = 29
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = .25

XMARGIN = 50
TOPMARGIN = XMARGIN

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (100, 100, 100)
BLACK       = (  0,   0,   0)
#RED         = (155,   0,   0)
#LIGHTRED    = (175,  20,  20)
#GREEN       = (  0, 155,   0)
#LIGHTGREEN  = ( 20, 175,  20)
#BLUE        = (  0,   0, 155)
#LIGHTBLUE   = ( 20,  20, 175)
#YELLOW      = (155, 155,   0)
#LIGHTYELLOW = (175, 175,  20)

#LIGHT BLUE FOR I Piece
LIGHTBLUE = (3,191,217)
LIGHTBLUESHADOW = (2,110,132)

#BLUE FOR J PIECE
BLUE = (46,88,236)
BLUESHADOW = (0,38,115)

#PURPLE FOR T PIECE
PURPLE = (209, 16, 215)
PURPLESHADOW = (98, 3, 101)

#YELLOW FOR SQUARE PIECE
YELLOW = (245, 227, 5)
YELLOWSHADOW = (111, 92 , 1)

#RED FOR Z PIECE
RED = (255, 61, 0)
REDSHADOW = (143, 0, 0)

#GREEN FOR S PIECE
GREEN = (75,218,5)
GREENSHADOW = (52,114,1)

#ORANGE FOR L PIECE
ORANGE = (251,166,34)
ORANGESHADOW = (131, 74,1)



BORDERCOLOR = WHITE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
LIGHTCOLORS      = (     LIGHTBLUE,      BLUE,      PURPLE,      YELLOW,    RED,     GREEN,    ORANGE)

COLORS = (LIGHTBLUESHADOW, BLUESHADOW, PURPLESHADOW, YELLOWSHADOW, REDSHADOW, GREENSHADOW, ORANGESHADOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....'],
                    ['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, INFOFONT
    mainStart.initServer()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('Courier.ttf', 18)
    INFOFONT =pygame.font.SysFont('Courier.ttf', 50)
    BIGFONT = pygame.font.SysFont('Courier.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')
    while True: # game loop
#        if random.randint(0, 1) == 0:
#            pygame.mixer.music.load('tetrisb.mid')
#        else:
#            pygame.mixer.music.load('tetrisc.mid')
#        pygame.mixer.music.play(-1, 0.0)
        runGame()
#        pygame.mixer.music.stop()
        showTextScreen('Game OVER')


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    board2 = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    lastMoveDownTime2 = time.time()
    lastMoveSidewaysTime2 = time.time()
    lastFallTime2 = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    movingDown2 = False # note: there is no movingUp variable
    movingLeft2 = False
    movingRight2 = False
    score = 40
    score2 = 40
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()
    nextnextPiece = getNewPiece()
    fallingPiece2 = getNewPiece()
    nextPiece2 = getNewPiece()
    nextnextPiece2 = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = nextnextPiece
            nextnextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over
        if fallingPiece2 == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece2 = nextPiece2
            nextPiece2 = nextnextPiece2
            nextnextPiece2 = getNewPiece()
            lastFallTime2 = time.time() # reset lastFallTime

            if not isValidPosition(board2, fallingPiece2):
                return # can't fit a new piece on the board, so game over
        checkForQuit()
        if mainStart.checkForCommand():
            mainStart.parseCommand(mainStart.character.value)
            mainStart.commandInputted.value = 0
        for event in pygame.event.get(): # event handling loop
            # if event.type == KEYUP:
            #     if (event.key == K_p):
            #         # Pausing the game
            #         DISPLAYSURF.fill(BGCOLOR)
            #         showTextScreen('Paused') # pause until a key press
            #         lastFallTime = time.time()
            #         lastMoveDownTime = time.time()
            #         lastMoveSidewaysTime = time.time()
            #     elif (event.key == K_LEFT or event.key == K_a):
            #         movingLeft = False
            #     elif (event.key == K_RIGHT or event.key == K_d):
            #         movingRight = False
            #     elif (event.key == K_DOWN or event.key == K_s):
            #         movingDown = False

            if event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_j) and isValidPosition(board2, fallingPiece2, adjX=-1):
                    fallingPiece2['x'] -= 1
                    movingLeft2 = True
                    movingRight2 = False
                    lastMoveSidewaysTime2 = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_l) and isValidPosition(board2, fallingPiece2, adjX=1):
                    fallingPiece2['x'] += 1
                    movingRight2 = True
                    movingLeft2 = False
                    lastMoveSidewaysTime2 = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_e):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                elif (event.key == K_o):
                    fallingPiece2['rotation'] = (fallingPiece2['rotation'] + 1) % len(PIECES[fallingPiece2['shape']])
                    if not isValidPosition(board2, fallingPiece2):
                        fallingPiece2['rotation'] = (fallingPiece2['rotation'] - 1) % len(PIECES[fallingPiece2['shape']])
                elif (event.key == K_u): # rotate the other direction
                    fallingPiece2['rotation'] = (fallingPiece2['rotation'] - 1) % len(PIECES[fallingPiece2['shape']])
                    if not isValidPosition(board2, fallingPiece2):
                        fallingPiece2['rotation'] = (fallingPiece2['rotation'] + 1) % len(PIECES[fallingPiece2['shape']])

                # making the piece fall faster with the down key
                # elif (event.key == K_DOWN or event.key == K_s):
                #     movingDown = True
                #     if isValidPosition(board, fallingPiece, adjY=1):
                #         fallingPiece['y'] += 1
                #     lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == K_w:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

                elif event.key == K_i:
                    movingDown2 = False
                    movingLeft2 = False
                    movingRight2 = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board2, fallingPiece2, adjY=i):
                            break
                    fallingPiece2['y'] += i - 1

        # handle moving the piece because of user input
        # if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
        #     if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
        #         fallingPiece['x'] -= 1
        #     elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
        #         fallingPiece['x'] += 1
        #     lastMoveSidewaysTime = time.time()
        #
        # if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
        #     fallingPiece['y'] += 1
        #     lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score -= removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        if time.time() - lastFallTime2 > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board2, fallingPiece2, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board2, fallingPiece2)
                score2 -= removeCompleteLines(board2)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece2 = None
            else:
                # piece did not land, just move the piece down
                fallingPiece2['y'] += 1
                lastFallTime2 = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawBoard2(board2)
        drawStatus(score, level)
        drawStatus2(score2, level)
        drawNextPiece(nextPiece, nextnextPiece)
        drawNextPiece2(nextPiece2, nextnextPiece2)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        if fallingPiece2 != None:
            drawPiece2(fallingPiece2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Waiting for connections...', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    # while checkForKeyPress() == None:
    #     pygame.display.update()
    #     FPSCLOCK.tick()

    p1Connected = False
    p2Connected = False

    while not p1Connected or not p2Connected:
        if mainStart.checkForCommand():
            mainStart.parseCommand(mainStart.character.value)
            mainStart.commandInputted.value = 0
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    p1Connected = True
                    # Draw the additional "Press a key to play." text.
                    p1Surf, p1Rect = makeTextObjs('Player 1 connected!', BASICFONT, TEXTCOLOR)
                    p1Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 130)
                    DISPLAYSURF.blit(p1Surf, p1Rect)
                elif event.key == K_2:
                    p2Connected = True
                    p2Surf, p2Rect = makeTextObjs('Player 2 connected!', BASICFONT, TEXTCOLOR)
                    p2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 160)
                    DISPLAYSURF.blit(p2Surf, p2Rect)
        pygame.display.update()
        FPSCLOCK.tick()



def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(score / 10) + 1
    fallFreq = 0.75 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    if shape == list(PIECES.keys())[0]:
        color = 0
    elif shape == list(PIECES.keys())[1]:
        color = 1
    elif shape == list(PIECES.keys())[2]:
        color = 6
    elif shape == list(PIECES.keys())[3]:
        color = 3
    elif shape == list(PIECES.keys())[4]:
        color = 5
    elif shape == list(PIECES.keys())[5]:
        color = 2
    elif shape == list(PIECES.keys())[6]:
        color = 4
    else:
        color = 0
    newPiece = {'shape': shape,
                'rotation': 0, # random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': color}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def convertToPixelCoords2(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (WINDOWWIDTH - (BOARDWIDTH * BOXSIZE) - XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBox2(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords2(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
    	pygame.draw.line(DISPLAYSURF, GRAY, (x*BOXSIZE + XMARGIN, TOPMARGIN), (x*BOXSIZE + XMARGIN, TOPMARGIN+BOXSIZE*BOARDHEIGHT), 1)
    for y in range(BOARDHEIGHT):
    	pygame.draw.line(DISPLAYSURF, GRAY, (XMARGIN, y*BOXSIZE + TOPMARGIN), (XMARGIN + BOXSIZE*BOARDWIDTH, y*BOXSIZE + TOPMARGIN), 1)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawBoard2(board):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (WINDOWWIDTH - (BOARDWIDTH * BOXSIZE) - XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (WINDOWWIDTH - (BOARDWIDTH * BOXSIZE) - XMARGIN - 3, TOPMARGIN - 7, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
    	pygame.draw.line(DISPLAYSURF, GRAY, (x*BOXSIZE + WINDOWWIDTH - (BOARDWIDTH * BOXSIZE) - XMARGIN, TOPMARGIN), (x*BOXSIZE + WINDOWWIDTH - (BOARDWIDTH * BOXSIZE) - XMARGIN, TOPMARGIN+BOXSIZE*BOARDHEIGHT), 1)
    for y in range(BOARDHEIGHT):
    	pygame.draw.line(DISPLAYSURF, GRAY, (WINDOWWIDTH - (BOARDWIDTH * BOXSIZE) - XMARGIN - 3, y*BOXSIZE + TOPMARGIN), (WINDOWWIDTH - XMARGIN, y*BOXSIZE + TOPMARGIN), 1)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox2(x, y, board[x][y])

def drawStatus(score, level):
    # draw the score text
    scoreSurf = BIGFONT.render('%s' % score, True, GRAY)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (XMARGIN + (BOARDWIDTH * BOXSIZE)/2 - 40, (BOARDHEIGHT * BOXSIZE) + 80)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawStatus2(score, level):
    # draw the score text
    scoreSurf = BIGFONT.render('%s' % score, True, GRAY)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - XMARGIN - (BOARDWIDTH * BOXSIZE)/2 - 40, (BOARDHEIGHT * BOXSIZE) + 80)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
#    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
#    levelRect = levelSurf.get_rect()
#    levelRect.topleft = (WINDOWWIDTH - 150, 50)
#    DISPLAYSURF.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawPiece2(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords2(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox2(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece , nextpiece):
#    # draw the "next" text
#    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
#    nextRect = nextSurf.get_rect()
#    nextRect.topleft = (WINDOWWIDTH - 120, 80)
#    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=XMARGIN + (BOARDWIDTH * BOXSIZE) + 20, pixely=TOPMARGIN)
    drawPiece(nextpiece, pixelx=XMARGIN + (BOARDWIDTH * BOXSIZE) + 20, pixely=TOPMARGIN + 100)

def drawNextPiece2(piece , nextpiece):
    drawPiece2(piece, pixelx=WINDOWWIDTH - XMARGIN - (BOARDWIDTH * BOXSIZE) - (5*BOXSIZE), pixely=TOPMARGIN)
    drawPiece2(nextpiece, pixelx=WINDOWWIDTH - XMARGIN - (BOARDWIDTH * BOXSIZE) - (5*BOXSIZE), pixely=TOPMARGIN + 100)

# if __name__ == '__main__':
#     main()
main()