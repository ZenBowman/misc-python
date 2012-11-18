import random

INITIAL_ACCEPTANCE_PROBABILITY = 0.95
EPSILON = 0.01

def simulated_anneal(problem):
	acceptance_probability = INITIAL_ACCEPTANCE_PROBABILITY
	while (problem.heuristic() != 0):
		currentH = problem.heuristic()
		problem.random_move()
		newH = problem.heuristic()
		if (newH > currentH):
			coinflip = random.random()
			if (coinflip > acceptance_probability):
				problem.revoke()
		acceptance_probability -= EPSILON
	return problem