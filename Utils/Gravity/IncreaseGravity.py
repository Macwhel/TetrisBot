import pygame

GRAVITY_EVENT = pygame.USEREVENT + 1


def G_to_miliseconds_per_row(G: float):
    return int(G ** (-1) * 60)


def increase_gravity(G, dg):
    G += dg
    pygame.time.set_timer(GRAVITY_EVENT, G_to_miliseconds_per_row(G))
    return G
