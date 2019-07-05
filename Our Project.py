import random, pygame, sys, time
from pygame.locals import *
FPS = 40
screenWidth = 640 
screenHeight = 480 
revealSpeed = 10
cellSize = 40
gapSize = 10
columns = 5
rows = 4
'''easy = [4,4]
medium = [6,6]
hard = [8,8]
level = input("choose a level: E/M/H")
if level == "E":
    columns = easy[0]
    rows = easy[1]
elif level == "M":
    columns = medium[0]
    rows = medium[1]
else:
    columns = hard[0]
    rows = hard[1]'''
assert (columns * rows) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMargin = int((screenWidth - (columns * (cellSize + gapSize))) / 2)
YMargin = int((screenHeight - (rows * (cellSize + gapSize))) / 2)

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

Background = NAVYBLUE
cellColour = WHITE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
resultImages = ['projectimage1.jpg', 'projectimage2.jpg', 'projectimage3.jpg', 'projectimage4.jpg', 'projectimage5.png',]
colours = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
shapes = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(colours) * len(shapes) * 2 >= columns * rows, "Board is too big for the number of shapes/colors defined."
def main():
    global FPSCLOCK, DISPLAYSURF
    SCORE = 0
    pygame.init()
    img = random.choice(resultImages)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((screenWidth, screenHeight))
    mousex = 0 
    mousey = 0
    pygame.display.set_caption('Memory Game                     SCORE = '+ str(SCORE))
    mainBoard = RandomizedBoard()
    revealedBoxes = initialiseRevealedState(False)
    firstSelection = None
    DISPLAYSURF.fill(Background)
    while True:
        mouseClicked = False
        DISPLAYSURF.fill(Background) 
        drawBoard(mainBoard, revealedBoxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                reveal_boxes(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True
                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        pygame.mixer.music.load('incorrect guess.mp3')
                        pygame.mixer.music.play(0)
                        pygame.time.wait(1000)
                        cover_boxes(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection [1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        pygame.display.set_caption('Memory Game                     SCORE = '+ str(SCORE))
                        SCORE = 0
                        pygame.time.wait(2000)
                        pygame.mixer.music.load('won game.wav')
                        pygame.mixer.music.play(0)
                        image = pygame.image.load(img)
                        image = pygame.transform.scale(image, (500, 400))
                        DISPLAYSURF =pygame.display.set_mode((screenWidth,screenHeight))
                        DISPLAYSURF.fill(Background)
                        DISPLAYSURF.blit(image,(((screenWidth-500)//2),((screenHeight-400)//2)))
                        pygame.display.update()
                        pygame.time.wait(10000)
                        decision = input("Do you want to play again? Y/N")
                        if decision == "Y":
                            pygame.display.set_caption('Memory Game                     SCORE = '+ str(SCORE))
                            img = random.choice(resultImages)  
                            mainBoard = RandomizedBoard()
                            revealedBoxes = initialiseRevealedState(False)
                            drawBoard(mainBoard, revealedBoxes)
                            pygame.display.update()
                            pygame.time.wait(1000)
                        else:
                            pygame.quit()
                            sys.exit()
                    else :
                        SCORE += 1
                        pygame.display.set_caption('Memory Game                     SCORE = '+ str(SCORE))
                        pygame.mixer.music.load('correct_guess.mp3')
                        pygame.mixer.music.play(0)
                    firstSelection = None
            pygame.display.update()
            FPSCLOCK.tick(FPS)

def initialiseRevealedState(val):
    revealedBoxes = []
    for i in range(columns):
        revealedBoxes.append([val] * rows)
    return revealedBoxes

def RandomizedBoard():
    icons = []
    for color in colours:
        for shape in shapes:
            icons.append( (shape, color) )
    random.shuffle(icons)
    numIconsUsed = int(columns * rows / 2) 
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)
    
    board = []
    for x in range(columns):
        column = []
        for y in range(rows):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (cellSize + gapSize) + XMargin
    top = boxy * (cellSize + gapSize) + YMargin
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(columns):
        for boxy in range(rows):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, cellSize, cellSize)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(cellSize * 0.25) 
    half =    int(cellSize * 0.5)  
    left, top = leftTopCoordsOfBox(boxx, boxy) 
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, Background, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, cellSize - half, cellSize - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + cellSize - 1, top + half), (left + half, top + cellSize - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, cellSize, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + cellSize - 1), (left + cellSize - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, cellSize, half))

def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, Background, (left, top, cellSize, cellSize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, cellColour, (left, top, coverage, cellSize))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def reveal_boxes(board, boxesToReveal):
    for coverage in range(cellSize, (-revealSpeed) - 1, - revealSpeed):
        drawBoxCovers(board, boxesToReveal, coverage)

def cover_boxes(board, boxesToCover):
    for coverage in range(0, cellSize + revealSpeed, revealSpeed):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    for boxx in range(columns):
        for boxy in range(rows):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, cellColour, (left, top, cellSize, cellSize))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == '__main__':
    main()

