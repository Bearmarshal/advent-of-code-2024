import io
import itertools
import os
import re
import sys

def part1(filename):
	directions = ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1, 1))
	word_search = [line for line in io.open(filename, mode = 'r')]
	total = 0
	for y in range(len(word_search)):
		for x in range(len(word_search[y])):
			if word_search[y][x] == "X":
				for dy, dx in directions:
					if y + 3*dy in range(len(word_search)) and x + 3*dx in range(len(word_search[y])) and all(word_search[yy][xx] == letter for (yy, xx), letter in zip(((y+d*dy, x+d*dx) for d in (1, 2, 3)), "MAS")):
						total += 1
	print("Part 1: {}".format(total))

def part2(filename):
	directions = (((1,1), (-1,1)), ((1,1), (1,-1)), ((-1,-1), (-1,1)), ((-1,-1), (1,-1)))
	word_search = [line for line in io.open(filename, mode = 'r')]
	total = 0
	for y in range(1, len(word_search) - 1):
		for x in range(1, len(word_search[y]) - 1):
			if word_search[y][x] == "A":
				for diagonal in directions:
						if all(all(word_search[yy][xx] == letter for (yy, xx), letter in zip(((y+d*ddy, x+d*ddx) for d in (-1, 1)), "MS")) for ddy, ddx in diagonal):
							total += 1
	print("Part 2: {}".format(total))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
