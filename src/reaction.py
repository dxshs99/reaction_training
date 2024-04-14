import sys
import os
import pygame
import random
from pathlib import Path
sys.path.insert(1, os.path.abspath(Path(__file__).resolve().parents[1]))
from src.button import Button
from config.config import COLOR_MAPPING, CONFIG

class Reaction:

    pygame.init()

    def __init__(self) -> None:
        
        self.window_width = CONFIG['window_width']
        self.window_height = CONFIG['window_height']
        self.size = (self.window_width, self.window_height)
        self.window = pygame.display.set_mode((self.window_width, self.window_height),pygame.RESIZABLE)
        
        pygame.display.set_caption(CONFIG['caption'])
        icon = pygame.image.load(r'images/logo.png').convert_alpha()
        pygame.display.set_icon(icon)

        self.game_state = 'start_menu'
        self.running = True
        self.color_training = CONFIG['color_training']
        self.full_screen = False
        self.timer_interval = CONFIG['time_interval']

        self.get_button_position()
        self.set_timer_event()
        self.select_color(self.color_training)

    def get_button_position(self):
        self.button_left = self.window_width - CONFIG['button_edge_value'] - CONFIG['button_width'] // 2
        self.button_left_range = [self.button_left - CONFIG['button_width'] // 2, self.button_left + CONFIG['button_width'] // 2]

        self.auto_start_top = CONFIG['button_edge_value'] + CONFIG['button_height'] // 2
        self.auto_start_top_range = [self.auto_start_top - CONFIG['button_height'] // 2, self.auto_start_top + CONFIG['button_height'] // 2]

        self.pause_top = self.auto_start_top + CONFIG['button_edge_value'] + CONFIG['button_height']
        self.pause_top_range = [self.pause_top - CONFIG['button_height'] // 2, self.pause_top + CONFIG['button_height'] // 2]

        self.manual_start_top = self.pause_top + CONFIG['button_edge_value'] + CONFIG['button_height']
        self.manual_start_top_range = [self.manual_start_top - CONFIG['button_height'] // 2, self.manual_start_top + CONFIG['button_height'] // 2]

        self.settings_top =  self.window_height - self.pause_top
        
        self.exit_top = self.window_height - self.auto_start_top
        self.exit_top_range = [self.exit_top - CONFIG['button_height'] // 2, self.exit_top + CONFIG['button_height'] // 2]

        self.prac_width = self.window_width - CONFIG['button_edge_value'] * 2 - CONFIG['button_width']
        self.prac_height = self.window_height

    def draw_start_menu(self):
        sel_auto_start, sel_pause, sel_manual_start = False, False, False

        if self.game_state == 'auto_start':
            sel_auto_start = True
        elif self.game_state == 'pause':
            sel_pause = True
        elif self.game_state == 'manual_start':
            sel_manual_start = True

        self.window.fill(COLOR_MAPPING['white'])
        Button(self.window, 'Auto Start', self.button_left, self.auto_start_top, sel_auto_start)
        Button(self.window, 'Pause', self.button_left, self.pause_top, sel_pause)
        Button(self.window, 'Manual Start', self.button_left, self.manual_start_top, sel_manual_start)

        # Button(self.window, 'Settings', self.button_left, self.settings_top)
        Button(self.window, 'Exit', self.button_left, self.exit_top)

        font = pygame.font.SysFont(None, CONFIG['button_font_size'])
        speed_text = font.render(f'Speed: {str(self.timer_interval)} ms', True, COLOR_MAPPING['black'])
        self.window.blit(speed_text, (self.button_left - CONFIG['button_width'] // 2,
                                      self.settings_top - CONFIG['button_height']))

        # pygame.display.flip()

    def set_timer_event(self):
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.timer_interval)

    def select_color(self, next_aval_color: list) -> None:
        self.curr_color = random.choice(next_aval_color)
        self.next_aval_color = [i for i in self.color_training if i != self.curr_color]

    def display_prac_clor(self):
        prac_rect = pygame.Rect(0, 0, self.prac_width, self.prac_height)
        pygame.draw.rect(self.window, self.curr_color, prac_rect)
        


    def main(self):
        while self.running:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.game_state == 'auto_start' and event.type == self.timer_event:
                    self.select_color(self.next_aval_color)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.button_left_range[0] <= mouse_pos[0] <= self.button_left_range[1] and self.auto_start_top_range[0] <= mouse_pos[1] <= self.auto_start_top_range[1]:
                        self.game_state = 'auto_start'
                    elif self.button_left_range[0] <= mouse_pos[0] <= self.button_left_range[1] and self.pause_top_range[0] <= mouse_pos[1] <= self.pause_top_range[1]:
                        self.game_state = 'pause'
                    elif self.button_left_range[0] <= mouse_pos[0] <= self.button_left_range[1] and self.manual_start_top_range[0] <= mouse_pos[1] <= self.manual_start_top_range[1]:
                        self.game_state = 'manual_start'
                    elif self.button_left_range[0] <= mouse_pos[0] <= self.button_left_range[1] and self.exit_top_range[0] <= mouse_pos[1] <= self.exit_top_range[1]:
                        self.running = False
                    elif self.game_state == 'manual_start' and 0 <= mouse_pos[0] <= self.prac_width and 0 <= mouse_pos[1] <= self.prac_height:
                        self.select_color(self.next_aval_color)
                        self.display_prac_clor()
                        pygame.display.flip()
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        if self.game_state == 'auto_start':
                            self.game_state = 'pause'
                        elif self.game_state == 'pause' or self.game_state == 'start_menu':
                            self.game_state = 'auto_start'
                        elif self.game_state == 'manual_start':
                            self.display_prac_clor()
                            pygame.display.flip()
                            self.select_color(self.next_aval_color)

                    if keys[pygame.K_LEFT]:
                        if self.timer_interval > CONFIG['time_interval_sensitivity']:
                            self.timer_interval -= CONFIG['time_interval_sensitivity']
                            self.set_timer_event()
                            self.draw_start_menu()
                    
                    if keys[pygame.K_RIGHT]:
                        if self.timer_interval <= CONFIG['time_interval_max']:
                            self.timer_interval += CONFIG['time_interval_sensitivity']
                            self.set_timer_event()
                            self.draw_start_menu()

                if event.type == pygame.VIDEORESIZE:
                    self.window_width, self.window_height = event.w, event.h
                    self.window = pygame.display.set_mode((self.window_width, self.window_height),pygame.RESIZABLE)
                    self.get_button_position()
                    self.draw_start_menu()

            if self.game_state == 'start_menu':
                self.draw_start_menu()
                pygame.display.flip()
            
            if self.game_state == 'auto_start' or self.game_state == 'manual_start' or self.game_state == 'pause':
                self.draw_start_menu()
                self.display_prac_clor()
                pygame.display.flip()
            
        pygame.quit()

if __name__ == '__main__':
    react = Reaction()
    react.main()