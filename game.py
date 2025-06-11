import pygame
import config

class GameOfLife:
    """
    Klasa reprezentująca logikę gry w życie Conwaya.
    Odpowiada za aktualizację siatki, rysowanie komórek i obsługę ich stanu.
    """
    def __init__(self):
        """Inicjalizuje pustą siatkę i ustawia stan gry na zatrzymany."""
        self.grid = [[0 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
        self.running = False

    def toggle_cell(self, x, y):
        """
        Zmienia stan komórki (żywa/martwa) na podanej pozycji, jeśli gra jest zatrzymana.

        :param x: Pozycja X komórki
        :param y: Pozycja Y komórki
        """
        if not self.running:
            if 0 <= y < config.GRID_HEIGHT and 0 <= x < config.GRID_WIDTH:
                self.grid[y][x] = 1 - self.grid[y][x]

    def clear(self):
        """Czyści siatkę, ustawiając wszystkie komórki jako martwe."""
        if not self.running:
            self.grid = [[0 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]

    def update(self):
        """
        Aktualizuje siatkę zgodnie z zasadami gry w życie:
        - Komórka żywa z 2 lub 3 sąsiadami przeżywa.
        - Martwa komórka z dokładnie 3 sąsiadami ożywa.
        """
        if self.running:
            new_grid = [[0 for _ in range(config.GRID_WIDTH)] for _ in range(config.GRID_HEIGHT)]
            for y in range(config.GRID_HEIGHT):
                for x in range(config.GRID_WIDTH):
                    alive = self.grid[y][x]
                    neighbors = self.count_neighbors(x, y)

                    if alive and neighbors in [2, 3]:
                        new_grid[y][x] = 1
                    elif not alive and neighbors == 3:
                        new_grid[y][x] = 1
            self.grid = new_grid

    def count_neighbors(self, x, y):
        """
        Zlicza żywych sąsiadów komórki (z uwzględnieniem otaczającego torusa).

        :param x: Pozycja X komórki
        :param y: Pozycja Y komórki
        :return: Liczba żywych sąsiadów
        """
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % config.GRID_WIDTH, (y + dy) % config.GRID_HEIGHT
                count += self.grid[ny][nx]
        return count

    def draw(self, screen):
        """
        Rysuje żywe komórki oraz siatkę na ekranie.

        :param screen: Obiekt ekranu Pygame
        """
        for y in range(config.GRID_HEIGHT):
            for x in range(config.GRID_WIDTH):
                if self.grid[y][x]:
                    rect = pygame.Rect(x * config.CELL_SIZE, y * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
                    pygame.draw.rect(screen, config.CELL_COLOR, rect)

        for x in range(0, config.GRID_WIDTH * config.CELL_SIZE, config.CELL_SIZE):
            pygame.draw.line(screen, config.GRID_COLOR, (x, 0), (x, config.GRID_HEIGHT * config.CELL_SIZE))
        for y in range(0, config.GRID_HEIGHT * config.CELL_SIZE, config.CELL_SIZE):
            pygame.draw.line(screen, config.GRID_COLOR, (0, y), (config.GRID_WIDTH * config.CELL_SIZE, y))
