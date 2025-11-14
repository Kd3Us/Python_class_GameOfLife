import arcade
from game_of_life import GameOfLife

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Jeu de la Vie"

GRID_WIDTH = 50
GRID_HEIGHT = 40
CELL_SIZE = 12

BACKGROUND_COLOR = arcade.color.BLACK
ALIVE_COLOR = arcade.color.WHITE
GRID_COLOR = arcade.color.DARK_GRAY

class GameOfLifeWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)
        
        self.game = GameOfLife(GRID_WIDTH, GRID_HEIGHT)
        
        self.paused = True
        self.update_timer = 0
        self.update_speed = 0.2
        
        self.offset_x = (SCREEN_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2
    
    def on_draw(self):
        self.clear()
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.game.grid[i, j] == 1:
                    x = self.offset_x + j * CELL_SIZE
                    y = self.offset_y + (GRID_HEIGHT - 1 - i) * CELL_SIZE
                    arcade.draw_rectangle_filled(
                        x + CELL_SIZE // 2, 
                        y + CELL_SIZE // 2, 
                        CELL_SIZE - 1, 
                        CELL_SIZE - 1, 
                        ALIVE_COLOR
                    )
        
        for i in range(GRID_HEIGHT + 1):
            y = self.offset_y + i * CELL_SIZE
            arcade.draw_line(
                self.offset_x, y, 
                self.offset_x + GRID_WIDTH * CELL_SIZE, y, 
                GRID_COLOR
            )
        
        for j in range(GRID_WIDTH + 1):
            x = self.offset_x + j * CELL_SIZE
            arcade.draw_line(
                x, self.offset_y, 
                x, self.offset_y + GRID_HEIGHT * CELL_SIZE, 
                GRID_COLOR
            )
        
        arcade.draw_text(
            f"Generation: {self.game.generation}", 
            10, SCREEN_HEIGHT - 30, 
            arcade.color.WHITE, 16
        )
        
        status = "PAUSE" if self.paused else "RUNNING"
        arcade.draw_text(
            f"Status: {status}", 
            10, SCREEN_HEIGHT - 60, 
            arcade.color.WHITE, 16
        )
        
        arcade.draw_text(
            "SPACE: Play/Pause | R/C: Clear | Click: Toggle cell", 
            10, 10, 
            arcade.color.WHITE, 12
        )
    
    def on_update(self, delta_time):
        if not self.paused:
            self.update_timer += delta_time
            if self.update_timer >= self.update_speed:
                self.game.apply_rules()
                self.update_timer = 0
                
                if self.game.is_extinct():
                    self.paused = True
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.paused = not self.paused
        elif key == arcade.key.R or key == arcade.key.C:
            self.game.clear()
            self.paused = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            grid_x = int((x - self.offset_x) // CELL_SIZE)
            grid_y = int(GRID_HEIGHT - 1 - ((y - self.offset_y) // CELL_SIZE))
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                self.game.toggle_cell(grid_y, grid_x)

def main():
    window = GameOfLifeWindow()
    arcade.run()

if __name__ == "__main__":
    main()