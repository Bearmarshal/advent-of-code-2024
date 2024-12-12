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
		city_map = [line.strip() for line in file.readlines()]
	city_dim_y = range(len(city_map))
	city_dim_x = range(len(city_map[0]))
	antinodes = set()

	antennas = {}
	for y in city_dim_y:
		for x in city_dim_x:
			if city_map[y][x] != ".":
				antennas.setdefault(city_map[y][x], []).append(Position(y, x))

	for _, positions in antennas.items():
		for antenna_a, antenna_b in itertools.permutations(positions, 2):
			antinode = antenna_b + (antenna_b - antenna_a)
			if antinode.y in city_dim_y and antinode.x in city_dim_x:
				antinodes.add(antinode)

	print("Part 1: {}".format(len(antinodes)))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		city_map = [line.strip() for line in file.readlines()]
	city_dim_y = range(len(city_map))
	city_dim_x = range(len(city_map[0]))
	antinodes = set()

	antennas = {}
	for y in city_dim_y:
		for x in city_dim_x:
			if city_map[y][x] != ".":
				antennas.setdefault(city_map[y][x], []).append(Position(y, x))

	for _, positions in antennas.items():
		for antenna_a, antenna_b in itertools.permutations(positions, 2):
			n = 0
			while True:
				antinode = antenna_b + n * (antenna_b - antenna_a)
				if antinode.y not in city_dim_y or antinode.x not in city_dim_x:
					break
				antinodes.add(antinode)
				n += 1

	print("Part 2: {}".format(len(antinodes)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
