import random

board = ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"]

currentPlayer = "x"
winner = None
gameRunning = True

def newBoard(board):
      print(board[0], board[1], board[2])
      print(board[3], board[4], board[5])
      print(board[6], board[7], board[8])


def playerChoose(board):
      move = int(input("Enter a number 1 - 9: "))
      if move >= 1 and move <= 9 and board[move - 1] == "-":
            board[move - 1] = currentPlayer
      else:
            print("thise spot is occupied")
            playerChoose(board)


def checkForWinHrizont(board):
      global winner
      if board[0] == board[1] == board[2] and board[1] != "-":
            winner = board[0]
            return True
      elif board[3] == board[4] == board[5] and board[4] != "-":
            winner = board[3]
            return True
      elif board[6] == board[7] == board[8] and board[8] != "-":
            winner = board[6]
            return True


def checkForWinRow(board):
      global winner
      if board[0] == board[3] == board[6] and board[0] != "-":
            winner = board[0]
            return True
      elif board[1] == board[4] == board[7] and board[1] != "-":
            winner = board[1]
            return True
      elif board[2] == board[5] == board[8] and board[2] != "-":
            winner = board[2]
            return True


def checkForWinDiagonal(board):
      global winner
      if board[0] == board[4] == board[8] and board[0] != "-":
            winner = board[0]
            return True
      elif board[2] == board[4] == board[6] and board[2] != "-":
            winner = board[2]
            return True


def masterCheckForWin():
      global gameRunning
      if checkForWinHrizont(board) or checkForWinRow(board) or \
            checkForWinDiagonal(board):
            print(f"The winner is {winner}")


def checkTie(board):
      global gameRunning
      if "-" not in board:
            newBoard(board)
            print("It is a tie !!!")
            gameRunning = False


def switchPlayer():
      global currentPlayer
      if currentPlayer == "x":
            currentPlayer = "o"
      else:
            currentPlayer = "x"

def cpu(board):
      while currentPlayer == "o":
            position = random.randint(0, 8)
            if board[position] == "-":
                  board[position] = "o"
                  switchPlayer()


while gameRunning:
      newBoard(board)
      playerChoose(board)
      masterCheckForWin()
      checkTie(board)
      switchPlayer()
      cpu(board)
      masterCheckForWin()
      checkTie(board)
