import pygame

from isec.environment.scene import EntityScene


class Detector:
    def __init__(self,
                 linked_world,
                 detector_dict: dict[str, str]) -> None:

        self.linked_world = linked_world
        self.detector_dict: dict[str, str] = detector_dict
        self.used = False
        self.rect = pygame.Rect(*detector_dict["rect"])

    async def update(self,
                     player_position: tuple[int, int]) -> None:

        if self.used:
            return

        if not self.rect.collidepoint(player_position):
            return

        action = self.detector_dict["action"]

        if action == "switch_zone":
            self.linked_world.spawn_position = self.detector_dict["player_new_position"]
            self.linked_world.spawn_angle = self.detector_dict["player_new_angle"]
            await self.linked_world.change_world(self.detector_dict["map_name"])

        elif action == "switch_music":
            await self.linked_world.set_music(self.detector_dict["track"], self.detector_dict["volume"])

        elif action == "create_detector":
            raise NotImplementedError("Create detector action not implemented yet")

        elif action == "remove_entity":
            for scene in self.linked_world.scenes:
                if not isinstance(scene, EntityScene):
                    continue

                scene.remove_entities_by_name(self.detector_dict["entity_name"])

        elif action == "add_entity":
            await self.linked_world.add_entity_dict(self.detector_dict["entity_dict"])

        else:
            raise ValueError(f"Invalid detector action: {self.detector_dict['action']}")

        if "keep" not in self.detector_dict or not self.detector_dict["keep"]:
            self.used = True
            return
