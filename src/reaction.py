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
        self.show_time_interval()
        self.select_color(self.color_training)

    def get_button_position(self):
        self.button_center_left = self.window_width - CONFIG['button_edge_value'] - CONFIG['button_width'] // 2
        
        self.auto_start_center_top = CONFIG['button_edge_value'] + CONFIG['button_height'] // 2
        self.pause_center_top = self.auto_start_center_top + CONFIG['button_edge_value'] + CONFIG['button_height']
        self.manual_start_center_top = self.pause_center_top + CONFIG['button_edge_value'] + CONFIG['button_height']

        self.settings_center_top =  self.window_height - self.pause_center_top
        self.exit_center_top = self.window_height - self.auto_start_center_top

        self.prac_width = self.window_width - CONFIG['button_edge_value'] * 2 - CONFIG['button_width']
        self.prac_height = self.window_height

    def draw_start_menu(self):
        self.window.fill(COLOR_MAPPING['white'])
        Button(self.window, 'Auto Start', self.button_center_left, self.auto_start_center_top)
        Button(self.window, 'Pause', self.button_center_left, self.pause_center_top)
        
        Button(self.window, 'Manual Start', self.button_center_left, self.manual_start_center_top)

        Button(self.window, 'Settings', self.button_center_left, self.settings_center_top)
        Button(self.window, 'Exit', self.button_center_left, self.exit_center_top)
        pygame.display.flip()

    def set_timer_event(self):
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.timer_interval)

    def select_color(self, next_aval_color: list) -> None:
        self.curr_color = random.choice(next_aval_color)
        self.next_aval_color = [i for i in self.color_training if i != self.curr_color]

    def show_time_interval(self):
        self.draw_start_menu()
        font = pygame.font.SysFont(None, CONFIG['button_font_size'])
        speed_text = font.render(f'Speed: {str(self.timer_interval)} ms', True, COLOR_MAPPING['black'])
        self.window.blit(speed_text, (self.button_center_left - CONFIG['button_width'] // 2,
                                      self.settings_center_top - CONFIG['button_height']))

    def display_prac_clor(self):
        prac_rect = pygame.Rect(0, 0, self.prac_width, self.prac_height)
        pygame.draw.rect(self.window, self.curr_color, prac_rect)
        pygame.display.flip()


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
                    
                    # Button left
                    pos0_range = [self.button_center_left - CONFIG['button_width'] // 2, self.button_center_left + CONFIG['button_width'] // 2]
                    
                    auto_start_pos1_range = [self.auto_start_center_top - CONFIG['button_height'] // 2, self.auto_start_center_top + CONFIG['button_height'] // 2]
                    pause_pos1_range = [self.pause_center_top - CONFIG['button_height'] // 2, self.pause_center_top + CONFIG['button_height'] // 2]
                    manual_start_pos1_range = [self.manual_start_center_top - CONFIG['button_height'] // 2, self.manual_start_center_top + CONFIG['button_height'] // 2]
                    exit_pos1_range = [self.exit_center_top - CONFIG['button_height'] // 2, self.exit_center_top + CONFIG['button_height'] // 2]


                    if pos0_range[0] <= mouse_pos[0] <= pos0_range[1] and auto_start_pos1_range[0] <= mouse_pos[1] <= auto_start_pos1_range[1]:
                        self.game_state = 'auto_start'
                    elif pos0_range[0] <= mouse_pos[0] <= pos0_range[1] and pause_pos1_range[0] <= mouse_pos[1] <= pause_pos1_range[1]:
                        self.game_state = 'pause'
                    elif pos0_range[0] <= mouse_pos[0] <= pos0_range[1] and manual_start_pos1_range[0] <= mouse_pos[1] <= manual_start_pos1_range[1]:
                        self.game_state = 'manual_start'
                    elif pos0_range[0] <= mouse_pos[0] <= pos0_range[1] and exit_pos1_range[0] <= mouse_pos[1] <= exit_pos1_range[1]:
                        self.running = False
                    elif 0 <= mouse_pos[0] <= self.prac_width and 0 <= mouse_pos[1] <= self.prac_height:
                        self.display_prac_clor()
                        self.select_color(self.next_aval_color)
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        if self.game_state == 'auto_start':
                            self.game_state = 'pause'
                        elif self.game_state == 'pause' or self.game_state == 'start_menu':
                            self.game_state = 'auto_start'

                    if keys[pygame.K_LEFT]:
                        if self.timer_interval > CONFIG['time_interval_sensitivity']:
                            self.timer_interval -= CONFIG['time_interval_sensitivity']
                            self.set_timer_event()
                            self.show_time_interval()
                            pygame.display.flip()
                    
                    if keys[pygame.K_RIGHT]:
                        if self.timer_interval <= CONFIG['time_interval_max']:
                            self.timer_interval += CONFIG['time_interval_sensitivity']
                            self.set_timer_event()
                            self.show_time_interval()
                            pygame.display.flip()

                if event.type == pygame.VIDEORESIZE:
                    self.window_width, self.window_height = event.w, event.h
                    self.window = pygame.display.set_mode((self.window_width, self.window_height),pygame.RESIZABLE)
                    self.get_button_position()
                    self.draw_start_menu()
                    self.show_time_interval()

            if self.game_state == 'start_menu':
                self.draw_start_menu()
                self.show_time_interval()
            
            if self.game_state == 'auto_start' or self.game_state == 'manual_start':
                self.display_prac_clor()
            
        pygame.quit()

if __name__ == '__main__':
    react = Reaction()
    react.main()