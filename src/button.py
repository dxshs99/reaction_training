import sys
import os
import pygame
from pygame import Surface
from pathlib import Path
from typing import Type
sys.path.insert(1, os.path.abspath(Path(__file__).resolve().parents[1]))
from config.config import COLOR_MAPPING, CONFIG

pygame.init()

class Button():
    def __init__(
            self,
            window: Type[Surface],
            text: str,
            center_left: float,
            center_top: float,
            select_status: bool = False,
    ) -> None:
        """Initate

        Args:
            window (Type[Surface]): window
            text (str): text show on button
            center_left (float | int): the width from origin to center of button 
            center_top (float | int): the height from origin to center of button
        """
        self.window = window
        self.text = text
        self.center_left = center_left
        self.center_top = center_top
        self.select_status = select_status

        self.width, self.height = CONFIG['button_width'], CONFIG['button_height']

        if self.select_status is True:
            self.button_color = COLOR_MAPPING['light_yellow']
        else:
            self.button_color = COLOR_MAPPING['grey']
        self.text_color = COLOR_MAPPING['white']
        self.font = pygame.font.SysFont(None, CONFIG['button_font_size'])

        self.rect = pygame.Rect(center_left - self.width // 2, center_top - self.height // 2, self.width, self.height)

        self.prep_msg()
        self.draw_button()

    def prep_msg(self):
        self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect(center=(self.center_left , self.center_top))

    def draw_button(self):
        self.window.fill(self.button_color, self.rect)
        self.window.blit(self.msg_image, self.msg_image_rect)


def get_button_center_position(
        window_width: float,
        center_top: float,
) -> list:
    center_left = window_width - CONFIG['button_edge_value'] - CONFIG['button_width'] // 2
    return [center_left, center_top]