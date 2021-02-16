from glob import *

def blend_subtract(col1, col2):
    if not var['grey']['var']:
        r = max(min(255, (col1[0]-col2[0])), 0)
        g = max(min(255, (col1[1]-col2[1])), 0)
        b = max(min(255, (col1[2]-col2[2])), 0)
        color = (r, g, b)
    else:
        c = max(min(255, ((sum(col1)/3)-(sum(col2)/3))), 0)
        color = (c, c, c)
    return color

def blend_add(col1, col2):
    if not var['grey']['var']:
        r = max(min(255, (col1[0]+col2[0])), 0)
        g = max(min(255, (col1[1]+col2[1])), 0)
        b = max(min(255, (col1[2]+col2[2])), 0)
        color = (r, g, b)
    else:
        c = max(min(255, ((sum(col1)/3)+(sum(col2)/3))), 0)
        color = (c, c, c)
    return color

def blend_combine(col1, col2):
    if not var['grey']['var']:
        r = max(min(255, ((col1[0]+col2[0])/2)), 0)
        g = max(min(255, ((col1[1]+col2[1])/2)), 0)
        b = max(min(255, ((col1[2]+col2[2])/2)), 0)
        color = (r, g, b)
    else:
        c = max(min(255, (((sum(col1)/3)+(sum(col2)/3))/2)), 0)
        color = (c, c, c)
    return color
