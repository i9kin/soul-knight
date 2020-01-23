import os
import pygame
import pygameMenu

ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 100, 36)
WINDOW_SIZE = (640, 480)

sound = None
surface = None
main_menu = None

def main_background():
    global surface
    surface.fill((40, 40, 40))


# noinspection PyUnusedLocal
def update_menu_sound(value, enabled):
    print(value)

test = False

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Example - Multi Input')
clock = pygame.time.Clock()

settings_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_HELVETICA,
                                font_color=COLOR_BLACK,
                                font_size=25,
                                font_size_title=50,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.85),
                                menu_width=int(WINDOW_SIZE[0] * 0.9),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                title='Settings',
                                widget_alignment=pygameMenu.locals.ALIGN_LEFT,
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

settings_menu.add_text_input('level *.tmx ', default='', textinput_id='file', input_underline='_')

about_menu = pygameMenu.TextMenu(surface,
                                 bgfun=main_background,
                                 color_selected=COLOR_WHITE,
                                 font=pygameMenu.font.FONT_BEBAS,
                                 font_color=COLOR_BLACK,
                                 font_size_title=30,
                                 font_title=pygameMenu.font.FONT_8BIT,
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_color_title=COLOR_WHITE,
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 onclose=pygameMenu.events.DISABLE_CLOSE,
                                 option_shadow=False,
                                 text_color=COLOR_BLACK,
                                 text_fontsize=20,
                                 title='About',
                                 window_height=WINDOW_SIZE[1],
                                 window_width=WINDOW_SIZE[0])
def data_fun():
    data = settings_menu.get_input_data()
    for k in data.keys():
        print(u'\t{0}\t=>\t{1}'.format(k, data[k]))

    return pygameMenu.events.BACK

settings_menu.add_option('save', data_fun, align=pygameMenu.locals.ALIGN_CENTER)
settings_menu.add_option('Return to main menu', pygameMenu.events.BACK, align=pygameMenu.locals.ALIGN_CENTER)

# Main menu
main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.font.FONT_COMIC_NEUE,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            font_size_title=40,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.7),
                            menu_width=int(WINDOW_SIZE[0] * 0.8),
                            # User press ESC button
                            onclose=pygameMenu.events.EXIT,
                            option_shadow=False,
                            title='Main menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )
main_menu.set_fps(FPS)

main_menu.add_option('Settings', settings_menu)
main_menu.add_selector('levels',
                       [('Off', False), ('On', True)],
                       onchange=update_menu_sound)

main_menu.add_option('about', about_menu)
main_menu.add_option('Quit', pygameMenu.events.EXIT)
while True:
    clock.tick(FPS)
    main_background()
    main_menu.mainloop(disable_loop=test)
    pygame.display.flip()

    if test:
        break


