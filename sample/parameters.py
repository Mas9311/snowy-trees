import sys


def retrieve():
    aspect = 'w'
    speed = 'c'
    density = 'c'
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'tall' or sys.argv[1] == 'portrait':
            aspect = 't'
        elif sys.argv[1] == 'wide' or sys.argv[1] == 'landscape':
            aspect = 'w'
        else:
            print(f'{sys.argv[1]} is not recognized as a monitor aspect.')
    if len(sys.argv) >= 3:
        if sys.argv[2] in ['ultra', 'super']:
            speed = 'u'
        if sys.argv[2] == 'fast' or sys.argv[2] == 'quick':
            speed = 'a'
        elif sys.argv[2] == 'average' or sys.argv[2] == 'medium' or sys.argv[2] == 'moderate':
            speed = 'b'
        elif sys.argv[2] == 'slow':
            speed = 'c'
        else:
            print(f'{sys.argv[2]} is not recognized as a snow speed.')
    if len(sys.argv) >= 4:
        if sys.argv[3] == 'heavy' or sys.argv[3] == 'thick' or sys.argv[3] == 'blizzard':
            density = 'a'
        elif sys.argv[3] == 'moderate' or sys.argv[3] == 'medium' or sys.argv[3] == 'average':
            density = 'b'
        elif sys.argv[3] == 'light' or sys.argv[3] == 'thin':
            density = 'c'
        else:
            print(f'{sys.argv[3]} is not recognized as a snow density.')
    if len(sys.argv) >= 5:
        if sys.argv[4] != "none":
            return aspect, speed, density, True
    return aspect, speed, density, False
