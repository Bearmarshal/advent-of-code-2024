import functools
import io
import itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(sum(int(a) * int(b) for line in io.open(filename, mode = 'r') for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line))))

def part2(filename):
	print("Part 2: {}".format(functools.reduce(lambda acc, match: (acc[0], True) if match["do"] else (acc[0], False) if match["dont"] else (acc[0] + int(match["a"]) * int(match["b"]), True) if acc[1] else acc, re.finditer(r"(?P<mul>mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\))|(?P<do>do\(\))|(?P<dont>don't\(\))", io.open(filename, mode = 'r').read()), (0, True))[0]))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
