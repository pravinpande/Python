#find pair of numbers from array which sum to the number passed
array = [1,3,2,2]
k = 4

def pair(array,k):
	if len(array) < 2:
		return print('Too small')

	seen = set()
	output = set()

	for num in array:
		target = k - num 

		if target not in seen:
			seen.add(num)
		else:
			output.add((min(num,target), max(num,target)))

	print('\n'.join(map(str, list(output))))

pair(array,k)
