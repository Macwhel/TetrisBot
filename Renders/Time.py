from Models.Colors import BLACK
from config import BOARD_END_Y_COORDINATE, TOP_LEFT_X_COORDINATE
import pygame


def draw_timer(font, display, minutes, seconds, milliseconds):
    timer_text = font.render(
        f"{minutes:02}:{seconds:02}.{milliseconds:03}", True, (255, 255, 255)
    )

    text_rect = timer_text.get_rect()

    text_rect.centerx = TOP_LEFT_X_COORDINATE - 65
    text_rect.bottom = BOARD_END_Y_COORDINATE

    pygame.draw.rect(display, BLACK, text_rect)

    display.blit(timer_text, text_rect)
    pygame.display.update(text_rect)
