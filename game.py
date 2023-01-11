import pygame
from sys import exit
from constants import WIN_WIDTH, WIN_HEIGHT, FIELD_SIZE, MAX_FPS, PIECE_PADDING, GREEN, BROWN
from piece_move_board import Board, Piece
from player import Player


class Game:

    def __init__(self, screen) -> None:
        self.board = Board()
        self.screen = screen
        self.players = [Player('white'), Player('black')]
        self.load_images()
        self.turn = 'white'
        self.selected_square = None
        # self.prev_selected_square = None
        self.selected_piece = None

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
        for row in self.board.fields:
            for field in row:
                field_rect = pygame.Rect(field.x * FIELD_SIZE, field.y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)
                pygame.draw.rect(self.screen, field.color, field_rect)

    def draw_pieces(self):
        for row in self.board.fields:
            for field in row:
                if field.is_taken():
                    current_piece = field.piece
                    piece_surf = self.images[current_piece.image_dict_ind]
                    piece_rect = piece_surf.get_rect(center=current_piece.location_to_draw())
                    self.screen.blit(piece_surf, piece_rect)

    def show_possible_moves(self, piece: 'Piece'):
        possible_moves = piece.all_possible_legal_moves(self.board)
        possible_move_squares = [move.new_cords for move in possible_moves]

        field_surf = pygame.Surface((FIELD_SIZE, FIELD_SIZE))
        field_surf.fill(BROWN)
        pygame.draw.circle(field_surf, GREEN, (FIELD_SIZE / 2, FIELD_SIZE / 2), FIELD_SIZE * 0.35)

        for square in possible_move_squares:
            x, y = square
            square_rect = pygame.Rect(x * FIELD_SIZE, y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE)
            self.screen.blit(field_surf, (square_rect))

    def player_by_color(self, color):
        player_color_dictionary = {
            player.color: player
            for player in self.players
        }
        return player_color_dictionary[color]

    def change_turn(self):
        self.turn = 'white' if self.turn == 'black' else 'black'


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

                if clicked_field.piece is not None:

                    game.draw_board()
                    if clicked_field.piece.color == game.turn:
                        game.selected_square = clicked_field
                        game.selected_piece = clicked_field.piece
                        game.show_possible_moves(game.selected_piece)
                    else:
                        game.selected_piece = None
                        game.selected_square = None

                else:
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
                                pass
                            else:
                                game.selected_piece = None
                                game.change_turn()

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
