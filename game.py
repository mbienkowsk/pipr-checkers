import pygame
from sys import exit
from constants import WIN_WIDTH, WIN_HEIGHT, FIELD_SIZE, MAX_FPS, PIECE_PADDING, GREEN, BROWN, BEIGE, TITLE_RECT_MID_X, TITLE_RECT_MID_Y, BUTTON_RECT_WIDTH, BUTTON_RECT_HEIGHT
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
        # TODO implement move counter

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
        if clicked_piece.color == self.turn and self.can_piece_move(clicked_piece):
            self.show_possible_moves(clicked_piece)
            self.selected_piece = clicked_piece
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
        self.update_possible_player_moves()
        self.selected_piece = None

    def calculate_jumped_piece(self, move):
        old_x, old_y = move.old_cords
        next_x, next_y = move.new_cords
        jumped_x, jumped_y = int((old_x + next_x) / 2), int((old_y + next_y) / 2)
        piece = self.board.get_field_by_location((jumped_x, jumped_y)).piece
        return piece

    def handle_attacking_move(self, move):
        attacking_piece = move.piece
        self.selected_piece = attacking_piece  # could delete this line later?
        jumped_piece = self.calculate_jumped_piece(move)
        self.board.delete_piece(jumped_piece)
        self.board.move_piece(attacking_piece, move)
        if attacking_piece.eligible_for_promotion_after_move(move):
            attacking_piece.promote()
        self.update_player_pieces()
        self.draw_board()
        if not attacking_piece.all_legal_attacking_moves(self.board):
            self.change_turn()
        self.selected_piece = None
        return

    def handle_field_click(self, clicked_field):
        if self.selected_piece is not None:
            possible_moves_for_selected_piece = [
                move for move in
                self.feasible_player_moves(self.selected_piece.color)[self.selected_piece]
            ]

            possible_move_locatinos_for_selected_piece = [
                move.new_cords
                for move in possible_moves_for_selected_piece]

            if clicked_field.location in possible_move_locatinos_for_selected_piece:
                move_to_make = self.find_move_by_move_location(clicked_field.location, possible_moves_for_selected_piece)
                if move_to_make.attacking:
                    self.handle_attacking_move(move_to_make)

                else:
                    self.handle_passive_move(move_to_make)

    def interpret_clicked_pixel_location(self, location):
        x, y = location
        clicked_field_location = (int(x // FIELD_SIZE), int(y // FIELD_SIZE))
        clicked_field = self.board.get_field_by_location(clicked_field_location)
        clicked_piece = clicked_field.piece
        return clicked_field, clicked_piece


def draw_loading_screen(window):
    fonts = load_fonts()
    title_font = fonts['title_font']
    autor_font = fonts['autor_font']
    button_font = fonts['button_font']

    window.fill(BEIGE)
    title_surf = title_font.render('Checkers', True, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(TITLE_RECT_MID_X, TITLE_RECT_MID_Y))
    window.blit(title_surf, title_rect)

    autor_surf = autor_font.render('by M. Bienkowski', True, (0, 0, 0))
    autor_rect = autor_surf.get_rect(topleft=(TITLE_RECT_MID_X + 20, TITLE_RECT_MID_Y + 50))
    window.blit(autor_surf, autor_rect)
    # pygame.draw.rect(window, (BROWN), autor_rect)

    # pvp_button_rect = pygame.Rect(160, 280, BUTTON_RECT_WIDTH, BUTTON_RECT_HEIGHT)
    # pygame.draw.rect(window, BROWN, pvp_button_rect)
    pvp_button_surf = button_font.render('Player vs Player', True, (0, 0, 0))
    pvp_button_rect = pvp_button_surf.get_rect(center=(title_rect.centerx, title_rect.centery + 170))
    pygame.draw.rect(window, BROWN, pvp_button_rect)
    pygame.draw.rect(window, BROWN, pvp_button_rect, 150)
    window.blit(pvp_button_surf, pvp_button_rect)

    pvb_button_surf = button_font.render('Player vs Bot', True, (0, 0, 0))
    pvb_button_rect = pvp_button_surf.get_rect(center=(title_rect.centerx, pvp_button_rect.bottom + 50))
    pygame.draw.rect(window, BROWN, pvb_button_rect)
    pygame.draw.rect(window, BROWN, pvb_button_rect, 150)
    window.blit(pvb_button_surf, pvb_button_rect)

    bvb_button_surf = button_font.render('Bot vs Bot', True, (0, 0, 0))
    bvb_button_rect = pvp_button_surf.get_rect(center=(title_rect.centerx, pvb_button_rect.bottom + 50))
    pygame.draw.rect(window, BROWN, bvb_button_rect)
    pygame.draw.rect(window, BROWN, bvb_button_rect, 150)
    window.blit(bvb_button_surf, bvb_button_rect)

def load_fonts():
    fonts = {
        'title_font': pygame.font.Font('fonts/coolvetica_rg.otf', 80),
        'autor_font': pygame.font.Font('fonts/coolvetica_rg.otf', 20),
        'button_font': pygame.font.Font('fonts/coolvetica_rg.otf', 40)
    }
    return fonts


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    draw_loading_screen(screen)

    # game = Game(screen)
    # game.draw_board()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                print(mouse_position)
            #     clicked_field, clicked_piece = game.interpret_clicked_pixel_location(mouse_position)

            #     if clicked_piece is not None:
            #         game.handle_piece_click(clicked_piece)

            #     else:
            #         game.handle_field_click(clicked_field)

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
