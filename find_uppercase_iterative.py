#print first uppercase letter
str_1 = "helloPravin"
str_2 = "HelloPravin"
str_3 = "hellopravin"

def find_uppercase_iterative(str):
	for i in range(len(str)):
		if str[i].isupper():
			return str[i]
	return 'No uppercase found'

print(find_uppercase_iterative(str_1))
print(find_uppercase_iterative(str_2))
print(find_uppercase_iterative(str_3))
