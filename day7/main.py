import io
import os
import re
import sys

def can_equate(value: int, operands: list[int]) -> bool:
	if len(operands) == 1:
		return operands[0] == value
	first, second, *remaining = operands
	if first + second > value and first * second > value:
		return False
	return can_equate(value, [first * second] + remaining) or can_equate(value, [first + second] + remaining)

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		calibrations = file.readlines()

	result = 0
	for calibration in calibrations:
		value, *operands = list(map(int, re.findall(r"(\d+)", calibration)))
		if can_equate(value, operands):
			result += value

	print("Part 1: {}".format(result))

def can_equate2(value: int, operands: list[int]) -> bool:
	if len(operands) == 1:
		return operands[0] == value
	first, second, *remaining = operands
	if first + second > value and first * second > value and int(f"{first}{second}") > value:
		return False
	return can_equate2(value, [int(f"{first}{second}")] + remaining) or can_equate2(value, [first * second] + remaining) or can_equate2(value, [first + second] + remaining)

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		calibrations = file.readlines()

	result = 0
	for calibration in calibrations:
		value, *operands = list(map(int, re.findall(r"(\d+)", calibration)))
		if can_equate2(value, operands):
			result += value

	print("Part 2: {}".format(result))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
