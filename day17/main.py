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

def combo_operand(operand, a, b, c):
	if operand <= 3:
		return operand
	elif operand == 4:
		return a
	elif operand == 5:
		return b
	elif operand == 6:
		return c

def part1(filename):
	(a, b, c), code = inputreader.read_int_groups(filename, separator="\n\n")
	ip = 0
	out = []
	while ip in range(len(code) - 1):
		opcode, operand = code[ip:ip+2]
		if opcode == 0:
			a >>= combo_operand(operand, a, b, c)
		elif opcode == 1:
			b ^= operand
		elif opcode == 2:
			b = combo_operand(operand, a, b, c) & 0b111
		elif opcode == 3:
			if a != 0:
				ip = operand
				continue
		elif opcode == 4:
			b ^= c
		elif opcode == 5:
			out.append(combo_operand(operand, a, b, c) & 0b111)
		elif opcode == 6:
			b = a >> combo_operand(operand, a, b, c)
		elif opcode == 7:
			c = a >> combo_operand(operand, a, b, c)
		ip += 2
	
	print("Part 1: {}".format(",".join(map(str, out))))

def part2(filename):
	_, code = inputreader.read_int_groups(filename, separator="\n\n")
	candidates = [0]
	for triplet in reversed(code):
		new_candidates = []
		for a_msb in candidates:
			for i in range(8):
				a = (a_msb << 3) | i
				b = 0
				c = 0
				ip = 0
				out = 0
				while ip in range(len(code) - 1):
					opcode, operand = code[ip:ip+2]
					if opcode == 0:
						a >>= combo_operand(operand, a, b, c)
					elif opcode == 1:
						b ^= operand
					elif opcode == 2:
						b = combo_operand(operand, a, b, c) & 0b111
					elif opcode == 3:
						if a != 0:
							ip = operand
							continue
					elif opcode == 4:
						b ^= c
					elif opcode == 5:
						out = combo_operand(operand, a, b, c) & 0b111
						break
					elif opcode == 6:
						b = a >> combo_operand(operand, a, b, c)
					elif opcode == 7:
						c = a >> combo_operand(operand, a, b, c)
					ip += 2
				if out == triplet:
					new_candidates.append((a_msb << 3) | i)
		candidates = new_candidates
	print("Part 2: {}".format(min(candidates)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
