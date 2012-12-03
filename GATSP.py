import random
import SelectionSort
import TSP

MUTATION_PROBABILITY = 0.1
SELECTION_PROBABILITIES = [0.25, 0.2, 0.15, 0.12, 0.11, 0.1, 0.07]	


def sort_by_fitness(population, data):
	m = lambda x: TSP.tourcost(data, x)
	return SelectionSort.selection_sort_by_func(population, m)

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
	child = TSP.partially_mapped_crossover(dad, mom)
	return child

def mutate(child):
	return child

def genetic_algorithm(population, data):
	new_population = []
	population = sort_by_fitness(population, data)
	i = 0
	for i in range(100):
		i += 1
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
				child = mutate(child)
			new_population.append(child)
		population = sort_by_fitness(new_population, data)
	return population

def random_soln(data):
	tour = []
	candidates = []
	for item in data.keys():
		candidates.append(item)
	tour.append(candidates[0])
	while len(tour) < len(candidates):
		dice = random.randint(1, len(candidates)-1)
		if candidates[dice] not in tour:
			tour.append(candidates[dice])
	tour.append(candidates[0])
	return tour

def analyze_pop(data, population):
	for person in population:
		print "%s : %s" % (str(person), str(TSP.tourcost(data, person)))
	print "-----------------------"

def initiate_genetic_algorithm():
	data = TSP.generateTSP(8) # create a new TSP
	population = []
	for i in range(0,8):
		population.append(random_soln(data))
	analyze_pop(data, population)
	finalpop = genetic_algorithm(population, data)
	analyze_pop(data, finalpop)

if __name__ == "__main__":
	initiate_genetic_algorithm()
