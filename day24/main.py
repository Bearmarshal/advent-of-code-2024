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
		inputs_string, gates_string = file.read().split("\n\n")

	wires = {wire: bool(int(value)) for wire, value in re.findall(r"(\w{3}): (\d)", inputs_string)}
	gates = {output_wire: (gate, {input_wire0, input_wire1}) for input_wire0, gate, input_wire1, output_wire in re.findall(r"(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})", gates_string)}
	
	open_set = collections.deque(wires.keys())
	closed_set = set()

	connected_gate_inputs = {}
	for output_wire, (_, (input_wire0, input_wire1)) in gates.items():
		wires.setdefault(output_wire)
		wires.setdefault(input_wire0)
		wires.setdefault(input_wire1)
		connected_gate_inputs.setdefault(input_wire0, set()).add(output_wire)
		connected_gate_inputs.setdefault(input_wire1, set()).add(output_wire)

	while open_set:
		wire = open_set.popleft()
		value = wires[wire]
		if wire in connected_gate_inputs:
			exhausted = True
			for gate in connected_gate_inputs[wire]:
				if gate in closed_set:
					continue
				operation, inputs = gates[gate]
				other_wire, = inputs.difference([wire])
				if (other_value := wires[other_wire]) is not None:
					match operation:
						case "AND": result = value & other_value
						case "OR":  result = value | other_value
						case "XOR": result = value ^ other_value
					wires[gate] = result
					open_set.append(gate)
					closed_set.add(gate)
					print(f"{wire} [{value}] {operation} {other_wire} [{other_value}] -> {gate} [{result}]")
				else:
					exhausted = False
			if not exhausted:
				open_set.append(wire)

	output = 0
	i = 0
	while (wire := f"z{i:02}") in wires:
		output |= wires[wire] << i
		print(output)
		i += 1

	print("Part 1: {}".format(output))

def part2(filename):
	print("Part 2: {}".format(""))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
