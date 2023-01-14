import pygame
from constants import (WIN_WIDTH, WIN_HEIGHT, BEIGE, TITLE_RECT_MID_X, TITLE_RECT_MID_Y, BUTTON_OUTLINE_HEIGHT, BUTTON_OUTLINE_WIDTH, LIGHT_BROWN, MAX_FPS)
from time import sleep


def load_fonts():
    '''Loads the font from the fonts folder and creates different pygame.Font
    objects with different sizes. Each size is needed for a different text prompt.'''
    fonts = {
        'title_font': pygame.font.Font('fonts/coolvetica_rg.otf', 80),
        'autor_font': pygame.font.Font('fonts/coolvetica_rg.otf', 20),
        'button_font': pygame.font.Font('fonts/coolvetica_rg.otf', 40),
        'message_font': pygame.font.Font('fonts/coolvetica_rg.otf', 30)
    }
    return fonts


def draw_menu(window):
    '''The method responsible for drawing a menu for the user
    before starting a game. The function is lengthy, but it capitalizes
    on it by creating the relations between all buttons and the title text
    - if the constant title_rect_mid_y in the constants file is changed by some value,
    the whole menu gets shifted down or up by it it was changed'''

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

    pvp_button_surf = button_font.render('Player vs Player', True, (0, 0, 0))
    pvp_button_outline_rect = pygame.Rect(title_rect.left + 20, title_rect.bottom + 50, BUTTON_OUTLINE_WIDTH, BUTTON_OUTLINE_HEIGHT)
    pvp_button_rect = pvp_button_surf.get_rect(center=pvp_button_outline_rect.center)
    pygame.draw.rect(window, LIGHT_BROWN, pvp_button_outline_rect)
    window.blit(pvp_button_surf, pvp_button_rect)

    pvb_button_outline_rect = pygame.Rect(title_rect.left + 20, pvp_button_outline_rect.bottom + 30, BUTTON_OUTLINE_WIDTH, BUTTON_OUTLINE_HEIGHT)
    pvb_button_surf = button_font.render('Player vs Bot', True, (0, 0, 0))
    pvb_button_rect = pvb_button_surf.get_rect(center=pvb_button_outline_rect.center)
    pygame.draw.rect(window, LIGHT_BROWN, pvb_button_outline_rect)
    window.blit(pvb_button_surf, pvb_button_rect)

    bvb_button_outline_rect = pygame.Rect(title_rect.left + 20, pvb_button_outline_rect.bottom + 30, BUTTON_OUTLINE_WIDTH, BUTTON_OUTLINE_HEIGHT)
    bvb_button_surf = button_font.render('Bot vs Bot', True, (0, 0, 0))
    bvb_button_rect = bvb_button_surf.get_rect(center=bvb_button_outline_rect.center)
    pygame.draw.rect(window, LIGHT_BROWN, bvb_button_outline_rect)
    window.blit(bvb_button_surf, bvb_button_rect)

    return pvp_button_outline_rect, pvb_button_outline_rect, bvb_button_outline_rect


def draw_game_over_screen(window):
    sleep(0.1)
    fonts = load_fonts()
    game_over_font = fonts['title_font']
    message_font = fonts['message_font']

    go_screen = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
    go_screen.fill(BEIGE)
    go_screen.set_alpha(40)

    game_over_surf = game_over_font.render('Game Over!', True, (0, 0, 0))
    game_over_rect = game_over_surf.get_rect(center=(WIN_WIDTH / 2, (WIN_HEIGHT / 2) - 50))

    message_surf = message_font.render('Press any key to continue to the menu.', True, (0, 0, 0))
    message_rect = message_surf.get_rect(top=game_over_rect.bottom + 15, centerx=game_over_rect.centerx)

    window.blit(go_screen, (0, 0))
    window.blit(game_over_surf, game_over_rect)
    window.blit(message_surf, message_rect)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    screen.fill('white')
    pygame.draw.rect(screen, 'red', pygame.Rect(200, 200, 100, 300))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    draw_game_over_screen(screen)
        pygame.display.update()
        clock.tick(MAX_FPS)


if __name__ == '__main__':
    main()
