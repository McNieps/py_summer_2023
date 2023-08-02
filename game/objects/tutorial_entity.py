from isec.environment import Entity
from isec.environment.sprite import DebugSprite
from isec.environment.position import SimplePos


class TutorialEntity(Entity):
    def __init__(self):
        super().__init__(SimplePos(), DebugSprite())
