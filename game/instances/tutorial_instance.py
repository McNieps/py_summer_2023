import pygame

from isec.instance import BaseInstance
from isec.environment import Scene


class TutorialInstance(BaseInstance):
    def __init__(self):
        super().__init__(50)
        self.scene = Scene()

    async def loop(self):
        self.event_handler.handle_events()
        self.window.fill((255, 255, 255))
        pygame.display.update()
        self.scene.render()


if __name__ == '__main__':
    import asyncio

    from isec.app import App, Resource


    async def main():
        App.init("../assets/", default_only=True)
        print(Resource.data, "\n", Resource.image, "\n", Resource.sound)
        Resource.sound["intro"].set_volume(0.1)
        Resource.sound["intro"].play()
        await TutorialInstance().execute()


    asyncio.run(main())
