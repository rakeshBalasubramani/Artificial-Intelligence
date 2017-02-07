# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from util import Queue
from game import Directions
import random, util
from game import Agent
bfsDistCache = {}
class ReflexAgent(Agent):

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) 
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        distfromghost = 0;
        for i in range(len(newGhostStates)):
            distfromghost += util.manhattanDistance(successorGameState.getGhostPosition(i+1), newPos)
        score = max(distfromghost,6) + successorGameState.getScore()
        foodlist = newFood.asList();
        closestfood = 100;
        for foodpos in foodlist:
            thisdist = util.manhattanDistance(foodpos, newPos)
            if (thisdist < closestfood):
                closestfood = thisdist
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 100
        if action == Directions.STOP:
            score -= 3
        score -= 3 * closestfood
        capsuleplaces = currentGameState.getCapsules()
        if successorGameState.getPacmanPosition() in capsuleplaces:
            score += 120
        return score
        
def scoreEvaluationFunction(currentGameState):

    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        res = self.bestAction(gameState, 0)
        return res[0]

    def bestAction(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxPacman(gameState, depth)
        else:
            return self.maxGhost(gameState, depth)

    def maxGhost(self, gameState, depth):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))
        min_val = (None,float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.bestAction(succ, depth+1)
            if res[1] < min_val[1]:
                min_val = (action, res[1])
        return min_val

    def maxPacman(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))
        max_val = (None, -float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.bestAction(succ, depth+1)
            if res[1] > max_val[1]:
                max_val = (action, res[1])
        return max_val

class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        res = self.bestAction(gameState, 0, -float("inf"), float("inf"))
        return res[0]

    def bestAction(self, gameState, depth, a, b):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxPacman(gameState, depth, a, b)
        else:
            return self.maxGhost(gameState, depth, a, b)

    def maxGhost(self, gameState, depth, a, b):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))
        min_val = (None,float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.bestAction(succ, depth+1, a, b)
            if res[1] < min_val[1]:
                min_val = (action, res[1])
            if min_val[1] < a:
                return min_val
            b = min(b, min_val[1])
        return min_val

    def maxPacman(self, gameState, depth, a, b):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))
        max_val = (None, -float("inf"))
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.bestAction(succ, depth+1, a, b)
            if res[1] > max_val[1]:
                max_val = (action, res[1])
            if max_val[1] > b:
                return max_val
            a = max(a, max_val[1])
        return max_val

class ExpectimaxAgent(MultiAgentSearchAgent):
    def expectimax(self, gameState, depth, agentIndex=0):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return ( self.evaluationFunction(gameState), )
        numAgents = gameState.getNumAgents()
        newDepth = depth if agentIndex != numAgents - 1 else depth - 1
        newAgentIndex = (agentIndex + 1) % numAgents
        legalActions = gameState.getLegalActions(agentIndex)

        try:
            legalActions.remove(DIRECTIONS.STOP)
        except: pass

        actionList = [ \
            (self.expectimax(gameState.generateSuccessor(agentIndex, a), \
           newDepth, newAgentIndex)[0], a) for a in gameState.getLegalActions(agentIndex)]

        if(agentIndex == 0): 
            return max(actionList)
        else:
            return ( reduce(lambda s, a: s + a[0], actionList, 0)/len(legalActions), )

    def getAction(self, gameState):
        
        return self.expectimax(gameState, self.depth)[1]
        util.raiseNotDefined()

def bfsDist(m, start):
    q = Queue()
    q.push(start)
    m[ start[0] ][ start[1] ] = 0
    dvs = [(1,0), (0,1), (-1,0), (0,-1)]
    while not q.isEmpty():
        current = q.pop()
        dist = m[ current[0] ][ current[1] ]
        for dv in dvs:
            pos = (current[0] + dv[0], current[1] + dv[1])
            if pos[0]>=0 and pos[0]<m.width and \
                pos[1]>=0 and pos[1]<m.height and \
                type(m[ pos[0] ][ pos[1] ]).__name__ == 'bool' and \
                m[ pos[0] ][ pos[1] ] == False:
                m[ pos[0] ][ pos[1] ] = dist + 1
                q.push(pos)
    return m

def betterEvaluationFunction(currentGameState):
    """
    DESCRIPTION:
        The score returned by this evaluation function is defined as follows:
        score = <current state score> + 1/<dist to nearest food> + 10/<dist to nearest scared ghost>
        f there are no scared ghosts, the last term is 0.
        The term <current state score> should dominant the following terms because it it this score
        that the pacman want to maximize. By putting the distance values in the denominator, the
        maximum impact on the final score for the distance valus is N, where N is the nominator of
        the term. The nominator value of 1 and 10 are chosen imperically, which tend to make ghost-
        hunting more vital.
    """
    global bfsDistCache
    currentPos = currentGameState.getPacmanPosition()
    oldfood = currentGameState.getFood().asList() + currentGameState.getCapsules()
    try: 
        bfsDists = bfsDistCache[currentPos]
    except:
        bfsDists = bfsDistCache[currentPos] = bfsDist(currentGameState.getWalls().deepCopy(), currentPos)
    ret = currentGameState.getScore()
    ghostScaredTimer = filter(lambda i: i[0] > 0,[(s.scaredTimer, s.getPosition()) for s in currentGameState.getGhostStates()] )
    ghostsFoodDist = map(lambda i: i[1],
    filter(lambda d: d[1] < d[0],[(s[0], bfsDists[int(s[1][0])][int(s[1][1])]) for s in ghostScaredTimer]) )
    if len(ghostsFoodDist) > 0:
        ret += 10.0/min(ghostsFoodDist)
    fooddist = [bfsDists[food[0]][food[1]] for food in oldfood]
    if len(fooddist) > 0:
        ret += 1.0/min(fooddist)
    return ret

# Abbreviation
better = betterEvaluationFunction
