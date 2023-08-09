import pygame

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene

from game.objects.menu.settings_buttons import ControlsButton, SoundsButton
from game.objects.menu.return_button import ReturnButton


class Settings(BaseInstance):
    def __init__(self) -> None:
        super().__init__(Resource.data["instances"]["menu"]["fps"])
        self.scene = EntityScene(Resource.data["instances"]["menu"]["fps"])
        self.scene.add_entities(ControlsButton(self, self.scene),
                                SoundsButton(self, self.scene),
                                ReturnButton(self, self.scene))

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

        self.event_handler.register_keydown_callback(pygame.K_ESCAPE, self.quit_instance)

    async def loop(self):
        self.window.blit(Resource.image["menu"]["settings_board"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)
