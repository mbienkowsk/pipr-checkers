import pygame
from constants import FIELD_SIZE, PIECE_PADDING, GREEN, BROWN, SLEEP_TIME_IN_PVB_GAME, SLEEP_TIME_IN_BVB_GAME
from piece_move_board import Board, Piece
from time import sleep


class Game:
    '''Class representing a single game of checkers.

    param board: the board the game is played on
    type board: Board

    param screen: the instance of pygame.display used to display the GUI
    type screen: pygame.display

    param players: list of players taking part in the game
    type players: List[Player, Player]

    param selected_piece: the piece currently selected by the user
    type selected_piece: Piece

    param moves_without_attacks: a counter keeping track of how many moves have been made
    since the last attack. If it reaches 50, the game is drawn.
    type moves_without_attacks: int

    param num_of_bots: the number of computer controlled players in a game
    type num_of_bots: int

    FIXME param player_color_dictionary: a dictionary mapping colors onto players
    type player_color_dictionary: dict
    '''

    def __init__(self, screen, players, num_of_bots) -> None:
        self.board = Board()
        self.screen = screen
        self.load_images()
        self.players = players
        self.selected_piece = None
        self.moves_without_attacks = 0
        self._player_color_dictionary = {
            player.color: player
            for player in self.players
        }
        if num_of_bots == 1:
            self.sleep_duration = SLEEP_TIME_IN_PVB_GAME
        elif num_of_bots == 2:
            self.sleep_duration = SLEEP_TIME_IN_BVB_GAME
        else:
            self.sleep_duration = None

    def load_images(self):
        '''Load the images from the folder and return a dictionary to assign them'''
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
        '''Display the board in the current state including fields and pieces'''
        self.draw_fields()
        self.draw_pieces()

    def draw_fields(self):
        '''Display the checkerboard onto the screen'''
        for field in self.board.one_dimensional_field_list:
            field_rect = pygame.Rect(field.x * FIELD_SIZE, field.y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)
            pygame.draw.rect(self.screen, field.color, field_rect)

    def draw_pieces(self):
        '''Display the pieces onto on the screen'''
        for field in self.board.one_dimensional_field_list:
            if field.is_taken():
                current_piece = field.piece
                piece_surf = self.images[current_piece.image_dict_ind]
                piece_rect = piece_surf.get_rect(center=current_piece.location_to_draw())
                self.screen.blit(piece_surf, piece_rect)

    def highlight_field(self, field):
        '''Display a green circle onto a given field indicating that a move there
        is possible'''
        field_surf = pygame.Surface((FIELD_SIZE, FIELD_SIZE))
        field_surf.fill(BROWN)
        square_rect = pygame.Rect(field.x * FIELD_SIZE, field.y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)
        pygame.draw.circle(field_surf, GREEN, (FIELD_SIZE / 2, FIELD_SIZE / 2), FIELD_SIZE * 0.35)
        self.screen.blit(field_surf, (square_rect))

    def show_possible_moves(self, piece: 'Piece'):
        '''Highlight all fields where a given piece can move at the moment
        '''
        self.draw_board()
        possible_moves = piece.all_possible_legal_moves(self.board)
        possible_move_squares = [self.board.get_field_by_location(move.new_cords) for move in possible_moves]
        for field in possible_move_squares:
            self.highlight_field(field)

    @property
    def player_color_dictionary(self):
        return self._player_color_dictionary

    def handle_piece_click(self, clicked_piece):
        self.board.update_possible_moves_by_colors()
        if clicked_piece.color == self.board.turn and self.board.can_piece_move(clicked_piece):
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

    def handle_field_click(self, clicked_field):
        if self.selected_piece is not None:
            possible_move_locations, possible_moves = self.board.feasible_locations_and_moves_for_piece(self.selected_piece)

            if clicked_field.location in possible_move_locations:
                move_to_make = self.find_move_by_move_location(clicked_field.location, possible_moves)
                if move_to_make.attacking:
                    self.board.handle_attacking_move(move_to_make)
                    self.draw_board()
                    self.moves_without_attacks = 0

                else:
                    self.board.handle_passive_move(move_to_make)
                    self.draw_board()
                    self.moves_without_attacks += 1

                self.selected_piece = None
            else:
                self.draw_board()

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

    def handle_random_bot_move(self):
        sleep(self.sleep_duration)
        bot = self.player_color_dictionary[self.board.turn]
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
