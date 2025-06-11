import pygame
import config

class Button:
    """
    Klasa reprezentująca przycisk interfejsu użytkownika.

    :param text: Tekst wyświetlany na przycisku.
    :type text: str
    :param pos: Pozycja lewego górnego rogu przycisku w formacie (x, y).
    :type pos: tuple[int, int]
    :param size: Rozmiar przycisku w formacie (szerokość, wysokość).
    :type size: tuple[int, int]
    :param font_size: Rozmiar czcionki tekstu przycisku, domyślnie 30.
    :type font_size: int
    """
    def __init__(self, text, pos, size, font_size=30):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color = config.BUTTON_COLOR
        self.font = pygame.font.SysFont("arial", font_size)
        self.hovered = False

    def draw(self, screen):
        """
        Rysuje przycisk na podanym ekranie.

        :param screen: Obiekt ekranu (powierzchnia Pygame), na którym ma być narysowany przycisk.
        :type screen: pygame.Surface
        """
        color = config.BUTTON_HOVER_COLOR if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        label = self.font.render(self.text, True, config.BG_COLOR)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def is_hovered(self, mouse_pos):
        """
        Sprawdza, czy mysz znajduje się nad przyciskiem.

        :param mouse_pos: Aktualna pozycja myszy w formacie (x, y).
        :type mouse_pos: tuple[int, int]
        """
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        """
        Sprawdza, czy mysz kliknęła przycisk.

        :param mouse_pos: Pozycja kliknięcia myszy.
        :type mouse_pos: tuple[int, int]
        :return: True jeśli kliknięto na przycisk, False w przeciwnym wypadku.
        :rtype: bool
        """
        return self.rect.collidepoint(mouse_pos)


def settings_menu(screen):
    """
    Wyświetla menu ustawień, w którym można zmieniać FPS i kolor komórek.

    :param screen: Ekran, na którym renderowane jest menu.
    :type screen: pygame.Surface
    :return: 'saved' jeśli zapisano ustawienia, 'cancel' jeśli anulowano.
    :rtype: str
    """
    font = pygame.font.SysFont("arial", 48)
    small_font = pygame.font.SysFont("arial", 28)
    title = font.render("Ustawienia", True, config.CELL_COLOR)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 80))

    fps = config.FPS
    colors = [
        ((255, 215, 0), "Żółty"),
        ((255, 0, 0), "Czerwony"),
        ((0, 255, 0), "Zielony"),
        ((0, 128, 255), "Niebieski"),
        ((255, 105, 180), "Różowy"),
    ]
    selected_color_index = next((i for i, (col, _) in enumerate(colors) if col == config.CELL_COLOR), 0)

    center_x = screen.get_width() // 2
    column_width = 200

    fps_minus = Button("-", (center_x - 100, 150), (40, 40))
    fps_plus = Button("+", (center_x + 60, 150), (40, 40))
    color_next = Button("Następny", (center_x - 100, 230), (120, 40))
    save_button = Button("Zapisz", (center_x - 150, 320), (120, 50))
    cancel_button = Button("Anuluj", (center_x + 30, 320), (120, 50))

    while True:
        screen.fill(config.BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(title, title_rect)

        fps_label = small_font.render("FPS:", True, config.TEXT_COLOR)
        screen.blit(fps_label, (center_x - column_width, 160))

        fps_value = small_font.render(str(fps), True, config.TEXT_COLOR)
        fps_value_rect = fps_value.get_rect(center=(center_x, 170))
        screen.blit(fps_value, fps_value_rect)

        color_label = small_font.render("Kolor:", True, config.TEXT_COLOR)
        screen.blit(color_label, (center_x - column_width, 240))

        color_next.is_hovered(mouse_pos)
        color_next.draw(screen)

        color_name = colors[selected_color_index][1]
        color_name_surf = small_font.render(color_name, True, config.TEXT_COLOR)
        color_name_rect = color_name_surf.get_rect(midleft=(center_x + 30, 250))
        screen.blit(color_name_surf, color_name_rect)

        pygame.draw.rect(screen, colors[selected_color_index][0], (color_name_rect.right + 20, 235, 40, 40))

        for btn in [fps_minus, fps_plus, save_button, cancel_button]:
            btn.is_hovered(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fps_minus.is_clicked(event.pos) and fps > 1:
                    fps -= 1
                elif fps_plus.is_clicked(event.pos) and fps < 60:
                    fps += 1
                elif color_next.is_clicked(event.pos):
                    selected_color_index = (selected_color_index + 1) % len(colors)
                elif save_button.is_clicked(event.pos):
                    config.FPS = fps
                    config.CELL_COLOR = colors[selected_color_index][0]
                    return "saved"
                elif cancel_button.is_clicked(event.pos):
                    return "cancel"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "cancel"


def start_screen(screen):
    """
    Wyświetla ekran startowy gry z opcją rozpoczęcia lub zakończenia gry.

    :param screen: Ekran, na którym renderowany jest interfejs.
    :type screen: pygame.Surface
    :return: 'start' lub 'quit' w zależności od wyboru użytkownika.
    :rtype: str
    """
    font = pygame.font.SysFont("arial", 60)
    title = font.render("Gra w życie - Conway", True, config.CELL_COLOR)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 100))

    start_btn = Button("Start", (screen.get_width() // 2 - 60, 250), (120, 50))
    quit_btn = Button("Wyjdź", (screen.get_width() // 2 - 60, 320), (120, 50))

    while True:
        screen.fill(config.BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(title, title_rect)

        for btn in [start_btn, quit_btn]:
            btn.is_hovered(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.is_clicked(event.pos):
                    return "start"
                elif quit_btn.is_clicked(event.pos):
                    return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"


def pause_menu(screen):
    """
    Wyświetla menu pauzy z opcjami: wznowienia gry, ustawień, powrotu do menu i wyjścia.

    :param screen: Ekran, na którym renderowane jest menu.
    :type screen: pygame.Surface
    :return: Jedna z wartości: 'resume', 'settings', 'menu', 'quit'.
    :rtype: str
    """
    font = pygame.font.SysFont("arial", 60)
    title = font.render("PAUZA", True, config.CELL_COLOR)
    title_rect = title.get_rect(center=(screen.get_width() // 2, 100))

    resume_btn = Button("Wznów", (screen.get_width() // 2 - 80, 250), (160, 50))
    settings_btn = Button("Ustawienia", (screen.get_width() // 2 - 80, 320), (160, 50))
    menu_btn = Button("Menu", (screen.get_width() // 2 - 80, 390), (160, 50))
    quit_btn = Button("Wyjdź", (screen.get_width() // 2 - 80, 460), (160, 50))

    while True:
        screen.fill(config.BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(title, title_rect)

        for btn in [resume_btn, settings_btn, menu_btn, quit_btn]:
            btn.is_hovered(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_btn.is_clicked(event.pos):
                    return "resume"
                elif settings_btn.is_clicked(event.pos):
                    return "settings"
                elif menu_btn.is_clicked(event.pos):
                    return "menu"
                elif quit_btn.is_clicked(event.pos):
                    return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
