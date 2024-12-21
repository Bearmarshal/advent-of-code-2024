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
from aoclib.posdir import *
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

def shortest_sequence_length(sequence, robots, keypads, keypad_sequences, cache = {}):
	if not robots:
		return len(sequence)
	robot, *robots = robots
	if (len(robots), sequence) in cache:
		return cache[(len(robots), sequence)]
	keypad, *keypads = keypads
	sequence_map = keypad_sequences[keypad]
	shortest_total_sequence_length = 0
	for button in sequence:
		robot_sequence = sequence_map[robot][button]
		shortest_total_sequence_length += shortest_sequence_length(robot_sequence, robots, keypads, keypad_sequences, cache)
		robot = button
	cache[(len(robots), sequence)] = shortest_total_sequence_length
	return shortest_total_sequence_length

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		codes = [line.strip() for line in file if line.strip()]

	numpad = TileMap(["789", "456", "123", " 0A"])
	dirpad = TileMap([" ^A", "<v>"])

	num_buttons = { button_num: position for y in numpad.y_dim for x in numpad.x_dim if (button_num := numpad[position := Position(y, x)]) != " " }
	dir_buttons = { button_num: position for y in dirpad.y_dim for x in dirpad.x_dim if (button_num := dirpad[position := Position(y, x)]) != " " }

	numpad_sequences = {button: {
		other: "".join(direction.glyph() for direction in sorted((num_buttons[other] - num_buttons[button]).discretise(), key=lambda direction: (WEST, SOUTH, NORTH, EAST).index(direction))) + "A" for other in "A0123456789"
		} for button in "A0123456789"}
	numpad_sequences["0"]["1"] = "^<A"
	numpad_sequences["0"]["4"] = "^^<A"
	numpad_sequences["0"]["7"] = "^^^<A"
	numpad_sequences["A"]["1"] = "^<<A"
	numpad_sequences["A"]["4"] = "^^<<A"
	numpad_sequences["A"]["7"] = "^^^<<A"
	numpad_sequences["1"]["0"] = ">vA"
	numpad_sequences["1"]["A"] = ">>vA"
	numpad_sequences["4"]["0"] = ">vvA"
	numpad_sequences["4"]["A"] = ">>vvA"
	numpad_sequences["7"]["0"] = ">vvvA"
	numpad_sequences["7"]["A"] = ">>vvvA"
	dirpad_sequences = {
		"A": {"A":    "A", "^":  "<A", "v": "<vA", "<": "v<<A", ">":  "vA" },
		"^": {"A":   ">A", "^":   "A", "v":  "vA", "<":  "v<A", ">": "v>A" },
		"v": {"A":  "^>A", "^":  "^A", "v":   "A", "<":   "<A", ">":  ">A" },
		"<": {"A": ">>^A", "^": ">^A", "v":  ">A", "<":    "A", ">": ">>A" },
		">": {"A":   "^A", "^": "<^A", "v":  "<A", "<":  "<<A", ">":   "A" },
		}

	for button in "A0123456789":
		print(f"{button}: [", " | ".join(f"{other}: {numpad_sequences[button][other]:>6}" for other in "A0123456789"), "]")
	print()
	for button in "A^<v>":
		print(f"{button}: [", " | ".join(f"{other}: {dirpad_sequences[button][other]:>6}" for other in "A^<v>"), "]")

	keypads = [numpad] + 25 * [dirpad]
	keypad_sequences = { numpad: numpad_sequences, dirpad: dirpad_sequences }
	robots = ["A" for _ in keypads]

	complexity = 0
	cache = {}
	for code in codes:
		print(shortest_sequence_length(code, robots, keypads, keypad_sequences, cache))
		complexity += int(code[:-1]) * shortest_sequence_length(code, robots, keypads, keypad_sequences, cache)

	print("Part 2: {}".format(complexity))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
