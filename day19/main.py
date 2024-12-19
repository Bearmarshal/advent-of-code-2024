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

def is_possible(pattern, towels):
	for towel in towels.get(pattern[0], []):
		if towel == pattern:
			return True
		elif len(towel) > len(pattern):
			return False
		elif pattern.startswith(towel):
			if is_possible(pattern.removeprefix(towel), towels):
				return True
	return False

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		towel_strings, pattern_strings = [block.strip() for block in file.read().split("\n\n")]
	towels = {}
	for towel in map(str.strip, towel_strings.split(",")):
		towels.setdefault(towel[0], []).append(towel)
	for towel in towels.values():
		towel.sort(key=len)
	patterns = [ pattern.strip() for pattern in pattern_strings.splitlines() ]
	num_possible = 0
	for pattern in patterns:
		if is_possible(pattern, towels):
			num_possible += 1
	print("Part 1: {}".format(num_possible))

def count_arrangements(pattern, towels, cache):
	if pattern in cache:
		return cache[pattern]
	num_patterns = 0
	for towel in towels.get(pattern[0], []):
		if towel == pattern:
			num_patterns += 1
		elif len(towel) > len(pattern):
			break
		elif pattern.startswith(towel):
			num_patterns += count_arrangements(pattern.removeprefix(towel), towels, cache)
	cache[pattern] = num_patterns
	return num_patterns

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		towel_strings, pattern_strings = [block.strip() for block in file.read().split("\n\n")]
	towels = {}
	for towel in map(str.strip, towel_strings.split(",")):
		towels.setdefault(towel[0], []).append(towel)
	for towel in towels.values():
		towel.sort(key=len)
	patterns = [ pattern.strip() for pattern in pattern_strings.splitlines() ]
	num_arrangements = 0
	cache = {}
	for pattern in patterns:
		num_arrangements += count_arrangements(pattern, towels, cache)
	print("Part 2: {}".format(num_arrangements))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
