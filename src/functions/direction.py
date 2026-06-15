def get_direction(start, end):
    return int((end - start)/abs(end - start))

def adjacent_squares(board, file, rank):
    file_idx = board.files.index(file)
    files = [board.files[j] for j in 
             [file_idx + 1, file_idx, file_idx - 1]
             if j in range(0,8)]
    ranks = [j for j in
             [rank - 1, rank, rank + 1]
             if j in range(1,9)]
    return [f'{i}{j}' for j in ranks for i in files if j != rank or i != file ]