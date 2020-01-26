import sprites
import math
import pygame


a = 135


def scalar(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


def module(x, y):
    return math.sqrt(x ** 2 + y ** 2)

class Engine():

    def __init__(self, person):
        self.obj = []
        self.person = person

    def check(self, x, y):
        # https://mrtsepa.gitbooks.io/pygame-tutorial/content/reference/pygame/masks.html
        for wall in sprites.walls:
            offset = (wall.rect.x - self.person.rect.x - x,
                      wall.rect.y - self.person.rect.y - y)
            if self.person.mask.overlap_area(wall.mask, offset) > 0:
                return False
        return True

    def move(self, i):
        if i == 0 and self.check(0, -1):
            self.person.rect = self.person.rect.move(0, -1)
            self.person.w()
        elif i == 1 and self.check(1, -1):
            self.person.rect = self.person.rect.move(1, -1)
            self.person.w()
        elif i == 2 and self.check(1, 0):
            self.person.rect = self.person.rect.move(1, 0)
            self.person.d()
        elif i == 3 and self.check(1, 1):
            self.person.rect = self.person.rect.move(1, 1)
            self.person.d()
        elif i == 4 and self.check(0, 1):
            self.person.rect = self.person.rect.move(0, 1)
            self.person.s()
        elif i == 5 and self.check(-1, 1):
            self.person.rect = self.person.rect.move(-1, 1)
            self.person.s()
        elif i == 6 and self.check(-1, 0):
            self.person.rect = self.person.rect.move(-1, 0)
            self.person.a()
        elif i == 7 and self.check(-1, -1):
            self.person.rect = self.person.rect.move(-1, -1)
            self.person.a()
        else:
            return False
        return True

    def key(self, w, a, s, d):
        if w and a:
            res = self.move(7)
            if not res:
                res = self.move(0)
                if not res:
                    self.move(6)
        elif s and a:
            res = self.move(5)
            if not res:
                res = self.move(4)
                if not res:
                    self.move(6)
        elif d and s:
            res = self.move(3)
            if not res:
                res = self.move(4)
                if not res:
                    self.move(2)
        elif w and d:
            res = self.move(1)
            if not res:
                res = self.move(0)
                if not res:
                    self.move(2)
        elif w:
            self.move(0)
        elif a:
            self.move(6)
        elif s:
            self.move(4)
        elif d:
            self.move(2)

    def attack_anim(self, angle):
        angle = angle % 360
        if 315 <= angle <= 360 or 0 <= angle <= 45:
            self.person.d_attack()
        elif 45 < angle <= 135:
            self.person.w_attack()
        elif 135 < angle <= 225:
            self.person.a_attack()
        else:
            self.person.s_attack()


    def atack(self, x, y):
        x2 = x - self.person.rect.x - 32
        y2 = - y + self.person.rect.y + 32
        cos1 = scalar(100, 0, x2, y2) / (module(100, 0) * module(x2, y2))
        cos2 = scalar(0, 100, x2, y2) / (module(0, 100) * module(x2, y2))
        ang1 = math.degrees(math.acos(cos1))
        ang2 = math.degrees(math.acos(cos2))
        if ang2 < 90:
            angle = math.degrees(math.acos(cos1))
        else:
            angle = 360 - math.degrees(math.acos(cos1))
        arrow = sprites.AroowSprite(pygame.image.load("tmp/270.png"))
        arrow.rotate_c((angle + a) % 360)
        arrow.rect.center = self.person.rect.center
        lenght = math.sqrt(x2 ** 2 + y2 ** 2)
        k = lenght / 15
        l = 1 / (k - 1)
        arrow.dx = (l * x2) / (1 + l)
        arrow.dy = -(l * y2) / (1 + l)
        self.person.cur_frame = 0
        return angle