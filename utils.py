import random

colors = [
    'aqua',
    'aquamarine',
    'black',
    'blue',
    'blueviolet',
    'brown',
    'burlywood',
    'cadetblue',
    'chartreuse',
    'chocolate',
    'coral',
    'cornflowerblue',
    'crimson',
    'cyan',
    'darkblue',
    'darkcyan',
    'darkgoldenrod',
    'darkgray',
    'darkgreen',
    'darkkhaki',
    'darkmagenta',
    'darkolivegreen',
    'darkorange',
    'darkorchid',
    'darkred',
    'darksalmon',
    'darkseagreen',
    'darkslateblue',
    'darkslategray',
    'darkturquoise',
    'darkviolet',
    'deeppink',
    'deepskyblue',
    'dimgray',
    'dimgrey',
    'dodgerblue',
    'firebrick',
    'forestgreen',
    'fuchsia',
    'gold',
    'goldenrod',
    'gray',
    'grey',
    'green',
    'greenyellow',
    'hotpink',
    'indianred',
    'indigo',
    'khaki',
    'lawngreen',
    'lemonchiffon',
    'lightblue',
    'lightcoral',
    'lightgray',
    'lightgreen',
    'lightpink',
    'lightsalmon',
    'lightseagreen',
    'lightskyblue',
    'lightslategray',
    'lightsteelblue',
    'lime',
    'limegreen',
    'magenta',
    'maroon',
    'mediumaquamarine',
    'mediumblue',
    'mediumorchid',
    'mediumpurple',
    'mediumseagreen',
    'mediumslateblue',
    'mediumspringgreen',
    'mediumturquoise',
    'mediumvioletred',
    'midnightblue',
    'moccasin',
    'navy',
    'olive',
    'olivedrab',
    'orange',
    'orangered',
    'orchid',
    'palegoldenrod',
    'palegreen',
    'paleturquoise',
    'palevioletred',
    'papayawhip',
    'peachpuff',
    'peru',
    'pink',
    'plum',
    'purple',
    'red',
    'rosybrown',
    'royalblue',
    'rebeccapurple',
    'saddlebrown',
    'salmon',
    'sandybrown',
    'seagreen',
    'sienna',
    'silver',
    'skyblue',
    'slateblue',
    'slategray',
    'slategrey',
    'springgreen',
    'steelblue',
    'tan',
    'teal',
    'thistle',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'yellow',
    'yellowgreen'
]

def random_palette(k):
    return random.choices(colors,k=k)

def last_name_and_initials(name):
    parts = name.split(' ')
    if len(parts) > 1:
        lname = parts[-1]
        initials = '. '.join([x[0] for x in parts[:-1] ])
        result = f'{lname}, {initials}.'
        return result
    else: return name

def get_numerical_label_values(strobj):
    vals = []
    parts = str(strobj).split('#')
    for i in range(1, len(parts), 2):
        vals.append(parts[i])
    return vals

def is_not_a_node(data):
    str_data = str(data)
    if 'depth' not in str_data: return True # Edge / Link
    elif 'playernode' in str_data: return True # Player Node (not match)
    else: return False # match