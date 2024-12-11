import collections
import io
import os
import re
import sys

def blink(value):
	if value == 0:
		return [1]
	elif (num_digits := len(str(value))) % 2 == 0:
		denominator = 10 ** (num_digits // 2)
		return [value % denominator, value // denominator]
	else:
		return [value * 2024]

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		pebbles = collections.Counter([int(x) for x in re.findall("\d+", file.read())])
	for _ in range(25):
		new_pebbles = collections.Counter()
		for value, count in pebbles.items():
			for new_value in blink(value):
				new_pebbles[new_value] += count
		pebbles = new_pebbles
	print("Part 1: {}".format(sum(pebbles.values())))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		pebbles = collections.Counter([int(x) for x in re.findall("\d+", file.read())])
	for _ in range(75):
		new_pebbles = collections.Counter()
		for value, count in pebbles.items():
			for new_value in blink(value):
				new_pebbles[new_value] += count
		pebbles = new_pebbles
	print("Part 2: {}".format(sum(pebbles.values())))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
