#print first uppercase letter
str_1 = "helloPravin"
str_2 = "HelloPravin"
str_3 = "hellopravin"

def find_uppercase_recursive(str, idx):
	if str[idx].isupper():
		return str[idx]
	elif idx == len(str) - 1:
		return 'No uppercase found'
	return find_uppercase_recursive(str, idx+1)

print(find_uppercase_recursive(str_1,0))
print(find_uppercase_recursive(str_2,0))
print(find_uppercase_recursive(str_3,0))
