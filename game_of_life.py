import numpy as np

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.generation = 0
    
    def count_neighbors(self, i, j):
        rows, cols = self.grid.shape
        neighbors = (
            self.grid[(i-1) % rows, (j-1) % cols] + self.grid[(i-1) % rows, j] + self.grid[(i-1) % rows, (j+1) % cols] +
            self.grid[i, (j-1) % cols]                                        + self.grid[i, (j+1) % cols] +
            self.grid[(i+1) % rows, (j-1) % cols] + self.grid[(i+1) % rows, j] + self.grid[(i+1) % rows, (j+1) % cols]
        )
        return neighbors
    
    def apply_rules(self):
        rows, cols = self.grid.shape
        new_grid = np.zeros_like(self.grid)
        
        for i in range(rows):
            for j in range(cols):
                current_cell = self.grid[i, j]
                neighbors_count = self.count_neighbors(i, j)
                
                if current_cell == 0 and neighbors_count == 3:
                    new_grid[i, j] = 1
                elif current_cell == 1 and neighbors_count in [2, 3]:
                    new_grid[i, j] = 1
                else:
                    new_grid[i, j] = 0
        
        self.grid = new_grid
        self.generation += 1
    
    def set_pattern(self, pattern, start_row=None, start_col=None):
        if start_row is None:
            start_row = (self.height - pattern.shape[0]) // 2
        if start_col is None:
            start_col = (self.width - pattern.shape[1]) // 2
        
        end_row = min(start_row + pattern.shape[0], self.height)
        end_col = min(start_col + pattern.shape[1], self.width)
        
        self.grid[start_row:end_row, start_col:end_col] = pattern[:end_row-start_row, :end_col-start_col]
    
    def clear(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.generation = 0
    
    def toggle_cell(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row, col] = 1 - self.grid[row, col]
    
    def is_extinct(self):
        return np.sum(self.grid) == 0