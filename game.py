import pygame
from sys import exit
from constants import WIN_WIDTH, WIN_HEIGHT, FIELD_SIZE, MAX_FPS, PIECE_PADDING, GREEN, BROWN
from piece_move_board import Board, Piece
from player import Player


class Game:

    def __init__(self, screen) -> None:
        self.board = Board()
        self.screen = screen
        self.possible_move_dict = {}
        self.players = [Player('white'), Player('black')]
        self.load_images()
        self.turn = 'white'
        self.selected_piece = None
        self.update_player_pieces()
        self.update_possible_player_moves()

    def load_images(self):
        self.images = {
            'BK': pygame.transform.scale(pygame.image.load('images/black_king.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
            'WK': pygame.transform.scale(pygame.image.load('images/white_king.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
            'WP': pygame.transform.scale(pygame.image.load('images/white_piece.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
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

    def update_player_pieces(self):
        for player in self.players:
            player.pieces.clear()

        for field in self.board.one_dimensional_field_list:
            if field.is_taken():
                self.player_by_color(field.piece.color).pieces.append(field.piece)

    def update_possible_player_moves(self):
        self.possible_move_dict = {
            player: {
                piece: piece.all_possible_legal_moves(self.board)
                for piece in player.pieces
            }
            for player in self.players
        }

    def player_has_to_attack(self, color):
        player = self.player_by_color(color)
        player_dict = self.possible_move_dict[player]
        for value in player_dict.values():
            for move in value:
                if move.attacking:
                    return True
        return False

    def can_piece_move(self, piece):
        '''Determines whether a piece can be moved during a player's turn
        If the piece can't attack and another one of its color can,
        returns False. Else, returns True
        '''
        if self.player_has_to_attack(piece.color):
            if not piece.all_legal_attacking_moves(self.board):
                return False
            #   have to come back to implement multiple jumps in a row
        return True

    def handle_piece_click(self, clicked_piece):
        self.update_possible_player_moves()
        if clicked_piece.color == self.turn:
            if self.can_piece_move(clicked_piece):
                self.show_possible_moves(clicked_piece)
                self.selected_piece = clicked_piece
            else:
                self.selected_piece = None
        else:
            self.selected_piece = None
            self.draw_board()

    def feasible_player_moves(self, color):
        self.update_possible_player_moves()
        move_dictionary = self.possible_move_dict[self.player_by_color(color)]
        return {
            piece: move_dictionary[piece]
            for piece in move_dictionary.keys()
            if self.can_piece_move(piece)
        }

    def handle_field_click(self, clicked_field):
        if self.selected_piece is None:
            #  FIXME do nothing if a random field is clicked
            pass
        else:
            possible_move_locatinos_for_selected_piece = [
                move.new_cords
                for move in self.feasible_player_moves(self.selected_piece.color)[self.selected_piece]
            ]
            if clicked_field.location in possible_move_locatinos_for_selected_piece:
                pass
                #   start here later


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    game = Game(screen)
    game.draw_board()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pixel_x, clicked_pixel_y = pygame.mouse.get_pos()
                clicked_field_location = (int(clicked_pixel_x // FIELD_SIZE), int(clicked_pixel_y // FIELD_SIZE))
                clicked_field = game.board.get_field_by_location(clicked_field_location)
                clicked_piece = clicked_field.piece

                if clicked_piece is not None:
                    game.handle_piece_click(clicked_piece)

                else:
                    game.handle_field_click(clicked_field)
                    if game.selected_piece is not None:
                        possible_moving_locations = {
                            move.new_cords: move
                            for move in game.selected_piece.all_possible_legal_moves(game.board)
                        }

                        if clicked_field.location in possible_moving_locations.keys():
                            move_to_be_made = possible_moving_locations[clicked_field.location]
                            game.board.move_piece(game.selected_piece, move_to_be_made)
                            new_y = move_to_be_made.new_cords[1]
                            game.draw_board()
                            if new_y in (0, 7):
                                game.selected_piece.promote()
                                game.draw_board()

                            if move_to_be_made.attacking:
                                old_x, old_y = move_to_be_made.old_cords
                                next_x, next_y = move_to_be_made.new_cords
                                jumped_x, jumped_y = int((old_x + next_x) / 2), int((old_y + next_y) / 2)
                                piece_to_take = game.board.get_field_by_location((jumped_x, jumped_y)).piece
                                game.board.delete_piece(piece_to_take)
                                game.board.move_piece(game.selected_piece, move_to_be_made)
                                game.draw_board()
                                while game.selected_piece.all_legal_attacking_moves(game.board):
                                    break
                                game.selected_piece = None
                                game.change_turn()
                                game.update_player_pieces()

                            else:
                                if not game.player_has_to_attack(game.turn):
                                    game.selected_piece = None
                                    game.change_turn()
                                else:
                                    game.selected_piece = None

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
