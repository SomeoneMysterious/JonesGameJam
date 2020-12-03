import EditedGames as games
import pygame
from superwires import color
import random
import time

games.init(screen_width=640, screen_height=480, fps=50)


class LittleRed(games.Sprite):
    image = games.load_image("LittleRed.png")
    spritename = "Red"

    def __init__(self):
        super(LittleRed, self).__init__(self.image, x=20, y=240, dx=.2)
        print(self.top, self.bottom)

    def update(self):
        for sprite in self.overlapping_sprites:
            if sprite.spritename == "Wolf":
                games.screen.quit()
        if self.x > 620:
            print("You Won!")
            games.screen.quit()
            time.sleep(5)


class MouseChecker(games.Sprite):
    image = games.load_image("mouseCollider.png")
    spritename = "Mouse"

    def __init__(self):
        super(MouseChecker, self).__init__(self.image, x=games.mouse.x, y=games.mouse.y)

    def update(self):
        self.x = games.mouse.x
        self.y = games.mouse.y
        for sprite in self.overlapping_sprites:
            if sprite.spritename == "Wolf":
                sprite.die()


class Wolf(games.Sprite):
    image = games.load_image("Wolf.png", True)
    spritename = "Wolf"

    def __init__(self, x, y, target):
        super(Wolf, self).__init__(self.image, x=x, y=y)
        self.target = target
        self.adj_angle()

    def adj_angle(self):
        a = (self.y - self.target.y) * -1
        b = (self.x - self.target.x) * -1
        self.dx = b / 200
        self.dy = a / 200
        # self.angle =

    def die(self):
        main.killWolf(self)
        self.destroy()


class Game(object):
    redhood = collider = None
    wolfs = []
    betweenWolfs = lastSpawn = 2

    def start(self):
        self.redhood = LittleRed()
        games.screen.add(self.redhood)
        self.collider = MouseChecker()
        games.screen.add(self.collider)
        self.spawn_wolf()

    def spawn_wolf(self):
        x = random.randint(40, 600)
        while x + 50 <= self.redhood.x <= x - 75:
            x = random.randint(40, 600)
        if random.randint(0, 2) == 1:
            y = random.randint(30, 125)
        else:
            y = random.randint(350, 450)
        self.wolfs.append(Wolf(x, y, self.redhood))
        games.screen.add(self.wolfs[-1])

    def main(self):
        games.screen.running = True
        self.lastSpawn = currTime = time.time()
        while games.screen.running:
            games.screen.updateGame(currTime)
            currTime = time.time()
            if self.lastSpawn + self.betweenWolfs < currTime:
                self.spawn_wolf()
                self.betweenWolfs -= .02
                self.lastSpawn = currTime

    def killWolf(self, wolfID):
        if wolfID in self.wolfs:
            del self.wolfs[self.wolfs.index(wolfID)]


if __name__ == "__main__":
    main = Game()
    main.start()
    main.main()
