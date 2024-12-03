import io
import itertools
import os
import re
import sys

def part1(filename):
	print("Part 1: {}".format([all(n - p in (1, 2, 3) for p, n in level_pairs) or all(n - p in (-1, -2, -3) for p, n in level_pairs) for level_pairs in (list(itertools.pairwise(map(int, re.findall(r"(\d+)", line)))) for line in io.open(filename, mode = 'r'))].count(True)))

def part2(filename):
	print("Part 2: {}".format([any(all(n - p in (1, 2, 3) for p, n in itertools.pairwise(alt_report)) or all(n - p in (-1, -2, -3) for p, n in itertools.pairwise(alt_report)) for alt_report in [report] + [report[0:i] + report[i+1:len(report)] for i in range(len(report))]) for report in (list(map(int, re.findall(r"(\d+)", line))) for line in io.open(filename, mode = 'r'))].count(True)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
