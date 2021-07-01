import proc

from random import randint
from glob import *

def over_circle(m):
    matrix = m
    size = randint(0, int(var['scale']['var']*.1))
    X = randint(0, int(var['pack']['var']*.1))
    Y = randint(0, int(var['pack']['var']*.1))
    w = int(size/2)
    h = int(size/2)
    cx = X + (int(size/2))
    cy = Y + int(size/2)
    v1 = (Y * var['width']['var']) + X
    for x in range(int(X), int((X)+size)):
        for y in range(int(Y), int((Y)+size)):
            v = v1 + (y * var['width']['var'] + x)
            try:
                if abs( (((x-cx)**2) / w**2) + (((y-cy)**2) / h**2) ) <= 1:
                    try:
                        R, G, B = proc.RGB(var['overlay']['var'])
                        matrix[v] = data['blnd'][var['blend']['var']]((var['R']['var'], var['G']['var'], var['B']['var']), (R, G, B))
                    except IndexError:
                        pass#print('index error')
            except ZeroDivisionError:
                pass#print('division error')
    return matrix

def over_blur(m):
    matrix = m
    blurred = []
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            valr = []
            valg = []
            valb = []
            for ny in range(-var['range']['var'], var['range']['var']):
                for nx in range(-var['range']['var'], var['range']['var']):
                    try:
                        index = (y * var['width']['var'] + x) + (ny * var['width']['var'] + nx)
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
            blurred.append((r, g, b))
    return blurred

def over_smear(m):
    matrix = m
    for y in range(var['height']['var']):
        for x in range(var['width']['var']):
            valr = []
            valg = []
            valb = []
            for ny in range(-var['range']['var'], var['range']['var']):
                for nx in range(-var['range']['var'], var['range']['var']):
                    try:
                        index = (y * var['width']['var'] + x) + (ny * var['width']['var'] + nx) 
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
            matrix[y * var['width']['var'] + x] = (r, g, b)
    return matrix

def overlay_img(matrix):
    if var['post']['var']:
        for dense in range(var['amount']['var']):
            matrix = over_circle(matrix)
        if var['swap']['var']:
            for i in range(var['smear']['var']):
                matrix = over_smear(matrix)
            for i in range(var['blur']['var']):
                matrix = over_blur(matrix)
        else:
            for i in range(var['blur']['var']):
                matrix = over_blur(matrix)
            for i in range(var['smear']['var']):
                matrix = over_smear(matrix)
    return matrix
