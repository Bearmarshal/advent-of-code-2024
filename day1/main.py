import io
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(sum(abs(left - right) for left, right in zip(*map(sorted, zip(*(map(int, re.findall(r"(\d+)", line)) for line in io.open(filename, mode = 'r'))))))))

def part2(filename):
	print("Part 2: {}".format((lambda left_list, right_list: sum((abs(int(x) * right_list.count(x)) for x in left_list)))(*zip(*(re.findall(r"(\d+)", line) for line in io.open(filename, mode = 'r'))))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
