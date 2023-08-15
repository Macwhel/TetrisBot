from Models.Colors import BLACK, WHITE
from Models.Stats import Stats
from config import BOARD_END_Y_COORDINATE, TOP_LEFT_X_COORDINATE
import pygame


def draw_apm(font, display, stats: Stats):
    apm_text = font.render(f"{stats.getPPS()} APM", True, WHITE)

    text_rect = apm_text.get_rect()

    text_rect.centerx = TOP_LEFT_X_COORDINATE - 65
    text_rect.bottom = BOARD_END_Y_COORDINATE - 100

    pygame.draw.rect(display, BLACK, text_rect)

    display.blit(apm_text, text_rect)
    pygame.display.update(text_rect)


def draw_pps(font, display, stats: Stats):
    pps_text = font.render(f"{stats.getPPS()} PPS", True, WHITE)

    text_rect = pps_text.get_rect()

    text_rect.centerx = TOP_LEFT_X_COORDINATE - 65
    text_rect.bottom = BOARD_END_Y_COORDINATE - 50

    pygame.draw.rect(display, BLACK, text_rect)

    display.blit(pps_text, text_rect)
    pygame.display.update(text_rect)


def draw_timer(font, display, minutes, seconds, milliseconds):
    timer_text = font.render(
        f"{minutes:02}:{seconds:02}.{milliseconds:03}", True, WHITE
    )

    text_rect = timer_text.get_rect()

    text_rect.centerx = TOP_LEFT_X_COORDINATE - 65
    text_rect.bottom = BOARD_END_Y_COORDINATE

    pygame.draw.rect(display, BLACK, text_rect)

    display.blit(timer_text, text_rect)
    pygame.display.update(text_rect)
