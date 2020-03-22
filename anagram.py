#check anagram\
str1 = 'Clint Eastwood'
str2 = 'old WEST Action' 

def anagram(str1, str2):
	a = str1.replace(' ','').lower()
	b = str2.replace(' ','').lower()
	if len(a) != len(b):
		return False
	
	dict1 = {}
	for l in a:
		if l in dict1:
			dict1[l] += 1
		else:
			dict1[l] = 1

	for l in b:
		if l in dict1:
			dict1[l] -= 1
		else:
			dict1[l] = 1

	for k in dict1:
		if dict1[k] != 0:
			return False
	return True

print(anagram(str1, str2))
