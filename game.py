import pygame
from sys import exit
from constants import WIN_WIDTH, WIN_HEIGHT, FIELD_SIZE, MAX_FPS, PIECE_PADDING
from piece_move_board import Board


class Game:

    def load_images(self):
        self.images = {
            'BK': pygame.transform.scale(pygame.image.load('images/black_king.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
            'WK': pygame.transform.scale(pygame.image.load('images/white_king.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
            'WP': pygame.transform.scale(pygame.image.load('images/white_piece.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING)),
            'BP': pygame.transform.scale(pygame.image.load('images/black_piece.png').convert_alpha(), (FIELD_SIZE - PIECE_PADDING, FIELD_SIZE - PIECE_PADDING))
        }

    def __init__(self, screen) -> None:
        self.board = Board()
        self.screen = screen
        self.load_images()

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


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game = Game(screen)
        game.draw_board()
        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
