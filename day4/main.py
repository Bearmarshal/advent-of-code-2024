import io
import itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format((lambda word_search, directions: [y + 3*dy in range(len(word_search)) and x + 3*dx in range(len(word_search[y])) and all(word_search[yy][xx] == letter for (yy, xx), letter in zip(((y+d*dy, x+d*dx) for d in (1, 2, 3)), "MAS")) for y in range(len(word_search)) for x in range(len(word_search[y])) if word_search[y][x] == "X" for dy, dx in directions].count(True))(io.open(filename, mode = 'r').readlines(), ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1, 1)))))

def part2(filename):
	print("Part 2: {}".format((lambda word_search, directions: [all(all(word_search[yy][xx] == letter for (yy, xx), letter in zip(((y+d*ddy, x+d*ddx) for d in (-1, 1)), "MS")) for ddy, ddx in diagonal) for y in range(1, len(word_search) - 1) for x in range(1, len(word_search[y]) - 1) if word_search[y][x] == "A" for diagonal in directions].count(True))(io.open(filename, mode = 'r').readlines(), (((1,1), (-1,1)), ((1,1), (1,-1)), ((-1,-1), (-1,1)), ((-1,-1), (1,-1))))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
