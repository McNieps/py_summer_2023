import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import EntityScene

from game.objects.menu.settings_buttons import ControlsButton, SoundsButton
from game.objects.menu.return_button import ReturnButton


class Settings(BaseInstance):
    def __init__(self) -> None:
        super().__init__(60)
        self.scene = EntityScene(60)
        self.scene.add_entities(ControlsButton(self, self.scene),
                                SoundsButton(self, self.scene),
                                ReturnButton(self, self.scene))

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

    async def loop(self):
        self.window.blit(Resource.image["menu"]["settings_board"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()
