import io
import os
import re
import sys

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		area = file.readlines()

	range_y = range(len(area))
	range_x = range(len(area[0]))

	for y in range_y:
		for x in range_x:
			if area[y][x] == "^":
				guard_y = y
				guard_x = x
				guard_dy = -1
				guard_dx = 0
				break
		else:
			continue
		break

	visited = {(guard_y, guard_x)}
	guard_in_area = True
	while guard_in_area:
		while True:
			next_y = guard_y + guard_dy
			next_x = guard_x + guard_dx
			if next_y not in range_y or next_y not in range_x:
				guard_in_area = False
				break
			if area[next_y][next_x] == "#":
				guard_dy, guard_dx = guard_dx, -guard_dy
				continue
			guard_y = next_y
			guard_x = next_x
			visited.add((guard_y, guard_x))
			break

	print("Part 1: {}".format(len(visited)))

def guard_pattern_loops(area, guard_y, guard_x, guard_dy, guard_dx):
	range_y = range(len(area))
	range_x = range(len(area[0]))
	visited = {(guard_y, guard_x): [(guard_dy, guard_dx)]}
	while True:
		next_y = guard_y + guard_dy
		next_x = guard_x + guard_dx
		if next_y not in range_y or next_x not in range_x:
			return False
		if area[next_y][next_x] == "#":
			guard_dy, guard_dx = guard_dx, -guard_dy
			continue
		guard_y = next_y
		guard_x = next_x
		pos_history = visited.setdefault((guard_y, guard_x), [])
		if (guard_dy, guard_dx) in pos_history:
			return True
		pos_history.append((guard_dy, guard_dx))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		area = file.readlines()

	range_y = range(len(area))
	range_x = range(len(area[0]))

	for y in range_y:
		for x in range_x:
			if area[y][x] == "^":
				guard_y = y
				guard_x = x
				guard_dy = -1
				guard_dx = 0
				break
		else:
			continue
		break

	visited = {(guard_y, guard_x): [(guard_dy, guard_dx)]}
	possible_obstructions = set()
	guard_in_area = True
	while guard_in_area:
		while True:
			next_y = guard_y + guard_dy
			next_x = guard_x + guard_dx
			if next_y not in range_y or next_x not in range_x:
				guard_in_area = False
				break
			if area[next_y][next_x] == "#":
				guard_dy, guard_dx = guard_dx, -guard_dy
				continue
			if (next_y, next_x) not in visited:
				would_be_area = area.copy()
				would_be_area[next_y] = would_be_area[next_y][:next_x] + "#" + would_be_area[next_y][next_x + 1:]
				if guard_pattern_loops(would_be_area, guard_y, guard_x, guard_dy, guard_dx):
					possible_obstructions.add((next_y, next_x))
			guard_y = next_y
			guard_x = next_x
			visited.setdefault((guard_y, guard_x), []).append((guard_dy, guard_dx))
			break
	
	print("Part 2: {}".format(len(possible_obstructions)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
