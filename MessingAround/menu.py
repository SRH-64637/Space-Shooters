import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.game.menu_running, self.game.game_running = True, False
        self.mid_w, self.mid_h = self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.screen, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = None
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionx, self.optiony = self.mid_w, self.mid_h + 50
        self.creditsx, self.credity = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        """Main menu loop."""
        while self.game.menu_running:
            self.move_cursor()  # Move cursor with keys

            # Draw menu
            self.game.screen.fill((0, 0, 0))
            self.game.draw_text("Main Menu", 20, self.mid_w, self.mid_h - 40)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionx, self.optiony)
            self.game.draw_text("Credits", 20, self.creditsx, self.credity)

            # Draw cursor and update screen
            self.draw_cursor()
            self.blit_screen()

            # Check input to start the game
            self.check_input()
            self.game.reset_keys()

    def move_cursor(self):
        """Handle cursor movement with Up and Down keys."""
        if self.game.Down_key:
            if self.state == None or self.state == "Start":
                self.cursor_rect.midtop = (self.optionx + self.offset, self.optiony)
                self.state = "Options"

            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.credity)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

        elif self.game.Up_key:
            if self.state == None or self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.credity)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionx + self.offset, self.optiony)
                self.state = "Options"

    def check_input(self):
        self.game.check_events()
        self.move_cursor()
        if self.game.Enter_key:
            if self.state == "Start" or self.state == None:
                self.start_game()
                self.game.initialize_game()
            elif self.state == "Options":
                print("Options selected")  # Placeholder for options logic
            elif self.state == "Credits":
                print("Credits selected")  # Placeholder for credits logic

    def start_game(self):
        """Exit the menu and start the game."""
        self.game.menu_running = False  # Exit the menu loop
        self.game.game_running = True  # Start the game loop
