#user input
#displaying current GameState object

import pygame as p
from Chess import engine

width = height = 512
dimension = 8
squareSize = height // dimension
maxFPS = 30
images = {}

'''
initialize global dict of images. this will be called once on main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'bR']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Chess/pieces/" + piece + ".png"), (squareSize, squareSize))

'''
user input and graphic updates
'''
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    loadImages() #only do once, before while loop
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: 
                location = p.mouse.get_pos() # xy location of cursor
                col = location[0] // squareSize
                row = location[1] // squareSize
                if sqSelected == (row, col): # preventing double clicks
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for 1st and 2nd clicks
                if len(playerClicks) == 2: # after 2nd click, make move
                    move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () # reset user clicks
                        playerClicks = []
                    else: 
                        playerClicks = [sqSelected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when z is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs)
        clock.tick(maxFPS)
        p.display.flip()

'''
responsible for all graphics within current gamestate
'''
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on squares

'''
Draw squares on board
'''
def drawBoard(screen):
    colors = [p.Color(195, 195, 195), p.Color(140, 140, 140)]
    
    for i in range(dimension):
        for j in range(dimension):
            color = colors[((i+j)%2)]
            p.draw.rect(screen, color, p.Rect(j*squareSize, i*squareSize, squareSize, squareSize))
'''
Draw pieces on board using current gamestate.board
'''
def drawPieces(screen, board):
    for i in range(dimension):
        for j in range(dimension):
            piece = board[i][j]
            if piece != "--": #not empty square
                screen.blit(images[piece], p.Rect(j*squareSize, i*squareSize, squareSize, squareSize)) #blit is draw ontop of


if __name__ == "__main__":
    main()