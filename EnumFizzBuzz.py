n = [45, 22, 14, 65, 97, 72]
def enum(n):
	for i, num in enumerate(n):
		if num % 3 == 0 and num % 5 ==0:
			n[i] = 'FizzBuzz'
		elif num % 3 == 0:
			n[i] = 'Fizz'
		elif num % 5 == 0:
			n[i] = 'Buzz'
	print n 

enum(n)
	
