from random import randint

import noise

from glob import *
from over import overlay_img

def RGB(scale):
    r = int(var['r']['var']*((scale*.1)*(var['strength']['var']*.1)))
    g = int(var['g']['var']*((scale*.1)*(var['strength']['var']*.1)))
    b = int(var['b']['var']*((scale*.1)*(var['strength']['var']*.1)))
    ls = [r, g, b]
    mn = var['minimum']['var']
    mx = min(ls)
    if mn > mx:
        mn = mx
        var['minimum']['var'] = mx
    if not var['grey']['var']:
        if var['solid']['var']:
            R = randint(mn, r)
            G = randint(mn, g)
            B = randint(mn, b)
        else:
            R = int(r)
            G = int(g)
            B = int(b)
    else:
        if var['solid']['var']:
            g = randint(mn, int((sum((var['r']['var'],var['g']['var'],var['b']['var']))/3)*((scale*.1)*(var['strength']['var']*.1))))
        else:
            g = int((sum((var['r']['var'],var['g']['var'],var['b']['var']))/3)*((scale*.1)*(var['strength']['var']*.1)))
        R, G, B = g, g, g
    return R, G, B

def proc_random(m):
    data['img_name'] = "random"
    matrix = m
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_fuzz(m):
    data['img_name'] = "fuzz"
    matrix = m
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_noise(m):
    data['img_name'] = "noise"
    matrix = m
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_noisy(m):
    data['img_name'] = "noisy"
    matrix = m
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            R, G, B = RGB(1)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            index = (y * var['width']['var']) + x
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))

    for y in range(int(var['height']['var']/var['count']['var'])):
        for x in range(int(var['width']['var']/var['stagger']['var'])):
            R, G, B = RGB(var['line']['var'])
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            index = ((y*var['count']['var']) * var['width']['var']) + (x*var['stagger']['var'])
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_perlin(m):
    matrix = m
    data['img_name'] = 'perlin'
    n = noise.Noise(2, octaves=var['octaves']['var'], tile=(var['pack']['var'], var['pack']['var']), unbias=True, seed=var['seed']['var'])
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            mod = n.get_plain_noise(x/(var['density']['var']*.1), y/(var['density']['var']*.1))
            R = int(var['r']['var']*(mod*(var['strength']['var']*.1)))
            G = int(var['g']['var']*(mod*(var['strength']['var']*.1)))
            B = int(var['b']['var']*(mod*(var['strength']['var']*.1)))
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_gradient(m):
    data['img_name'] = "gradient"
    matrix = m
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            i = (y/(var['density']['var']*.1))+1
            R, G, B = RGB(i)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_cloth(m):
    data['img_name'] = "cloth"
    matrix = m
    count = 0
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            if y % var['count']['var'] == 0 and count % 2 == 0:
                R, G, B = RGB(var['line']['var'])
            count += 1
            if count > var['align']['var']:
                count = 0
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_skin(m):
    data['img_name'] = "skin"
    matrix = m
    count = 0
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            chance = randint(0, 100)
            if chance < var['grain']['var']:
                R, G, B = RGB(var['texture']['var'])
            if y % var['count']['var'] == 0 and count % 2 == 0:
                R, G, B = RGB(var['line']['var'])
            count += 1
            if count > var['stagger']['var']:
                count = 0
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_wood(m):
    data['img_name'] = "wood"
    matrix = m
    count = 0
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            if x % int(var['width']['var']/var['count']['var']) == 0:
                count += 1
            if x % var['density']['var'] == 0 and count % 2 == 0:
                R, G, B = RGB(var['line']['var'])
                chance = randint(0, 100)
                if chance < var['grain']['var']:
                    R, G, B = RGB(var['texture']['var'])
            if x % var['stagger']['var'] == 0 and count % 2 == 1:
                R, G, B = RGB(var['line']['var'])
                chance = randint(0, 100)
                if chance < var['grain']['var']:
                    R, G, B = RGB(var['texture']['var'])
            if count > var['align']['var']:
                count = 0
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_brick(m):
    data['img_name'] = "brick"
    matrix = m
    count = 0
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            if y % var['density']['var'] == 0 and x % var['density']['var'] == 0:
                chance = randint(0, 100)
                if chance < var['grain']['var']:
                    R, G, B = RGB(var['texture']['var'])
            if y % int(var['height']['var']/var['count']['var']) == 0:
                count += 1
                R, G, B = RGB(var['line']['var'])
            if x % int(var['width']['var'] / var['stagger']['var']) == 0 and count % 2 == 0:
                R, G, B = RGB(var['line']['var'])
            if x % int(var['width']['var'] / var['stagger']['var']) == int(var['width']['var'] / int(var['stagger']['var']/2)) and count % 2 == 1:
                R, G, B = RGB(var['line']['var'])
            if count > var['align']['var']:
                count = 0
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix

def proc_plank(m):
    data['img_name'] = "plank"
    matrix = m
    count = 0
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            index = (y * var['width']['var']) + x
            R, G, B = RGB(1)
            if x % int(var['width']['var'] / int(var['width']['var'] / var['density']['var'])) == 0:
                chance = randint(0, 100)
                if chance < var['grain']['var']:
                    R, G, B = RGB(var['texture']['var'])
            if x % int(var['width']['var']/var['count']['var']) == 0:
                count += 1
                R, G, B = RGB(var['line']['var'])
            if y % int(var['height']['var'] / var['stagger']['var']) == 0 and count % 2 == 0:
                R, G, B = RGB(var['line']['var'])
            if y % int(var['height']['var'] / var['stagger']['var']) == int(var['height']['var'] / int(var['stagger']['var']/2)) and count % 2 == 1:
                R, G, B = RGB(var['line']['var'])
            if count > var['align']['var']:
                count = 0
            matrix[index] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
    matrix = overlay_img(matrix)
    return matrix
