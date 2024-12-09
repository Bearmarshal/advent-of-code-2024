import io
import os
import re
import sys


def part1(filename):
	with io.open(filename, mode = 'r') as file:
		disk_map = [int(x) for x in re.findall("\d", file.read())]
	files = disk_map[0::2]
	space = disk_map[1::2]
	disk = [0] * sum(files)

	file_id_front = 0
	file_id_back = len(files) - 1
	left_to_move = files[file_id_back]
	disk_head = 0

	while file_id_front < file_id_back:
		disk[disk_head:disk_head + files[file_id_front]] = [file_id_front] * files[file_id_front]
		disk_head += files[file_id_front]
		space_to_fill = space[file_id_front]
		while space_to_fill > 0 and file_id_front < file_id_back:
			move_amount = min(space_to_fill, left_to_move)
			disk[disk_head:disk_head + move_amount] = [file_id_back] * move_amount
			disk_head += move_amount
			space_to_fill -= move_amount
			left_to_move -= move_amount
			if left_to_move == 0:
				file_id_back -= 1
				left_to_move = files[file_id_back]
		file_id_front += 1
	if file_id_front == file_id_back:
		disk[disk_head:disk_head + left_to_move] = [file_id_front] * left_to_move
	checksum = sum(i * file_id for i, file_id in enumerate(disk))
	print("Part 1: {}".format(checksum))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		disk_map = [int(x) for x in re.findall("\d", file.read())]
	file_sizes = disk_map[0::2]
	space_sizes = disk_map[1::2]
	num_files = len(file_sizes)
	num_spaces = len(space_sizes)
	file_loc = [0] * num_files
	space_loc = [0] * num_spaces
	disk_head = 0
	space_by_size = {size: [i for i, s in enumerate(space_sizes) if s == size] for size in range(10)}
	for i in range(num_files):
		file_loc[i] = disk_head
		disk_head += file_sizes[i]
		if i < num_spaces:
			space_loc[i] = disk_head
			disk_head += space_sizes[i]
	file_id_back = num_files - 1

	while file_id_back > 0:
		candidate_space = num_spaces
		for size in range(file_sizes[file_id_back], 10):
			if len(spaces := space_by_size[size]) > 0 and (space := spaces[0]) < candidate_space and space < file_id_back:
				candidate_space = space
		if candidate_space < num_spaces:
			file_loc[file_id_back] = space_loc[candidate_space]
			space_loc[candidate_space] += file_sizes[file_id_back]
			space_by_size[space_sizes[candidate_space]].pop(0)
			space_sizes[candidate_space] -= file_sizes[file_id_back]
			space_by_size[space_sizes[candidate_space]].append(candidate_space)
			space_by_size[space_sizes[candidate_space]].sort()
		file_id_back -= 1
	checksum = sum(file_id * ((size := file_sizes[file_id]) * file_loc[file_id] + (size * (size - 1)) // 2) for file_id in range(num_files))
	print("Part 2: {}".format(checksum))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
