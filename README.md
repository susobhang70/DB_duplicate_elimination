# Database Duplication Elimination using BTree and Hashing

Code to perform duplicate elimination for a given relation.  
(Refer to `Database Systems: The Complete Book by Garcia-Molina, Ullman and Widom` for a detailed description)  

To compile: `g++ filename.cpp -o ./filename`  
Do the above for `main.cpp`, `findunique.cpp` and `randomnumgen.cpp`  

**FUNCTION PROTOTYPE** : `​distinct(R, n, M, type_of_index)`  
- R is a name of relation
- n the number of attributes
- M is the number of blocks. Note that B(R) > M and M > 2  
- Type_of_index takes two values: hash - 0 or btree - 1  
  
We have to remove the duplicates. We'll need to write three routines `open()`, `Getnext()` and​ ​ `close()`​. The program should call above routines to eliminate the duplicates. One can create indexes​​ as a part of open(). To search whether the record is duplicate or not, we use B+ Tree and Hashing main memory structures for inserting and checking.  

**To run:**`python code/code.py <inputfilepath> <no_of_attributes> <no_of_buffers> <"btree"/"hash"> <blocksize>`  
Output is the time taken and the number of unique tuples. The unique tuples are printed to corresponding `filename_output.txt`

- `input/1MB_50Percent` - Input File  
- `input/100MB_20Percent` - Input File  
- `code/Btree.py` - contains code for the BTree indexing  
- `code/Hash.py` contains code for the Hash indexing  

Out of the `M` buffers, `M-1` Buffers will be used as `input buffers` (which will hold the records from the input file). `1` buffer will be used as `output buffer` (holds the distinct records). If the output buffer gets filled, it should be flushed to the output file. If the input buffers get empty, next chunk of records should be read from the input file.  
`Getnext()` function when called should always return one of the following:  
1. Record : This needs to be forwarded to the output buffer (If it's a distinct record)  
2. Null : The input file is completely processed. Proceed for close() routine  

Two assumptions have been made here:  
1. For the `BTree`, it is assumed that the number of unique tuples is not larger than what can fit into the main memory's M-1 blocks. If the number is larger than that, an error is thrown. Ideally we should be using the B+ Tree for indexing as it doesn't store the entire tuple of the relation as a key in its non leaf nodes. Another difference would be the chain of pointers amongst the leaf nodes for a linear full scan which is not possible in a BTree. But to make things simple, a BTree has been used here instead of the B+ Tree.  
2. For `Hashing`, there are M - 1 blocks to which the tuples can hash to. The maximum number of unique tuples which can hash to a block (amongst the M - 1 blocks) is the number which can fit in M - 1 blocks since we employ a two pass algorithm here if overflow occurs, and the entire content of each of those M-1 hash blocks needs to fit into the main memory at once during the second pass.  

**Output:** Vary from `M >= B(R)` to `M= (3/4)(B(R))` and calculate the execution time by employing
BTree and Hashing for inserting and checking duplicate entry.  
