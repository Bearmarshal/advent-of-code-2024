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

def rand(secret):
	mask = 16777216 - 1
	secret ^= secret << 6
	secret &= mask
	secret ^= secret >> 5
	secret ^= secret << 11
	secret &= mask
	return secret

def part1(filename):
	secrets = list(*zip(*inputreader.read_int_groups(filename)))

	for _ in range(2000):
		secrets = [rand(secret) for secret in secrets]
	print("Part 1: {}".format(sum(secrets)))

def price(secret):
	return secret % 10

def part2(filename):
	secrets = list(*zip(*inputreader.read_int_groups(filename)))
	num_buyers = len(secrets)
	buyers = range(num_buyers)
	num_iterations = 2000
	prices = [[price(secret) for secret in secrets]] + num_iterations * [[]]
	deltas = num_iterations * [[]]

	for i in range(num_iterations):
		secrets = [rand(secret) for secret in secrets]
		prices[i + 1] = [price(secret) for secret in secrets]
		deltas[i] = [curr - prev for prev, curr in zip(prices[i], prices[i + 1])]

	price_patterns = {}
	for i in range(3, num_iterations):
		patterns = list(zip(*deltas[i - 3:i + 1]))
		for buyer in buyers:
			pattern = patterns[buyer]
			pattern_prices = price_patterns.setdefault(pattern, num_buyers * [0])
			if pattern_prices[buyer] == 0:
				pattern_prices[buyer] = prices[i + 1][buyer]
	best_pattern = None
	best_total = None
	for pattern, prices in price_patterns.items():
		total = sum(prices)
		if best_pattern is None or total > best_total:
			best_pattern = pattern
			best_total = total
	most_bananas = max(sum(prices) for prices in price_patterns.values())
	
	print("Part 2: {}".format(most_bananas))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
