from isec.instance import BaseInstance
from isec.environment import EntityScene


class Map(BaseInstance):
    def __init__(self):
        super().__init__()

        self.scene = EntityScene()

    def loop(self):
        self.scene.update(self.delta)
        self.scene.render()
