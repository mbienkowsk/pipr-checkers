import pygame
from sys import exit
from constants import WIN_WIDTH, WIN_HEIGHT, FIELD_WIDTH, FIELD_HEIGHT
from board import Board


class Graphics:
    def __init__(self) -> None:
        self.board_internal = Board()


    def draw_board(self):
        self.draw_squares()
        self.draw_pieces()




def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    images = {
        'BK': pygame.transform.scale(pygame.image.load('images/black_king.png').convert_alpha(), (FIELD_WIDTH, FIELD_HEIGHT)),
        'WK': pygame.transform.scale(pygame.image.load('images/white_king.png').convert_alpha(), (FIELD_WIDTH, FIELD_HEIGHT)),
        'WP': pygame.transform.scale(pygame.image.load('images/white_piece.png').convert_alpha(), (FIELD_WIDTH, FIELD_HEIGHT)),
        'BP': pygame.transform.scale(pygame.image.load('images/black_piece.png').convert_alpha(), (FIELD_WIDTH, FIELD_HEIGHT))
    }


    test_rect = images['BK'].get_rect(center=(300, 300))


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill('white')
        screen.blit(images['BK'], test_rect)
        pygame.display.update()



if __name__ == '__main__':
    main()