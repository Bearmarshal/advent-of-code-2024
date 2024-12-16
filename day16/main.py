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
from aoclib.posdir import Position, CardinalDirection
import aoclib.inputreader as inputreader

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritisedItem:
    priority: int
    item: Any=field(compare=False)

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		maze_map = [line.strip() for line in file.readlines()]
	
	maze_dim_y = range(len(maze_map))
	maze_dim_x = range(len(maze_map[0]))
	for y in maze_dim_y:
		for x in maze_dim_x:
			if maze_map[y][x] == "S":
				start = Position(y, x)
			if maze_map[y][x] == "E":
				end = Position(y, x)

	open_set = queue.PriorityQueue()
	open_set.put(PrioritisedItem(0, (start, CardinalDirection.EAST)))
	closed_set = {}
	while open_set.qsize():
		prioritised_item = open_set.get()
		score = prioritised_item.priority
		position, direction = prioritised_item.item
		if (position, direction) in closed_set:
			continue
		closed_set[(position, direction)] = score
		if position == end:
			break
		if (forward := (position + direction, direction)) not in closed_set and (position + direction)[maze_map] != "#":
			open_set.put(PrioritisedItem(score + 1, forward))
		if (left := (position, direction.left())) not in closed_set:
			open_set.put(PrioritisedItem(score + 1000, left))
		if (right := (position, direction.right())) not in closed_set:
			open_set.put(PrioritisedItem(score + 1000, right))
	print("Part 1: {}".format(score))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		maze_map = [line.strip() for line in file.readlines()]
	
	maze_dim_y = range(len(maze_map))
	maze_dim_x = range(len(maze_map[0]))
	for y in maze_dim_y:
		for x in maze_dim_x:
			if maze_map[y][x] == "S":
				start = Position(y, x)
			if maze_map[y][x] == "E":
				end = Position(y, x)

	open_set = queue.PriorityQueue()
	open_set.put(PrioritisedItem(0, (start, CardinalDirection.EAST)))
	closed_set = {}
	while open_set.qsize():
		prioritised_item = open_set.get()
		score = prioritised_item.priority
		position, direction = prioritised_item.item
		if (position, direction) in closed_set:
			continue
		closed_set[(position, direction)] = score
		if position == end:
			break
		if (forward := (position + direction, direction)) not in closed_set and (position + direction)[maze_map] != "#":
			open_set.put(PrioritisedItem(score + 1, forward))
		if (left := (position, direction.left())) not in closed_set:
			open_set.put(PrioritisedItem(score + 1000, left))
		if (right := (position, direction.right())) not in closed_set:
			open_set.put(PrioritisedItem(score + 1000, right))
	part_of_best = 0
	open_set = collections.deque([(end, direction)])
	backtracked = set()
	part_of_best = set()
	while open_set:
		position, direction = open_set.popleft()
		part_of_best.add(position)
		backtracked.add((position, direction))
		score = closed_set[(position, direction)]
		if (reverse := (position - direction, direction)) not in backtracked and closed_set.get(reverse) == score - 1:
			open_set.append(reverse)
		if (counter_right := (position, direction.left())) not in backtracked and closed_set.get(counter_right) == score - 1000:
			open_set.append(counter_right)
		if (counter_left := (position, direction.right())) not in backtracked and closed_set.get(counter_left) == score - 1000:
			open_set.append(counter_left)
	print("Part 2: {}".format(len(part_of_best)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
