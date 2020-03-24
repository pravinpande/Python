#find common elements from ordered array

def common(a,b):
	x = 0
	y = 0
	e_list = []

	while x < len(a) and y < len(b):
		if a[x] == b[y]:
			e_list.append(a[x])
			x += 1
			y += 1

		elif a[x] > b[y]:
			y += 1

		else:
			x += 1
	return e_list

print(common([0,1,2,3,4],[0,3,4,5,6,9,0])) 
