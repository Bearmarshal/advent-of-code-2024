import collections
import io
import itertools
import math
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoclib.posdir import Position, Direction
import aoclib.inputreader as inputreader

def part1(filename):
	(y_size := 103), (x_size := 101), print("Part 1: {}".format(math.prod(collections.Counter(selector for robot in ((Position(y, x) + 100 * Direction(dy, dx)).wraparound(y_size, x_size) for x, y, dx, dy in inputreader.read_int_groups(filename)) if (selector := (robot.y < y_size // 2, robot.y > y_size // 2, robot.x < x_size // 2, robot.x > x_size // 2)).count(True) == 2).values())))

def part2(filename):
	y_size = 103
	x_size = 101
	robots = [(Position(y, x), Direction(dy, dx)) for x, y, dx, dy in inputreader.read_int_groups(filename)]
	elapsed = 0
	while True:
		symmetry = 52
		while symmetry > 46:
			robots = [((position + direction).wraparound(y_size, x_size), direction) for position, direction in robots]
			nonants = [[0 for _ in range(3)] for _ in range(3)]
			for position, _ in robots:
				nonants[3 * position.y // y_size][3 * position.x // x_size] += 1
			symmetry = round(math.log2(math.prod(itertools.chain.from_iterable(nonants))))
			elapsed += 1
		robot_set = {robot[0] for robot in robots}
		robot_map = [["#" if Position(y, x) in robot_set else "." for x in range(x_size)] for y in range(y_size)]
		if input("\n".join("".join(row) for row in robot_map) + "\nElapsed: " + str(elapsed) + ", symmetry: " + str(symmetry) + "\n"):
			break
	print("Part 2: {}".format(elapsed))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
