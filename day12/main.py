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
		garden_map = [line.strip() for line in file.readlines()]
	y_dim = len(garden_map)
	x_dim = len(garden_map[0])
	unchecked_plots = { Position(y, x) for y in range(y_dim) for x in range(x_dim) }
	checked_plots = set()

	total = 0
	while unchecked_plots:
		plot = unchecked_plots.pop()
		region_type = garden_map[plot.y][plot.x]
		unchecked_region_plots = { plot }
		region_size = 0
		region_perimeter = 0

		while unchecked_region_plots:
			plot = unchecked_region_plots.pop()
			checked_plots.add(plot)
			region_size += 1
			for direction in CardinalDirection:
				neighbor = plot + direction
				if neighbor.y not in range(y_dim) or neighbor.x not in range(x_dim) or garden_map[neighbor.y][neighbor.x] != region_type:
					region_perimeter += 1
				elif garden_map[neighbor.y][neighbor.x] == region_type and neighbor in unchecked_plots:
					unchecked_plots.remove(neighbor)
					unchecked_region_plots.add(neighbor)
		total += region_size * region_perimeter

	print("Part 1: {}".format(total))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		garden_map = [line.strip() for line in file.readlines()]
	y_dim = len(garden_map)
	x_dim = len(garden_map[0])
	unchecked_plots = { Position(y, x) for y in range(y_dim) for x in range(x_dim) }
	checked_plots = set()

	total = 0
	while unchecked_plots:
		plot = unchecked_plots.pop()
		region_type = garden_map[plot.y][plot.x]
		unchecked_region_plots = { plot }
		region_size = 0
		region_perimeter = set()

		while unchecked_region_plots:
			plot = unchecked_region_plots.pop()
			checked_plots.add(plot)
			region_size += 1
			for direction in CardinalDirection:
				neighbor = plot + direction
				if neighbor.y not in range(y_dim) or neighbor.x not in range(x_dim) or garden_map[neighbor.y][neighbor.x] != region_type:
					region_perimeter.add((plot, direction))
				elif garden_map[neighbor.y][neighbor.x] == region_type and neighbor in unchecked_plots:
					unchecked_plots.remove(neighbor)
					unchecked_region_plots.add(neighbor)
		num_sides = 0
		while region_perimeter:
			plot, direction = region_perimeter.pop()
			left = plot + direction.left()
			while ((left, direction)) in region_perimeter:
				region_perimeter.remove((left, direction))
				left = left + direction.left()
			right = plot + direction.right()
			while ((right, direction)) in region_perimeter:
				region_perimeter.remove((right, direction))
				right = right + direction.right()
			num_sides += 1
		total += region_size * num_sides

	print("Part 2: {}".format(total))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
