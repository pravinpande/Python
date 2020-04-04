class Node:
	def __init__(self,data):
		self.left = None
		self.right = None
		self.data = data

	def insert(self,data):
		if self.data:
			if data < self.data:
				if self.left is None:
					self.left=Node(data)
				else:
					self.left.insert(data)
			if data > self.data:
				if self.right is None:
					self.right=Node(data)
				else:
					self.right.insert(data)
		else:
			self.data=data

	def findval(self,lkpval):
		if lkpval < self.data:
			if self.left is None:
				return str(lkpval) + " Not found"
			return
		elif lkpval > self.data:
			if self.right is None:
				return str(lkpval) + " Not found"
		else:
			print(str(lkpval) + " Found")


	def PrintTree(self):
		print(self.data)

root = Node(10)
root.insert(1)
root.insert(11)
print(root.findval(1))
