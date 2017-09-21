#!/usr/bin/python
import sys
import csv
import time
import os

INT_SIZE = sys.getsizeof(int())

def Open(filename, M, records):
	fp = open(filename, "r")
	GetNext(fp, M, records)
	Close(fp)

def Close(filepointer):
	filepointer.close()

def GetNext(filepointer, M, records):
	hashtable = {}
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
				try:
					temp = hashtable[key]
				except:
					hashtable[key] = j
					outputbuffer.append(j)
				if len(outputbuffer) == records:
					for row in outputbuffer:
						outfp.writerow(row)
					outputbuffer = []
	outputfp.close()

def distinct(filename, n_attr, M, blocksize):
	r_per_block = blocksize / (INT_SIZE * n_attr)
	print type(r_per_block)
	start_time = time.time()
	Open(filename, M, r_per_block)
	time_elapsed = time.time() - start_time
	total_number_of_lines = sum(1 for line in open('./../output/temp_201503005_output.txt', "r"))
	fp = open("./../output/201503005_output", "a")
	fp.write(str(time_elapsed) + " " + str(total_number_of_lines) + "\n")
	os.remove("./../output/temp_201503005_output.txt")