import pygame
from constants import WIN_HEIGHT, WIN_WIDTH, MAX_FPS, Color, MAX_MOVES_WITHOUT_ATTACKS
from gui import draw_game_over_screen, draw_menu
from game import Game
from player import Player, MinimaxBot, Bot
from sys import exit


def main():
    '''The main function controlling the flow of the entire experience,
    starting with the menu, going on through the game and
    ending at the game over screen. To play, run the file:)'''
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
                            game = Game(screen, [Player(Color.WHITE), Player(Color.BLACK)], 0)
                            game.draw_board()
                        if pvb_button.collidepoint(mouse_position):
                            game_running = True
                            menu_active = False
                            game = Game(screen, [Player(Color.WHITE), MinimaxBot(Color.BLACK)], 1)
                            game.draw_board()
                        if bvb_button.collidepoint(mouse_position):
                            game_running = True
                            menu_active = False
                            game = Game(screen, [MinimaxBot(Color.WHITE), Bot(Color.BLACK)], 2)
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
                    piece_click, field_click = bot_to_move.make_move(game.board)
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

            if game.board.is_game_over:
                game_running = False
                game_over_screen_active = True
                if game.board.moves_without_attacks >= MAX_MOVES_WITHOUT_ATTACKS:  # FIXME
                    print('tie')

        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
