import random
import sys
import SimulatedAnnealing

# positions are represented by tuples (1,3), (0,2), etc
QUEENCOUNTER = 1

class Queen:
	def __init__ (self, position):
		global QUEENCOUNTER
		self.name = "Queen%s" % QUEENCOUNTER
		QUEENCOUNTER += 1
		self.position = position

	def clash_exists(self, other_queen):
		if (self.position[0] == other_queen.position[0]):
			return True
		if (self.position[1] == other_queen.position[1]):
			return True
		diff_x = self.position[0] - other_queen.position[0]
		diff_y = self.position[1] - other_queen.position[1]
		if (abs(diff_x) == abs(diff_y)):
			return True
	
	def __repr__ (self):
		return self.name

	def move(self, newpos):
		self.lastpos = self.position
		self.position = newpos

	def revoke(self):
		self.position = self.lastpos

class EightQueens:
	def __init__ (self, queens):
		self.queens = queens

	def __repr__(self):
		a = []
		for j in range(0,8):
			a.append(self.queens[j].position[1])
		return str(a) + ":" + str(self.heuristic())

	def draw(self):
		print "-------------------------"
		print "Clashes = %s" % self.heuristic()
		print "-------------------------"	
		for j in range(0,8):
			for i in range(0,8):
				if self.queens[i].position[1] == j:
					sys.stdout.write("x ")
				else:
					sys.stdout.write("o ")
			print " " 		
		print "-------------------------"			
	
	def calculate_clashes(self):
		clashes = []
		for i in range(0,8):
			for j in range(i+1, 8):
				if self.queens[i].clash_exists(self.queens[j]):
					clashes.append([self.queens[i], self.queens[j]])
		return clashes

	def heuristic (self):
		return len(self.calculate_clashes())

	def random_move(self):
		queenToMove = random.randint(0,7)
		newPosition = random.randint(0,7)
		self.queens[queenToMove].move((queenToMove, newPosition))
		self.lastQueenMoved = self.queens[queenToMove]

	def revoke(self):		
		self.lastQueenMoved.revoke()		

if __name__ == "__main__":
	q0 = Queen((0,4))
	q1 = Queen((1,5))
	q2 = Queen((2,6))
	q3 = Queen((3,3))
	q4 = Queen((4,4))
	q5 = Queen((5,5))
	q6 = Queen((6,6))
	q7 = Queen((7,5))
	eq = EightQueens([q0,q1,q2,q3,q4,q5,q6,q7])

	eq.draw()

	eq.random_move()
	eq.draw()

	eq.revoke()
	eq.draw()

	SimulatedAnnealing.simulated_anneal(eq)
	eq.draw()