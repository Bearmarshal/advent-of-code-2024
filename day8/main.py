import io
import itertools
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position

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
