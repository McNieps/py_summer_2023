import pygame


class Detector:
    def __init__(self,
                 linked_world,
                 detector_dict: dict[str, str]) -> None:

        self.linked_world = linked_world
        self.detector_dict: dict[str, str] = detector_dict

        self.rect = pygame.Rect(*detector_dict["rect"])

    async def update(self,
                     player_position: tuple[int, int]) -> None:

        print("called")
        print("player_position", player_position)
        print("self.rect", self.rect)
        if not self.rect.collidepoint(player_position):
            return

        print("AAAAAAAAA")
        if self.detector_dict["action"] == "switch_zone":
            self.linked_world.spawn_position = self.detector_dict["spawn_position"]
            self.linked_world.spawn_angle = self.detector_dict["spawn_angle"]
            await self.linked_world.load_world(self.detector_dict["map_name"])

        else:
            raise ValueError(f"Invalid detector action: {self.detector_dict['action']}")