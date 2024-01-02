import time
from copy import deepcopy


def get_floors(filename):
    first, second = [], []
    with open(filename, "r") as fp:
        n, m = map(int, fp.readline().split())
        for _ in range(n):
            first.append(list(fp.readline().rstrip()))
        fp.readline()  # Skip the empty line
        for _ in range(n):
            second.append(list(fp.readline().rstrip()))
    return first, second


def find_start(floor):
    for i, row in enumerate(floor):
        if "A" in row:
            return i, row.index("A")
    return None


def go_right(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if x >= len(solved_field[floor][0]) - 3:
        return
    if solved_field[floor][y][x+1] == "." and solved_field[floor][y][x+2] in [".", "B"]:
        return [1, [floor, x+2, y], path_string + ">>"]


def go_left(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if x <= 2:
        return
    if solved_field[floor][y][x-1] == "." and solved_field[floor][y][x-2] in [".", "B"]:
        return [1, [floor, x-2, y], path_string + "<<"]


def go_down(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if y >= len(solved_field[floor]):
        return
    if solved_field[floor][y+1][x] == "." and solved_field[floor][y+2][x] in [".", "B"]:
        return [1, [floor, x, y+2], path_string + "vv"]


def go_up(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if y <= 2:
        return
    if solved_field[floor][y-1][x] == "." and solved_field[floor][y-2][x] in [".", "B"]:
        return [1, [floor, x, y-2], path_string + "^^"]


def go_other_floor(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if solved_field[not (floor and 1)][y][x] in [".", "B"]:
        return [3, [int(not (floor and 1)), x, y], path_string + "!"]


def find_next_moves(path, solved_field):
    new_paths = []
    directions = [go_right, go_left, go_up, go_down, go_other_floor]
    for direction in directions:
        result = direction(path, solved_field)
        new_paths.append(result) if result else None
    return new_paths


def path_available(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if solved_field[floor][y][x] == "." or solved_field[floor][y][x] == "A":
        return True
    return False


def final_path(path, solved_field):
    seconds, coordinates, path_string = path
    floor, x, y = coordinates
    if solved_field[floor][y][x] == "B":
        return True
    return False


def find_path(solved_field):
    start = find_start(first_floor)
    seconds = 0
    paths = find_next_moves([1, [0, start[1], start[0]], ""], solved_field)
    while True:
        seconds += 1
        next_moves = []
        for path in reversed(paths):
            if final_path(path, solved_field):
                return seconds + path[0] - 1, path
            if not path_available(path, solved_field):
                paths.remove(path)
                continue
            path[0] -= 1
            if path[0] == 0:
                s, coordinates, path_string = path
                floor, x, y = coordinates
                solved_field[floor][y][x] = path
                next_moves += find_next_moves(path, solved_field)
                paths.remove(path)
        paths += next_moves


# [1, [current_floor, x, y], ">><<!!^v"]

start_time = time.time()
filename = "zauberschule5.txt"
first_floor, second_floor = get_floors(filename)
floors = [first_floor, second_floor]
seconds, path = find_path([deepcopy(first_floor), deepcopy(second_floor)])
print(seconds)
print(path)

end_time = time.time()
# Differenz berechnen
elapsed_time = (end_time - start_time) * 1000  # In Millisekunden umrechnen
print(f"Die Zeit verging: {elapsed_time} ms")
