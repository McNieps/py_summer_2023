import typing

import pygame.mouse

from isec.app import Resource
from isec.environment import Entity, sprite, position, Scene
from isec.instance import BaseInstance


class Button(Entity):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: Scene,
                 button_position: position.Pos = None,
                 button_sprite: sprite.SimpleSprite = None,
                 up_callback: typing.Callable[[], None] = None,
                 down_callback: typing.Callable[[], None] = None,
                 pressed_callback: typing.Callable[[], None] = None) -> None:

        if button_position is None:
            button_position = position.SimplePos()

        if button_sprite is None:
            button_sprite = sprite.SimpleSprite(Resource.image["stock"]["button"],
                                                "static")

        if up_callback is None:
            up_callback = self._empty_callback

        if down_callback is None:
            down_callback = self._empty_callback

        if pressed_callback is None:
            pressed_callback = self._empty_callback

        self.linked_instance = linked_instance
        self.linked_scene = linked_scene

        self.up_callback = up_callback
        self.down_callback = down_callback
        self.pressed_callback = pressed_callback

        self.pressed = False

        super().__init__(button_position, button_sprite)

        self.linked_instance.event_handler.register_buttonup_callback(1, self.mouse_up)
        self.linked_instance.event_handler.register_buttondown_callback(1, self.mouse_down)
        self.linked_instance.event_handler.register_buttonpressed_callback(1, self.mouse_pressed)

    def _check_if_mouse_over(self) -> bool:
        print("TRY")
        self.sprite.rect.center = self.position.position
        mouse_pos_in_scene = self.linked_scene.camera.get_coordinates_from_screen(pygame.mouse.get_pos())
        return self.sprite.rect.collidepoint(mouse_pos_in_scene)

    def mouse_down(self) -> None:
        if self._check_if_mouse_over():
            print("i")
        return
        self.pressed = True
        self.down_callback()

    def mouse_up(self) -> None:
        if self._check_if_mouse_over():
            print("i")
        return
        self.pressed = False
        self.up_callback()

    def mouse_pressed(self) -> None:
        if self._check_if_mouse_over():
            print("i")
        return
        self.pressed_callback()

    def _empty_callback(self):
        return
