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
from aoclib.posdir import Direction, Position, CardinalDirection
from aoclib.tilemap import TileMap
import aoclib.inputreader as inputreader


def part1(filename):
	with io.open(filename, mode = 'r') as file:
		transposed_keys_and_locks = [key_or_lock.strip().splitlines() for key_or_lock in file.read().strip().split("\n\n")]
	keys_and_locks = [["".join(col) for col in zip(*key_or_lock)] for key_or_lock in transposed_keys_and_locks]

	length = len(keys_and_locks[0])
	max_height = len(keys_and_locks[0][0]) - 2
	num_heights = max_height + 1

	key_and_lock_patterns = {".": [[]] * num_heights, "#": [[]] * num_heights}
	num = collections.Counter()

	num_fitting = 0
	for key_or_lock in keys_and_locks:
		heights = [col.count("#") - 1 for col in key_or_lock]
		type = "key" if key_or_lock[0][0] == "." else "lock"
		num[type] += 1
		key_or_lock_pattern = key_and_lock_patterns[key_or_lock[0][0]]
		for height in heights[:-1]:
			if not key_or_lock_pattern[height]:
				key_or_lock_pattern[height] = [[]] * num_heights
			key_or_lock_pattern = key_or_lock_pattern[height]
		height = heights[-1]
		if not key_or_lock_pattern[height]:
			key_or_lock_pattern[height] = 0
		key_or_lock_pattern[height] += 1
		possible_fits = [key_and_lock_patterns[".#".replace(key_or_lock[0][0], "")]]
		for i in range(length - 1):
			max_other_height = max_height - heights[i]
			possible_fits = [fits for subset in possible_fits for fits in subset[:max_other_height + 1] if fits]
			if not possible_fits:
				break
		else:
			max_other_height = max_height - heights[-1]
			num_fitting += sum((fits for subset in possible_fits for fits in subset[:max_other_height + 1] if fits))

	print("Part 1: {}".format(num_fitting))

def part2(filename):
	print("Part 2: {}".format("God jul!"))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
