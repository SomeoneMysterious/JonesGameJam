import EditedGames as games
import pygame
from superwires import color
import random
import time
import math

games.init(screen_width=640, screen_height=480, fps=50)


class LittleRed(games.Sprite):
    image = games.load_image("LittleRed.png")
    spritename = "Red"

    def __init__(self):
        super(LittleRed, self).__init__(self.image, x=20, y=240, dx=.2)
        print(self.top, self.bottom)

    def update(self):
        for sprite in self.overlapping_sprites:
            if game.won is None:
                if sprite.spritename == "Wolf":
                    game.won = False
                    game.killAllWolfs(spare=sprite)
                    print("You Lost!")
                    # games.screen.running = False
                    game.ending()
                    self.dx = game.wolfs[0].dx
                    self.dy = game.wolfs[0].dy
                elif sprite.spritename == "House":
                    game.won = True
                    game.killAllWolfs()
                    print("You Won!")
                    # games.screen.running = False
                    game.ending()
                    self.dx = 0


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
                if game.won is None:
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
        c = math.sqrt(abs(a * a) + abs(b * b))
        cos = b / c
        angle = math.acos(cos)
        angle = angle * (180 / math.pi)
        # This code below is guess and check, it doesn't work perfectly, and I don't know how it works or should work.
        if self.y < 120:
            angle += 180
        else:
            if game.redhood.x > self.x:
                angle += 90
            else:
                angle -= 90
        self.angle = angle

    def die(self, spare=None):
        if spare != self:
            game.killWolf(self)
            self.destroy()
        else:
            self.dx *= -2
            self.dy *= -2


class House(games.Sprite):
    image = games.load_image("House.png")
    spritename = "House"

    def __init__(self):
        super(House, self).__init__(self.image, x=580, y=240)


class Game(object):
    redhood = collider = background = house = won = None
    wolfs = []
    betweenWolfs = lastSpawn = 2

    def __init__(self):
        self.background = games.load_image("background.png", False)
        games.screen.background = self.background

    def start(self):
        self.redhood = LittleRed()
        games.screen.add(self.redhood)
        self.collider = MouseChecker()
        games.screen.add(self.collider)
        self.house = House()
        games.screen.add(self.house)
        self.spawn_wolf()

    def spawn_wolf(self):
        x = random.randint(40, 600)
        while x + 50 <= self.redhood.x <= x - 75:
            x = random.randint(40, 600)
        if random.randint(0, 2) == 1:
            y = random.randint(30, 100)
        else:
            y = random.randint(375, 450)
        self.wolfs.append(Wolf(x, y, self.redhood))
        games.screen.add(self.wolfs[-1])

    def main(self):
        games.screen.running = True
        self.lastSpawn = currTime = time.time()
        while games.screen.running:
            games.screen.updateGame(currTime)
            currTime = time.time()
            if self.won is None:
                if self.lastSpawn + self.betweenWolfs < currTime:
                    self.spawn_wolf()
                    self.betweenWolfs -= .04
                    if self.betweenWolfs < .4:
                        self.betweenWolfs = .4
                    self.lastSpawn = currTime

    def ending(self):
        if self.won:
            message = games.Message(value="You Won!",
                                          size=80,
                                          color=color.yellow,
                                          x=games.screen.width / 2,
                                          y=games.screen.height / 2,
                                          lifetime=3 * games.screen.fps,
                                          after_death=self.wrapup,
                                          is_collideable=False)
        else:
            message = games.Message(value="You Lost!",
                                          size=80,
                                          color=color.yellow,
                                          x=games.screen.width / 2,
                                          y=games.screen.height / 2,
                                          lifetime=3 * games.screen.fps,
                                          after_death=self.wrapup,
                                          is_collideable=False)
        games.screen.add(message)

    def wrapup(self):
        games.screen.running = False
        pygame.quit()

    def killWolf(self, wolfID):
        if wolfID in self.wolfs:
            del self.wolfs[self.wolfs.index(wolfID)]

    def killAllWolfs(self, spare=None):
        [wolf.die(spare) for wolf in self.wolfs]


if __name__ == "__main__":
    game = Game()
    game.start()
    game.main()
