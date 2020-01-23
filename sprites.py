import pygame

character = pygame.sprite.Group()
character_death = pygame.sprite.Group()
aroows = pygame.sprite.Group()
walls = pygame.sprite.Group()
background = pygame.sprite.Group()
doors = pygame.sprite.Group()

T = pygame.sprite.Group()

class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y, main_person, group):
        self.main_person = main_person
        super().__init__(group)
        self.main_sheet = sheet
        self.frames = []
        self.cut_sheet(sheet)
        self.cur_frame = 0
        self.image = self.frames[0][0]
        self.rect = self.rect.move(x, y)
        self.r = self.rect.copy()

        self.mask = pygame.mask.from_surface(self.image)
        self.xp = 100
        self.fps_draw = 0
        self.cnt_death = 0

    def draw(self, screen, dx=0, dy=0):
        if dx != 0 or dy != 0:
            rect = self.rect
            rect = rect.move(dx, dy)
            screen.blit(self.image, rect)
        else:
            screen.blit(self.image, self.rect)

    def cut_sheet(self, sheet):
        pos = [7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 4, 4, 4, 4, 13, 13, 13, 13, 6]
        self.frames = [[] for _ in range(len(pos))]
        self.rect = pygame.Rect(0, 0, 64, 64)
        for j in range(len(pos)):
            for i in range(pos[j]):
                frame_location = (self.rect.w * i, self.rect.h * j)
                e = sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))
                self.frames[j].append(e)

    def update(self, i):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[i])
        self.image = self.frames[i][self.cur_frame]

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def w(self):
        self.update(8)

    def a(self):
        self.update(9)

    def s(self):
        self.update(10)

    def d(self):
        self.update(11)

    def d_attack(self):
        self.update(19)

    def s_attack(self):
        self.update(18)

    def a_attack(self):
        self.update(17)

    def w_attack(self):
        self.update(16)

    def death(self):
        self.update(20)

class AroowSprite(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super().__init__(aroows)
        self.dx = 0
        self.dy = 0
        self.rect = pygame.Rect(0, 0, sheet.get_width(), sheet.get_height())
        self.mask = pygame.mask.from_surface(sheet)
        self.image = sheet
        self.center = (100, 100)
        self.main_image = self.image
        
    def draw(self, screen, dx=0, dy=0):
        if dx != 0 or dy != 0:
            rect = self.rect
            rect = rect.move(dx, dy)
            screen.blit(self.image, rect)
        else:
            screen.blit(self.image, self.rect)

    def blitRotate(self, originPos, angle):
        # https://stackoverflow.com/a/54714144
        pos = (200, 200)
        w, h       = self.main_image.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move   = pivot_rotate - pivot        
        self.image = pygame.transform.rotate(self.main_image, angle)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - originPos[0] + min_box[0] - pivot_move[0]
        self.rect.y = pos[1] - originPos[1] - max_box[1] + pivot_move[1]
        self.mask = pygame.mask.from_surface(self.image)


    def rotate_c(self, angle):
        self.blitRotate((self.main_image.get_width() //2, self.main_image.get_height() // 2), angle)

class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self, screen, dx=0, dy=0):
        if dx != 0 or dy != 0:
            rect = self.rect
            rect = rect.move(dx, dy)
            screen.blit(self.image, rect)
        else:
            screen.blit(self.image, self.rect)
        

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

class Door(pygame.sprite.Sprite):

    def __init__(self, doors_):
        super().__init__(doors)
        self.frames = [pygame.image.load(door) for door in doors_]
        self.rect = self.frames[0].get_rect()
        self.cur_frame = 0
        self.image = self.frames[0]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def draw(self, screen, dx=0, dy=0):
        if dx != 0 or dy != 0:
            rect = self.rect
            rect = rect.move(dx, dy)
            screen.blit(self.image, rect)
        else:
            screen.blit(self.image, self.rect)