import pygame
from counterGUI import *


def main():
    pygame.init()
    pygame.display.set_caption("Encounter Counter")
    pygame_icon = pygame.image.load('ec_resources\pokeMMO.jpg')
    pygame.display.set_icon(pygame_icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    try:
        config_file = open("ec_resources/encounter.config", "r")
        encounters = int(config_file.read())
        config_file.close()
    except FileNotFoundError:
        encounters = 0

    in_encounter = False
    frame = 0

    try:
        main_screen = pygame.image.load("ec_resources/main_screen.jpg")
    except pygame.error:
        print("error finding main_screen")

    update_encounters(screen, main_screen, encounters)
    pygame.display.flip()

    running = True
    while running:
        start_tick = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config_file = open("ec_resources/encounter.config", "w")
                config_file.write(str(encounters))
                config_file.close()
                return 0
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 412 < pos[0] < 426 and 2 < pos[1] < 16:
                    hp_img = settings_click(screen, main_screen)
                    hp_img.save("ec_resources/hp_img.png", "PNG")
                    update_encounters(screen, main_screen, encounters)
                elif 353 < pos[0] < 376 and 9 < pos[1] < 29:
                    encounters = reset_click(screen, main_screen)
                elif 380 < pos[0] < 400:
                    if 5 < pos[1] < 15:
                        encounters += 1
                        update_encounters(screen, main_screen, encounters)
                    elif 20 < pos[1] < 30:
                        encounters -= 1
                        update_encounters(screen, main_screen, encounters)

        if frame == FPS * refresh_seconds:
            matches = len(search_for_hp("ec_resources/hp_img.png"))
            if matches > 0:
                if not in_encounter:
                    encounters += matches
                    in_encounter = True
                    update_encounters(screen, main_screen, encounters)
            else:
                in_encounter = False
            frame = 0
            print(in_encounter)
            print(encounters)

        pygame.time.wait(FPS_MS - (pygame.time.get_ticks() - start_tick))
        pygame.display.flip()
        frame += 1

if __name__ == '__main__':
    main()
