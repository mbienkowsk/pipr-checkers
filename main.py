import pygame
from constants import WIN_HEIGHT, WIN_WIDTH, MAX_FPS
from gui import draw_game_over_screen, draw_menu
from game import Game
from player import Player, MinimaxBot, Bot
from sys import exit


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
            if game.player_by_color(game.board.turn).ai:
                if isinstance(game.player_by_color(game.board.turn), MinimaxBot):
                    piece_click, field_click = game.player_by_color(game.board.turn).make_move(game.board)
                    game.handle_mouse_click(piece_click)
                    game.handle_mouse_click(field_click)
                else:
                    game.handle_random_bot_move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    game.handle_mouse_click(mouse_position)

            if game.moves_without_attacks >= 50 or game.board.is_game_over:
                game_running = False
                game_over_screen_active = True

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
