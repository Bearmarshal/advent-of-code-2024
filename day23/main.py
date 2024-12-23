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
		connections_list = [sorted(re.findall(r"\w{2}", line)) for line in file.readlines() if line.strip()]

	connections = {}
	for alice, bob in sorted(connections_list):
		connections.setdefault(alice, []).append(bob)

	t_interconnects = 0
	for alice, connected in connections.items():
		for i in range(len(connected) - 1):
			bob = connected[i]
			if bob in connections:
				for j in range(i + 1, len(connected)):
					charlie = connected[j]
					if charlie in connections[bob]:
						if alice[0] == "t" or bob[0] == "t" or charlie[0] == "t":
							t_interconnects += 1

	print("Part 1: {}".format(t_interconnects))

def largest_group(connections, nodes):
	largest = []
	for node in nodes:
		if node in connections:
			peers = connections[node]
			curr_largest = [node] + largest_group(connections, nodes.intersection(peers))
		else:
			curr_largest = [node]
		if len(curr_largest) > len(largest):
			largest = curr_largest
	return largest

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		connections_list = [sorted(re.findall(r"\w{2}", line)) for line in file.readlines() if line.strip()]

	connections = {}
	for alice, bob in sorted(connections_list):
		connections.setdefault(alice, []).append(bob)
	nodes = {node for pair in connections_list for node in pair}

	print("Part 2: {}".format(",".join(sorted(largest_group(connections, nodes)))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
