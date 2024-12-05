import io
import os
import re
import sys

def part1(filename):
	with io.open(filename, mode = 'r') as file:
		rules_text, pages_text = file.read().split("\n\n")

	rules = {}
	for rule_text in rules_text.splitlines():
		before, after = map(int, rule_text.split("|"))
		rules.setdefault(before, set()).add(after)

	result = 0
	for page_text in pages_text.splitlines():
		pages = list(map(int, page_text.split(",")))
		for i in range(1, len(pages)):
			if any(must_be_after in pages[:i-1] for must_be_after in rules.get(pages[i], set())):
				break
		else:
			result += pages[len(pages) // 2]
	
	print("Part 1: {}".format(result))

def part2(filename):
	with io.open(filename, mode = 'r') as file:
		rules_text, pages_text = file.read().split("\n\n")

	rules = {}
	for rule_text in rules_text.splitlines():
		before, after = map(int, rule_text.split("|"))
		rules.setdefault(before, set()).add(after)

	result = 0
	for page_text in pages_text.splitlines():
		pages = list(map(int, page_text.split(",")))
		for i in range(1, len(pages)):
			if any(must_be_after in pages[:i-1] for must_be_after in rules.get(pages[i], set())):
				break
		else:
			continue
		new_pages = []
		for i in range(len(pages)):
			for j in range(len(pages)):
				if rules.get(pages[j], set()).isdisjoint(pages):
					new_pages.append(pages.pop(j))
					break
		result += new_pages[len(new_pages) // 2]
	
	print("Part 2: {}".format(result))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = os.path.dirname(sys.argv[0]) + "/input.txt"
	part1(filename)
	part2(filename)
