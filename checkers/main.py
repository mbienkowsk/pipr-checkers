import pygame
from checkers.constants import (WIN_HEIGHT, WIN_WIDTH,
                                MAX_FPS, Color)
from checkers.gui import (draw_game_over_screen,
                          draw_menu, get_bot_settings_from_the_user)
from checkers.game import Game
from checkers.player import Player, MinimaxBot
from sys import exit
from time import perf_counter, sleep


def main():
    '''The main function controlling the flow of the entire program,
    starting with the menu, going on through the game and
    ending at the game over screen. To play, run the file via terminal.'''
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
                            game = Game(
                                screen, [Player(Color.WHITE),
                                         Player(Color.BLACK)])
                            game.draw_board()

                        if pvb_button.collidepoint(mouse_position):
                            black_bot = get_bot_settings_from_the_user(
                                [Color.BLACK])[0]
                            game_running = True
                            menu_active = False
                            game = Game(
                                screen, [Player(Color.WHITE),
                                         black_bot])
                            game.draw_board()

                        if bvb_button.collidepoint(mouse_position):
                            players = get_bot_settings_from_the_user([
                                Color.WHITE, Color.BLACK
                            ])
                            game_running = True
                            menu_active = False
                            game = Game(screen, players)
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
            if game.player_color_dictionary[game.board.turn].ai:
                bot_to_move = game.player_color_dictionary[game.board.turn]
                if isinstance(bot_to_move, MinimaxBot):
                    start_time = perf_counter()
                    piece_click, field_click = bot_to_move.make_move(
                        game.board)
                    end_time = perf_counter()
                    if end_time - start_time < 1:
                        sleep(game.sleep_duration)
                    game.handle_mouse_click(piece_click)
                    game.handle_mouse_click(field_click)
                else:
                    game.handle_random_bot_move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_running = False
                        menu_active = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    game.handle_mouse_click(mouse_position)

            if game.board.is_game_over:
                game_running = False
                game_over_screen_active = True

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
