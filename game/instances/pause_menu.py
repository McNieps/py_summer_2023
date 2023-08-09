from isec.app import Resource
from isec.instance import BaseInstance


class PauseMenu(BaseInstance):
    def __init__(self):
        super().__init__(Resource.data["instances"]["menu"]["fps"])
