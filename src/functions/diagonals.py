from src.functions.direction import get_direction

def get_diagonal_edges(direction):
    ranks = [i for i in range(0,8)]
    files = list("abcdefgh")

    # from top left to bottom right
    def back_diagonal(file, rank):
        # New plan for refactor:
        #   - if file_idx == rank_idx: a8, h1
        #   - if file_idx > 7- rank_idx: left at top, right on right
        #   - if file_idx < 7- rank_idx: left on left, right at bottom 
        file_idx = files.index(file)
        rank_idx = ranks.index(rank - 1)
        edge_left = min([file_idx, 7- rank_idx])
        edge_right = min([
            7 - file_idx, rank_idx
        ])
        # if file_idx == 7 and rank_idx == 7:
        #     edge_left = 

        square_left = [files[file_idx-edge_left], 
                       ranks[rank_idx+edge_left] + 1]
        square_right= [files[file_idx+edge_right], 
                       ranks[rank_idx-edge_right] + 1]
        # print(f'Back diag edge image: \n{file_idx}, {rank_idx}\n{edge_left}, {edge_right}\n{square_left}\n{square_right}')

        return square_left, square_right
    # from bottom left to top right
    def forward_diagonal(file, rank):
        # New plan for refactor:
        #   - if file_idx == rank_idx: a1, h8
        #   - if file_idx > rank_idx: left at bottom, right on right
        #   - if file_idx < rank_idx: left on left, right at top 
        file_idx = files.index(file)
        rank_idx = ranks.index(rank - 1)
        edge_left = min([file_idx, rank_idx])
        edge_right = min([
            7 - file_idx, 7 - rank_idx
        ])

        square_left = [files[file_idx-edge_left],
                       ranks[rank_idx-edge_left] + 1]
        square_right= [files[file_idx+edge_right], 
                       ranks[rank_idx+edge_right] + 1]

        return square_left, square_right
    
    match direction:
        case 'back':
            return back_diagonal
        case 'forward':
            return forward_diagonal
        
def get_diagonal_squares(left, right):
    # print(f'squares from get_diagonal_squares: {left}, {right}')
    ranks = [i for i in range(0,8)]
    files = list("abcdefgh")
    i_file_idx, f_file_idx = (files.index(left[0]), 
                              files.index(right[0]))
    i_rank_idx, f_rank_idx = (ranks.index(left[1]-1), 
                              ranks.index(right[1]-1))
    # print(f'Direction indices: {i_rank_idx}, {f_rank_idx}')
    direction = get_direction(i_rank_idx, f_rank_idx)
    if f_rank_idx+direction <0:
        rank_arr = ranks[i_rank_idx::direction]
    else:
        rank_arr = ranks[i_rank_idx:f_rank_idx+direction:direction]
    file_arr = files[i_file_idx:f_file_idx+1]
    squares = []
    for i in range(0, len(rank_arr)):
        squares.append((file_arr[i], rank_arr[i]+1))

    return squares