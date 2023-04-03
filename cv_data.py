CONTROL_CURVES = {
    'four_arrow': 'curve -d 1 -p -1 0 -1 -p -1 0 -3 -p -2 0 -3 -p 0 0 -5 -p 2 0 -3 -p 1 0 -3 -p 1 0 -1 -p 3 0 -1 -p 3 0'
                  '-2 -p 5 0 0 -p 3 0 2 -p 3 0 1 -p 1 0 1 -p 1 0 3 -p 2 0 3 -p 0 0 5 -p -2 0 3 -p -1 0 3 -p -1 0 1 '
                  '-p -3 0 1 -p -3 0 2 -p -5 0 0 -p -3 0 -2 -p -3 0 -1 -p -1 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 '
                  '-k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k '
                  '23 -k 24 ;',
    'two_arrow': '',
    'circle': 'circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1; objectMoveCommand;',
    'square': 'curve -d 1 -p 2 0 -2 -p -2 0 -2 -p -2 0 2 -p 2 0 2 -p 2 0 -2 -k 0 -k 1 -k 2 -k 3 -k 4 ;',
    'cube_square': 'curve -d 1 -p 2 0 -2 -p -2 0 -2 -p -2 0 2 -p 2 0 2 -p 2 0 -2 -k 0 -k 1 -k 2 -k 3 -k 4 ;',
    'cube_line': 'curve -d 1 -p 0 2 0 -p 0 -2 0 -k 0 -k 1;',
    'cube': 'polyCube -w 1 -h 1 -d 1 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1;',
}

CUBE_CURVES_DATA = {
    'front_left_line': [2, 2, 2],
    'front_right_line': [-2, 2, 2],
    'back_left_line': [2, 2, -2],
    'back_right_line': [-2, 2, -2]
}
