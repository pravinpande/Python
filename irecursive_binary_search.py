data = [1,2,3,4,5,6,7,8,9]
target = 5

def irecursive_binary_search(data,target, low, high): 
	if low > high:
		return False
	else:
		mid = (low + high) // 2
		if target == data[mid]:
			return True
		elif target < data[mid]:
			return irecursive_binary_search(data,target,low,mid - 1)
		else:
			return irecursive_binary_search(data,target,mid + 1,high)
	return False

print(irecursive_binary_search(data,target,0,5))
