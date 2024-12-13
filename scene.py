import pygame as pg

class Scene:
    def __init__(
            self,
            resolution: tuple[int, int],
            name: str = "PyEngine",
            fps: int = 60,
            background: tuple[int, int, int] = (255, 255, 255),
            embedded=False
    ):
        self.width, self.height = resolution
        self.name = name
        if embedded:
            self.window = pg.Surface(resolution)
        else:
            self.window = pg.display.set_mode(resolution, flags=pg.RESIZABLE)
            pg.display.set_caption(name)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.run = True
        self.background = background
        self.deltaTime = 0

        self.objects = []

        self.onInit()

    def onInit(self): ...

    def tick(self) -> None: ...

    def display(self) -> None: ...

    def event(self, event: pg.event.Event) -> None: ...

    def debug(self): ...

    def videoResize(self):
        """self.width and self.height are automatically updated, use them for rescaling"""

    def mouseDown(self, event): ...

    def mouseUp(self, event): ...

    def scroll(self, event): ...

    def keyDown(self, event): ...

    def renderFrame(self):
        """This function is only used for embedded scenes so that the display output may be displayed"""
        self.window.fill(self.background)
        self.display()

    def quit(self):
        """Use this function if you want to return something from the [game].start() function"""

    def start(self):
        """WARNING! Avoid modifying this function"""

        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN:
                    self.keyDown(event)

                    if event.key == pg.K_F3:
                        print(f"[Graphics] delta time {self.deltaTime}")
                        self.debug()

                if event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict["size"]
                    self.videoResize()

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mouseDown(event)

                if event.type == pg.MOUSEBUTTONUP:
                    self.mouseUp(event)

                if event.type == pg.MOUSEWHEEL:
                    self.scroll(event)

                self.event(event)

            self.deltaTime = self.clock.tick(self.fps) / 16
            if self.deltaTime > 1.2:
                print("[Graphics] Low FPS")
            self.tick()
            self.window.fill(self.background)
            self.display()
            pg.display.update()

        return self.quit()