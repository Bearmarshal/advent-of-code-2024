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
		memory_writes = [Position(y, x) for x, y in inputreader.read_int_groups(filename)]
	
	memory_dim_y = range(71)
	memory_dim_x = range(71)
	memory_map = [["." for _ in memory_dim_x] for _ in memory_dim_y]
	start = Position(0, 0)
	end = Position(70, 70)

	for memory_write in memory_writes[:1024]:
		memory_write[memory_map] = "#"

	open_set = queue.PriorityQueue()
	open_set.put(PrioritisedItem(start.get_manhattan_distance(end), (start, 0)))
	closed_set = {}
	while open_set.qsize():
		prioritised_item = open_set.get()
		position, distance = prioritised_item.item
		if position in closed_set:
			continue
		closed_set[position] = distance
		if position == end:
			break
		for direction in CardinalDirection:
			neighbour = position + direction
			if neighbour.y in memory_dim_y and neighbour.x in memory_dim_x and neighbour[memory_map] != "#" and neighbour not in closed_set:
				open_set.put(PrioritisedItem(distance + 1 + neighbour.get_manhattan_distance(end), (neighbour, distance + 1)))
	print("Part 1: {}".format(distance))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		memory_writes = [Position(y, x) for x, y in inputreader.read_int_groups(filename)]
	
	memory_dim_y = range(71)
	memory_dim_x = range(71)
	start = Position(0, 0)
	end = Position(70, 70)

	last_succesful = 1023
	first_failed = len(memory_writes)
	while first_failed - last_succesful > 1:
		i = (last_succesful + first_failed) // 2
		memory_map = [["." for _ in memory_dim_x] for _ in memory_dim_y]
		for memory_write in memory_writes[:i + 1]:
			memory_write[memory_map] = "#"
		open_set = queue.PriorityQueue()
		open_set.put(PrioritisedItem(start.get_manhattan_distance(end), (start, 0)))
		closed_set = {}
		while open_set.qsize():
			prioritised_item = open_set.get()
			position, distance = prioritised_item.item
			if position in closed_set:
				continue
			closed_set[position] = distance
			if position == end:
				last_succesful = i
				break
			for direction in CardinalDirection:
				neighbour = position + direction
				if neighbour.y in memory_dim_y and neighbour.x in memory_dim_x and neighbour[memory_map] != "#" and neighbour not in closed_set:
					open_set.put(PrioritisedItem(distance + 1 + neighbour.get_manhattan_distance(end), (neighbour, distance + 1)))
		else:
			first_failed = i
	first_failed_write = memory_writes[first_failed]
	print("Part 2: {},{}".format(first_failed_write.x, first_failed_write.y))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
