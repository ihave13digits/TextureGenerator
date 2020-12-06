#!/usr/bin/python3

import pygame as pg
from os import path

class TextureGenerator:

    def __init__(self, w, h, t, C, c):
        self.running = True
        self.grey = True
        self.width = w
        self.height = h
        self.tile = t
        self.procedure = 0
        self.procedures = [self.proc_random, self.proc_cloth, self.proc_wood, self.proc_brick, self.proc_plank]
        self.blend = 0
        self.blends = [self.combine]
        self.base_color = C
        self.color = c
        self.t = 0
        self.target = 0
        self.targets = [self.base_color, self.color]
        self.matrix = self.make_matrix()
        self.img = pg.Surface((w, h))
        self.rect = self.img.get_rect()
        self.rect.topleft = (0, 0)
        self.root_dir = path.dirname(__file__)
        self.img_dir = path.join(self.root_dir, 'img')
        self.img_name = 'random'
        self.saved_imgs = {
                'random':0, 'cloth':0, 'wood':0, 'brick':0, 'plank':0}
        self.screen = pg.display.set_mode((w*self.tile+128, h*self.tile))
        pg.display.set_caption("TextureGenerator")
        pg.key.set_repeat(50, 100)

    def start(self):
        try:
            from os import mkdir
            mkdir(path.join(self.root_dir, 'img'))
        except:
            pass
        self.img_dir = path.join(self.root_dir, 'img')

        pg.font.init()
        self.update_all()
        self.run()

    def update_info(self):
        self.show_text("Base R: {}".format(self.base_color[0]), self.width*self.tile, 0)
        self.show_text("Base G: {}".format(self.base_color[1]), self.width*self.tile, 32)
        self.show_text("Base B: {}".format(self.base_color[2]), self.width*self.tile, 64)
        self.show_text("Hue R:  {}".format(self.color[0]), self.width*self.tile, 128)
        self.show_text("Hue G:  {}".format(self.color[1]), self.width*self.tile, 160)
        self.show_text("Hue B:  {}".format(self.color[2]), self.width*self.tile, 192)
        self.show_text("{}:  {}".format(self.img_name, self.saved_imgs[self.img_name]), self.width*self.tile, 256)
        self.show_text("{} {}".format(self.target, self.t), self.width*self.tile, 288)

    def update_all(self):
        self.screen.fill((0, 0, 0))
        self.show_img()
        self.update_info()

    def update(self):
        for event in pg.event.get():
            # Window Input
            if event.type == pg.QUIT:
                self.running = False
                quit()

            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if event.key == pg.K_1:
                    if self.procedure  > 0:
                        self.procedure -= 1
                        self.update_all()
                if event.key == pg.K_2:
                    if self.procedure < len(self.procedures)-1:
                        self.procedure += 1
                        self.update_all()

                if event.key == pg.K_3:
                    self.update_all()
                if event.key == pg.K_4:
                    self.port()
                    self.update_all()

                if event.key == pg.K_g:
                    if self.grey == False:
                        self.grey = True
                    else:
                        self.grey = False
                    self.update_all()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    if self.t > 0:
                        self.t -= 1
                    else:
                        if self.target > 0:
                            self.t = 2
                            self.target -= 1
                    self.update_all()
                if event.key == pg.K_s:
                    if self.t < 2:
                        self.t += 1
                    else:
                        if self.target < 1:
                            self.t = 0
                            self.target += 1
                    self.update_all()

                if event.key == pg.K_a:
                    if self.targets[self.target][self.t] > 0:
                        self.targets[self.target][self.t] -= 1
                    self.update_all()
                if event.key == pg.K_d:
                    if self.targets[self.target][self.t] < 255:
                        self.targets[self.target][self.t] += 1
                    self.update_all()

    def run(self):
        while self.running:
            self.update()

    def make_matrix(self):
        matrix = self.fill_solid(self.base_color)
        self.matrix = self.procedures[self.procedure](matrix)

    def make_img(self):
        for x in range(self.width):
            for y in range(self.height):
                v = int((y * self.width) + x)
                try:
                    self.img.set_at((x, y), self.matrix[v])
                except IndexError:
                    pass

    def show_img(self):
        self.make_matrix()
        self.make_img()
        
        img = self.img
        img = pg.transform.scale(img, (self.width*self.tile, self.height*self.tile))
        rect = img.get_rect()
        self.screen.blit(img, rect)
        
        pg.display.flip()

    def show_text(self, txt, x, y, color=(255, 255, 255), a=True):
        font = pg.font.Font(pg.font.get_default_font(), 16)
        text = font.render(txt, a, color)
        self.screen.blit(text, (x, y))
        pg.display.flip()

    def port(self):
        filename = "{}_{}".format(self.img_name, self.saved_imgs[self.img_name])
        pg.image.save(self.img, path.join(self.img_dir, filename))
        self.saved_imgs[self.img_name] += 1

    def fill_solid(self, color):
        matrix = []
        for y in range(self.height):
            for x in range(self.width):
                matrix.append(color)

        return matrix

    def combine(self, col1, col2):
        if not self.grey:
            r = int(col1[0] + col2[0])
            g = int(col1[1] + col2[1])
            b = int(col1[2] + col2[2])

            if r > 255:
                r = 255
            if r < 0:
                r = 0

            if g > 255:
                g = 255
            if g < 0:
                g = 0

            if b > 255:
                b = 255
            if b < 0:
                b = 0

            color = (r, g, b)
        else:
            g = int(col1[0] + col2[0])
            if g > 255:
                g = 255
            if g < 0:
                 g = 0
            color = (g, g, g)
        return color

    def proc_random(self, m):
        from random import randint
        
        self.img_name = "random"
        matrix = m
        if not self.grey:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    R = randint(0, self.color[0])
                    G = randint(0, self.color[1])
                    B = randint(0, self.color[2])
                    matrix[index] = self.blends[self.blend](self.base_color, (R, G, B))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    g = randint(-self.color[0], 0)
                    matrix[index] = self.blends[self.blend](self.base_color, (g, g, g))
        return matrix

    def proc_cloth(self, m):
        from random import randint

        self.img_name = "cloth"
        matrix = m
        count = 0
        stagger = 1
        if not self.grey:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    R = randint(-int(self.color[0]/8), 0)
                    G = randint(-int(self.color[1]/8), 0)
                    B = randint(-int(self.color[2]/8), 0)
                    if y % 2 == 0 and count % 2 == 0:
                        R = randint(-int(self.color[0]/4), 0)
                        G = randint(-int(self.color[1]/4), 0)
                        B = randint(-int(self.color[2]/4), 0)
                    count += 1
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (R, G, B))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    g = randint(-self.color[0], 0)
                    if y % 2 == 0 and count % 2 == 0:
                        g = randint(-int(self.color[0]/4), 0)
                    count += 1
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (g, g, g))
        return matrix

    def proc_wood(self, m):
        from random import randint

        self.img_name = "wood"
        matrix = m
        count = 0
        stagger = int(self.width*4)
        if not self.grey:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    R = randint(-int(self.color[0]/8), 0)
                    G = randint(-int(self.color[1]/8), 0)
                    B = randint(-int(self.color[2]/8), 0)
                    if y % int(self.width/8) == 0:
                        count += 1
                    if y % 2 == 0 and count == 0:
                        R = randint(-int(self.color[0]/4), 0)
                        G = randint(-int(self.color[1]/4), 0)
                        B = randint(-int(self.color[2]/4), 0)
                    if y % 2 == 0 and count == 1:
                        R = randint(-int(self.color[0]/2), 0)
                        G = randint(-int(self.color[1]/2), 0)
                        B = randint(-int(self.color[2]/2), 0)
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (R, G, B))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    g = randint(-self.color[0], 0)
                    if x % int(self.width/8) == 0:
                        count += 1
                    if x % 2 == 0 and count % 2 == 0:
                        g = randint(-int(self.color[0]/4), 0)
                    if x % 2 == 0 and count % 2 == 1:
                        g = randint(-int(self.color[0]/2), 0)
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (g, g, g))
        return matrix

    def proc_brick(self, m):
        from random import randint
        from math import sqrt

        self.img_name = "brick"
        matrix = m
        count = 0
        stagger = int(self.height / sqrt(self.height))
        if not self.grey:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    R = randint(-int(self.color[0]/16), 0)
                    G = randint(-int(self.color[1]/16), 0)
                    B = randint(-int(self.color[2]/16), 0)
                    if y % int(self.height / 8) == 0:
                        count += 1
                        R = randint(-self.color[0], 0)
                        G = randint(-self.color[1], 0)
                        B = randint(-self.color[2], 0)
                    if x % int(self.width / 4) == 0 and count % 2 == 0:
                        R = randint(-self.color[0], 0)
                        G = randint(-self.color[1], 0)
                        B = randint(-self.color[2], 0)
                    if x % int(self.width / 4) == int(self.width / 8) and count % 2 == 1:
                        R = randint(-self.color[0], 0)
                        G = randint(-self.color[1], 0)
                        B = randint(-self.color[2], 0)
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (R, G, B))
        
        else:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    g = randint(-int(self.color[0]/16), 0)
                    if y % int(self.height / 8) == 0:
                        count += 1
                        g = randint(-self.color[0], 0)
                    if x % int(self.width / 4) == 0 and count % 2 == 0:
                        g = randint(-self.color[0], 0)
                    if x % int(self.width / 4) == int(self.width / 8) and count % 2 == 1:
                        g = randint(-self.color[0], 0)
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (g, g, g))
        return matrix

    def proc_plank(self, m):
        from random import randint

        self.img_name = "plank"
        matrix = m
        count = 0
        stagger = 3
        grain = 33

        if not self.grey:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    R = randint(-int(self.color[0]/16), 0)
                    G = randint(-int(self.color[1]/16), 0)
                    B = randint(-int(self.color[2]/16), 0)
                    if x % int(self.width / int(self.width / 2)) == 0:
                        chance = randint(0, 100)
                        if chance < grain:
                            R = randint(-(self.color[0]/4), 0)
                            G = randint(-(self.color[1]/4), 0)
                            B = randint(-(self.color[2]/4), 0)
                    if x % int(self.width / 8) == 0:
                        count += 1
                        R = randint(-self.color[0], 0)
                        G = randint(-self.color[1], 0)
                        B = randint(-self.color[2], 0)
                    if y % int(self.height / 2) == 0 and count % 2 == 0:
                        R = randint(-self.color[0], 0)
                        G = randint(-self.color[1], 0)
                        B = randint(-self.color[2], 0)
                    if y % int(self.height / 2) == int(self.height / 4) and count % 2 == 1:
                        R = randint(-self.color[0], 0)
                        G = randint(-self.color[1], 0)
                        B = randint(-self.color[2], 0)
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (R, G, B))
        else:
            for y in range(self.height):
                for x in range(self.width):
                    index = (y * self.width) + x
                    g = randint(-int(self.color[0]/16), 0)
                    if x % int(self.width / int(self.width / 2)) == 0:
                        chance = randint(0, 100)
                        if chance < grain:
                            g = randint(-(self.color[0]/4), 0)
                    if x % int(self.width / 8) == 0:
                        count += 1
                        g = randint(-self.color[0], 0)
                    if y % int(self.height / 2) == 0 and count % 2 == 0:
                        g = randint(-self.color[0], 0)
                    if y % int(self.height / 2) == int(self.height / 4) and count % 2 == 1:
                        g = randint(-self.color[0], 0)
                    if count > stagger:
                        count = 0
                    matrix[index] = self.blends[self.blend](self.base_color, (g, g, g))
        return matrix

TG = TextureGenerator(64, 64, 10, [255, 255, 255], [32, 32, 32])
TG.start()
