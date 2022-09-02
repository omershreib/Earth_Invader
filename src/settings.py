from utilities import get_windows_screen_size

# screen settings
vertical_tile_number = 11
invader_size = (64,64)
tile_size = 64
cannon_size = (66*2,9*2)


#screen_height = vertical_tile_number * tile_size
#screen_width = 2000

screen_size = get_windows_screen_size()
screen_width, screen_height = screen_size

# main settings
background_color = 'blue'
background_path = '../graphic/background/nebula.jpg'
font_path = '../graphic/font/VCR_OSD_MONO_1.001.ttf'
CLOCK_RATE = 30

# sprites positions
EARTH_POSITION = screen_width/2, screen_height/2
CANNON_POSITION = screen_width/2, screen_height/2
SHELL_POSITION = screen_width/2, screen_height/2

# colors
COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (105,105,105)
COLOR_LIME = (0,255,0) # kind of green

# text positions
SCORE_TEXT_POSOTION = [screen_width-250,10]
SHELL_TEXT_POSOTION = [screen_width-250,50]
CANNON_STATUS_TEXT_POSOTION = [screen_width-300,screen_height - 70]
