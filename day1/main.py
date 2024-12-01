import io
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format(sum((abs(int(a) - int(b)) for a, b in zip(*(sorted(location_list) for location_list in zip(*(re.findall(r"(\d+)", line) for line in io.open(filename, mode = 'r')))))))))

def part2(filename):
	left_list, right_list = zip(*(re.findall(r"(\d+)", line) for line in io.open(filename, mode = 'r')))
	print("Part 2: {}".format(sum((abs(int(x) * right_list.count(x)) for x in left_list))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
