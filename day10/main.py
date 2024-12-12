import collections
import enum
import io
import os
import re
import sys

class EnumContainsValueMeta(enum.EnumMeta):
	def __contains__(cls, value):
		return value in cls.__members__.values()

class Direction(tuple):
	def __new__(cls, dy, dx):
		self = tuple.__new__(cls, (dy, dx))
		self.dy = dy
		self.dx = dx
		return self

	def __neg__(self):
		return Direction(-self.dy, -self.dx)

	def __add__(self, other):
		return Direction(self.dy + other.dy, self.dx + other.dx)
	
	def __sub__(self, other):
		return Direction(self.dy - other.dy, self.dx - other.dx)
	
	def __mul__(self, value):
		return Direction(self.dy * value, self.dx * value)
	
	def __rmul__(self, value):
		return self.__mul__(value)
	
class CardinalDirection(Direction, enum.Enum):
	def __new__(cls, dy, dx):
		self = Direction.__new__(cls, dy, dx)
		self._value_ = (dy, dx)
		return self

	def __neg__(self):
		return CardinalDirection((-self.dy, -self.dx))

	def opposite(self):
		return -self

	def right(self):
		return CardinalDirection((self.dx, -self.dy))

	def left(self):
		return CardinalDirection((-self.dx, self.dy))

	@classmethod
	def from_glyph(cls, glyph):
		match glyph:
			case "^": return cls.NORTH
			case "v": return cls.SOUTH
			case "<": return cls.WEST
			case ">": return cls.EAST

	NORTH = (-1, 0)
	SOUTH = (1, 0)
	WEST = (0, -1)
	EAST = (0, 1)

class Position(tuple):
	def __new__(cls, y, x):
		self = tuple.__new__(cls, (y, x))
		self.y = y
		self.x = x
		return self

	def __add__(self, direction: Direction):
		return Position(self.y + direction.dy, self.x + direction.dx)
	
	def __sub__(self, other):
		return Direction(self.y - other.y, self.x - other.x)

	def get_manhattan_distance(self, other):
		return abs(self.y - other.y) + abs(self.x - other.x)


def part1(filename):
	with io.open(filename, mode = 'r') as file:
		topographic_map = [[int(x) for x in re.findall("\d", line)] for line in file.readlines()]
	trailheads = set()
	y_dim = len(topographic_map)
	x_dim = len(topographic_map[0])
	for y in range(y_dim):
		for x in range(x_dim):
			if topographic_map[y][x] == 0:
				trailheads.add(Position(y, x))

	total = 0
	for trailhead in trailheads:
		open_set = collections.deque([trailhead])
		closed_set = {trailhead}
		score = 0
		while open_set:
			current = open_set.popleft()
			current_height = topographic_map[current.y][current.x]
			if current_height == 9:
				score += 1
			else:
				for direction in CardinalDirection:
					neighbor = current + direction
					if neighbor.y in range(y_dim) and neighbor.x in range(x_dim) and topographic_map[neighbor.y][neighbor.x] == current_height + 1 and neighbor not in closed_set:
						open_set.append(neighbor)
						closed_set.add(neighbor)
		total += score
	print("Part 1: {}".format(total))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		topographic_map = [[int(x) for x in re.findall("\d", line)] for line in file.readlines()]
	trailheads = set()
	y_dim = len(topographic_map)
	x_dim = len(topographic_map[0])
	for y in range(y_dim):
		for x in range(x_dim):
			if topographic_map[y][x] == 0:
				trailheads.add(Position(y, x))

	total = 0
	for trailhead in trailheads:
		open_set = collections.deque([trailhead])
		rating = 0
		while open_set:
			current = open_set.popleft()
			current_height = topographic_map[current.y][current.x]
			if current_height == 9:
				rating += 1
			else:
				for direction in CardinalDirection:
					neighbor = current + direction
					if neighbor.y in range(y_dim) and neighbor.x in range(x_dim) and topographic_map[neighbor.y][neighbor.x] == current_height + 1 and neighbor:
						open_set.append(neighbor)
		total += rating
	print("Part 2: {}".format(total))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
