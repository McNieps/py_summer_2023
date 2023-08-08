from isec.app import Resource
from isec.environment import EntityScene, Pos
from isec.gui import Button
from isec.environment.sprite import AnimatedSprite
from isec.instance import BaseInstance, LoopHandler


class ReturnButton(Button):
    def __init__(self,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.position = Pos((200, 275))
        self.linked_instance = linked_instance
        surfaces = [Resource.image["menu"][f"return_{i+1}"] for i in range(2)]
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
            LoopHandler.stop_instance(self.linked_instance)

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
