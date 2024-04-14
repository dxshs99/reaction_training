COLOR_MAPPING = {
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'black': (255, 255, 255),
    'grey': (232, 232, 232),
    'white': (0, 0, 0),
    'light_yellow': (251, 243, 183)
}

CONFIG = {
    'caption': 'Reaction Training',
    'window_width': 1000,
    'window_height': 800,
    'time_interval': 500,
    'time_interval_max': 2000,
    'time_interval_sensitivity': 50,
    'color_training': [COLOR_MAPPING['green'],
                       COLOR_MAPPING['red'],
                       COLOR_MAPPING['blue'],
                       COLOR_MAPPING['yellow']],
    'button_edge_value': 25,
    'button_width': 150,
    'button_height': 50,
    'button_font_size': 30,

}