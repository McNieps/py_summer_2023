from isec.app import Resource
from isec.gui import Button
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene, Pos
from isec.environment.sprite import AnimatedSprite


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

        def down_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        def up_callback() -> None:
            print("Play")

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

        def down_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        def up_callback() -> None:
            print("Settings")

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

        def down_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        def pressed_callback() -> None:
            self.hovered = True
            self.sprite.frame_durations = [0, 1]
            self.sprite.current_frame = 1

        def up_callback() -> None:
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
