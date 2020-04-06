n = 'Was it a cat I saw?'

def is_palindrom(n):
	i = 0
	j = len(n) - 1

	while i < j:
		while not n[i].isalnum() and i<j:
			i += 1
		while not n[j].isalnum() and i<j:
			j -= 1
		if n[i].lower() != n[j].lower():
			return False

		i += 1
		j -= 1 
	return True

print(is_palindrom(n))

	
