import collections
import io
import itertools
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, CardinalDirection


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
