def st(str):
	letters = {}
	for letter in str:
		if letter in letters:
			return False
		letters[letter] = True
	return True

print(st('pravin'))
