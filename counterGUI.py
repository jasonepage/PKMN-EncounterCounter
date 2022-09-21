import pyautogui
from pynput import mouse
import pygame
import math

SCREEN_WIDTH = 430
SCREEN_HEIGHT = 61

FPS = 30
FPS_MS = math.floor(1000 / FPS)
refresh_seconds = 1

global clicked
clicked = False


def on_click(x, y, button, pressed):
    global clicked
    if pressed:
        clicked = True


def render_text(screen, font, text, text_pos, color=(0, 0, 0), center=False):
    sentence_text = font.render(text, True, color)
    text_rect = sentence_text.get_rect()
    if not center:
        text_rect.x = text_pos[0]
        text_rect.y = text_pos[1]
    else:
        text_rect.center = text_pos
    screen.blit(sentence_text, text_rect)


def get_click():
    global clicked
    listener = mouse.Listener(on_click=on_click)
    listener.start()

    while True:
        start_tick = pygame.time.get_ticks()
        pygame.event.get()

        if clicked:
            clicked = False
            listener.stop()
            return pyautogui.position()

        pygame.time.wait(FPS_MS - (pygame.time.get_ticks() - start_tick))
        pygame.display.flip()


def settings_click(screen, main_screen):
    font = pygame.font.Font('freesansbold.ttf', 12)
    text_pos = (0, SCREEN_HEIGHT - 12)
    render_text(screen, font, "Click top left corner of HP", text_pos, (170, 170, 170))

    top_left = get_click()

    screen.blit(main_screen, (0, 0))
    render_text(screen, font, "Click bottom right corner of HP", text_pos, (170, 170, 170))

    bottom_right = get_click()

    screen.blit(main_screen, (0, 0))

    return pyautogui.screenshot(region=(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]))


def reset_click(screen, main_screen):
    update_encounters(screen, main_screen, 0)
    return 0


def update_encounters(screen, main_screen, encounters):
    font = pygame.font.Font('freesansbold.ttf', 20)
    screen.blit(main_screen, (0, 0))
    render_text(screen, font, str(encounters), (309, 19), (200, 200, 200), True)


def search_for_hp(hp_img):
    try:
        loc = list(pyautogui.locateAllOnScreen(hp_img, confidence=0.98))
        return loc
    except Exception:
        return []