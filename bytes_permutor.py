# Thank you Sterling: n ! ~ sqrt(2 pi n)(n / e)^n
# Using Sterlings approximation, and since 1 Googol = 10^100 is greater than the number of atoms in the observable universe ...
# Now go ahead

import hashlib

def compute_SHA256(message):
    
    h = hashlib.sha256()
    h.update(message.encode('utf-8'))

    return h.digest()

num_chunks = 100
seed = input("Seed: ")
FILE_NAME = input("File name: ")
PERMUTED_FILE_NAME = 'permuted_' + FILE_NAME

def compute_permuted_index_set(seed):
    global num_chunks

    index_set = []

    i = 0
    while(i < num_chunks):
        index_set.append(i)
        i += 1
    
    i = 0
    import copy
    while(i < num_chunks):
        _hash = compute_SHA256(seed + str(i)).hex()
        j = int(_hash, 16) % num_chunks
        x = copy.deepcopy(index_set[i])
        y = copy.deepcopy(index_set[j])
        index_set[j] = x
        index_set[i] = y
        i += 1

    return index_set

def permute_file(seed):
    global num_chunks

    # Get length of file as bytes
    # Generate 100 indexes
    # Leave last few bytes
    _file = open(FILE_NAME, 'rb+')
    _data = _file.read()
    _len = len(_data)
    chunk_len = _len // num_chunks

    file_permuted = open('permuted_' + FILE_NAME, 'wb+')
    # Scan through, and switch chunk_index i with uniformly and randomly generated j
    # Zero indexed example: for j = 2 with i = 0, then j = 2 with i = 1
    # [A, B, C] -> [C, B, A] -> [C, A, B]
    chunk_index = 0
    index_set = compute_permuted_index_set(seed)

    buffers = []
    # Read to buffer
    i = 0
    while(i < num_chunks):
        index = index_set[i]
        chunk_index = index * chunk_len
        _file.seek(chunk_index)
        buffer = _file.read(chunk_len)
        buffers.append(buffer)
        i += 1

    # Write buffer to permuted_file
    i = 0
    while(i < num_chunks):
        file_permuted.write(buffers[i])
        i += 1

    # Now write odd bytes (tail) at the end of FILE_NAME to tail_file
    tail_file = open('tail_file', 'wb+')
    tail_start_index = chunk_len * num_chunks
    _file.seek(tail_start_index)
    tail_file.write(_file.read(_len - tail_start_index))

############################################################################################################

def unpermute_file(seed):
    global num_chunks
    global FILE_NAME
    global PERMUTED_FILE_NAME

    permuted_index_set = compute_permuted_index_set(seed)
    print(len(permuted_index_set))
    print(sorted(list(permuted_index_set)))

    mapping = {}
    file_permuted = open(PERMUTED_FILE_NAME, 'rb+')
    chunk_len = len(file_permuted.read()) // num_chunks
    file_permuted.seek(0)
    permuted_file_buffers = []
    i = 0
    while(i < num_chunks):
        permuted_file_buffers.append(file_permuted.read(chunk_len))
        mapping[str(permuted_index_set[i])] = permuted_file_buffers[i]
        i += 1
    _file = open('unpermuted_' + FILE_NAME, 'wb+')
    
    i = 0
    while(i < num_chunks):
        _file.write(mapping[str(i)])
        i += 1
    
    tail_file = open('tail_file', 'rb+')
    tail_data = tail_file.read()
    _file.write(tail_data)

_in = input("Permute (P) or Unpermute (U): ")
while(_in != 'P' and _in != 'U'):
    print("Incorrect input, try again.")
    _in = input("Permute (P) or Unpermute (U): ")
if(_in == 'P'):
    permute_file(seed)
else:
    unpermute_file(seed)