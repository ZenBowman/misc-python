import random
import SelectionSort
import EightQueens

MUTATION_PROBABILITY = 0.1
SELECTION_PROBABILITIES = [0.25, 0.2, 0.15, 0.12, 0.11, 0.1, 0.07]	

def sort_by_fitness(population):
	return SelectionSort.selection_sort_by_heuristic(population)

def random_selection(population):
	# Random selection algorithm - first rank population by fitness, then
	sum = 0.0
	goal = random.random()
	i = 0
	while 1:
		sum = sum + SELECTION_PROBABILITIES[i]
		if (sum > goal):
			return (population[i], i)
		i += 1
	return (population[7], 7)	

def reproduce(dad, mom):
	#print "dad"
	#dad.draws()
	#print "mom"
	#mom.draws()
	l = random.randint(0,7)
	queens = []
	for i in range(l):
		queens.append(EightQueens.Queen(dad.queens[i].position))
	for i in range(l,8):
		queens.append(EightQueens.Queen(mom.queens[i].position))		
	eq = EightQueens.EightQueens(queens)
	#eq.draw()
	#print "son"
	#eq.draws()
	return eq

def mutate(child):
	child.random_move()
	return child

def genetic_algorithm(population):
	new_population = []
	population = sort_by_fitness(population)
	i = 0
	while 1:
		i += 1
		if (i%100 == 0):
			print population
		new_population = []
		for i in range(len(population)):
			xt = random_selection(population)
			yt = random_selection(population)
			while (yt[1] == xt[1]):
				yt = random_selection(population)
			x = xt[0]
			y = yt[0]
			child = reproduce(x, y)
			dice = random.random()
			if (dice < MUTATION_PROBABILITY):
				if child.heuristic() == 0:
					return child
				child = mutate(child)
			new_population.append(child)
			if child.heuristic() == 0:
				print "Solved"
				return child
		#print ("Items in population: " + str(len(population)))
		population = sort_by_fitness(new_population)
		#print ("Items in population: " + str(len(population)))
	return population

def create_random_queen(column):
	l = random.randint(0,7)
	q = EightQueens.Queen((column, l))
	return q

def create_random_eq():
	queens = []
	for i in range(0,8):
		queens.append(create_random_queen(i))
	eq = EightQueens.EightQueens(queens)
	return eq

def initiate_genetic_algorithm():
	population = []
	for i in range(0,8):
		population.append(create_random_eq())
	return genetic_algorithm(population)

if __name__ == "__main__":
	print initiate_genetic_algorithm()
