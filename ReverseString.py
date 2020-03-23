#reverse string
 
def reverse_join(s):
	return " ".join(reversed(s.split()))

print(reverse_join('This is a string'))

def reverse_while(s):
	length = len(s)
	spaces = [' ']
	word = []
	i = 0

	while i < length:
		if s[i] not in spaces:
			word_start = i 

			while i < length and s[i] not in spaces:
				i += 1
			word.append(s[word_start:i])

		i += 1
	return " ".join(reversed(word))

print(reverse_while('This is a string'))
