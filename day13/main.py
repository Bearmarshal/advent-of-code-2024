import collections
import io
import itertools
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, Direction
import aoclib.inputreader as input

def part1(filename):
	machines = [(Direction(a_dy, a_dx), Direction(b_dy, b_dx), Position(y, x)) for a_dx, a_dy, b_dx, b_dy, x, y in input.read_int_groups(filename, separator="\n\n")]
	total = 0
	for a, b, price in machines:
		num_a = round((price.x / b.dx - price.y / b.dy) / (a.dx / b.dx - a.dy / b.dy))
		num_b = round((price.y - num_a * a.dy) / b.dy)
		if num_a in range(0, 101) and num_b in range(0, 101) and Position(0, 0) + num_a * a + num_b * b == price:
			total += 3 * num_a + num_b
	print("Part 1: {}".format(total))

def part2(filename):
	machines = [(Direction(a_dy, a_dx), Direction(b_dy, b_dx), Position(10000000000000 + y, 10000000000000 + x)) for a_dx, a_dy, b_dx, b_dy, x, y in input.read_int_groups(filename, separator="\n\n")]
	total = 0
	for a, b, price in machines:
		num_a = round((price.x / b.dx - price.y / b.dy) / (a.dx / b.dx - a.dy / b.dy))
		num_b = round((price.y - num_a * a.dy) / b.dy)
		if num_a >= 0 and num_b >= 0 and Position(0, 0) + num_a * a + num_b * b == price:
			total += 3 * num_a + num_b
	print("Part 2: {}".format(total))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
