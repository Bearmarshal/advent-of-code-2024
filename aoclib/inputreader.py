import io
import re

number_regex = re.compile(r"\d+")

def read_int_groups(filename, separator = "\n"):
	with io.open(filename, mode = 'r') as file:
		return [list(map(int, number_regex.findall(group))) for group in file.read().split(separator)]