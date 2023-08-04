import time
import math

from isec.app import Resource
from isec.environment import Entity, Pos, Sprite
from isec.environment.sprite import AnimatedSprite


class Sea(Entity):
    def __init__(self):
        durations = Resource.data["instances"]["menu"]["sea_frames_durations"]
        surfaces = [Resource.image["menu"][f"sea_{i}"] for i in range(1, len(durations)+1)]
        position = Pos((200, 224))
        animated_sprite = AnimatedSprite(surfaces,
                                         durations)

        super().__init__(position, animated_sprite)


class Stars(Entity):
    def __init__(self):
        surface = Resource.image["menu"]["stars"]
        position = Pos((200, 74))
        super().__init__(position, Sprite(surface))


class Boat(Entity):
    def __init__(self):
        durations = Resource.data["instances"]["menu"]["boat_frames_durations"]
        surfaces = [Resource.image["menu"][f"boat_{i}"] for i in range(1, len(durations)+1)]
        position = Pos((200, 224))
        animated_sprite = AnimatedSprite(surfaces,
                                         durations)

        super().__init__(position, animated_sprite)


class Constellation(Entity):
    def __init__(self):
        surface = Resource.image["menu"]["constellations"]
        position = Pos((200, 75))

        self.creation_time = time.time()
        super().__init__(position, Sprite(surface))

    def update(self, delta):
        super().update(delta)
        elapsed_time = time.time() - self.creation_time
        sine_value = math.sin(-elapsed_time/2)
        surface_alpha = max(0, int((sine_value-0.8)*255/0.2))
        self.sprite.surface.set_alpha(surface_alpha)
