import collections
import io
import itertools
import math
import os
import queue
import re
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Direction, Position, CardinalDirection
from aoclib.tilemap import TileMap
import aoclib.inputreader as inputreader

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		code_map = TileMap([line.strip() for line in file if line.strip()])

	for y in code_map.y_dim:
		for x in code_map.x_dim:
			pos = Position(y, x)
			if code_map[pos] == "S":
				start = pos
			if code_map[pos] == "E":
				end = pos
	
	naive_path = code_map.bfs(start, end,
						  neighbours=lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self and code_map[neighbour] != "#"],
	)
	naive_distance = len(naive_path)
	
	code_path = { pos: (dist_start, naive_distance - dist_start) for dist_start, pos in enumerate(naive_path) }

	num_good_cheats = 0
	for pos, (dist_start, _) in code_path.items():
		for direction in CardinalDirection:
			if (landing := (pos + 2 * direction)) in code_path:
				_, dist_end = code_path[landing]
				if dist_start + 2 + dist_end <= naive_distance - 100:
					num_good_cheats += 1
	print("Part 1: {}".format(num_good_cheats))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		code_map = TileMap([line.strip() for line in file if line.strip()])

	for y in code_map.y_dim:
		for x in code_map.x_dim:
			pos = Position(y, x)
			if code_map[pos] == "S":
				start = pos
			if code_map[pos] == "E":
				end = pos
	
	naive_path = code_map.bfs(start, end,
						  neighbours=lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self and code_map[neighbour] != "#"],
	)
	naive_distance = len(naive_path)
	
	code_path = { pos: (dist_start, naive_distance - dist_start) for dist_start, pos in enumerate(naive_path) }

	cheats = [(Direction(dy, dx), cheat_length) for dy in range(-20, 21) for dx in range(-20, 21) if (cheat_length := abs(dy) + abs(dx)) <= 20]

	num_good_cheats = 0
	for pos, (dist_start, _) in code_path.items():
		for cheat, cheat_length in cheats:
			if (landing := pos + cheat) in code_path:
				_, dist_end = code_path[landing]
				if dist_start + cheat_length + dist_end <= naive_distance - 100:
					num_good_cheats += 1
	print("Part 2: {}".format(num_good_cheats))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
