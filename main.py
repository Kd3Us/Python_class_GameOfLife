import numpy as np

def add_padding(frame):
    
    rows, cols = frame.shape
    padded_frame = np.zeros((rows + 2, cols + 2), dtype=int)
    padded_frame[1:rows+1, 1:cols+1] = frame
    return padded_frame

def count_neighbors(padded_frame, i, j):
    """
    Compter le nombre de voisins vivants autour de la cellule (i,j)
    """
    pass

def apply_rules(padded_frame):
    """
    Appliquer les règles du jeu de la vie
    Retourne la nouvelle grille avec padding
    """
    pass

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