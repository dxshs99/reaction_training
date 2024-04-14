import sys
import os
import pygame
import random
from pygame import Surface
from pathlib import Path
from typing import Type
sys.path.insert(1, os.path.abspath(Path(__file__).resolve().parents[1]))
from src.button import Button
from config.config import COLOR_MAPPING, CONFIG

class Reaction:

    pygame.init()

    def __init__(self) -> None:
        
        self.window_width = CONFIG['window_width']
        self.window_height = CONFIG['window_height']
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(CONFIG['caption'])

        self.game_state = 'start_menu'
        self.running = True
        self.color_training = CONFIG['color_training']

        self.set_timer_event()
        self.select_color(self.color_training)

    def draw_start_menu(self):
        self.window.fill(COLOR_MAPPING['white'])
        Button(self.window, 'Start', 700, 50)
        Button(self.window, 'Pause', 700, 125)
        Button(self.window, 'Settings', 700, 475)
        Button(self.window, 'Exit', 700, 550)
        pygame.display.flip()

    def set_timer_event(self):
        self.timer_interval = CONFIG['time_interval'] # 0.5 seconds
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.timer_interval)

    def select_color(self, next_aval_color: list) -> None:
        self.curr_color = random.choice(next_aval_color)
        self.next_aval_color = [i for i in self.color_training if i != self.curr_color]

    def main(self):
        while self.running:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.game_state == 'start' and event.type == self.timer_event:
                    self.select_color(self.next_aval_color)

            if self.game_state == 'start_menu':
                self.draw_start_menu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 625 <= mouse_pos[0] <= 775 and 25 <= mouse_pos[1] <= 75:
                    self.game_state = 'start'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 625 <= mouse_pos[0] <= 775 and 100 <= mouse_pos[1] <= 150:
                    self.game_state = 'pause'

            if self.game_state == 'start':
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.game_state = 'pause'

            if self.game_state == 'start_menu' or self.game_state == 'pause':
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.game_state = 'start'

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 625 <= mouse_pos[0] <= 775 and 525 <= mouse_pos[1] <= 575:
                    self.running = False

            if self.game_state == 'start':
                prac_rect = pygame.Rect(0, 0, 600, 600)
                pygame.draw.rect(self.window, self.curr_color, prac_rect)
                pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    react = Reaction()
    react.main()