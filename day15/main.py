import collections
import io
import itertools
import math
import os
import re
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, CardinalDirection
import aoclib.inputreader as inputreader

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		warehouse_map_string, movements_string = file.read().split("\n\n")
	warehouse_map = [[c for c in line.strip()] for line in warehouse_map_string.strip().splitlines()]
	movements = [CardinalDirection.from_glyph(glyph) for glyph in movements_string.strip() if glyph in "<>^v"]

	warehouse_dim_y = range(len(warehouse_map))
	warehouse_dim_x = range(len(warehouse_map[0]))
	for y in warehouse_dim_y:
		for x in warehouse_dim_x:
			if warehouse_map[y][x] == "@":
				robot = Position(y, x)

	for movement in movements:
		to_move = [robot]
		new_pos = robot + movement
		while new_pos[warehouse_map] == "O":
			to_move.append(new_pos)
			new_pos = new_pos + movement
		if new_pos[warehouse_map] == ".":
			for pos in reversed(to_move):
				(pos + movement)[warehouse_map] = pos[warehouse_map]
			robot[warehouse_map] = "."
			robot += movement
	coordinate_sum = sum(100 * y + x for y in warehouse_dim_y for x in warehouse_dim_x if warehouse_map[y][x] == "O")
	print("Part 1: {}".format(coordinate_sum))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		warehouse_map_string, movements_string = file.read().split("\n\n")
	warehouse_map = [[c for c in line.strip().translate({ord("#"): "##", ord("O"): "[]", ord("."): "..", ord("@"): "@."})] for line in warehouse_map_string.strip().splitlines()]
	movements = [CardinalDirection.from_glyph(glyph) for glyph in movements_string.strip() if glyph in "<>^v"]
	warehouse_dim_y = range(len(warehouse_map))
	warehouse_dim_x = range(len(warehouse_map[0]))
	for y in warehouse_dim_y:
		for x in warehouse_dim_x:
			if warehouse_map[y][x] == "@":
				robot = Position(y, x)

	for movement in movements:
		to_move = [robot]
		new_pos = robot + movement
		to_check = collections.deque([new_pos])
		while to_check:
			new_pos = to_check.popleft()
			if new_pos[warehouse_map] == "#":
				break
			if new_pos[warehouse_map] in "[]":
				to_move.append(new_pos)
				to_check.append(new_pos + movement)
				if movement in (CardinalDirection.NORTH, CardinalDirection.SOUTH):
					other_half = new_pos + (CardinalDirection.EAST if new_pos[warehouse_map] == "[" else CardinalDirection.WEST)
					to_move.append(other_half)
					if other_half in to_check:
						to_check.remove(other_half)
					to_check.append(other_half + movement)
		else:
			for pos in reversed(to_move):
				(pos + movement)[warehouse_map] = pos[warehouse_map]
				pos[warehouse_map] = "."
			robot += movement
		
	coordinate_sum = sum(100 * y + x for y in warehouse_dim_y for x in warehouse_dim_x if warehouse_map[y][x] == "[")
	print("Part 2: {}".format(coordinate_sum))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
