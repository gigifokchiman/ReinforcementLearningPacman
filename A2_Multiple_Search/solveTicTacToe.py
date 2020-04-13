#############################################################################
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
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
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
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
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


    def getAction(self, gameState, gameRules):

        """
        The target: is to make sure that the game ends with odd number of future moves.
        What can we do to change if the board with end with odd/even numver of future moves.
        - change the pattern of single board.
        - design what board we should change (to kill some board or change its odd/even nature).

        In theory, we could try every combinations but it will definitely run out of time.

        The video below has simplified the game using 2 layers of template matching
        - the first layer: (A) the cross pattern ---> (B) whether the board could be ended with odd/even number of moves.
        - the second layer: (B) --> (B) final winning condition of the game

        https://www.youtube.com/watch?v=h09XU8t8eUM

        For this exercise, I am not going to use template matching.
        First, the machine could not afford to evaluate all actions of 3 boards jointly but
        could afford the computation of 3 separate boards within the time limit. We don't need
        to use the 1st layer of template matching and we could apply what we learn in the multiple agent problem.

        For the second layer, we could model the reward with a similar manner so the agent will know what to do next.

        # max score: 8; this is the early stopping condition to save time"
        # Step 1: to evaluate the score if there is no move"
        # Step 2: to evaluate the score if there is one move

        """

        # Step 1: pre-trained the score of a single board  -> serve as hueristic
        # could be saved for future use; for the assignment purpose, I won't save it.

        self.pattern_to_score_single = self.maxmin_value(gameState, gameRules, 0, 0)

        print(self.pattern_to_score_single)


    def score_single(self, turns):
        # AI prefers odd number of future moves.
        if turns % 2 == 0:
            return 1
        else:
            return -1

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
        for i in range (0, 3):
            board_nested_0 = self.board_rotation(board_nested_0, score)
            board_nested_1 = self.board_rotation(board_nested_1, score)
            board_nested_2 = self.board_rotation(board_nested_2, score)
            board_nested_3 = self.board_rotation(board_nested_3, score)


    def maxmin_value(self, gameState, gameRules, turns, boardNum):

        print(f"turns:{turns}; boardNum:{boardNum}")

        if gameRules.deadTest(gameState.boards[boardNum]):
            score = self.score_single(turns)
            self.add_record_all_equivalent(gameState.boards[boardNum], score)
            # print(score)
            # print(self.pattern_to_score_single)
            return score

        hashed_board = str(np.hstack(gameState.boards[boardNum]))
        if hashed_board in self.pattern_to_score_single.keys():
            return self.pattern_to_score_single[hashed_board]

        actions = gameState.getLegalActions(gameRules)

        if boardNum == 0:
            temp = copy.deepcopy(actions)
            actions = [action for action in temp if action.startswith("A")]

        print(f"turns:{turns}; boardNum:{boardNum}; actions:")
        # print(actions)

        action_value = [self.maxmin_value(gameState.generateSuccessor(action),
                                          gameRules, turns + 1, boardNum)
                        for action in actions]

        if turns % 2 == 0:
            if turns == 0:
                # TODO
                print (self.pattern_to_score_single)
                return 0
            else:
                max_val = max(action_value)
                optimal_action = []
                for key, val in enumerate(action_value):
                    if val == max_val:
                        optimal_action.append(gameState.getLegalActions(gameRules)[key])
                for action in optimal_action:
                    self.add_record_all_equivalent(gameState.generateSuccessor(action).boards[boardNum], max_val)
                return max_val
        else:
            min_val = max(action_value)
            optimal_action = []
            for key, val in enumerate(action_value):
                if val == min_val:
                    optimal_action.append(gameState.getLegalActions(gameRules)[key])
            for action in optimal_action:
                self.add_record_all_equivalent(gameState.generateSuccessor(action).boards[boardNum], min_val)
            return min_val

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
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

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
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
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

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

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
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
