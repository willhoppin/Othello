import turtle
import math
import copy
import random as r
import time as ti
import os

# Constants
n = 8
boardsize = 600
margin = 75
mainwidth = 8
cells = 8
cellsize = (boardsize - 2 * margin) / cells
edgeBL = -boardsize/2+margin
edgeTR = boardsize/2-margin
playerColors = {
    'w': 'white',
    'b': 'black'
}

# Turtle Initialization
t = turtle.Turtle()
movesT = turtle.Turtle()
textT = turtle.Turtle()
s = turtle.Screen()
s.bgcolor('forest green')
s.setup(boardsize, boardsize)
t.hideturtle()
movesT.hideturtle()
textT.hideturtle()
textT.color('black')
movesT.shapesize(0.5, 0.5)
movesT.shape('circle')
movesT.penup()
textT.penup()
s.tracer(0, 0)

# Data Structure Setup
gameBoard = [[0 for _ in range(cells)] for _ in range(cells)]
gameBoard[3][3] = 'w'
gameBoard[3][4] = 'b'
gameBoard[4][4] = 'w'
gameBoard[4][3] = 'b'
currentPlayer = 'b'
oppPlayer = 'w'
moveDir = {
    'L': [0, -1],
    'R': [0, 1],
    'U': [-1, 0],
    'D': [1, 0],
    'UL': [-1, -1],
    'DL': [1, -1],
    'DR': [1, 1],
    'UR': [-1, 1]
}


# Dev
def printBoard(board):
    [print([str(loc) for loc in line]) for line in board]


# Functions
def whichRow(y):
    row = cells-math.ceil((y+boardsize/2-margin)/cellsize)
    if row >= 0 and row < cells:
        return row


def whichColumn(x):
    col = math.ceil((x+boardsize/2-margin)/cellsize)-1
    if col >= 0 and col < cells:
        return col


def yFromRow(row):
    return (row * cellsize + cellsize / 2 + margin) - boardsize / 2


def xFromColumn(column):
    return -((column * cellsize + cellsize / 2 + margin) - boardsize / 2)


def validChain(chain):
    valid = False
    if len(chain) > 1:
        if not chain[0] == chain[1] and not chain[0] == 0:
            for item in chain[1:]:
                if item == 0:
                    return False
                if item == chain[0]:
                    return True
    return valid

def flatten(lst):
	if lst == []:
		return lst
	if isinstance(lst[0], list):
		return flatten(lst[0]) + flatten(lst[1:])
	return lst[:1] + flatten(lst[1:])

def updateBoard(board, player, row, col, movesOverride=False):
    if not movesOverride:
        moves = validMove(board, player, row, col)
    else:
        moves = movesOverride
    if(moves):
        board[row][col] = player
        for dir in moves:
            for i in range(1, cells):
                if board[row + i * moveDir[dir][0]][col + i * moveDir[dir][1]] == player or board[row + i * moveDir[dir][0]][col + i * moveDir[dir][1]] == 0:
                    break
                else:
                    board[row + i * moveDir[dir][0]][col + i * moveDir[dir][1]] = player
    return board


def calculateScore(board, player):
    score = 0
    for row in board:
        for col in row:
            if col == player:
                score += 1
    return score


def validMove(board, player, row, col):
    newBoard = copy.deepcopy(board)
    if not board[row][col] == 0:
        return False
    newBoard[row][col] = player
    fullCol = [newBoard[i][col] for i in range(cells)]
    diagPosA = []
    diagNegA = []
    diagPosB = []
    diagNegB = []
    validMoves = []
    for i in range(-cells + 1, 1):
        if row + i >= 0 and col + i >= 0 and row + i < cells and col + i < cells:
            diagPosA.append(newBoard[row + i][col + i])
        if row - i >= 0 and col + i >= 0 and row - i < cells and col + i < cells:
            diagNegA.append(newBoard[row - i][col + i])
    for i in range(0, cells):
        if row + i >= 0 and col + i >= 0 and row + i < cells and col + i < cells:
            diagPosB.append(newBoard[row + i][col + i])
        if row - i >= 0 and col + i >= 0 and row - i < cells and col + i < cells:
            diagNegB.append(newBoard[row - i][col + i])
    if validChain(newBoard[row][:col + 1][::-1]):
        validMoves.append('L')
    if validChain(newBoard[row][col:]):
        validMoves.append('R')
    if validChain(fullCol[:row + 1][::-1]):
        validMoves.append('U')
    if validChain(fullCol[row:]):
        validMoves.append('D')
    if validChain(diagPosA[::-1]):
        validMoves.append('UL')
    if validChain(diagNegA[::-1]):
        validMoves.append('DL')
    if validChain(diagPosB):
        validMoves.append('DR')
    if validChain(diagNegB):
        validMoves.append('UR')

    if len(validMoves) > 0:
        return validMoves
    else:
        return False


def nextBoard(board, player, move, movesOverride=False):
    board = copy.deepcopy(board)
    return updateBoard(board, player, move[0], move[1], movesOverride)


def allValidMoves(board, player):
    output = []
    zeros = 0
    for rowIndex in range(cells):
        for colIndex in range(cells):
            if board[rowIndex][colIndex] == 0:
                zeros += 1
                if validMove(board, player, rowIndex, colIndex):
                    output.append([colIndex, rowIndex])
    if zeros > 0:
        return output
    else:
        return 'Winner'


def flipCurrentPlayer():
    global currentPlayer
    textT.goto(0, -boardsize / 2 + margin / 2)
    if currentPlayer == 'b':
        currentPlayer = 'w'
        oppPlayer = 'b'
        textT.write('White\'s Move', move=True, align="center", font=('Helvetica Neue', '16', 'bold'))
    else:
        currentPlayer = 'b'
        oppPlayer = 'w'
        textT.write('Black\'s Move', move=True, align="center", font=('Helvetica Neue', '16', 'bold'))


def drawBoard():
    t.width(mainwidth)
    t.penup()
    t.goto(edgeBL, edgeBL)
    t.pendown()
    t.color('black')
    t.goto(edgeTR, edgeBL)
    t.goto(edgeTR, edgeTR)
    t.goto(edgeBL, edgeTR)
    t.goto(edgeBL, edgeBL)

    t.width(mainwidth/2)
    for cell in range(1,cells+1):
        t.penup()
        t.goto(edgeBL + (cell * cellsize), edgeTR)
        t.pendown()
        t.goto(edgeBL + (cell * cellsize), edgeBL)
        t.penup()
        t.goto(edgeBL, edgeTR - (cell * cellsize))
        t.pendown()
        t.goto(edgeTR, edgeTR - (cell * cellsize))


def stampPlayer(row, column, player):
    t.goto(yFromRow(row), xFromColumn(column))
    t.color(player)
    t.stamp()


def drawPieces():
    for rowIndex in range(cells):
        for colIndex in range(cells):
            if not gameBoard[rowIndex][colIndex] == 0:
                stampPlayer(colIndex, rowIndex, playerColors[gameBoard[rowIndex][colIndex]])


def drawMoves():
    moves = allValidMoves(gameBoard, currentPlayer)
    if moves == 'Winner':
        textT.goto(0, -boardsize/2 + margin/4)
        winner = playerColors['b']
        if calculateScore(gameBoard, 'w') > calculateScore(gameBoard, 'b'):
            winner = playerColors['w']
        textT.write('The winner is ' + winner + '!', move=True, align="center", font=('Helvetica Neue', '16', 'normal'))
    elif len(moves) > 0:
        for move in moves:
            movesT.goto(yFromRow(move[0]), xFromColumn(move[1]))
            movesT.color(playerColors[currentPlayer])
            movesT.stamp()
    else:
        textT.goto(0, -boardsize/2 + margin/4)
        textT.write('No valid moves, skipped ' + playerColors[currentPlayer] + '\'s turn.', move=True, align="center", font=('Helvetica Neue', '16', 'normal'))
        draw()
        flipCurrentPlayer()
        postDraw()


def drawScore():
    t.goto(-cellsize, boardsize/2 - margin/2)
    t.color('black')
    t.stamp()
    t.color('white')
    t.goto(-cellsize, boardsize/2 - margin/2 - 8)
    t.write(calculateScore(gameBoard, 'b'), move=True, align="center", font=('Helvetica Neue', '16', 'normal'))
    t.goto(cellsize, boardsize/2 - margin/2)
    t.color('white')
    t.stamp()
    t.color('black')
    t.goto(cellsize, boardsize/2 - margin/2 - 8)
    t.write(calculateScore(gameBoard, 'w'), move=True, align="center", font=('Helvetica Neue', '16', 'normal'))


def draw():
    movesT.clear()
    textT.clear()
    t.penup()
    t.shape('circle')
    t.shapesize(2, 2)
    drawScore()
    drawPieces()


def postDraw():
    drawMoves()


def move(row, col):
    global gameBoard
    if (row or row == 0) and (col or col == 0):
        moveCheck = validMove(gameBoard, currentPlayer, row, col)
        if moveCheck:
            gameBoard = nextBoard(gameBoard, currentPlayer, [row, col], moveCheck)
            draw()
            flipCurrentPlayer()
            postDraw()
        else:
            print('Invalid Move')




def startGame():
    drawBoard()
    draw()
    postDraw()

startGame()

priorities = [[0,0],[0,7],[7,0],[7,7],[0,2],[0,3],[0,4],[0,5],[2,0],[3,0],[4,0],[5,0],[7,2],[7,3],[7,4],[7,5],[2,7],[3,7],[4,7],[5,7],[2,2],[2,3],[2,4],[2,5],[3,5],[4,5],[5,5],[5,4],[5,3],[5,2],[4,2],[3,2],[1,2],[1,3],[1,4],[1,5],[2,6],[3,6],[4,6],[5,6],[6,5],[6,4],[6,3],[6,2],[5,1],[4,1],[3,1],[2,1],[0,1],[1,1],[1,0],[0,6],[1,6],[1,7],[6,0],[6,1],[7,1],[6,6],[6,7],[7,6]]

def score(x,priority):
    if x == priority[0]:
        return 1
    else:
        return 1 + score(x,priority[1:])

def bestValid(moves):
    scores = [score(x,priorities) for x in moves]
    minscore = min(scores)
    targ = scores.index(minscore)
    return moves[targ]

def intelligentMove():
    valids = allValidMoves(gameBoard,currentPlayer)
    choice = bestValid(valids)
    row = choice[1]
    col = choice[0]
    #print (row)
    #print (col)
    move(row,col)

def randomMove():
    #print ('yes')
    valids = allValidMoves(gameBoard,currentPlayer)
    choice = r.choice(valids)
    row = choice[1]
    col = choice[0]
    move(row,col)

def minimaxMove():
    global movelist
    global coslist
    global movedict
    global hlist
    hl = endvalue(miniMax(gameBoard,currentPlayer))
    if hl in allValidMoves(gameBoard,currentPlayer):
        print (hl)
        row = hl[1]
        print (row)
        col = hl[0]
        print (col)
        coslist = []
        movelist = []
        hlist = []
        print (currentPlayer)
        move(row,col)



def speedMove():
    valids = allValidMoves(gameBoard,currentPlayer)
    choice = valids[0]
    row = choice[1]
    col = choice[0]
    move(row,col)

def minimaxGame():

    while len(allValidMoves(gameBoard,currentPlayer)) > 0:
        minimaxMove()
        postDraw()
        print (currentPlayer)
        ti.sleep(10)

def randomGame(players):
    countdown = 100
    #drawBoard()
    #draw()
    print(players )
    if players == 0:
        while len(allValidMoves(gameBoard,currentPlayer)) > 0:
            randomMove()
            postDraw()
            #ti.sleep(1)

def intelligentGame(players):
    if players == 0:
        while len(allValidMoves(gameBoard,currentPlayer)) > 0:
            intelligentMove()
            postDraw()
            #ti.sleep(1)


def speedOthello(players):
    if players == 0:
        while len(allValidMoves(gameBoard,currentPlayer)) > 0:
            speedMove()
            postDraw()
            #ti.sleep(1)

def IsTerminalNode(board, player):
    for y in range(n):
        for x in range(n):
            if validMove(board, player,y,x):
                return False
    return True

def miniFunc(list1,board):
    plist = []
    for x in list1:

        plist.insert(miniMax(currentPlayer,board),x-1)
    return plist


movelist = []
movedict = {}
coslist = []
hlist = []

def miniMax(board,player,alpha = -1 * math.inf,beta = math.inf, depth = 0, Maxturn=True):
    global movelist
    global coslist
    global movedict
    global hlist
    if depth == 4 or allValidMoves(board,player) == 'Winner':
        #print (movedict)
        #print (movelist)
        #print (coslist)

        return evaluateBoard(board,player)
        #return the dict value with this evalboard answer

    moves = allValidMoves(board,player)
    #print (moves)
    if Maxturn:
        for x in moves:
            score = miniMax(nextBoard(board,player,x),oppPlayer,alpha,beta,depth+1, Maxturn = False)#wieght equation
            if score > alpha:
                alpha = score
                movelist.append(x)
                coslist.append(alpha)
                movedict[alpha] = str(x)
            if alpha >= beta:
                return alpha
        return alpha
    else:
        for x in moves:
            score = miniMax(nextBoard(board,player,x),oppPlayer,alpha,beta,depth +1, Maxturn = True)
            if score < beta:
                beta = score
                #movelist.append(x)
                #coslist.append(beta)
                #print ('this is')
                #print (x)
                movedict[beta] = str(x)
            if alpha >= beta:
                return beta
        #print (movelist)
        #print (coslist)

        return beta

def evaluateBoard(board, alpha):
    if alpha == 'w':
        opp = 'b'
    else:
        opp = 'w'
    weight = 0
    countX = -1
    countI = -1
    for x in board:
        countX += 1
        countI = -1
        for i in x:
            countI += 1
            if i == alpha:
                if [countX,countI] in [[0,0],[0,7],[7,7],[7,0]]:
                    weight += 16
                elif [countX,countI] in [[1,0],[0,1],[0,6],[1,7],[6,0],[7,1],[7,6],[6,7]]:
                    weight -= 5
                elif [countX,countI] in [[1,1],[1,6],[6,1],[6,6]]:
                    weight -= 4
                elif [countX,countI] in [[2,0],[0,2],[0,5],[2,7],[5,7],[7,5],[7,2],[5,0]]:
                    weight += 1.5
                elif [countX,countI] in [[3,0],[4,0],[0,3],[0,4],[3,7],[4,7],[7,3],[7,4]]:
                    weight += 0.6
                elif [countX,countI] in  [[1,2],[1,3],[1,4],[1,5],[2,1],[3,1],[4,1],[5,1],[6,2],[6,3],[6,4],[6,5],[2,6],[3,6],[4,6],[5,6]]:
                    weight -= 0.2
                elif [countX,countI] in [[2,2],[2,5],[5,2],[5,5]]:
                    weight += 0.5
                else:
                    weight += 0.5
            elif i != 0:
                if [countX,countI] in [[0,0],[0,7],[7,7],[7,0]]:
                    weight -= 16
                elif [countX,countI] in [[1,0],[0,1],[0,6],[1,7],[6,0],[7,1],[7,6],[6,7]]:
                    weight += 5
                elif [countX,countI] in [[1,1],[1,6],[6,1],[6,6]]:
                    weight += 4
                elif [countX,countI] in [[2,0],[0,2],[0,5],[2,7],[5,7],[7,5],[7,2],[5,0]]:
                    weight -= 1.5
                elif [countX,countI] in [[3,0],[4,0],[0,3],[0,4],[3,7],[4,7],[7,3],[7,4]]:
                    weight -= 0.6
                elif [countX,countI] in  [[1,2],[1,3],[1,4],[1,5],[2,1],[3,1],[4,1],[5,1],[6,2],[6,3],[6,4],[6,5],[2,6],[3,6],[4,6],[5,6]]:
                    weight += 0.2
                elif [countX,countI] in [[2,2],[2,5],[5,2],[5,5]]:
                    weight -= 0.5
                else:
                    weight -= 0.5
    weight += countWedges(board,alpha) * 0.5
    disparity = calculateScore(board,alpha) - calculateScore(board,opp)
    weight += disparity
    return weight

def wedge(board,player,row,col):
    #print([row,col])
    opp = 0
    if player == 'w':
        opp = 'b'
    else:
        opp = 'w'
    if [row,col] in [[0,1],[0, 2],[0,3],[0,4],[0,5],[0,6],[7,1],[7,2],[7,3],[7,4],[7,5],[7,6]]:
        if board[row][col+1] == opp and board[row][col-1] == opp and board[row][col] == player:
            #print([row,col])
            return True
        else:
            return False
    elif [row,col] in [[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[1,7],[2,7],[3,7],[4,7],[5,7],[6,7]]:
        if board[row+1][col] == opp and board[row-1][col] == opp and board[row][col] == player:
            #print([row,col])
            return True
        else:
            return False
    elif [row,col] == [7,0]:
        if board[row-1][col] == opp and board[row][col+1] == opp and board[row-1][col+1]== opp:
            return True
        else:
            return False
    elif [row,col] == [0,0]:
        if board[row+1][col] == opp and board[row][col+1] == opp and board[row+1][col+1]== opp:
            return True
        else:
            return False
    elif [row,col] == [7,7]:
        if board[row-1][col] == opp and board[row][col-1] == opp and board[row-1][col-1]== opp:
            return True
        else:
            return False
    elif [row,col] == [0,7]:
        if board[row+1][col] == opp and board[row][col-1] == opp and board[row+1][col-1]== opp:
            return True
        else:
            return False
    else:
        return False

def countWedges(board,player):
    wedgeCount = 0
    for y in range(n):
        for x in range(n):
            if wedge(board, player,y,x):
                wedgeCount += 1
    return wedgeCount

def safeSide(board,player,row,col):
    if [row,col] in [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[7,1],[7,2],[7,3],[7,4],[7,5],[7,6],

def safePiece(board,player,row,col):
    if board[row][col] == player:
        if [row,col] in [[0,0],[0,7],[7,0],[7,7]]:
            return True
        elif safeSide(board,player,row,col):
            return True



#miniMax(gameBoard,currentPlayer)
#maxValue = miniMax(gameBoard,currentPlayer)
#listPos = coslist.index(maxValue)
#print( movelist[listPos])

def endvalue(function):
    global coslist
    global movelist
    global hlist
    maxValue = function
    listPos = coslist.index(maxValue)
    hlist = []
    return(movelist[listPos])


def randomGamey():
    while len(allValidMoves(gameBoard,currentPlayer)) > 0:
        minimaxMove()


def click(x,y):
    move(whichRow(y), whichColumn(x))
    #minimaxMove()

s.onclick(click)
