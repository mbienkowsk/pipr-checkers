import pygame
from sys import exit
from constants import (WIN_WIDTH, WIN_HEIGHT, FIELD_SIZE, MAX_FPS, PIECE_PADDING, GREEN, BROWN, SLEEP_TIME_IN_PVB_GAME, SLEEP_TIME_IN_BVB_GAME)
from piece_move_board import Board, Piece
from player import Player, Bot, MinimaxBot
from gui import draw_menu, draw_game_over_screen
from time import sleep


class Game:

    def __init__(self, screen, players, num_of_bots) -> None:
        self.board = Board()
        self.screen = screen
        self.load_images()
        self.players = players
        self.turn = 'white'
        self.selected_piece = None
        self.moves_without_attacks = 0
        self.is_over = False
        if num_of_bots == 1:
            self.sleep_duration = SLEEP_TIME_IN_PVB_GAME
        elif num_of_bots == 2:
            self.sleep_duration = SLEEP_TIME_IN_BVB_GAME
        else:
            self.sleep_duration = None

    def load_images(self):
        #   tone down the alpha value of the white pieces so they don't stand out after the game over animation
        WP = pygame.transform.scale(pygame.image.load('images/white_piece.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING))
        WP.set_alpha(200)
        WK = pygame.transform.scale(pygame.image.load('images/white_king.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING))
        WK.set_alpha(200)
        self.images = {
            'WP': WP,
            'BK': pygame.transform.scale(pygame.image.load('images/black_king.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
            'WK': WK,
            'BP': pygame.transform.scale(pygame.image.load('images/black_piece.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING))
        }

    def draw_board(self):
        self.draw_squares()
        self.draw_pieces()

    def draw_squares(self):
        for field in self.board.one_dimensional_field_list:
            field_rect = pygame.Rect(field.x * FIELD_SIZE, field.y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)
            pygame.draw.rect(self.screen, field.color, field_rect)

    def draw_pieces(self):
        for field in self.board.one_dimensional_field_list:
            if field.is_taken():
                current_piece = field.piece
                piece_surf = self.images[current_piece.image_dict_ind]
                piece_rect = piece_surf.get_rect(center=current_piece.location_to_draw())
                self.screen.blit(piece_surf, piece_rect)

    def highlight_field(self, field):
        field_surf = pygame.Surface((FIELD_SIZE, FIELD_SIZE))
        field_surf.fill(BROWN)
        square_rect = pygame.Rect(field.x * FIELD_SIZE, field.y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)
        pygame.draw.circle(field_surf, GREEN, (FIELD_SIZE / 2, FIELD_SIZE / 2), FIELD_SIZE * 0.35)
        self.screen.blit(field_surf, (square_rect))

    def show_possible_moves(self, piece: 'Piece'):
        self.draw_board()
        possible_moves = piece.all_possible_legal_moves(self.board)
        possible_move_squares = [self.board.get_field_by_location(move.new_cords) for move in possible_moves]
        for field in possible_move_squares:
            self.highlight_field(field)

    def player_by_color(self, color):
        player_color_dictionary = {
            player.color: player
            for player in self.players
        }
        return player_color_dictionary[color]

    def change_turn(self):
        self.turn = 'white' if self.turn == 'black' else 'black'

    def player_has_moving_options(self, color):
        player_dict = self.board.moves_by_colors[color]
        for value in player_dict.values():
            if len(value) > 0:
                return True
        return False

    def handle_piece_click(self, clicked_piece):
        self.board.update_pieces_by_colors()
        self.board.update_possible_moves_by_colors()
        if clicked_piece.color == self.turn and self.board.can_piece_move(clicked_piece):
            self.show_possible_moves(clicked_piece)
            self.selected_piece = clicked_piece
        else:
            self.selected_piece = None
            self.draw_board()

    @staticmethod
    def find_move_by_move_location(location, piece_move_list):
        for move in piece_move_list:
            if move.new_cords == location:
                return move
        raise IndexError('Tried to reach a nonexisting move')

    def handle_passive_move(self, move):
        self.board.move_piece(self.selected_piece, move)
        if self.selected_piece.eligible_for_promotion_after_move(move):
            self.selected_piece.promote()
        self.draw_board()
        self.change_turn()
        self.board.update_possible_moves_by_colors()
        if not self.player_has_moving_options(self.turn):
            self.is_over = True
        self.selected_piece = None

    def calculate_jumped_piece(self, move):
        old_x, old_y = move.old_cords
        next_x, next_y = move.new_cords
        jumped_x, jumped_y = int((old_x + next_x) / 2), int((old_y + next_y) / 2)
        piece = self.board.get_field_by_location((jumped_x, jumped_y)).piece
        return piece

    def handle_attacking_move(self, move):
        attacking_piece = move.piece
        self.selected_piece = attacking_piece
        jumped_piece = self.calculate_jumped_piece(move)
        self.board.delete_piece(jumped_piece)
        self.board.move_piece(attacking_piece, move)
        if attacking_piece.eligible_for_promotion_after_move(move):
            attacking_piece.promote()

        self.board.update_pieces_by_colors()
        self.board.update_possible_moves_by_colors()

        self.draw_board()
        if not attacking_piece.all_legal_attacking_moves(self.board):
            self.change_turn()
            if not self.player_has_moving_options(self.turn):
                self.is_over = True

        self.selected_piece = None
        return

    def handle_field_click(self, clicked_field):
        if self.selected_piece is not None:
            possible_move_locations, possible_moves = self.board.feasible_locations_and_moves_for_piece(self.selected_piece)

            if clicked_field.location in possible_move_locations:
                move_to_make = self.find_move_by_move_location(clicked_field.location, possible_moves)
                if move_to_make.attacking:
                    self.handle_attacking_move(move_to_make)
                    self.moves_without_attacks = 0

                else:
                    self.handle_passive_move(move_to_make)
                    self.moves_without_attacks += 1

    def interpret_clicked_pixel_location(self, location):
        x, y = location
        clicked_field_location = (int(x // FIELD_SIZE), int(y // FIELD_SIZE))
        clicked_field = self.board.get_field_by_location(clicked_field_location)
        clicked_piece = clicked_field.piece
        return clicked_field, clicked_piece

    def handle_mouse_click(self, click_position):
        clicked_field, clicked_piece = self.interpret_clicked_pixel_location(click_position)

        if clicked_piece is not None:
            self.handle_piece_click(clicked_piece)

        else:
            self.handle_field_click(clicked_field)

    def make_random_bot_move(self):
        sleep(self.sleep_duration)
        bot = self.player_by_color(self.turn)
        if bot.color == 'white':
            movable_pieces = [piece for piece in self.board.all_white_pieces() if self.board.moves_by_colors['white'][piece]]
            piece_click_location = bot.click_random_piece(movable_pieces)
        else:
            movable_pieces = [piece for piece in self.board.all_black_pieces() if self.board.moves_by_colors['black'][piece]]
            piece_click_location = bot.click_random_piece(movable_pieces)
        self.handle_mouse_click(piece_click_location)
        moves_for_chosen_piece = self.board.feasible_locations_and_moves_for_piece(self.selected_piece)[1]
        move_click_location = bot.choose_random_possible_move_location(moves_for_chosen_piece)
        self.handle_mouse_click(move_click_location)


def main():
    pygame.init()
    game_running = False
    menu_active = True
    game_over_screen_active = False

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    while True:
        if not game_running:
            if menu_active:
                pvp_button, pvb_button, bvb_button = draw_menu(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        if pvp_button.collidepoint(mouse_position):
                            game_running = True
                            menu_active = False
                            game = Game(screen, [Player('white'), Player('black')], 0)
                            game.draw_board()
                        if pvb_button.collidepoint(mouse_position):
                            game_running = True
                            menu_active = False
                            game = Game(screen, [Player('white'), MinimaxBot('black')], 1)
                            game.draw_board()
                        if bvb_button.collidepoint(mouse_position):
                            game_running = True
                            menu_active = False
                            game = Game(screen, [MinimaxBot('white'), Bot('black')], 2)
                            game.draw_board()

            elif game_over_screen_active:
                draw_game_over_screen(screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                        game_over_screen_active = False
                        menu_active = True
                        draw_menu(screen)
        else:
            if game.player_by_color(game.turn).ai:
                if isinstance(game.player_by_color(game.turn), MinimaxBot):
                    piece_click, field_click = game.player_by_color(game.turn).make_move(game.board)
                    game.handle_mouse_click(piece_click)
                    game.handle_mouse_click(field_click)
                else:
                    game.make_random_bot_move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    game.handle_mouse_click(mouse_position)

            if game.moves_without_attacks >= 50 or game.is_over:
                game_running = False
                game_over_screen_active = True

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
