import pygame

from isec.app import Resource
from isec.gui import Button
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene, Pos
from isec.environment.sprite import AnimatedSprite

from game.instances.world import World
from game.instances.settings import Settings


_height_offset = -30
_width_offset = 10


class PlayButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = Pos((62+_width_offset, 216+_height_offset))

        surfaces = [Resource.image["menu"][f"play_{i}"] for i in range(1, 3)]
        self.sprite = AnimatedSprite(surfaces, [1, 0])

        self.hovered = False

        async def down_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1
            Resource.sound["effect"]["click_1"].play()

        async def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        async def up_callback() -> None:
            Resource.sound["effect"]["click_2"].play()
            x = World()
            await x.execute()

            pygame.mixer.music.load(Resource.project_assets_directory+"sound/music/menu.ogg")
            music_volume = (Resource.data["engine"]["resource"]["sound"]["master_volume"] *
                            Resource.data["engine"]["resource"]["sound"]["music_volume"])
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frame_durations = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False


class OptionButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = Pos((62+_width_offset, 250+_height_offset))

        surfaces = [Resource.image["menu"][f"settings_{i}"] for i in range(1, 3)]
        self.sprite = AnimatedSprite(surfaces, [1, 0])

        self.hovered = False

        async def down_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1
            Resource.sound["effect"]["click_1"].play()

        async def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        async def up_callback() -> None:
            Resource.sound["effect"]["click_2"].play()
            x = Settings()
            await x.execute()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frame_durations = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False


class QuitButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = Pos((62+_width_offset, 284+_height_offset))

        surfaces = [Resource.image["menu"][f"quit_{i}"] for i in range(1, 3)]
        self.sprite = AnimatedSprite(surfaces, [1, 0])

        self.hovered = False

        async def down_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1
            Resource.sound["effect"]["click_1"].play()

        async def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        async def up_callback() -> None:
            Resource.sound["effect"]["click_2"].play()
            LoopHandler.stop_game()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frame_durations = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False
