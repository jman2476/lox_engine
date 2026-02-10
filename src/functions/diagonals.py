

def get_diagonal_edges(direction):
    ranks = [i for i in range(0,8)]
    files = list("abcdefgh")

    # from top left to bottom right
    def back_diagonal(file, rank):
        file_idx = files.index(file)
        rank_idx = ranks.index(rank - 1)
        edge_left = min([file_idx, 7- rank_idx])
        edge_right = min([
            7 - file_idx, rank_idx
        ])
        print(f'edge left: {edge_left}')
        print(f'edge right: {edge_right}')

        square_left = [files[file_idx-edge_left], ranks[rank_idx+edge_left] + 1]
        square_right= [files[file_idx+edge_right], ranks[rank_idx-edge_right] + 1]

        return square_left, square_right
    # from bottom left to top right
    def forward_diagonal(file, rank):
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