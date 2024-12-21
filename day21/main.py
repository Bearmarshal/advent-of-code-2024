import collections
from dataclasses import dataclass
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
		codes = [line.strip() for line in file if line.strip()]

	numpad = TileMap(["789", "456", "123", " 0A"])
	dirpad = TileMap([[" ", CardinalDirection.NORTH, "A"], [CardinalDirection.WEST, CardinalDirection.SOUTH, CardinalDirection.EAST]])

	num_buttons = { button_num: position for y in numpad.y_dim for x in numpad.x_dim if (button_num := numpad[position := Position(y, x)]) != " " }
	dir_buttons = { button_num: position for y in dirpad.y_dim for x in dirpad.x_dim if (button_num := dirpad[position := Position(y, x)]) != " " }

	robot0 = num_buttons["A"]
	robot1 = dir_buttons["A"]
	robot2 = dir_buttons["A"]

	complexity = 0
	for code in codes:
		for button_num in code:
			best_robot0_complexity = None
			for robot0_sequence in numpad.find_all_shortest_paths(robot0, num_buttons[button_num], neighbours=lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self and numpad[neighbour] != " "]):
				current_robot0_complexity = 0
				robot0_directions = [to_button - from_button for from_button, to_button in itertools.pairwise(robot0_sequence)] + ["A"]
				for robot0_direction in robot0_directions:
					best_robot1_complexity = None
					for robot1_sequence in dirpad.find_all_shortest_paths(robot1, dir_buttons[robot0_direction], neighbours=lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self and dirpad[neighbour] != " "]):
						current_robot1_complexity = 0
						robot1_directions = [to_button - from_button for from_button, to_button in itertools.pairwise(robot1_sequence)] + ["A"]
						for robot1_direction in robot1_directions:
							robot2_sequence = dirpad.bfs(robot2, dir_buttons[robot1_direction], neighbours=lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self and dirpad[neighbour] != " "])
							robot2 = dir_buttons[robot1_direction]
							best_robot2_complexity = len(robot2_sequence)
							current_robot1_complexity += best_robot2_complexity
						if best_robot1_complexity is None or current_robot1_complexity < best_robot1_complexity:
							best_robot1_complexity = current_robot1_complexity
					robot1 = dir_buttons[robot0_direction]
					current_robot0_complexity += best_robot1_complexity
				if best_robot0_complexity is None or current_robot0_complexity < best_robot0_complexity:
					best_robot0_complexity = current_robot0_complexity
			robot0 = num_buttons[button_num]
			complexity += int(code[:-1]) * best_robot0_complexity

	print("Part 1: {}".format(complexity))

def sequence_to_string(sequence):
	return "".join(CardinalDirection.glyph(direction) if isinstance(direction, Direction) else direction for direction in sequence)

def shortest_sequence(sequence, robots, keypads, keypad_buttons, cache = {}, cache2 = {}):
	if not robots:
		return sequence
	robot, *robots = robots
	if (len(robots), sequence_to_string(sequence)) in cache:
		return cache[(len(robots), sequence_to_string(sequence))]
	keypad, *keypads = keypads
	shortest_total_sequence = []
	for button in sequence:
		shortest_button_sequence = None
		if (robot, keypad_buttons[keypad][button]) in cache2:
			robot_sequences = cache2[(robot, keypad_buttons[keypad][button])]
		else:
			robot_sequences = keypad.find_all_shortest_paths(robot, keypad_buttons[keypad][button], neighbours=lambda self, position: [neighbour for direction in CardinalDirection if (neighbour := position + direction) in self and keypad[neighbour] != " "])
			cache2[(robot, keypad_buttons[keypad][button])] = robot_sequences
		for robot_sequence in robot_sequences:
			robot_directions = [to_button - from_button for from_button, to_button in itertools.pairwise(robot_sequence)] + ["A"]
			current_button_sequence = shortest_sequence(robot_directions, robots, keypads, keypad_buttons, cache)
			if shortest_button_sequence is None or len(current_button_sequence) < len(shortest_button_sequence):
				shortest_button_sequence = current_button_sequence
		if shortest_button_sequence is None:
			return None
		shortest_total_sequence += shortest_button_sequence
		robot = keypad_buttons[keypad][button]
	cache[(len(robots), sequence_to_string(sequence))] = shortest_total_sequence
	return shortest_total_sequence

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		codes = [line.strip() for line in file if line.strip()]

	numpad = TileMap(["789", "456", "123", " 0A"])
	dirpad = TileMap([[" ", CardinalDirection.NORTH, "A"], [CardinalDirection.WEST, CardinalDirection.SOUTH, CardinalDirection.EAST]])

	num_buttons = { button_num: position for y in numpad.y_dim for x in numpad.x_dim if (button_num := numpad[position := Position(y, x)]) != " " }
	dir_buttons = { button_num: position for y in dirpad.y_dim for x in dirpad.x_dim if (button_num := dirpad[position := Position(y, x)]) != " " }

	keypads = [numpad] + 25 * [dirpad]
	keypad_buttons = { numpad: num_buttons, dirpad: dir_buttons }
	robots = [keypad_buttons[keypad]["A"] for keypad in keypads]

	complexity = 0
	cache = {}
	cache2 = {}
	for code in codes:
		complexity += int(code[:-1]) * len(shortest_sequence(code, robots, keypads, keypad_buttons, cache, cache2))

	print("Part 2: {}".format(complexity))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
