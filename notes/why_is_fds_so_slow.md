# From Gemini:
Because you are using a standard multiprocessing.Manager dictionary for a shared evaluation cache (Transposition Table) and the move tree nodes, every worker process has to make a synchronized network/pipe round-trip to the manager process every single time it checks or updates a position.
In a chess engine, where evaluation lookups happen millions of times per second, the overhead of multiprocessing.Manager completely destroys your performance.
Here is how you can restructure your architecture to keep the parallel scaling but eliminate the speed penalties.
1. Fix the Shared Evaluation Dict (Transposition Table)
A standard Python dict wrapped in a Manager cannot handle the high-throughput demands of a chess engine. You have two excellent alternatives:
Option A: Lockless Shared Memory (The Industry Standard). Move away from a Python dictionary entirely for the evaluation cache. Use multiprocessing.shared_memory to allocate a raw byte array that all processes can read from and write to simultaneously without locks.You can map chess positions to a fixed-size table using an integer hash (like Zobrist hashing).
Worker processes can use a "lossy/overwrite" strategy (e.g., if a slot is full, overwrite it if the new depth is higher) which eliminates the need for expensive locking mechanisms.


Option B: Independent Local Caches. Give each worker process its own separate, local Python dictionary as a transposition table. While processes won't benefit from each other's discoveries during the search, they will run at 100% native CPU speed without hitting a network bottleneck. Often, the raw speed gain of independent caches far outweighs the minor duplication of work.

2. Fix the Move Tree Reconstruction
Right now, your workers are constantly writing individual nodes back to a shared manager dict during the search.
The Fix: Stop updating the tree mid-search. Let each worker process build its slice of the move tree locally in a normal Python dictionary. When a worker finishes its assigned task from the queue, have it return its entire completed local tree fragment all at once in its final queue response payload. Your main process can then merge these tree fragments together at the very end.

3. Replace deepcopy with standard dict.copy() or In-Place Moves
Your profile showed that deepcopy is heavily tied to _deepcopy_dict. If your game board representation is a flat dictionary (e.g., mapping coordinate strings/tuples to pieces), you don't need copy.deepcopy().
If your board is a flat dict: Use board.copy() instead. It creates a shallow copy, which is drastically faster than deepcopy because it skips the object-tracking and metadata checks.
If you have nested objects: Write a custom .copy() method on your board class that manually instantiates a new board and copies over only the raw data arrays/dictionaries.

🛠️ Example: Refactoring to Shared Memory
If you want to keep a truly shared evaluation cache across all processes without the Manager bottleneck, here is a simplified blueprint using multiprocessing.shared_memory:
python

import ctypes
from multiprocessing import shared_memory

# Imagine a fixed-size table of 1 million entries
# Each entry: [Zobrist Hash (8 bytes), Evaluation Score (4 bytes), Depth (4 bytes)] = 16 bytes
ENTRY_SIZE = 16
TABLE_SIZE = 1_000_000 
TOTAL_BYTES = ENTRY_SIZE * TABLE_SIZE

# --- In your main process (Initialization) ---
shm = shared_memory.SharedMemory(create=True, size=TOTAL_BYTES, name="transposition_table")

# --- In your worker processes ---
# Connect to the existing block of memory
existing_shm = shared_memory.SharedMemory(name="transposition_table")
# Create a raw view of the memory that can be modified instantly
shared_array = existing_shm.buf

def lookup_position(zobrist_hash):
    # Map the hash to a specific index in your shared memory array
    index = (zobrist_hash % TABLE_SIZE) * ENTRY_SIZE
    
    # Read the raw bytes directly without any IPC overhead
    stored_hash = int.from_bytes(shared_array[index:index+8], byteorder='big')
    if stored_hash == zobrist_hash:
        score = int.from_bytes(shared_array[index+8:index+12], byteorder='big', signed=True)
        depth = int.from_bytes(shared_array[index+12:index+16], byteorder='big')
        return score, depth
    return None
Use code with caution.



Would you like to explore writing a Zobrist hashing system to back a shared-memory table like this, or would you prefer to look at how to implement a quick Make/Unmake Move pattern to completely wipe out that deepcopy bottleneck first?


