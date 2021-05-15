from collections import Counter

def has_unique_characters(string):
	counts = dict(Counter(string))
	for char, count in counts.items():
		if count > 1:
			return False
	return True
