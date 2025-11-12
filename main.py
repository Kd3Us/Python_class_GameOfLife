import numpy as np

def add_padding(frame):
    
    rows, cols = frame.shape
    padded_frame = np.zeros((rows + 2, cols + 2), dtype=int)
    padded_frame[1:rows+1, 1:cols+1] = frame
    return padded_frame

def count_neighbors(padded_frame, i, j):

    neighbors = (
        padded_frame[i-1, j-1] + padded_frame[i-1, j] + padded_frame[i-1, j+1] +
        padded_frame[i, j-1]                         + padded_frame[i, j+1] +
        padded_frame[i+1, j-1] + padded_frame[i+1, j] + padded_frame[i+1, j+1]
    )
    return neighbors

def apply_rules(padded_frame):
    
    rows, cols = padded_frame.shape
    new_padded_frame = np.zeros_like(padded_frame)
    
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            current_cell = padded_frame[i, j]
            neighbors_count = count_neighbors(padded_frame, i, j)
            
            if current_cell == 0 and neighbors_count == 3:
                new_padded_frame[i, j] = 1
            elif current_cell == 1 and neighbors_count in [2, 3]:
                new_padded_frame[i, j] = 1
            else:
                new_padded_frame[i, j] = 0
    
    return new_padded_frame

def remove_padding(padded_frame):
    """
    Enlèver le padding pour retourner à la grille 7x7
    """
    pass

frame = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
])

print("Grille initiale:")
print(frame)