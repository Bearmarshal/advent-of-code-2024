import collections
import enum
import io
import itertools
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
	
	def __str__(self):
		return self.name

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
		machines = [(Direction(a_dy, a_dx), Direction(b_dy, b_dx), Position(y, x)) for a_dx, a_dy, b_dx, b_dy, x, y in (map(int, re.findall(r"\d+", machine)) for machine in file.read().split("\n\n"))]
	total = 0
	for a, b, price in machines:
		num_a = round((price.x / b.dx - price.y / b.dy) / (a.dx / b.dx - a.dy / b.dy))
		num_b = round((price.y - num_a * a.dy) / b.dy)
		if num_a in range(0, 101) and num_b in range(0, 101) and Position(0, 0) + num_a * a + num_b * b == price:
			total += 3 * num_a + num_b
	print("Part 1: {}".format(total))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		machines = [(Direction(a_dy, a_dx), Direction(b_dy, b_dx), Position(10000000000000 + y, 10000000000000 + x)) for a_dx, a_dy, b_dx, b_dy, x, y in (map(int, re.findall(r"\d+", machine)) for machine in file.read().split("\n\n"))]
	total = 0
	for a, b, price in machines:
		num_a = round((price.x / b.dx - price.y / b.dy) / (a.dx / b.dx - a.dy / b.dy))
		num_b = round((price.y - num_a * a.dy) / b.dy)
		if Position(0, 0) + num_a * a + num_b * b == price:
			total += 3 * num_a + num_b
	print("Part 2: {}".format(total))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
