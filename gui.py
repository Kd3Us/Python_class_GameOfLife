import arcade
import os
import tkinter as tk
from tkinter import simpledialog
from groq import Groq
import json
import re
from dotenv import load_dotenv
from game_of_life import GameOfLife

# Charger les variables d'environnement
load_dotenv()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Jeu de la Vie"

GRID_WIDTH = 50
GRID_HEIGHT = 40
CELL_SIZE = 12

BACKGROUND_COLOR = (15, 15, 25)
ALIVE_COLOR = (0, 255, 150)
GRID_COLOR = (40, 40, 60)
TEXT_COLOR = (220, 220, 240)
ACCENT_COLOR = (255, 100, 100)

class GameOfLifeWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)
        
        self.game = GameOfLife(GRID_WIDTH, GRID_HEIGHT)
        
        self.paused = True
        self.update_timer = 0
        self.update_speed = 0.2
        self.show_grid = True
        
        self.offset_x = (SCREEN_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
        self.offset_y = (SCREEN_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2
        
        self.mouse_pressed = False
        self.last_cell_pos = None
        
        # Groq client
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.ai_mode = False
    
    def on_draw(self):
        self.clear()
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                x = self.offset_x + j * CELL_SIZE
                y = self.offset_y + (GRID_HEIGHT - 1 - i) * CELL_SIZE
                
                if self.game.grid[i, j] == 1:
                    arcade.draw_rectangle_filled(
                        x + CELL_SIZE // 2, 
                        y + CELL_SIZE // 2, 
                        CELL_SIZE + 2, 
                        CELL_SIZE + 2, 
                        (*ALIVE_COLOR, 60)
                    )
                    arcade.draw_rectangle_filled(
                        x + CELL_SIZE // 2, 
                        y + CELL_SIZE // 2, 
                        CELL_SIZE - 1, 
                        CELL_SIZE - 1, 
                        ALIVE_COLOR
                    )
                    arcade.draw_rectangle_filled(
                        x + CELL_SIZE // 2, 
                        y + CELL_SIZE // 2, 
                        CELL_SIZE - 4, 
                        CELL_SIZE - 4, 
                        (255, 255, 255, 80)
                    )
        
        if self.show_grid:
            for i in range(GRID_HEIGHT + 1):
                y = self.offset_y + i * CELL_SIZE
                arcade.draw_line(
                    self.offset_x, y, 
                    self.offset_x + GRID_WIDTH * CELL_SIZE, y, 
                    GRID_COLOR, 1
                )
            
            for j in range(GRID_WIDTH + 1):
                x = self.offset_x + j * CELL_SIZE
                arcade.draw_line(
                    x, self.offset_y, 
                    x, self.offset_y + GRID_HEIGHT * CELL_SIZE, 
                    GRID_COLOR, 1
                )
        
        self._draw_ui()
    
    def _draw_ui(self):
        arcade.draw_rectangle_filled(
            100, SCREEN_HEIGHT - 50, 180, 80, 
            (0, 0, 0, 120)
        )
        
        arcade.draw_text(
            f"Generation: {self.game.generation}", 
            11, SCREEN_HEIGHT - 29, 
            (0, 0, 0), 16
        )
        arcade.draw_text(
            f"Generation: {self.game.generation}", 
            10, SCREEN_HEIGHT - 30, 
            TEXT_COLOR, 16
        )
        
        status = "PAUSE" if self.paused else "RUNNING"
        status_color = TEXT_COLOR if self.paused else ACCENT_COLOR
        
        arcade.draw_text(
            f"Status: {status}", 
            11, SCREEN_HEIGHT - 59, 
            (0, 0, 0), 16
        )
        arcade.draw_text(
            f"Status: {status}", 
            10, SCREEN_HEIGHT - 60, 
            status_color, 16
        )
        
        instructions = [
            "SPACE: Play/Pause",
            "G: Toggle Grid", 
            "R/C: Clear",
            "A: AI Pattern",
            "Drag: Paint cells"
        ]
        
        for i, instruction in enumerate(instructions):
            arcade.draw_text(
                instruction, 
                11, 21 + i * 20, 
                (0, 0, 0), 11
            )
            arcade.draw_text(
                instruction, 
                10, 20 + i * 20, 
                TEXT_COLOR, 11
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
        elif key == arcade.key.G:
            self.show_grid = not self.show_grid
        elif key == arcade.key.A:
            self._prompt_ai_pattern()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = True
            self._draw_at_position(x, y)
    
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = False
            self.last_cell_pos = None
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressed:
            self._draw_at_position(x, y)
    
    def _draw_at_position(self, x, y):
        grid_x = int((x - self.offset_x) // CELL_SIZE)
        grid_y = int(GRID_HEIGHT - 1 - ((y - self.offset_y) // CELL_SIZE))
        
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            current_cell = (grid_y, grid_x)
            if current_cell != self.last_cell_pos:
                self.game.grid[grid_y, grid_x] = 1
                self.last_cell_pos = current_cell
    
    def _prompt_ai_pattern(self):
        root = tk.Tk()
        root.withdraw()
        
        user_input = simpledialog.askstring(
            "AI Pattern Generator", 
            "Décris le pattern que tu veux (ex: 'un crabe qui danse', 'une spirale', 'un coeur'):"
        )
        
        root.destroy()
        
        if user_input:
            self._generate_ai_pattern(user_input)
    
    def _generate_ai_pattern(self, description):
        try:
            prompt = f"""Tu es un expert en Conway's Game of Life créatif.

                        TÂCHE: Créer un pattern pour "{description}" sur une grille 50x40.

                        RÈGLES IMPORTANTES:
                        - Pour les formes arrondies (rond, cercle, ovale), utilise des approximations géométriques
                        - EXEMPLE de rond approximatif : place des cellules en carré avec des coins arrondis
                        - EXEMPLE de cercle : utilise un octogone ou hexagone
                        - Pour "rond", pense à un carré avec des diagonales coupées

                        STRATÉGIE pour "{description}":
                        - Si c'est arrondi → utilise des formes polygonales (hexagone, octogone)
                        - Si c'est droit → utilise des lignes et carrés
                        - Sois pratique, pas perfectionniste

                        RÉPONSE OBLIGATOIRE: Tu DOIS répondre UNIQUEMENT avec ce JSON exact :

                        {{"pattern": [[ligne, colonne], [ligne, colonne]]}}

                        Coordonnées: lignes 0-39, colonnes 0-49."""
            
            completion = self.groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=1000
            )
            
            response = completion.choices[0].message.content
            self._apply_ai_pattern(response)
            
        except Exception as e:
            print(f"Erreur API Groq : {e}")
    
    def _apply_ai_pattern(self, ai_response):
        try:
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                pattern_data = json.loads(json_match.group())
                
                self.game.clear()
                
                for row, col in pattern_data["pattern"]:
                    if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                        self.game.grid[row, col] = 1
                        
                print(f"Pattern appliqué : {len(pattern_data['pattern'])} cellules")
            else:
                print("Impossible d'extraire le pattern de la réponse")
                
        except Exception as e:
            print(f"Erreur lors de l'application du pattern : {e}")

def main():
    window = GameOfLifeWindow()
    arcade.run()

if __name__ == "__main__":
    main()