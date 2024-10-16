import pygame
import random
import block
import os
from player import Player
from enemy import Enemy
from menu import MainMenu


# Screen setup
class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        self.menu_running, self.game_running = True, False
        self.Enter_key, self.Up_key, self.Down_key = False, False, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.window = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font_name = os.path.join("MessingAround", "assets/8-BIT WONDER.TTF")
        pygame.display.set_caption("SPACE SHOOTERS")
        self.curr_menu = MainMenu(self)
        self.heart_image = pygame.image.load(
            os.path.join("MessingAround", "assets/heart-removebg-preview.png")
        ).convert_alpha()
        # Set the size you want to scale the image to
        new_size = (60, 60)  # Change this to your desired size
        # Scale the heart image
        self.heart_image = pygame.transform.scale(self.heart_image, new_size)
        self.lives = 5
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))
        # Initialize clock and FPS after menu initialization
        self.FPS = 60
        self.score = 0
        self.clock = pygame.time.Clock()

        # Call the menu display function here instead
        self.curr_menu.display_menu()

    def game_loop(self):
        self.game_running = True
        while self.game_running:
            self.clock.tick(self.FPS)
            self.check_events()  # Check for events
            self.update()  # Update game elements
            self.draw()  # Draw everything
            pygame.display.update()

    def update(self):
        # Update player, enemies, and handle lasers
        self.player_group.update()
        self.enemy_group.update()

        # Check if all enemies are defeated
        if len(self.enemy_group) == 0:
            self.game_win()  # Trigger win if all enemies are defeated

        for laser in self.player_laser_group:
            self.plaser_block(laser, self.block_group, self.player_laser_group)
            self.plaser_enemy(laser, self.enemy_group, self.player_laser_group)

        for enemy in self.enemy_group:
            for e_laser in enemy.enemy_laser_group:
                self.elaser_block(e_laser, self.block_group, enemy.enemy_laser_group)
                self.elaser_player(e_laser, self.player_group, enemy.enemy_laser_group)

    def draw(self):
        self.screen.blit(self.BG2, (0, 0))
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.player_laser_group.draw(self.screen)
        self.block_group.draw(self.screen)

        # Draw enemy lasers
        for enemy in self.enemy_group:
            enemy.enemy_laser_group.draw(self.screen)

        # Draw hearts to indicate remaining lives
        self.draw_hearts()

    def handle_collisions(self):
        for laser in self.player_laser_group:
            self.plaser_enemy(laser, self.enemy_group, self.player_laser_group)
            self.plaser_block(laser, self.block_group, self.player_laser_group)

        for alien in self.enemy_group:
            for e_laser in alien.enemy_laser_group:
                self.elaser_block(e_laser, self.block_group, alien.enemy_laser_group)
                self.elaser_player(e_laser, self.player_group, alien.enemy_laser_group)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.Up_key = True

                if event.key == pygame.K_DOWN:
                    self.Down_key = True

                if event.key == pygame.K_RETURN:  # Start game on Enter key
                    self.Enter_key = True

    def reset_keys(self):
        self.Enter_key, self.Up_key, self.Down_key = False, False, False

    def initialize_game(self):
        BG = pygame.image.load(
            os.path.join("MessingAround", "assets/background-black.png")
        ).convert_alpha()
        self.BG2 = pygame.transform.scale(BG, (800, 600))
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # Create player objects
        player = Player(400, 500, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.player_laser_group = player.player_laser_group
        self.player_group.add(player)
        self.create_enemies()

        # Create obstacle blocks
        self.block_size = 8
        self.block_color = (241, 79, 80)
        self.block_group = pygame.sprite.Group()
        self.create_block(block.shape, 50, self.SCREEN_HEIGHT - 200)
        self.create_block(block.shape, 360, self.SCREEN_HEIGHT - 200)
        self.create_block(block.shape, 680, self.SCREEN_HEIGHT - 200)

        self.game_loop()

    def create_block(self, shapes, pos_x, pos_y):
        for row_index, row in enumerate(shapes):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = col_index * self.block_size + pos_x
                    y = row_index * self.block_size + pos_y
                    blocks = block.Block(self.block_size, (241, 79, 80), x, y)
                    self.block_group.add(blocks)

    def create_enemies(self):
        # Spawn columns and a range for staggered heights.
        x_vals = [100, 200, 300, 400, 500, 600, 700]
        y_offsets = [
            50,
            100,
            150,
            200,
            250,
            300,
        ]  # Different heights to avoid clustering

        laser_intervals = (1000, 3000, 5000)  # Enemy fire rate variety
        colors = ("blue", "green", "red")  # Enemy color variety

        for i in range(8):  # Adjust number of enemies to prevent screen clutter
            x = random.choice(x_vals)
            y = random.choice(y_offsets)  # Staggered vertical starting points
            speed = random.uniform(1.5, 3.5)  # Control speed to avoid extreme values

            # Create the enemy and add to the group
            enemy = Enemy(
                random.choice(colors),
                x,
                y,  # Ensure it doesn't overlap with top of the screen
                speed + 2,  # Ensure minimum movement for all enemies
                1,  # Randomize movement direction
                self.SCREEN_WIDTH,
                self.SCREEN_HEIGHT,
                random.choice(laser_intervals),
                pygame.sprite.Group(),
            )

            self.enemy_group.add(enemy)

    def draw_hearts(self):
        """Display the player's remaining lives as hearts."""
        for i in range(self.lives):
            # Add a subtle vibration effect to hearts
            offset = random.randint(-1, 1)  # Slight random shift for vibration
            x = 10 + (i * 40) + offset
            y = 10 + offset
            self.screen.blit(self.heart_image, (x, y))

    def game_win(self):
        print("Congratulations! You've defeated all the enemies.")  # Debug message
        self.draw_text("You Win!", 50, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds before quitting
        self.game_running = False  # Stop the game loop
        pygame.quit()
        exit()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (250, 250, 250))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Collision checks
    def plaser_enemy(self, laser, group, laser_group):
        if pygame.sprite.spritecollide(laser, group, False):
            if pygame.sprite.spritecollide(
                laser, group, True, pygame.sprite.collide_mask
            ):
                laser_group.remove(laser)

    def elaser_block(self, laser, group, laser_group):
        if pygame.sprite.spritecollide(laser, group, False):
            if pygame.sprite.spritecollide(
                laser, group, True, pygame.sprite.collide_mask
            ):
                laser_group.remove(laser)

    def plaser_block(self, laser, group, laser_group):
        if pygame.sprite.spritecollide(laser, group, True, pygame.sprite.collide_mask):
            laser_group.remove(laser)

    def elaser_player(self, laser, group, laser_group):
        if pygame.sprite.spritecollide(laser, group, False, pygame.sprite.collide_mask):
            laser_group.remove(laser)
            self.lives -= 1  # Decrease lives by 1

            if self.lives <= 0:
                self.game_over()  # End the game if out of lives

    def game_over(self):
        print("You've lost the game. Better luck next time.")  # Debug message
        self.draw_text(
            "Game Over!", 50, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2
        )
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds before quitting
        self.game_running = False  # Stop the game loop
        pygame.quit()
        exit()  # Ensure the program exits


game = Game()
