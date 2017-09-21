#!/usr/bin/python
import sys
import csv
import time
import os

INT_SIZE = sys.getsizeof(int())

def Open(filename, M, records, blocksize):
	fp = open(filename, "r")
	GetNext(fp, M, records, blocksize)
	Close(fp)

def Close(filepointer):
	filepointer.close()

def GetNext(filepointer, M, records, blocksize):
	degree = (blocksize - INT_SIZE) / (2 * INT_SIZE)
	degree = (degree + 1)/2
	btree_obj = BTree(degree)
	outputfp = open("./../output/temp_201503005_output.txt", "w")
	outfp = csv.writer(outputfp)
	outputbuffer = []
	while True:
		memory_buffers = []
		temp = []
		flag = 0
		m = 0
		r = 0
		for i in filepointer:
			flag = 1
			temp.append(tuple(map(int, list(i.rstrip().split(',')))))
			r += 1
			if r == records:
				if m == M - 2:
					memory_buffers.append(temp)
					temp = []
					r = 0
					break
				else:
					memory_buffers.append(temp)
					temp = []
					m += 1
					r = 0
		if flag == 0:
			for row in outputbuffer:
				outfp.writerow(row)
			break

		if r != 0:
			memory_buffers.append(temp)

		for i in memory_buffers:
			for j in i:
				key = hash(j)
				temp = btree_obj.search(key)
				if temp is not None:
					pass
				else:
					btree_obj.insert(key)
					outputbuffer.append(j)
				if len(outputbuffer) == records:
					for row in outputbuffer:
						outfp.writerow(row)
					outputbuffer = []
	outputfp.close()

class BTreeNode():
	'''BTree Node'''
	def __init__(self, t, leaf):
		self.keys = []
		self.pointers = []
		self.t = t
		self.n = 0
		self.leaf = leaf

	def insert_not_full(self, key):
		# Initialize index as index of rightmost element
		i = self.n - 1
		if self.leaf == True:
			# The following loop does two things
	        # Finds the location of new key to be inserted
	        # Moves all greater keys to one place ahead
			while(i >= 0 and self.keys[i] > key):
				try:
					self.keys[i+1] = self.keys[i]
				except:
					self.keys.append(self.keys[i])
				i -= 1

			# Insert the new key at found location
			try:
				self.keys[i + 1] = key
			except:
				self.keys.append(key)
			self.n += 1
		else:
			# Find the child which is going to have the new key
			while(i >= 0 and self.keys[i] > key):
				i -= 1

			# See if the found child is full
			if self.pointers[i + 1].n == 2 * self.t - 1:

				# If the child is full, then split it
				self.splitchild(i + 1, self.pointers[i + 1])

	            # After split, the middle key of projections goes up and
    	        # projections is splitted into two. See which of the two
        	    # is going to have the new key
				if self.keys[i + 1] < key:
					i += 1

			self.pointers[i + 1].insert_not_full(key)

	def splitchild(self, i, node):
		# Create a new node which is going to store (t-1) keys of node to be split
		newnode = BTreeNode(node.t, node.leaf)
		newnode.n = self.t - 1

		# Copy the last (t-1) keys of node to newnode
		for j in range(self.t - 1):
			newnode.keys.append(node.keys[j + self.t])

		# Copy the last t children of node to newnode
		if node.leaf == False:
			for j in range(self.t):
				try:
					newnode.pointers[j] = node.pointers[j + self.t]
				except:
					newnode.pointers.append(node.pointers[j + self.t])

		# Reduce no. of keys in node
		node.n = self.t - 1

		# Since this node is going to have a new child, create space for new child
		for j in range(self.n, i, -1):
			try:
				self.pointers[j + 1] = self.pointers[j]
			except:
				self.pointers.append(self.pointers[j])

		# Link the new child to this node
		try:
			self.pointers[i + 1] = newnode
		except:
			self.pointers.append(newnode)

		# A key of node will move to this node. Find location of new key and move all greater keys one space ahead
		for j in range(self.n - 1, i - 1, -1):
			try:
				self.keys[j + 1] = self.keys[j]
			except:
				self.keys.append(self.keys[j])

		# Copy the middle key of node to this node
		try:
			self.keys[i] = node.keys[self.t - 1]
		except:
			self.keys.append(node.keys[self.t - 1])
		self.n += 1

	def search(self, key):
		i = 0
		while i < self.n and key > self.keys[i]:
			i += 1
		if i < len(self.keys) and self.keys[i] == key:
			return self
		if self.leaf == True:
			return None
		return self.pointers[i].search(key)


class BTree():
	def __init__(self, N):
		self.degree = N
		self.root = None

	def search(self, key):
		if self.root != None:
			return self.root.search(key)
		else:
			return None

	def insert(self, key):
		if self.root is None:
			self.root = BTreeNode(self.degree, True)
			self.root.keys.append(key)
			self.root.n = len(self.root.keys)
		else:
			# If root is full, then tree grows in height
			if self.root.n == 2 * self.degree - 1:
				newnode = BTreeNode(self.degree, False)

				# old root is appended as a pointer from new node
				newnode.pointers.append(self.root)

				# Split the old root and move 1 key to the new root
				newnode.splitchild(0, self.root)

				# New root has two children now.  Decide which of the two children is going to have new key
				i = 0
				if newnode.keys[0] < key:
					i += 1
				newnode.pointers[i].insert_not_full(key)

				# Change root
				self.root = newnode
			else:
				# If root is not full, call insert_not_full for root
				self.root.insert_not_full(key)


def distinct(filename, n_attr, M, blocksize):
	r_per_block = blocksize / (INT_SIZE * n_attr)
	start_time = time.time()
	Open(filename, M, r_per_block, blocksize)
	time_elapsed = time.time() - start_time
	total_number_of_lines = sum(1 for line in open('./../output/temp_201503005_output.txt', "r"))
	fp = open("./../output/201503005_output", "a")
	fp.write(str(time_elapsed) + " " + str(total_number_of_lines) + "\n")
	os.remove("./../output/temp_201503005_output.txt")

def main():
	a = BTree(3)
	a.insert(10)
	a.insert(20)
	a.insert(5)
	a.insert(6)
	a.insert(12)
	a.insert(30)
	a.insert(7)
	a.insert(17)

	print a.search(100)

if __name__ == '__main__':
	main()