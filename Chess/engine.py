#current state of game
#determining valid moves
#move log

class GameState():
    def __init__(self):
        #8x8 2d list, 2 char per element
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.moveLog = []
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        #1

    '''
    Takes move as parameter and executes (won't work for castling, pawn promotion, en-passant)
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # undo move // display history
        self.whiteToMove = not self.whiteToMove # swap player turn
    
    '''
    Undo last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that movelog isn't empty
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls appropriate moveFunction based on piece type
        return moves

    def getPawnMoves(self, r, c, moves):
        #forward 1, forward 2, diagonal 1
        if self.whiteToMove:
            if self.board[r-1][c] == "--": # forward 1
                moves.append(Move((r,c), (r-1,c), self.board))
                if self.board[r-2][c] == "--" and r==6: # forward 2
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': # take left
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': # take right
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        else: #black
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board)) #f1
                if self.board[r+2][c] == "--" and r==1: #f2
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': # take left
                    moves.append(Move((r,c), (r+1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w': # take right
                    moves.append(Move((r,c), (r+1,c+1), self.board))

        # add promotions later
    
    def getRookMoves(self, r, c, moves): #hyugens (prime only)
        if self.whiteToMove:
            # up
            if r >= 2 and self.board[r-2][c][0] != 'w':
                moves.append(Move((r,c), (r-2,c), self.board))
            if r >= 3 and self.board[r-3][c][0] != 'w':
                moves.append(Move((r,c), (r-3,c), self.board))
            if r >= 5 and self.board[r-5][c][0] != 'w':
                moves.append(Move((r,c), (r-5,c), self.board))
            # down
            if 7-r >= 2 and self.board[r+2][c][0] != 'w':
                moves.append(Move((r,c), (r+2,c), self.board))
            if 7-r >= 3 and self.board[r+3][c][0] != 'w':
                moves.append(Move((r,c), (r+3,c), self.board))
            if 7-r >= 5 and self.board[r+5][c][0] != 'w':
                moves.append(Move((r,c), (r+5,c), self.board))
            # right
            if 7-c >= 2 and self.board[r][c+2][0] != 'w':
                moves.append(Move((r,c), (r,c+2), self.board))
            if 7-c >= 3 and self.board[r][c+3][0] != 'w':
                moves.append(Move((r,c), (r,c+3), self.board))
            if 7-c >= 5 and self.board[r][c+5][0] != 'w':
                moves.append(Move((r,c), (r,c+5), self.board))
            # left
            if c >= 2 and self.board[r][c-2][0] != 'w':
                moves.append(Move((r,c), (r,c-2), self.board))
            if c >= 3 and self.board[r][c-3][0] != 'w':
                moves.append(Move((r,c), (r,c-3), self.board))
            if c >= 5 and self.board[r][c-5][0] != 'w':
                moves.append(Move((r,c), (r,c-5), self.board))
        else: #black
            # up
            if r >= 2 and self.board[r-2][c][0] != 'w':
                moves.append(Move((r,c), (r-2,c), self.board))
            if r >= 3 and self.board[r-3][c][0] != 'w':
                moves.append(Move((r,c), (r-3,c), self.board))
            if r >= 5 and self.board[r-5][c][0] != 'w':
                moves.append(Move((r,c), (r-5,c), self.board))
            # down
            if 7-r >= 2 and self.board[r+2][c][0] != 'w':
                moves.append(Move((r,c), (r+2,c), self.board))
            if 7-r >= 3 and self.board[r+3][c][0] != 'w':
                moves.append(Move((r,c), (r+3,c), self.board))
            if 7-r >= 5 and self.board[r+5][c][0] != 'w':
                moves.append(Move((r,c), (r+5,c), self.board))
            # right
            if 7-c >= 2 and self.board[r][c+2][0] != 'w':
                moves.append(Move((r,c), (r,c+2), self.board))
            if 7-c >= 3 and self.board[r][c+3][0] != 'w':
                moves.append(Move((r,c), (r,c+3), self.board))
            if 7-c >= 5 and self.board[r][c+5][0] != 'w':
                moves.append(Move((r,c), (r,c+5), self.board))
            # left
            if c >= 2 and self.board[r][c-2][0] != 'w':
                moves.append(Move((r,c), (r,c-2), self.board))
            if c >= 3 and self.board[r][c-3][0] != 'w':
                moves.append(Move((r,c), (r,c-3), self.board))
            if c >= 5 and self.board[r][c-5][0] != 'w':
                moves.append(Move((r,c), (r,c-5), self.board))

    def getKnightMoves(self, r, c, moves): #flyingcat (semi circle up, 1 back)
        if self.whiteToMove:
            if r >= 2 and self.board[r-2][c][0] != 'w': # up 2
                moves.append(Move((r,c), (r-2,c), self.board))
            if c <= 6 and r >= 2 and self.board[r-2][c+1][0] != 'w': # up 2 right 1
                moves.append(Move((r,c), (r-2,c+1), self.board))
            if c >= 1 and r >= 2 and self.board[r-2][c-1][0] != 'w': # up 2 left 1
                moves.append(Move((r,c), (r-2,c-1), self.board))
            if c <= 5 and r >= 1 and self.board[r-1][c+2][0] != 'w': # up 1 right 2
                moves.append(Move((r,c), (r-1,c+2), self.board))
            if c >= 2 and r >= 1 and self.board[r-1][c-2][0] != 'w': # up 1 left 2
                moves.append(Move((r,c), (r-1,c-2), self.board))
            if c <= 5 and self.board[r][c+2][0] != 'w': # right 2
                moves.append(Move((r,c), (r,c+2), self.board))
            if c >= 2 and self.board[r][c-2][0] != 'w': # left 2
                moves.append(Move((r,c), (r,c-2), self.board))
            if r <= 6 and self.board[r+1][c][0] != 'w': # down 1
                moves.append(Move((r,c), (r+1,c), self.board))
            if r <= 6 and c >= 1 and self.board[r+1][c-1][0] != 'w': # down 1 left 1
                moves.append(Move((r,c), (r+1,c-1), self.board))
            if r <= 6 and c <= 6 and self.board[r+1][c+1][0] != 'w': # down 1 right 1
                moves.append(Move((r,c), (r+1,c+1), self.board))
            
        else: # black
            if r <= 5 and self.board[r+2][c][0] != 'b':  # down 2
                moves.append(Move((r, c), (r+2, c), self.board))
            if c <= 6 and r <= 5 and self.board[r+2][c+1][0] != 'b':  # down 2 right 1
                moves.append(Move((r, c), (r+2, c+1), self.board))
            if c >= 1 and r <= 5 and self.board[r+2][c-1][0] != 'b':  # down 2 left 1
                moves.append(Move((r, c), (r+2, c-1), self.board))
            if c <= 5 and r <= 6 and self.board[r+1][c+2][0] != 'b':  # down 1 right 2
                moves.append(Move((r, c), (r+1, c+2), self.board))
            if c >= 2 and r <= 6 and self.board[r+1][c-2][0] != 'b':  # down 1 left 2
                moves.append(Move((r, c), (r+1, c-2), self.board))
            if c <= 5 and self.board[r][c+2][0] != 'b':  # right 2
                moves.append(Move((r, c), (r, c+2), self.board))
            if c >= 2 and self.board[r][c-2][0] != 'b':  # left 2
                moves.append(Move((r, c), (r, c-2), self.board))
            if r >= 1 and self.board[r-1][c][0] != 'b':  # up 1
                moves.append(Move((r, c), (r-1, c), self.board))
            if r >= 1 and c >= 1 and self.board[r-1][c-1][0] != 'b':  # up 1 left 1
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if r >= 1 and c <= 6 and self.board[r-1][c+1][0] != 'b':  # up 1 right 1
                moves.append(Move((r, c), (r-1, c+1), self.board))
        
    def getBishopMoves(self, r, c, moves): #bishknight (bishop forward, knight backwards)
        if self.whiteToMove:
            # Bishop-like movement upwards (diagonals)
            for i in range(1, min(r+1, len(self.board))):  # Up-left diagonal
                if c - i >= 0 and self.board[r-i][c-i][0] != 'w':  # If within bounds and not occupied by white piece
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                    if self.board[r-i][c-i][0] != '-':  # Stop if a piece is blocking the path
                        break
                else:
                    break
            
            for i in range(1, min(r+1, len(self.board) - c)):  # Up-right diagonal
                if c + i <= 7 and self.board[r-i][c+i][0] != 'w':  # If within bounds and not occupied by white piece
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                    if self.board[r-i][c+i][0] != '-':  # Stop if a piece is blocking the path
                        break
                else:
                    break

            # Knight-like movement downwards (backwards L-shaped moves)
            if r <= 5 and c <= 6 and self.board[r+2][c+1][0] != 'w':  # Down 2, right 1
                moves.append(Move((r, c), (r+2, c+1), self.board))
            if r <= 5 and c >= 1 and self.board[r+2][c-1][0] != 'w':  # Down 2, left 1
                moves.append(Move((r, c), (r+2, c-1), self.board))
            if r <= 6 and c <= 5 and self.board[r+1][c+2][0] != 'w':  # Down 1, right 2 
                moves.append(Move((r, c), (r+1, c+2), self.board))
            if r <= 6 and c >= 2 and self.board[r+1][c-2][0] != 'w':  # Down 1, left 2
                moves.append(Move((r, c), (r+1, c-2), self.board))

        else: # black
            # Bishop-like movement downwards (diagonals)
            for i in range(1, len(self.board) - r):  # Down-left diagonal
                if c - i >= 0 and self.board[r+i][c-i][0] != 'b':  # If within bounds and not occupied by black piece
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                    if self.board[r+i][c-i][0] != '-':  # Stop if a piece is blocking the path
                        break
                else:
                    break
            
            for i in range(1, len(self.board) - r):  # Down-right diagonal
                if c + i <= 7 and self.board[r+i][c+i][0] != 'b':  # If within bounds and not occupied by black piece
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                    if self.board[r+i][c+i][0] != '-':  # Stop if a piece is blocking the path
                        break
                else:
                    break

            # Knight-like movement upwards (backwards L-shaped moves)
            if r >= 2 and c <= 6 and self.board[r-2][c+1][0] != 'b':  # Up 2, right 1
                moves.append(Move((r, c), (r-2, c+1), self.board))
            if r >= 2 and c >= 1 and self.board[r-2][c-1][0] != 'b':  # Up 2, left 1
                moves.append(Move((r, c), (r-2, c-1), self.board))
            if r >= 1 and c <= 5 and self.board[r-1][c+2][0] != 'b':  # Up 1, right 2
                moves.append(Move((r, c), (r-1, c+2), self.board))
            if r >= 1 and c >= 2 and self.board[r-1][c-2][0] != 'b':  # Up 1, left 2
                moves.append(Move((r, c), (r-1, c-2), self.board))

    def getQueenMoves(self, r, c, moves): #wizard stork (queen except no straight or diagback)
        if self.whiteToMove:
            # Horizontal movement (left and right)
            for i in range(1, 8):  # Move to the right
                if c + i <= 7 and self.board[r][c + i][0] != 'w':
                    moves.append(Move((r, c), (r, c + i), self.board))
                    if self.board[r][c + i][0] != '-':  # Stop if blocked
                        break
                else:
                    break
            
            for i in range(1, 8):  # Move to the left
                if c - i >= 0 and self.board[r][c - i][0] != 'w':
                    moves.append(Move((r, c), (r, c - i), self.board))
                    if self.board[r][c - i][0] != '-':  # Stop if blocked
                        break
                else:
                    break

            # Vertical movement (downward only)
            for i in range(1, 8):  # Move down
                if r + i <= 7 and self.board[r + i][c][0] != 'w':
                    moves.append(Move((r, c), (r + i, c), self.board))
                    if self.board[r + i][c][0] != '-':  # Stop if blocked
                        break
                else:
                    break
            
            # Diagonal movement (up-left and up-right only)
            for i in range(1, 8):  # Up-right diagonal
                if r - i >= 0 and c + i <= 7 and self.board[r - i][c + i][0] != 'w':
                    moves.append(Move((r, c), (r - i, c + i), self.board))
                    if self.board[r - i][c + i][0] != '-':  # Stop if blocked
                        break
                else:
                    break

            for i in range(1, 8):  # Up-left diagonal
                if r - i >= 0 and c - i >= 0 and self.board[r - i][c - i][0] != 'w':
                    moves.append(Move((r, c), (r - i, c - i), self.board))
                    if self.board[r - i][c - i][0] != '-':  # Stop if blocked
                        break
                else:
                    break
        else: # black
            # Horizontal movement (left and right)
            for i in range(1, 8):  # Move to the right
                if c + i <= 7 and self.board[r][c + i][0] != 'b':
                    moves.append(Move((r, c), (r, c + i), self.board))
                    if self.board[r][c + i][0] != '-':  # Stop if blocked
                        break
                else:
                    break
            
            for i in range(1, 8):  # Move to the left
                if c - i >= 0 and self.board[r][c - i][0] != 'b':
                    moves.append(Move((r, c), (r, c - i), self.board))
                    if self.board[r][c - i][0] != '-':  # Stop if blocked
                        break
                else:
                    break

            # Vertical movement (upward only)
            for i in range(1, 8):  # Move up
                if r - i >= 0 and self.board[r - i][c][0] != 'b':
                    moves.append(Move((r, c), (r - i, c), self.board))
                    if self.board[r - i][c][0] != '-':  # Stop if blocked
                        break
                else:
                    break
            
            # Diagonal movement (down-left and down-right only)
            for i in range(1, 8):  # Down-right diagonal
                if r + i <= 7 and c + i <= 7 and self.board[r + i][c + i][0] != 'b':
                    moves.append(Move((r, c), (r + i, c + i), self.board))
                    if self.board[r + i][c + i][0] != '-':  # Stop if blocked
                        break
                else:
                    break

            for i in range(1, 8):  # Down-left diagonal
                if r + i <= 7 and c - i >= 0 and self.board[r + i][c - i][0] != 'b':
                    moves.append(Move((r, c), (r + i, c - i), self.board))
                    if self.board[r + i][c - i][0] != '-':  # Stop if blocked
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves): #king (regular)
        if self.whiteToMove:
            # King can move one square in any direction
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for d in directions:
                new_r, new_c = r + d[0], c + d[1]
                if 0 <= new_r <= 7 and 0 <= new_c <= 7:  # Ensure the move is within the board
                    if self.board[new_r][new_c][0] != 'w':  # Can't capture own piece
                        moves.append(Move((r, c), (new_r, new_c), self.board))
        else:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for d in directions:
                new_r, new_c = r + d[0], c + d[1]
                if 0 <= new_r <= 7 and 0 <= new_c <= 7:  # Ensure the move is within the board
                    if self.board[new_r][new_c][0] != 'b':  # Can't capture own piece
                        moves.append(Move((r, c), (new_r, new_c), self.board))



class Move():
    # mapping keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} # reversing ranksToRows
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()} # reversing filesToCols
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]