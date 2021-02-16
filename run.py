#!/usr/bin/python3

import json
import pygame as pg
from os import path
from sys import argv
from random import seed, randint

from glob import *
from proc import proc_random, proc_noise, proc_noisy, proc_fuzz, proc_perlin, proc_gradient, proc_cloth, proc_skin, proc_wood, proc_brick, proc_plank
from blend import blend_subtract, blend_add, blend_combine

pg.init()
screen = None
clock = pg.time.Clock()

def init_session():
    if (len(argv) == 10):
        var['width']['var'] = int(argv[1])
        var['height']['var'] = int(argv[2])
        var['tile']['var'] = int(argv[3])

        var['R']['var'] = int(argv[4])
        var['G']['var'] = int(argv[5])
        var['B']['var'] = int(argv[6])

        var['r']['var'] = int(argv[7])
        var['g']['var'] = int(argv[8])
        var['b']['var'] = int(argv[9])
    elif (len(argv) == 4):
        var['width']['var'] = int(argv[1])
        var['height']['var'] = int(argv[2])
        var['tile']['var'] = int(argv[3])

        var['R']['var'] = 255
        var['G']['var'] = 255
        var['B']['var'] = 255

        var['r']['var'] = 125
        var['g']['var'] = 125
        var['b']['var'] = 125

def start():
    global screen
    pg.font.init()
    pg.display.set_caption("TextureGenerator")
    pg.key.set_repeat(50, 100)

    init_session()
    load()
    screen = pg.display.set_mode((var['width']['var']*var['tile']['var']+128, var['height']['var']*var['tile']['var']), pg.RESIZABLE)
    try:
        from os import mkdir
        mkdir(path.join(__file__, 'img'))
    except:
        pass

    for key in var:
        data['trgt'].append(key)
    data['proc'] = [proc_random, proc_fuzz, proc_noise, proc_noisy, proc_perlin, proc_gradient, proc_cloth, proc_skin, proc_wood, proc_brick, proc_plank]
    data['blnd'] = [blend_subtract, blend_add, blend_combine]
    var['procedure']['lmt'][1] = len(data['proc'])-1
    var['blend']['lmt'][1] = len(data['blnd'])-1
    data['matrix'] = make_matrix()
    if var['auto']['var']:
        new_img()
    update_all()
    run()

def run():
    while var['running']['var']:
        dt = clock.tick(10)/1000
        update()
    save()

def save():
    img_dir = path.join(path.dirname(__file__), 'img')
    with open(path.join(img_dir, 'data.json'), 'w') as f:
        json.dump(data['saved_imgs'], f)
        f.close()

def load():
    img_dir = path.join(path.dirname(__file__), 'img')
    try:
        with open(path.join(img_dir, 'data.json'), 'r') as f:
            data['saved_imgs'] = json.load(f)
            f.close()
    except FileNotFoundError:
        pass

def port():
    img_dir = path.join(path.dirname(__file__), 'img')
    if var['W']['var'] == 1 and var['H']['var'] == 1:
        filename = "{}_{}-{}x{}.png".format(data['img_name'], data['saved_imgs'][data['img_name']], var['width']['var'], var['height']['var'])
        pg.image.save(data['imgs'][var['img']['var']], path.join(img_dir, filename))
        data['saved_imgs'][data['img_name']] += 1
    else:
        filename = "atlas_{}-{}x{}.png".format(data['saved_imgs']['atlas'], var['width']['var']*var['W']['var'], var['height']['var']*var['H']['var'])
        atlas = pg.Surface((var['width']['var']*var['W']['var'], var['height']['var']*var['H']['var']))
        
        for y in range(var['H']['var']):
            for x in range(var['W']['var']):
                index = y * var['W']['var'] + x
                atlas.blit(data['imgs'][index], (x*var['width']['var'], y*var['height']['var']))
        pg.image.save(atlas, path.join(img_dir, filename))
        data['saved_imgs']['atlas'] += 1

def update_atlas():
    expected = var['W']['var']*var['H']['var']
    var['img']['lmt'][1] = expected-1
    if len(data['imgs']) > expected:
        while len(data['imgs']) > expected:
            data['imgs'].pop(len(data['imgs'])-1)
        var['img']['var'] = expected-1
    elif len(data['imgs']) < expected:
        while len(data['imgs']) < expected:
            data['imgs'].append(pg.Surface((var['width']['var'], var['height']['var'])))

def update_info():
    begin = data['target']-var['list']['var']
    end = data['target']+var['list']['var']
    for i, key in enumerate(data['saved_imgs']):
        if i == var['procedure']['var']:
            img_name = key
    line = 0
    for i, key in enumerate(var):
        if i >= begin and i <= end:
            line += 1*var['font']['var']
            color = (128, 128, 128)
            if key == data['trgt'][data['target']]:
                color = (255, 255, 255)
            if key != 'procedure':
                show_text("{}: {}".format(key, var[key]['var']), var['W']['var']*var['width']['var']*var['tile']['var'], line, color=color)
            else:
                show_text("{}: {}".format(key, data['img_name']), var['W']['var']*var['width']['var']*var['tile']['var'], line, color=color)

def update_all():
    seed(var['seed']['var'])
    size = pg.display.get_surface().get_size()
    pg.draw.rect(
            screen,
            (0, 0, 0),
            (var['W']['var']*var['width']['var']*var['tile']['var'],
            0,
            size[0]-(var['W']['var']*var['width']['var']*var['tile']['var']),
            size[1]))#-(var['W']['var']*var['height']['var']*var['tile']['var'])))
    update_atlas()
    show_img()
    update_info()

def update():
    for event in pg.event.get():
        # Window Input
        if event.type == pg.QUIT:
            var['running']['var'] = False

        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                var['running']['var'] = False

            if event.key == pg.K_1:
                new_img()
                update_all()
            if event.key == pg.K_2:
                port()
                update_all()
            if event.key == pg.K_0:
                var[data['trgt'][data['target']]]['var'] = var[data['trgt'][data['target']]]['lmt'][0]
                update_all()

            if event.key == pg.K_g:
                if var['grey']['var'] == False:
                    var['grey']['var'] = True
                else:
                    var['grey']['var'] = False
                update_all()
            if event.key == pg.K_m:
                if var['mode']['var'] == False:
                    var['mode']['var'] = True
                else:
                    var['mode']['var'] = False
                update_all()
            if event.key == pg.K_p:
                if var['auto']['var'] == False:
                    var['auto']['var'] = True
                else:
                    var['auto']['var'] = False
                update_all()
            if event.key == pg.K_r:
                var['seed']['var'] = randint(0, 99999999)
                new_img()
                update_all()

            if event.key == pg.K_w:
                if data['target'] > 0:
                    data['target'] -= 1
                    update_all()
            if event.key == pg.K_s:
                if data['target'] < len(data['trgt'])-1:
                    data['target'] += 1
                    update_all()

        if event.type == pg.KEYDOWN:
            if (event.mod == pg.KMOD_LSHIFT or event.mod == pg.KMOD_RSHIFT) and event.key == pg.K_a:
                if var[data['trgt'][data['target']]]['var'] > var[data['trgt'][data['target']]]['lmt'][0]+5:
                    var[data['trgt'][data['target']]]['var'] -= 5
                if var['auto']['var']:
                    new_img()
                update_all()
            elif event.key == pg.K_a:
                if var[data['trgt'][data['target']]]['var'] > var[data['trgt'][data['target']]]['lmt'][0]:
                    var[data['trgt'][data['target']]]['var'] -= 1
                if var['auto']['var']:
                    new_img()
                update_all()
            if (event.mod == pg.KMOD_LSHIFT or event.mod == pg.KMOD_RSHIFT) and event.key == pg.K_d:
                if var[data['trgt'][data['target']]]['lmt'][1] != 0:
                    if var[data['trgt'][data['target']]]['var'] < var[data['trgt'][data['target']]]['lmt'][1]-5:
                        var[data['trgt'][data['target']]]['var'] += 5
                else:
                    var[data['trgt'][data['target']]]['var'] += 5
                if var['auto']['var']:
                    new_img()
                update_all()
            elif event.key == pg.K_d:
                if var[data['trgt'][data['target']]]['lmt'][1] != 0:
                    if var[data['trgt'][data['target']]]['var'] < var[data['trgt'][data['target']]]['lmt'][1]:
                        var[data['trgt'][data['target']]]['var'] += 1
                else:
                    var[data['trgt'][data['target']]]['var'] += 1
                if var['auto']['var']:
                    new_img()
                update_all()

            #if event.key == pg.K_UP:
            #    var['y']['var'] -= 1
            #    if var['auto']['var']:
            #        new_img()
            #if event.key == pg.K_DOWN:
            #    var['y']['var'] += 1
            #    if var['auto']['var']:
            #        new_img()

            #if event.key == pg.K_LEFT:
            #    var['x']['var'] -= 1
            #    if var['auto']['var']:
            #        new_img()
            #if event.key == pg.K_RIGHT:
            #    var['x']['var'] += 1
            #    if var['auto']['var']:
            #        new_img()

def make_matrix():
    data['matrix'] = fill_solid((var['R']['var'], var['G']['var'], var['B']['var']))
    data['matrix'] = data['proc'][var['procedure']['var']](data['matrix'])

def make_img():
    img = pg.Surface((var['width']['var'], var['height']['var']))
    try:
        data['imgs'][var['img']['var']] = img
    except IndexError:
        data['imgs'].append(img)
    for x in range(var['width']['var']):
        for y in range(var['height']['var']):
            v = int((y * var['width']['var']) + x)
            try:
                data['imgs'][var['img']['var']].set_at((x, y), data['matrix'][v])
            except IndexError:
                print('failed')

def new_img():
    make_matrix()
    make_img()

def show_img():
    for y in range(var['H']['var']):
        for x in range(var['W']['var']):
            img = pg.transform.scale(data['imgs'][y*var['W']['var']+x], (var['width']['var']*var['tile']['var'], var['height']['var']*var['tile']['var']))
            rect = img.get_rect()
            rect.move_ip(x*(var['tile']['var']*var['width']['var']), y*(var['tile']['var']*var['height']['var']))
            screen.blit(img, rect)
    pg.display.update()

def show_text(txt, x, y, color=(128, 128, 128), a=True):
    font = pg.font.Font(pg.font.get_default_font(), var['font']['var'])
    text = font.render(txt, a, color)
    screen.blit(text, (x, y))
    pg.display.update()

def fill_solid(color):
    matrix = []
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            matrix.append(color)
    return matrix

start()
