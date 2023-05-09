from random import randint
from random import uniform

"""
https://help.instagram.com/155833707900388

Information we obtain from these devices includes:

Device operations: information about operations and behaviors performed on the device, such as whether a window is 
foregrounded or backgrounded, or mouse movements (which can help distinguish humans from bots).
"""


def curve_from_straight(start_x=0, start_y=0, end_x=0, end_y=0):
    x_coordinates_path = []
    if end_x > start_x:
        for i in range(start_x, end_x + 1):
            x_coordinates_path.append(i)
    else:
        for i in range(end_x, start_x + 1):
            x_coordinates_path.append(i)
    if end_x - start_x < 0:
        x_coordinates_path.reverse()
    final_x_path = []
    first_modified = False
    first_coordinate = 0
    count = 0
    do_in_length = round(len(x_coordinates_path) * 0.8)
    for i in x_coordinates_path:
        if first_modified:
            if first_coordinate > i:
                i = randint(i, first_coordinate)
                final_x_path.append(i)
            elif first_coordinate < i:
                i = randint(first_coordinate, i)
                final_x_path.append(i)
            else:
                first_modified = False
                final_x_path.append(i)
        else:
            if 0.1 > uniform(0, 1) and count < do_in_length:
                i = round(i * uniform(0.95, 1.05))
                first_modified = True
                final_x_path.append(i)
            else:
                final_x_path.append(i)
        first_coordinate = i

    y_coordinates_path = []
    if end_y > start_y:
        for i in range(start_y, end_y + 1):
            y_coordinates_path.append(i)
    else:
        for i in range(end_y, start_y + 1):
            y_coordinates_path.append(i)
    if end_y - start_y < 0:
        y_coordinates_path.reverse()

    equalized_y_path = []
    proportion = round(len(x_coordinates_path) / len(y_coordinates_path))
    for y in y_coordinates_path:
        count = 0
        while count < proportion:
            equalized_y_path.append(y)
            count += 1

    count = 0
    if len(equalized_y_path) > len(x_coordinates_path):
        while len(equalized_y_path) < len(x_coordinates_path):
            del equalized_y_path[randint(0, len(equalized_y_path))]
            count += 1
    elif len(equalized_y_path) < len(x_coordinates_path):
        last_value = equalized_y_path[-1]
        while len(x_coordinates_path) > len(equalized_y_path):
            equalized_y_path.append(last_value)
            count += 1
    print('lengths', len(equalized_y_path), len(x_coordinates_path))

    final_y_path = []
    first_modified = False
    first_coordinate = 0
    count = 0
    do_in_length = round(len(y_coordinates_path) * 0.8)
    for i in y_coordinates_path:
        if first_modified:
            if first_coordinate > i:
                i = randint(i, first_coordinate)
                final_y_path.append(i)
            elif first_coordinate < i:
                i = randint(first_coordinate, i)
                final_y_path.append(i)
            else:
                first_modified = False
                final_y_path.append(i)
        else:
            if 0.2 > uniform(0, 1) and count < do_in_length:
                i = round(i * uniform(0.96, 1.04))
                final_y_path.append(i)
            else:
                final_y_path.append(i)
        first_coordinate = i

    return list(zip(final_x_path, final_y_path))
