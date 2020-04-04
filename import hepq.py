def l_Search(data, target):
	for i in range(len(data)):
		if data[i] == target:
			return True
		return False

def b_Search(data,target):
	low = 0
	high = len(data) - 1
	while low <= high:
		mid=(low+high)//2
		if target == data[mid]:
			return True
		elif target < data[mid]:
			high = mid - 1
		else:
			low = mid + 1
	return False

print(b_Search([1,2,3],3))