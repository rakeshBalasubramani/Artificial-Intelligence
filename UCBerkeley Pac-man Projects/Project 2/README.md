Project 2: Multi-Agent Pacman
=============================

Introduction
------------

In this project, you will design agents for the classic version of Pacman, including ghosts. Along the way, you will
implement both minimax and expectimax search and try your hand at evaluation function design.

As in project 1, this project includes an autograder for you to grade your answers on your machine. This can be run on
all questions with the command:

    python autograder.py

To run it on a spefic question N without graphics, use:

    python autograder.py -q qN --no-graphics

Questions
---------

**Question 1: Multi-Agent Pacman (3 points)**

First, play a game of classic Pacman:

    python pacman.py

Now, run the provided ReflexAgent in multiAgents.py:

    python pacman.py -p ReflexAgent

Note that it plays quite poorly even on simple layouts:

    python pacman.py -p ReflexAgent -l testClassic

Inspect its code (in multiAgents.py) and make sure you understand what it's doing.

Improve the ReflexAgent in multiAgents.py to play respectably. The provided reflex agent code provides some helpful
examples of methods that query the GameState for information. A capable reflex agent will have to consider both food
locations and ghost locations to perform well.

**Question 2: MiniMax Agent (4 points)**

Now you will write an adversarial search agent in the provided MinimaxAgent class stub in multiAgents.py. Your minimax
agent should work with any number of ghosts, so you'll have to write an algorithm that is slightly more general than
what you've previously seen in lecture. In particular, your minimax tree will have multiple min layers (one for each
ghost) for every max layer. Your code should also expand the game tree to an arbitrary depth.

**Question 3: Alpha-Beta pruning (4 points)**

Make a new agent that uses alpha-beta pruning to more efficiently explore the minimax tree, in AlphaBetaAgent.
You should see a speed-up (perhaps depth 3 alpha-beta will run as fast as depth 2 minimax).

**Question 4: Expectimax (4 points)**

Minimax and alpha-beta are great, but they both assume that you are playing against an adversary who makes optimal
decisions. As anyone who has ever won tic-tac-toe can tell you, this is not always the case.

In this question you will implement the ExpectimaxAgent, which is useful for modeling probabilistic behavior of agents
who may make suboptimal choices.

**Question 5: Better evaluation function (5 points)**

Write a better evaluation function for pacman in the provided function betterEvaluationFunction. The evaluation function
should evaluate states, rather than actions like your reflex agent evaluation function did.

**Mini Contest (2 points extra credit)**

Pacman's been doing well so far, but things are about to get a bit more challenging. This time, we'll pit Pacman against
smarter foes in a trickier maze. In particular, the ghosts will actively chase Pacman instead of wandering around
randomly, and the maze features more twists and dead-ends, but also extra pellets to give Pacman a fighting chance.

You're free to have Pacman use any search procedure, search depth, and evaluation function you like. The only limit is
that games can last a maximum of 3 minutes (with graphics off), so be sure to use your computation wisely.

Grades
------

    Question q1: 3/3
    Question q2: 4/4
    Question q3: 4/4
    Question q4: 4/4
    Question q5: 5/5
    Question extra: 0/0
    -------------------
    Total: 20/20