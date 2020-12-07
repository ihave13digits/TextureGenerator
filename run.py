#!/usr/bin/python3

import pygame as pg
from os import path
from random import randint

class TextureGenerator:

    def __init__(self, w, h, t, C, c):
        self.running = True
        self.grey = True
        self.width = w
        self.height = h
        self.tile = t
        self.procedures = [self.proc_random, self.proc_noise, self.proc_fuzz, self.proc_cloth, self.proc_skin, self.proc_wood, self.proc_brick, self.proc_plank]
        self.blends = [self.blend_subtract, self.blend_add, self.blend_combine]
        self.target = 0
        self.targets = []
        self.matrix = []
        self.img = pg.Surface((w, h))
        self.rect = self.img.get_rect()
        self.rect.topleft = (0, 0)
        self.root_dir = path.dirname(__file__)
        self.img_dir = path.join(self.root_dir, 'img')
        self.img_name = 'random'
        self.lmt = {
                'procedure' : [0, len(self.procedures)-1],
                'blend' : [0, len(self.blends)-1],
                'grain' : [0, 100],
                'scale' : [0, 0],
                'pack' : [1, 0],
                'stagger' : [0, 0],
                'density' : [0, 0],
                'octaves' : [0, 8],
                'R' : [0, 255],
                'G' : [0, 255],
                'B' : [0, 255],
                'r' : [0, 255],
                'g' : [0, 255],
                'b' : [0, 255],
                }
        self.var = {
                'procedure' : 0,
                'blend' : 0,
                'grain' : 0,
                'scale' : 1,
                'pack' : 3,
                'stagger' : 0,
                'density' : 0,
                'octaves' : 0,
                'R' : C[0],
                'G' : C[1],
                'B' : C[2],
                'r' : c[0],
                'g' : c[1],
                'b' : c[2]
                }
        self.saved_imgs = {'random':0, 'noise':0, 'fuzz':0, 'cloth':0, 'skin':0, 'wood':0, 'brick':0, 'plank':0}
        self.screen = pg.display.set_mode((w*self.tile+128, h*self.tile))

    def start(self):
        pg.font.init()
        pg.display.set_caption("TextureGenerator")
        pg.key.set_repeat(50, 100)

        try:
            from os import mkdir
            mkdir(path.join(self.root_dir, 'img'))
        except:
            pass
        self.img_dir = path.join(self.root_dir, 'img')

        for key in self.var:
            self.targets.append(key)
        
        self.matrix = self.make_matrix()
        self.new_img()
        self.update_all()
        self.run()

    def update_info(self):
        self.show_text("{}:  {}".format(self.img_name, self.saved_imgs[self.img_name]), self.width*self.tile, 0)
        self.show_text("{}".format(self.targets[self.target]), self.width*self.tile, 20)
        
        self.show_text("type:  {}".format(self.img_name), self.width*self.tile, 60)
        self.show_text("blend:  {}".format(self.var['blend']), self.width*self.tile, 80)
        self.show_text("grain:  {}".format(self.var['grain']), self.width*self.tile, 100)
        self.show_text("scale:  {}".format(self.var['scale']), self.width*self.tile, 120)
        self.show_text("pack:  {}".format(self.var['pack']), self.width*self.tile, 140)
        self.show_text("stagger:  {}".format(self.var['stagger']), self.width*self.tile, 160)
        self.show_text("density:  {}".format(self.var['density']), self.width*self.tile, 180)
        self.show_text("octaves:  {}".format(self.var['octaves']), self.width*self.tile, 200)

        self.show_text("R: {}".format(self.var['R']), self.width*self.tile, 240)
        self.show_text("G: {}".format(self.var['G']), self.width*self.tile, 260)
        self.show_text("B: {}".format(self.var['B']), self.width*self.tile, 280)
        
        self.show_text("r:  {}".format(self.var['r']), self.width*self.tile, 320)
        self.show_text("g:  {}".format(self.var['g']), self.width*self.tile, 340)
        self.show_text("b:  {}".format(self.var['b']), self.width*self.tile, 360)

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
                    self.new_img()
                    self.update_all()
                if event.key == pg.K_2:
                    self.port()
                    self.update_all()

                if event.key == pg.K_g:
                    if self.grey == False:
                        self.grey = True
                    else:
                        self.grey = False
                    self.update_all()

                if event.key == pg.K_w:
                    if self.target > 0:
                        self.target -= 1
                    self.update_all()
                if event.key == pg.K_s:
                    if self.target < len(self.targets)-1:
                        self.target += 1
                    self.update_all()

            if event.type == pg.KEYDOWN:
                if (event.mod == pg.KMOD_LSHIFT or event.mod == pg.KMOD_RSHIFT) and event.key == pg.K_a:
                    if self.var[self.targets[self.target]] > self.lmt[self.targets[self.target]][0]+5:
                        self.var[self.targets[self.target]] -= 5
                    self.new_img()
                    self.update_all()
                elif event.key == pg.K_a:
                    if self.var[self.targets[self.target]] > self.lmt[self.targets[self.target]][0]:
                        self.var[self.targets[self.target]] -= 1
                    self.new_img()
                    self.update_all()
                if (event.mod == pg.KMOD_LSHIFT or event.mod == pg.KMOD_RSHIFT) and event.key == pg.K_d:
                    if self.lmt[self.targets[self.target]][1] != 0:
                        if self.var[self.targets[self.target]] < self.lmt[self.targets[self.target]][1]-5:
                            self.var[self.targets[self.target]] += 5
                    else:
                        self.var[self.targets[self.target]] += 5
                    self.new_img()
                    self.update_all()
                elif event.key == pg.K_d:
                    if self.lmt[self.targets[self.target]][1] != 0:
                        if self.var[self.targets[self.target]] < self.lmt[self.targets[self.target]][1]:
                            self.var[self.targets[self.target]] += 1
                    else:
                        self.var[self.targets[self.target]] += 1
                    self.new_img()
                    self.update_all()

                if event.key == pg.K_UP:
                    self.img.scroll(0, -1)
                    self.update_all()
                if event.key == pg.K_DOWN:
                    self.img.scroll(0, 1)
                    self.update_all()

                if event.key == pg.K_LEFT:
                    self.img.scroll(-1, 0)
                    self.update_all()
                if event.key == pg.K_RIGHT:
                    self.img.scroll(1, 0)
                    self.update_all()

    def run(self):
        while self.running:
            self.update()

    def make_matrix(self):
        matrix = self.fill_solid((self.var['R'], self.var['G'], self.var['B']))
        self.matrix = self.procedures[self.var['procedure']](matrix)

    def make_img(self):
        for x in range(self.width):
            for y in range(self.height):
                v = int((y * self.width) + x)
                try:
                    self.img.set_at((x, y), self.matrix[v])
                except IndexError:
                    pass

    def new_img(self):
        self.make_matrix()
        self.make_img()

    def show_img(self):
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

    def blend_subtract(self, col1, col2):
        if not self.grey:
            r = max(min(255, (col1[0]-col2[0])), 0)
            g = max(min(255, (col1[1]-col2[1])), 0)
            b = max(min(255, (col1[2]-col2[2])), 0)
            color = (r, g, b)
        else:
            c = max(min(255, (((col1[0]+col1[1]+col1[2])/3)-((col2[0]+col2[1]+col2[2])/3))), 0)
            color = (c, c, c)
        return color

    def blend_add(self, col1, col2):
        if not self.grey:
            r = max(min(255, (col1[0]+col2[0])), 0)
            g = max(min(255, (col1[1]+col2[1])), 0)
            b = max(min(255, (col1[2]+col2[2])), 0)
            color = (r, g, b)
        else:
            c = max(min(255, (((col1[0]+col1[1]+col1[2])/3)+((col2[0]+col2[1]+col2[2])/3))), 0)
            color = (c, c, c)
        return color

    def blend_combine(self, col1, col2):
        if not self.grey:
            r = max(min(255, ((col1[0]+col2[0])/2)), 0)
            g = max(min(255, ((col1[1]+col2[1])/2)), 0)
            b = max(min(255, ((col1[2]+col2[2])/2)), 0)
            color = (r, g, b)
        else:
            c = max(min(255, ((((col1[0]+col1[1]+col1[2])/3)+((col2[0]+col2[1]+col2[2])/3))/2)), 0)
            color = (c, c, c)
        return color

    def RGB(self, scale):
        if not self.grey:
            R = randint(-int(self.var['r']/scale), 0)
            G = randint(-int(self.var['g']/scale), 0)
            B = randint(-int(self.var['b']/scale), 0)
        else:
            g = randint(-int(((self.var['r']+self.var['g']+self.var['b'])/3)/scale), 0)
            R, G, B = g, g, g
        return R, G, B

    def over_circle(self, m, scale=1, pack=1):
        matrix = m
        try:
            size = int(randint(int(self.width/8), int(self.width/4))*scale)
            X = randint(int(size/2), int(size*pack))
            Y = randint(int(size/2), int(size*pack))
            w = int(size/2)
            h = int(size/2)
            cx = X + (int(size/2))
            cy = Y + int(size/2)
            v1 = (Y * self.width) + X
            for x in range(int(X), int((X)+size)):
                for y in range(int(Y), int((Y)+size)):
                    v = v1 + (y * int(self.width) + x)
                    try:
                        if abs( (((x-cx)**2) / w**2) + (((y-cy)**2) / h**2) ) <= 1:
                            try:
                                R, G, B = self.RGB(1)
                                matrix[v] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
                            except IndexError:
                                pass#print('index error')
                    except ZeroDivisionError:
                        pass#print('division error')
                d -= 1
        except:
            pass
        return matrix

    def over_oval(self, m, scale=1, pack=1):
        matrix = m
        try:
            size = int(randint(int(self.width/8), int(self.width/4))*scale)
            X = randint(int(size/2), int(size*pack))
            Y = randint(int(size/2), int(size*pack))
            w = int(size/8)
            h = int(size/4)
            cx = X + int(w/2)
            cy = Y + int(h/2)
            v1 = (Y * self.width) + X
            for x in range(int(X), int((X)+(w*2))):
                for y in range(int(Y), int((Y)+(h*2))):
                    v = v1 + (y * int(self.width) + x)
                    try:
                        if abs( (((x-cx)**2) / w**2) + (((y-cy)**2) / h**2) ) <= 1:
                            try:
                                R, G, B = self.RGB(depth)
                                matrix[v] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
                            except IndexError:
                                pass#print('index error')
                    except ZeroDivisionError:
                        pass#print('division error')
        except:
            pass
        return matrix

    def proc_random(self, m):
        self.img_name = "random"
        matrix = m
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(1)
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_circle(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)
        return matrix

    def proc_noise(self, m):
        self.img_name = "noise"
        matrix = []
        for y in range(self.height):
            for x in range(self.height):
                R, G, B = self.RGB(1)
                chance = randint(0, 100)
                if chance < self.var['grain']:
                    R, G, B = self.RGB(2)
                matrix.append(self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B)))
        for i in range(self.var['octaves']):
            for y in range(self.height):
                for x in range(self.width):
                    valr = []
                    valg = []
                    valb = []
                    for ny in range(-1, 1):
                        for nx in range(-1, 1):
                            try:
                                index = (y * self.width + x) + (ny * self.width + nx)
                                vr = matrix[index][0]
                                vg = matrix[index][1]
                                vb = matrix[index][2]
                                valr.append(vr)
                                valg.append(vg)
                                valb.append(vb)
                            except:
                                pass
                    r = int(sum(valr)/len(valr))
                    g = int(sum(valg)/len(valg))
                    b = int(sum(valb)/len(valb))
                    matrix[y * self.width + x] = (r, g, b)
        return matrix

    def proc_fuzz(self, m):
        self.img_name = "fuzz"
        matrix = m
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(1)
                chance = randint(0, 100)
                if chance < self.var['grain']:
                    R, G, B = self.RGB(4)
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_circle(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)
        return matrix

    def proc_cloth(self, m):
        self.img_name = "cloth"
        matrix = m
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(1)
                chance = randint(0, 100)
                if chance < self.var['grain']:
                    R, G, B = self.RGB(8)
                if y % 2 == 0 and count % 2 == 0:
                    R, G, B = self.RGB(4)
                count += 1
                if count > self.var['stagger']:
                    count = 0
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_circle(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)
        return matrix

    def proc_skin(self, m):
        self.img_name = "skin"
        matrix = m
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(8)
                chance = randint(0, 100)
                if chance < self.var['grain']:
                    R, G, B = self.RGB(1)
                if y % 2 == 0 and count % 2 == 0:
                    R, G, B = self.RGB(4)
                count += 1
                if count > self.var['stagger']:
                    count = 0
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_circle(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)
        return matrix

    def proc_wood(self, m):
        self.img_name = "wood"
        matrix = m
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(8)
                if x % int(self.width/8) == 0:
                    count += 1
                if x % 2 == 0 and count % 2 == 0:
                    R, G, B = self.RGB(4)
                    chance = randint(0, 100)
                    if chance < self.var['grain']:
                        R, G, B = self.RGB(3)
                if x % 2 == 0 and count % 2 == 1:
                    R, G, B = self.RGB(2)
                    chance = randint(0, 100)
                    if chance < self.var['grain']:
                        R, G, B = self.RGB(3)
                if count > self.var['stagger']:
                    count = 0
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_oval(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)

        return matrix

    def proc_brick(self, m):
        self.img_name = "brick"
        matrix = m
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(16)
                if y % 2 == 0:
                    chance = randint(0, 100)
                    if chance < self.var['grain']:
                        R, G, B = self.RGB(4)
                if y % 2 == 1:
                    chance = randint(0, 100)
                    if chance < self.var['grain']:
                        R, G, B = self.RGB(8)
                if y % int(self.height / 8) == 0:
                    count += 1
                    R, G, B = self.RGB(1)
                if x % int(self.width / 4) == 0 and count % 2 == 0:
                    R, G, B = self.RGB(1)
                if x % int(self.width / 4) == int(self.width / 8) and count % 2 == 1:
                    R, G, B = self.RGB(1)
                if count > self.var['stagger']:
                    count = 0
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_circle(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)
        return matrix

    def proc_plank(self, m):
        self.img_name = "plank"
        matrix = m
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                index = (y * self.width) + x
                R, G, B = self.RGB(16)
                if x % int(self.width / int(self.width / 2)) == 0:
                    chance = randint(0, 100)
                    if chance < self.var['grain']:
                        R, G, B = self.RGB(4)
                if x % int(self.width / 8) == 0:
                    count += 1
                    R, G, B = self.RGB(1)
                if y % int(self.height / 2) == 0 and count % 2 == 0:
                    R, G, B = self.RGB(1)
                if y % int(self.height / 2) == int(self.height / 4) and count % 2 == 1:
                    R, G, B = self.RGB(1)
                if count > self.var['stagger']:
                    count = 0
                matrix[index] = self.blends[self.var['blend']]((self.var['R'], self.var['G'], self.var['B']), (R, G, B))
        for dense in range(randint(0, self.var['density'])):
            matrix = self.over_circle(matrix, scale=self.var['scale']*.1, pack=self.var['pack']*.1)
        return matrix

TG = TextureGenerator(64, 64, 10, [255, 255, 255], [255, 255, 255])
TG.start()
