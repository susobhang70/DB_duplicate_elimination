#!/usr/bin/python
import sys
import os
import Btree
import Hash

INT_SIZE = sys.getsizeof(int())

def check_remove_file():
	try:
		total_number_of_lines = sum(1 for line in open('./../output/201503005_output', "r"))
		if total_number_of_lines >= 12:
			os.remove('./../output/201503005_output')
	except:
		pass

def main():
	if len(sys.argv) < 6:
		print "Incorrect parameters! Retry with correct cmd parameters"
		print "filename n_attr buffers btree/hash blocksize"
		sys.exit(0)

	filename = str(sys.argv[1])
	n_attr = int(sys.argv[2])
	M = int(sys.argv[3])
	indexType = str(sys.argv[4])
	block_size = int(sys.argv[5])
	# if block_size % (INT_SIZE * n_attr) != 0:
	# 	print "Block size should be a multiple of " + str(INT_SIZE) + " * n"
	# 	sys.exit(0)
	if not os.path.isfile(filename):
		print "Enter valid Relation file name"
		sys.exit(0)
	if indexType.lower() == "hash":
		Hash.distinct(filename, n_attr, M, block_size)
	elif indexType.lower() == "btree":
		Btree.distinct(filename, n_attr, M, block_size)
	else:
		print "Incorrect type of index; should be either btree or hash"
		sys.exit(0)

if __name__ == '__main__':
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	check_remove_file()
	main()