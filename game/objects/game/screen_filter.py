import pygame

from isec.app import Resource

from isec.environment import Pos, Sprite, Entity


class ScreenFilter(Entity):
    def __init__(self):
        self.enabled = True
        self.brightness = 0

        super().__init__(Pos((200, 150), (0, 0)),
                         Sprite(Resource.image["game"]["shadow"], blit_flag=pygame.BLEND_MULT))

    def update_filter(self,
                      enabled: bool = True,
                      brightness: int = 0) -> None:

        print(brightness)

        self.enabled = enabled
        self.brightness = brightness

        if self.brightness == 255 or not self.enabled:
            self.enabled = False
            return

        surf = Resource.image["game"]["shadow"].copy()

        if self.brightness < 0:
            flag = pygame.BLEND_RGB_SUB
        else:
            flag = pygame.BLEND_RGB_ADD

        brightness_abs_value = abs(self.brightness)
        print(brightness_abs_value)
        brightness_surf = pygame.Surface((400, 300))
        brightness_surf.fill((brightness_abs_value, brightness_abs_value, brightness_abs_value))
        surf.blit(brightness_surf, (0, 0), special_flags=flag)

        self.sprite.surface = surf
