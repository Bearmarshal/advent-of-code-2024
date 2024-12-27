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
				else:
					exhausted = False
			if not exhausted:
				open_set.append(wire)

	output = 0
	i = 0
	while (wire := f"z{i:02}") in wires:
		output |= wires[wire] << i
		i += 1

	print("Part 1: {}".format(output))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		inputs_string, gates_string = file.read().split("\n\n")

	wires = {wire: bool(int(value)) for wire, value in re.findall(r"(\w{3}): (\d)", inputs_string)}
	gates = {output_wire: (gate, frozenset({input_wire0, input_wire1})) for input_wire0, gate, input_wire1, output_wire in re.findall(r"(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})", gates_string)}
	
	num_x_bits = max(int(*re.findall(r"x(\d+)", bit)) for bit in wires.keys()) + 1
	num_y_bits = max(int(*re.findall(r"y(\d+)", bit)) for bit in wires.keys()) + 1
	num_z_bits = max(int(*re.findall(r"z(\d+)", bit)) for bit in gates.keys()) + 1

	assert(num_y_bits == num_x_bits)
	assert(num_z_bits == num_x_bits + 1)

	num_bits = num_x_bits

	input_adders = {}
	carry_adders = {}
	carry_joiners = {}
	for output_wire, (gate, input_wires) in gates.items():
		if gate == "OR":
			carry_joiners[input_wires] = output_wire
		elif all(re.match(r"[xy]\d{2}", wire) for wire in input_wires):
			input_adders.setdefault(input_wires, {})[gate] = output_wire
		else:
			carry_adders.setdefault(input_wires, {})[gate] = output_wire

	z_wires = {f"z{i:02}" for i in range(1, num_bits)}

	####################################################################################################################
	## NOTE: This does not catch when an output wire to someone else's instance of the correct type,                  ##
	##       e.g. routing a carry carry to someone else's carry joiner, but that doesn't seem to happen in the input. ##
	####################################################################################################################

	swapped_wires = set()
	for input_adder_inputs, input_adder_outputs in input_adders.items():
		input_sum = input_adder_outputs["XOR"]
		input_carry = input_adder_outputs["AND"]
		if all(re.match(r"[xy]00", wire) for wire in input_adder_inputs):
			if input_sum != "z00":
				swapped_wires.add(input_sum)
			if not any(input_carry in carry_adder for carry_adder in carry_adders):
				swapped_wires.add(input_carry)
		else:
			if not any(input_sum in carry_adder_inputs for carry_adder_inputs in carry_adders):
				swapped_wires.add(input_sum)
			if not any(input_carry in carry_joiner_inputs for carry_joiner_inputs in carry_joiners):
				swapped_wires.add(input_carry)
	for carry_adder_outputs in carry_adders.values():
		carry_sum = carry_adder_outputs["XOR"]
		carry_carry = carry_adder_outputs["AND"]
		if carry_sum not in z_wires:
			swapped_wires.add(carry_sum)
		if not any(carry_carry in carry_joiner_inputs for carry_joiner_inputs in carry_joiners):
			swapped_wires.add(carry_carry)
	for carry in carry_joiners.values():
		if not any(carry in carry_adder for carry_adder in carry_adders):
			if carry != f"z{num_bits:02}":
				swapped_wires.add(carry)

	print("Part 2: {}".format(",".join(sorted(swapped_wires))))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
