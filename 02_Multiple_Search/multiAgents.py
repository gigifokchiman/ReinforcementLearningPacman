from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import numpy as np
import sys
import os
PACKAGE_PARENT = '../A1_Search'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import searchAgents as sa

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        food_distance = min([manhattanDistance(food, newPos) for food in prevFood.asList()])
        ghost_distance = min(
            [manhattanDistance(ghost.getPosition(), newPos) for ghost in successorGameState.getGhostStates()])


        if ghost_distance < 2 or Directions.STOP in action:
            return -99999
        else:
            return 1.0 / (1.0 + food_distance)
        # return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    # Choose one of the best actions

    def maxmin_value(self, gameState, agentIndex, curDepth):

        if curDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex + 1 == gameState.getNumAgents():
            nextAgent = 0
            nextDepth = curDepth + 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = curDepth

        action_value = [self.maxmin_value(gameState.generateSuccessor(agentIndex, agentAction),
                                       nextAgent,
                                       nextDepth)
                        for agentAction in gameState.getLegalActions(agentIndex)]

        if self.index == agentIndex:
            if curDepth == 0:
                return gameState.getLegalActions()[int(np.argmax(action_value))]
            else:
                return max(action_value)
        else:
            return min(action_value)



    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.maxmin_value(gameState, 0, 0)

        # util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxmin_value_pruning(self, gameState, agentIndex, curDepth, alpha=np.NINF, beta=np.Inf):

        best_action = ""

        if curDepth == self.depth or gameState.isWin() or gameState.isLose():


            return self.evaluationFunction(gameState)


        if agentIndex + 1 == gameState.getNumAgents():
            nextAgent = 0
            nextDepth = curDepth + 1

        else:
            nextAgent = agentIndex + 1
            nextDepth = curDepth

        if self.index == agentIndex:
            value = np.NINF
            for agentAction in gameState.getLegalActions(agentIndex):
                # max
                action_value = self.maxmin_value_pruning(gameState.generateSuccessor(agentIndex, agentAction),
                                                             nextAgent,
                                                             nextDepth, alpha, beta)
                if action_value > value:
                    value = action_value
                    if curDepth == 0 and agentIndex == 0:
                        best_action = agentAction

                alpha = max(alpha, value)

                if alpha > beta:
                    break

            if curDepth == 0:

                return best_action
            else:
                return value
        else:
            value = np.Inf
            for agentAction in gameState.getLegalActions(agentIndex):
                action_value = self.maxmin_value_pruning(gameState.generateSuccessor(agentIndex, agentAction),
                                                        nextAgent,
                                                        nextDepth, alpha, beta)
                value = min(value, action_value)
                beta = min(beta, value)

                if alpha > beta:
                    break
            return value

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        return self.maxmin_value_pruning(gameState, 0, 0)

# util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

     # def expectimax_value(self, gameState, agentIndex, curDepth):
    #     if curDepth == self.depth or gameState.isWin() or gameState.isLose():
    #         return self.evaluationFunction(gameState)
    #
    #     if agentIndex + 1 == gameState.getNumAgents():
    #         nextAgent = 0
    #         nextDepth = curDepth + 1
    #     else:
    #         nextAgent = agentIndex + 1
    #         nextDepth = curDepth
    #
    #     action_value = [self.expectimax_value(gameState.generateSuccessor(agentIndex, agentAction),
    #                                    nextAgent,
    #                                    nextDepth)
    #                     for agentAction in gameState.getLegalActions(agentIndex)]
    #
    #
    #     if self.index == agentIndex:
    #         if curDepth == 0:
    #             return gameState.getLegalActions()[int(np.argmax(action_value))]
    #         else:
    #             return max(action_value)
    #     else:
    #         n = len(gameState.getLegalActions(agentIndex))
    #
    #         return float(sum(action_value)/ n)
    #
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """
        "*** YOUR CODE HERE ***"
        # calling expectimax with the depth we are going to investigate
        maxDepth = self.depth * gameState.getNumAgents()
        return self.expectimax(gameState, "expect", maxDepth, 0)[0]

    def expectimax(self, gameState, action, depth, agentIndex):

        if depth is 0 or gameState.isLose() or gameState.isWin():
            return (action, self.evaluationFunction(gameState))

        # if pacman (max agent) - return max successor value
        if agentIndex is 0:
            return self.maxvalue(gameState,action,depth,agentIndex)
        # if ghost (EXP agent) - return probability value
        else:
            return self.expvalue(gameState,action,depth,agentIndex)

    def maxvalue(self,gameState,action,depth,agentIndex):
        bestAction = ("max", -(float('inf')))
        for legalAction in gameState.getLegalActions(agentIndex):
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            succAction = None
            if depth != self.depth * gameState.getNumAgents():
                succAction = action
            else:
                succAction = legalAction
            succValue = self.expectimax(gameState.generateSuccessor(agentIndex, legalAction),
                                        succAction,depth - 1,nextAgent)
            bestAction = max(bestAction,succValue,key = lambda x:x[1])
        return bestAction

    def expvalue(self,gameState,action,depth,agentIndex):
        legalActions = gameState.getLegalActions(agentIndex)
        averageScore = 0
        propability = 1.0/len(legalActions)
        for legalAction in legalActions:
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            bestAction = self.expectimax(gameState.generateSuccessor(agentIndex, legalAction),
                                         action, depth - 1, nextAgent)
            averageScore += bestAction[1] * propability
        return (action, averageScore)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # return self.expectimax_value(gameState, 0, 0)
        # util.raiseNotDefined()
        maxDepth = self.depth * gameState.getNumAgents()
        return self.expectimax(gameState, "expect", maxDepth, 0)[0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

      //TODO
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)

    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    Capsules = currentGameState.getCapsules()


    # "*** YOUR CODE HERE ***"
    #
    # food_distance = min([manhattanDistance(food, Pos) for food in Food.asList()])
    #
    # ghost_distance = min(
    #      [manhattanDistance(ghost.getPosition(), Pos) for ghost in currentGameState.getGhostStates()])
    # capsule_distance = min(
    #      [manhattanDistance(cap, Pos) for cap in Capsules])
    # # if ghost_distance < 2 or Directions.STOP in action:
    # #     return -99999
    # # else:
    # actions = currentGameState.getLegalActions()


    # return currentGameState.getScore() + 1/(food_distance + 1)

    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()

    minFoodist = float('inf')
    for food in newFood:
        minFoodist = min(minFoodist, manhattanDistance(newPos, food))

    ghostDist = 0
    for ghost in currentGameState.getGhostPositions():
        ghostDist = manhattanDistance(newPos, ghost)
        if (ghostDist < 2):
            return -float('inf')

    foodLeft = currentGameState.getNumFood()
    capsLeft = len(currentGameState.getCapsules())

    foodLeftMultiplier = 950050
    capsLeftMultiplier = 10000
    foodDistMultiplier = 950

    additionalFactors = 0
    if currentGameState.isLose():
        additionalFactors -= 50000
    elif currentGameState.isWin():
        additionalFactors += 50000

    return 1.0/(foodLeft + 1) * foodLeftMultiplier + ghostDist + \
           1.0/(minFoodist + 1) * foodDistMultiplier + \
           1.0/(capsLeft + 1) * capsLeftMultiplier + additionalFactors


# util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
