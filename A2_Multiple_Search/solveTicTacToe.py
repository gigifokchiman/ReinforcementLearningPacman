#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :
#################################################################################

import copy
import util
import sys
import random
import time
from optparse import OptionParser
import numpy as np


class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything,
      however.
    """

    def __init__(self):
        """
          Represent 3 boards with lists of boolean value
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                       [False, False, False, False, False, False, False, False, False],
                       [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board)
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append(chr(b + ASCII_OF_A) + str(i))
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]:
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)


class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe.
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """

    def __init__(self):
        """
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}

    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            # check every row
            row = i * 3
            if board[row] and board[row + 1] and board[row + 2]:
                return True
            # check every column
            if board[i] and board[i + 3] and board[i + 6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])


class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8.

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.

      However, please don't modify the name and input parameters of the function getAction(),
      because autograder will call this function to check your algorithm.
    """

    def __init__(self):
        """
          You can initialize some variables here, but please do not modify the input parameters.
        """
        self.pattern_to_score_single = {}
        none = 1
        a = 2
        b = 3
        c = 5
        d = 7

        raw_patterns = {
            # Row 1
            "000000000": c,
            "100000000": none,
            "010000000": none,
            "000010000": c ** 2,
            "110000000": a * d,
            "101000000": b,
            "100010000": b,
            "100001000": b,
            "100000001": a,
            # Row 2
            "010100000": a,
            "010010000": b,
            "010000010": a,

            "110100000": b,
            "110010000": a * b,
            "110001000": d,
            "110000100": a,
            "110000010": d,
            # Row 3
            "110000001": d,
            "101010000": a,
            "101000100": a * b,
            "101000010": a,
            "100011000": a,

            "100001010": none,
            "010110000": a * b,
            "010101000": b,
            # Row 4
            "110110000": a,
            "110101000": a,
            "110100001": a,
            "110011000": b,
            # Row 5
            "110010100": b,
            "110001100": b,
            "110001010": a * b,
            "110001001": a * b,
            "110000110": b,
            "110000101": b,
            "110000011": a,
            # Row 6
            "101010010": b,
            "101000101": a,
            "100011010": b,
            "010101010": a,
            # Row 1 (p2)
            "110101001": b,
            "110011100": a,
            "110001110": a,
            "110001101": a,
            "110101011": a,

            "110101010": b
        }

        raw_patterns = {
            str([True if d == "1" else False for d in k]): v
            for k, v in raw_patterns.items()
        }

        self.winningpattern = [25, 2, 15, 9]
        for k, v in raw_patterns.items():
            pattern_list = eval(k)
            self.add_record_all_equivalent(pattern_list, v)

    def nested_list_to_string(self, nested_list):
        return str(np.hstack(nested_list))

    def add_dict(self, new_list, score):
        str = self.nested_list_to_string(new_list)
        self.pattern_to_score_single[str] = score

    def board_rotation(self, nested_list, score):
        new_list = list(map(list, zip(*nested_list)))[::-1]
        self.add_dict(new_list, score)
        return new_list

    def board_reflect_up_down(self, nested_list, score):
        new_list = list(nested_list[::-1])
        self.add_dict(new_list, score)
        return new_list

    def board_reflect_left_right(self, nested_list, score):
        new_list = list([row[::-1] for row in nested_list])
        self.add_dict(new_list, score)
        return new_list

    def board_to_nested_list(self, board, num, score):
        new_list = list(map(lambda x: board[num * x:(x + 1) * num], range(num)))
        self.add_dict(new_list, score)
        return new_list

    def add_record_all_equivalent(self, board, score):
        # add records to all equivalent boards

        equivalent_set = {}
        board_nested_0 = self.board_to_nested_list(board, 3, score)
        board_nested_1 = self.board_reflect_left_right(board_nested_0, score)
        board_nested_2 = self.board_reflect_up_down(board_nested_0, score)
        board_nested_3 = self.board_reflect_up_down(board_nested_1, score)

        # apply rotation for 3 times per each array
        for i in range(0, 3):
            board_nested_0 = self.board_rotation(board_nested_0, score)
            board_nested_1 = self.board_rotation(board_nested_1, score)
            board_nested_2 = self.board_rotation(board_nested_2, score)
            board_nested_3 = self.board_rotation(board_nested_3, score)

    def score(self, gameState, gameRules):

        if gameRules.isGameOver(gameState.boards):
            return -1
        else:
            pattern = 1
            for board in gameState.boards:
                if not gameRules.deadTest(board):
                    pattern *= self.pattern_to_score_single[str(np.hstack(board))]

            if pattern in self.winningpattern:
                return 1
            else:
                return 0

    def getAction(self, gameState, gameRules):

        actions = gameState.getLegalActions(gameRules)

        action_value = [self.score(gameState.generateSuccessor(action), gameRules)
                        for action in actions]

        return actions[int(np.argmax(action_value))]


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two
      random agents fight with each other.
    """

    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """

    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action


class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """

    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players.
        """
        self.numOfGames = numOfGames
        self.muteOutput = muteOutput
        self.maxTimeOut = 30

        self.AIforHuman = AIforHuman
        self.gameRules = GameRules()
        self.AIPlayer = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()

        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI
          exceed this time limit, this function will throw an error prompt and return.
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0  # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0:
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (
                        agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i + 1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i + 1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    # random.seed(1)
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
