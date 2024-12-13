import collections
import io
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, CardinalDirection


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
