import random

def whoGoesFirst():
    
    if random.randint(0, 1) == 0:
        return 'Comp'
    else:
        return 'Jugador'

def playAgain():
    
    print('Jugar de nuevo? (si o no)')
    return input().lower().startswith('s')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or 
    (bo[4] == le and bo[5] == le and bo[6] == le) or 
    (bo[1] == le and bo[2] == le and bo[3] == le) or 
    (bo[7] == le and bo[4] == le and bo[1] == le) or 
    (bo[8] == le and bo[5] == le and bo[2] == le) or 
    (bo[9] == le and bo[6] == le and bo[3] == le) or 
    (bo[7] == le and bo[5] == le and bo[3] == le) or 
    (bo[9] == le and bo[5] == le and bo[1] == le)) 

def getBoardCopy(board):
    
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    
    return board[move] == ' '

def getPlayerMove(board):
    
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('Cual es su siguiente movimiento? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    if isSpaceFree(board, 5):
        return 5

    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


# print('Triqui')
# 
# while True:
#     
#     theBoard = [' '] * 10
#     playerLetter, computerLetter = inputPlayerLetter()
#     turn = whoGoesFirst()
#     print('Inicia ' + turn + '.')
#     gameIsPlaying = True
# 
#     while gameIsPlaying:
#         if turn == 'Jugador':
#             
#             drawBoard(theBoard)
#             move = getPlayerMove(theBoard)
#             makeMove(theBoard, playerLetter, move)
# 
#             if isWinner(theBoard, playerLetter):
#                 drawBoard(theBoard)
#                 print('Victoria!')
#                 gameIsPlaying = False
#             else:
#                 if isBoardFull(theBoard):
#                     drawBoard(theBoard)
#                     print('Empate')
#                     break
#                 else:
#                     turn = 'Comp'
# 
#         else:
#             
#             move = getComputerMove(theBoard, computerLetter)
#             makeMove(theBoard, computerLetter, move)
# 
#             if isWinner(theBoard, computerLetter):
#                 drawBoard(theBoard)
#                 print('Derrota!')
#                 gameIsPlaying = False
#             else:
#                 if isBoardFull(theBoard):
#                     drawBoard(theBoard)
#                     print('Empate')
#                     break
#                 else:
#                     turn = 'Jugador'
# 
#     if not playAgain():
#         break