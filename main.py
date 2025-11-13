import numpy as np

# def add_padding(frame):
    
#     rows, cols = frame.shape
#     padded_frame = np.zeros((rows + 2, cols + 2), dtype=int)
#     padded_frame[1:rows+1, 1:cols+1] = frame
#     return padded_frame

def count_neighbors(frame, i, j):

    rows, cols = frame.shape
    neighbors = (
        frame[(i-1) % rows, (j-1) % cols] + frame[(i-1) % rows, j] + frame[(i-1) % rows, (j+1) % cols] +
        frame[i, (j-1) % cols]                                    + frame[i, (j+1) % cols] +
        frame[(i+1) % rows, (j-1) % cols] + frame[(i+1) % rows, j] + frame[(i+1) % rows, (j+1) % cols]
    )
    return neighbors

def apply_rules(frame):

    rows, cols = frame.shape
    new_frame = np.zeros_like(frame)
    
    for i in range(rows):
        for j in range(cols):
            current_cell = frame[i, j]
            neighbors_count = count_neighbors(frame, i, j)
            
            if current_cell == 0 and neighbors_count == 3:
                new_frame[i, j] = 1
            elif current_cell == 1 and neighbors_count in [2, 3]:
                new_frame[i, j] = 1
            else:
                new_frame[i, j] = 0

    return new_frame

# def remove_padding(padded_frame):
#     return padded_frame[1:-1, 1:-1]

frame = np.array([
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
])

print("Grille initiale:")
print(frame)

generation = 0
while True:
    try:
        input(f"\nAppuyez sur Entrée pour la génération {generation + 1} (Ctrl+C pour quitter)...")
        
        frame = apply_rules(frame)
        generation += 1
        
        print(f"Génération {generation}:")
        print(frame)
        
        if np.sum(frame) == 0:
            print("Simulation terminée - extinction!")
            break
    except KeyboardInterrupt:
        print("\nSimulation arrêtée!")
        break