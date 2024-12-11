import io
import os
import re
import sys

class Pebble:
	def __init__(self, value, next=None):
		self.value = value
		self.next = next

	def __iter__(self):
		current = self
		while current:
			yield current
			current = current.next

	def add_after(self, value):
		self.next = Pebble(value, self.next)

	def blink(self):
		current = self
		while current:
			next = current.next
			if current.value == 0:
				current.value = 1
			elif (num_digits := len(str(current.value))) % 2 == 0:
				current.add_after(current.value % 10 ** (num_digits // 2))
				current.value //= 10 ** (num_digits // 2)
			else:
				current.value *= 2024
			current = next

	def from_list(values):
		head_pebble = None
		for value in reversed(values):
			head_pebble = Pebble(value, head_pebble)
		return head_pebble


def part1(filename):
	with io.open(filename, mode = 'r') as file:
		pebbles = Pebble.from_list([int(x) for x in re.findall("\d+", file.read())])
	for _ in range(25):
		pebbles.blink()
	print("Part 1: {}".format(len(list(pebbles))))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		pebbles = Pebble.from_list([int(x) for x in re.findall("\d+", file.read())])
	for _ in range(75):
		pebbles.blink()
	print("Part 2: {}".format(len(list(pebbles))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
