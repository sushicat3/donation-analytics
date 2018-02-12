"""
	In order to calculate a percentile from the TRANSACTION_AMTs, they must be ordered.
	A binary search tree removes need to sort.
	Instead of sorting a list each time the percentile needs to be calculated (O(nlgn)),
	and obtaining the nth element of the list (O(1)) 
	the bst is updated each time a percentile needs to be calculated (worst case O(n))
	and the nth element is obtained by traversing the tree (worst case O(n)) 

	O(nlgn) --reduced to--> O(n)

	The size and total value of the tree is also stored to omit the need for calculating
	it later.

	findNth() gets the nth element by travesing the bst in order.
"""

class Node:
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data
		

class BSTree:
	def __init__(self):
		self.root = None
		self.size = 0
		self.total = 0

		self.traverseCount = 0
		self.nth = None

	def insert(self, data):
		if self.root == None:
			self.root = Node(data)
		else:
			self.insertChild(self.root, data)
		self.size = self.size + 1
		self.total = self.total + data

	def insertChild(self, node, data):
		if data <= node.data:
			# left
			if node.left == None:
				node.left = Node(data)
			else:
				self.insertChild(node.left, data)
		else:
			# right
			if node.right == None:
				node.right = Node(data)
			else:
				self.insertChild(node.right, data)

	def findNth(self, n):
		self.traverseNode(self.root, n)
		ret = self.nth
		# reset helper variables
		self.traverseCount = 0
		self.nth = None
		
		return ret

	def traverseNode(self, node, n):
		if node != None:
			# left
			self.traverseNode(node.left, n)

			# middle
			self.traverseCount = self.traverseCount + 1
			if self.traverseCount == n:
				self.nth = node.data
				return

			#right
			self.traverseNode(node.right, n)