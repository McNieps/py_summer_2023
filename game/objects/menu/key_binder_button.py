import pygame

from isec.app import Resource
from isec.gui import Button
from isec.instance import BaseInstance, LoopHandler
from isec.environment import EntityScene, Pos
from isec.environment.sprite import AnimatedSprite

from game.objects.controls import Controls


class KeyBinderButton(Button):
    last_key = pygame.K_a
    font = None

    def __init__(self,
                 position: tuple[int, int],
                 action_name: str,
                 linked_instance: BaseInstance,
                 linked_scene: EntityScene) -> None:

        self.action = action_name
        self.position = Pos(position)

        surfaces = self.create_surfaces()
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
            x = KeyBindingInstance()
            await x.execute()
            if self.last_key != pygame.K_ESCAPE:
                Controls.change_bind(self.action, self.last_key)
                self.sprite.surfaces = self.create_surfaces()

        super().__init__(linked_instance,
                         linked_scene,
                         self.position,
                         self.sprite,
                         up_callback,
                         down_callback,
                         pressed_callback)

    def create_surfaces(self) -> list[pygame.Surface]:
        if self.font is None:
            self.font = pygame.font.Font(Resource.project_assets_directory+"/font/Ernst-Regular.ttf", 15)

        surfaces = []
        for i in range(2):
            surf = Resource.image["menu"][f"none_{i + 1}"].copy()
            font_surf = self.font.render(Controls.get_key_name_from_action(self.action),
                                         False,
                                         Resource.data["color"]["list"][-3])
            blit_rect = font_surf.get_rect()
            blit_rect.center = (surf.get_width() // 2, i+surf.get_height() // 2)
            surf.blit(font_surf, blit_rect)
            surfaces.append(surf)

        return surfaces

    def update(self, delta) -> None:
        super().update(delta)

        if not self.hovered:
            self.sprite.frame_durations = [1, 0]
            self.sprite.current_frame = 0

        self.hovered = False


class KeyBindingInstance(BaseInstance):
    def __init__(self) -> None:
        super().__init__(60)

    async def loop(self):
        self.window.blit(Resource.image["menu"]["key_confirmation"], (100, 100))
        found_key = False
        for event in self.event_handler.events:
            if event.type == pygame.KEYDOWN:
                KeyBinderButton.last_key = event.key
                found_key = True
                break

        if found_key:
            LoopHandler.stop_instance(self)
