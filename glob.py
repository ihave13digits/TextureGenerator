var = {
        'img' : {'var' : 0, 'lmt' : [0, 0]},
        # Functions
        'procedure' : {'var' : 0, 'lmt' : [0, 0]},
        'blend' : {'var' : 0, 'lmt' : [0, 0]},
        # Variables
        'seed' : {'var' : 0, 'lmt' : [0, 0]},
        'grain' : {'var' : 0, 'lmt' : [0, 100]},
        'scale' : {'var' : 1, 'lmt' : [1, 0]},
        # Variables
        'pack' : {'var' : 1, 'lmt' : [1, 0]},
        'amount' : {'var' : 0, 'lmt' : [0, 0]},
        'count' : {'var' : 1, 'lmt' : [1, 0]},
        # Variables
        'align' : {'var' : 0, 'lmt' : [0, 0]},
        'stagger' : {'var' : 2, 'lmt' : [2, 0]},
        'density' : {'var' : 1, 'lmt' : [1, 0]},
        # Noise
        'range' : {'var' : 1, 'lmt' : [1, 8]},
        'octaves' : {'var' : 0, 'lmt' : [0, 8]},
        'blur' : {'var' : 0, 'lmt' : [0, 8]},
        'smear' : {'var' : 0, 'lmt' : [0, 8]},
        # Levels
        'line' : {'var' : 8, 'lmt' : [1, 0]},
        'overlay' : {'var' : 4, 'lmt' : [1, 0]},
        'texture' : {'var' : 2, 'lmt' : [1, 0]},
        'strength' : {'var' : 25, 'lmt' : [1, 0]},
        'minimum' : {'var' : 0, 'lmt' : [0, 0]},
        # Colors
        'R' : {'var' : 255, 'lmt' : [0, 255]},
        'G' : {'var' : 255, 'lmt' : [0, 255]},
        'B' : {'var' : 255, 'lmt' : [0, 255]},
        'r' : {'var' : 128, 'lmt' : [0, 255]},
        'g' : {'var' : 128, 'lmt' : [0, 255]},
        'b' : {'var' : 128, 'lmt' : [0, 255]},
        # Dimensions
        'x' : {'var' : 0, 'lmt' : [0, 0]},
        'y' : {'var' : 0, 'lmt' : [0, 0]},
        'W' : {'var' : 1, 'lmt' : [1, 0]},
        'H' : {'var' : 1, 'lmt' : [1, 0]},
        'width' : {'var' : 64, 'lmt' : [1, 0]},
        'height' : {'var' : 64, 'lmt' : [1, 0]},
        'tile' : {'var' : 8, 'lmt' : [1, 32]},
        'font' : {'var' : 11, 'lmt' : [8, 16]},
        'list' : {'var' : 2, 'lmt' : [0, 16]},
        # Triggers
        'auto' : {'var' : True, 'lmt' : [0, 1]},
        'grey' : {'var' : True, 'lmt' : [0, 1]},
        'mode' : {'var' : True, 'lmt' : [0, 1]},
        'solid' : {'var' : True, 'lmt' : [0, 1]},
        'running' : {'var' : True, 'lmt' : [0, 1]},
        }

data = {
        'target' : 0,
        'img_name' : 'random',

        'saved_imgs' : {'random':0, 'fuzz':0, 'noise':0, 'noisy':0, 'perlin':0, 'gradient':0, 'cloth':0, 'skin':0, 'wood':0, 'brick':0, 'plank':0, 'atlas':0},

        'proc' : [],
        'blnd' : [],
        'trgt' : [],

        'imgs' : [],
        'matrix' : []
    }
