import pygame
import sys
import config
from game import GameOfLife
from gui import start_screen, pause_menu, settings_menu

pygame.init()

def create_screen():
    """
    Tworzy i zwraca powierzchnię Pygame o rozmiarze określonym w konfiguracji.

    :return: Obiekt pygame.Surface reprezentujący okno gry.
    """
    return pygame.display.set_mode((config.GRID_WIDTH * config.CELL_SIZE, config.GRID_HEIGHT * config.CELL_SIZE))

screen = create_screen()
pygame.display.set_caption("Gra w życie – Conway (stopped)")
clock = pygame.time.Clock()

def main():
    """
    Główna funkcja programu zarządzająca ekranem startowym oraz uruchamianiem gry.
    Po wybraniu opcji "start" uruchamia pętlę gry.
    """
    game = GameOfLife()

    while True:
        action = start_screen(screen)
        if action == "start":
            run_game(game)
        else:
            break

def run_game(game):
    """
    Uruchamia główną pętlę gry, obsługując zdarzenia, rysowanie i pauzę.

    :param game: Instancja klasy GameOfLife zarządzająca logiką gry.
    """
    global screen, clock

    paused = False

    while True:
        screen.fill(config.BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.running = not game.running
                    title_state = "started" if game.running else "stopped"
                    pygame.display.set_caption(f"Gra w życie – Conway ({title_state})")

                elif event.key == pygame.K_c:
                    game.clear()

                elif event.key == pygame.K_ESCAPE:
                    paused = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                cell_x = x // config.CELL_SIZE
                cell_y = y // config.CELL_SIZE
                game.toggle_cell(cell_x, cell_y)

        if paused:
            choice = pause_menu(screen)
            if choice == "resume":
                paused = False
            elif choice == "settings":
                result = settings_menu(screen)
                if result == "saved":
                    screen = pygame.display.set_mode((config.GRID_WIDTH * config.CELL_SIZE, config.GRID_HEIGHT * config.CELL_SIZE))
                    game = GameOfLife()
                    paused = False
                elif result == "cancel":
                    paused = False
            elif choice == "menu":
                return
            elif choice == "quit":
                pygame.quit()
                sys.exit()

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(config.FPS)

if __name__ == "__main__":
    main()
