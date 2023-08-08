import pygame

from isec.app import Resource
from isec.instance import BaseInstance
from isec.environment import EntityScene

from game.objects.menu.key_binder_button import KeyBinderButton
from game.objects.menu.return_button import ReturnButton


class Controls(BaseInstance):
    def __init__(self) -> None:
        super().__init__(60)
        self.scene = EntityScene(60)
        self.scene.add_entities(ReturnButton(self, self.scene))

        for i, action in enumerate(["UP", "LEFT", "DOWN", "RIGHT", "BOOST"]):
            self.scene.add_entities(KeyBinderButton((200, 112+i*30),
                                                    action,
                                                    self,
                                                    self.scene))

        blur_window = pygame.transform.box_blur(self.window, 1)
        self.window.blit(blur_window, (0, 0))

    async def loop(self):
        self.window.blit(Resource.image["menu"]["controls_board"], (50, 37))
        self.scene.update(self.delta)
        self.scene.render()
