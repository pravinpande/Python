#find max sum from array of positive and negative numbers

array = [1,3,2,2,-12,1,-2,3,-1]

def largesum(array):
	if len(array) == 0:
		return print('Too Small')

	max_sum = current_sum = array[0]

	for num in array[1:]:
		current_sum = max(current_sum + num, num)
		max_sum = max(current_sum, max_sum)

	return print(max_sum)

largesum(array)
