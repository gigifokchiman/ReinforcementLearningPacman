import mdp, util

from learningAgents import ValueEstimationAgent
import numpy as np

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for ite in range(0, self.iterations):
            temp_value = util.Counter()
            # find terminal states
            for state in mdp.getStates():
                actions = mdp.getPossibleActions(state)

                if mdp.isTerminal(state) or not actions:
                    temp_value[state] = mdp.getReward(state, "", "")
                else:
                    temp_value[state] = max([self.computeQValueFromValues(state, action) for action in actions])

            self.values = temp_value

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        return sum([prob * (
                    self.mdp.getReward(state, action, nextState) +
                    self.discount * self.getValue(nextState))
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action)])

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        actions = self.mdp.getPossibleActions(state)
        if self.mdp.isTerminal(state) or not actions:
            return None
        else:
            values = [self.computeQValueFromValues(state, action)
                         for action in actions]

            return actions[int(np.argmax(values))]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
