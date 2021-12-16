from os import defpath
import sys
from types import resolve_bases
from aoc_helper import read_and_clean_file

# Day Questions

def day_one_question_one():
    lines = []
    with open(".\data\day_one_data.txt", "r") as file:
        lines = file.readlines()

    depth_increase = 0

    prev_depth = sys.maxsize
    for line in lines:
        cur_depth = int(line.strip())
        if(cur_depth > prev_depth):
            depth_increase+=1
        prev_depth = cur_depth
    
    print(depth_increase)

def day_one_question_two():
    lines = []
    with open(".\data\day_one_data.txt", "r") as file:
        lines = file.readlines()

    depths = []
    for line in lines:
        depths.append(int(line.strip()))

    depth_count = len(depths)
    windows = []
    for x in range(depth_count):
        if((depth_count - x) < 3):
            continue

        inc = 0
        inc += depths[x]
        inc += depths[x + 1]
        inc += depths[x + 2]
        windows.append(inc)
        
    depth_increase = 0

    prev_depth = sys.maxsize
    for window in windows:
        if(window > prev_depth):
            depth_increase+=1
        prev_depth = window

    print(depth_increase)

def day_two():
    horizontal = 0
    depth = 0
    aim = 0

    lines = []
    with open(".\data\day_two_data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        params = line.strip().split(" ")

        change = int(params[1])

        match params[0]:
            case "forward":
                horizontal += change
                depth += (aim * change)
            case "down":
                aim += change
            case "up":
                aim -= change

    result = horizontal * depth
    print(result)

def day_three():
    lines = []
    with open(".\data\day_three_data.txt", "r") as file:
        lines = file.readlines()

    epsilon = 0
    gamma  = 0

    line_length = len(lines[0].strip())
    culm = [0 for i in range(line_length)]
    for line in lines:
        code = line.strip()
        for x in range(line_length):
            value = int(code[x])
            culm[x] += value

    gamma_str = ""
    epsilon_str = ""
    for x in range(line_length):

        if(culm[x] > 500):
            gamma_str += "1"
            epsilon_str += "0"
        else:
            gamma_str += "0"
            epsilon_str += "1"
        
        gamma = int(gamma_str, 2)
        epsilon = int(epsilon_str, 2)

    result = gamma * epsilon
    print(result)

def culm_bit(values, bit):
    high = 0
    low = 0
    for x in range(len(values)):
        v = int(values[x][bit])
        if(v == 1):
            high += 1
        else:
            low += 1

    return high, low

def day_three_question_two():
    
    values, count = read_and_clean_file(".\data\day_three_data.txt")
    oxygen_values = values.copy()
    co2_values = values.copy()

    bit_count = len(values[0])

    for x in range(bit_count):
        if(len(oxygen_values) > 1):
            oxy_high, oxy_low = culm_bit(oxygen_values, x)
            if(oxy_low > oxy_high):
                oxygen_values = [i for i in oxygen_values if i[x] == '0']
            else:
                oxygen_values = [i for i in oxygen_values if i[x] == '1']

        if(len(co2_values) > 1):
            co2_high, co2_low = culm_bit(co2_values, x)
            if(co2_low < co2_high or co2_low == co2_high):
                co2_values = [i for i in co2_values if i[x] == '0']
            else:
                co2_values = [i for i in co2_values if i[x] == '1']

    oxygen = int(oxygen_values[0], 2)
    co2 = int(co2_values[0], 2)
    result = oxygen * co2
    print(result)

class BingoCard:
    data = []
    results = []
    won = False

    def __init__(self, data):
        self.data = data
        self.results = [[False, False, False, False, False] for i in range(5)]

    def has_won(self, num) -> bool:
        for y in range(5):
            for x in range(5):
                if(self.data[y][x] == num):
                    self.results[y][x] = True

        self.won = self.check_board()

        return self.won

    def check_board(self) -> bool:
        for y in range(5):
            result = not False in self.results[y] or not False in [x[y] for x in self.results]
            if(result):
                return True

        return False

    def sum_of_false(self) -> int:
        result = 0
        for y in range(5):
            for x in range(5):
                if(not self.results[y][x]):
                    result += self.data[y][x]

        return result

def day_four_question_one():

    values, count = read_and_clean_file(".\data\day_four_data.txt")
    draw_numbers = [int(i) for i in values[0].split(',')]

    boards = []

    for x in range(2, count, 6):
        data = []
        data.append([int(i) for i in values[x].replace('  ',' ').split(' ')])
        data.append([int(i) for i in values[x + 1].replace('  ',' ').split(' ')])
        data.append([int(i) for i in values[x + 2].replace('  ',' ').split(' ')])
        data.append([int(i) for i in values[x + 3].replace('  ',' ').split(' ')])
        data.append([int(i) for i in values[x + 4].replace('  ',' ').split(' ')])
        boards.append(BingoCard(data))

    winner = None
    winning_num = None

    for num in draw_numbers:

        for board in boards:
            if(not board.won):
                if(board.has_won(num)):
                    winner = board
        
        left = [b for b in boards if not b.won]
        if(len(left) == 0):
            winning_num = num
            break

    if(winner is not None):
        sum = winner.sum_of_false()
        result = sum * winning_num
        print(result)


def day_five():
    values, count = read_and_clean_file(".\data\day_five_data.txt")
    values = [i.replace(' -> ', ',') for i in values]

    grid = [[0 for x in range(1000)] for i in range(1000)]
    
    for value in values:
        x1,y1,x2,y2 = map(int, value.split(','))

        if(x1 == x2 or y1 == y2):
            if(x1 == x2):
                x = x1
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y][x] += 1
            else:
                y = y1
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[y][x] += 1
        else:
            x = x1
            y = y1
            grid[y][x] += 1

            dx = (x2 - x1)
            dy = (y2 - y1)
            
            while x != x2 and y != y2:
                x += (dx // abs(dx))
                y += (dy // abs(dy))
                grid[y][x] += 1
                    
    result = 0
    for y in range(1000):
        for x in range(1000):
            if(grid[y][x] >= 2):
                result += 1

    print(result)

def day_six():
    values, count = read_and_clean_file(".\data\day_six_data.txt")
    inital = list(map(int, values[0].split(',')))

    groups = [0 for x in range(9)]

    for i in inital:
        groups[i] += 1

    days = 256

    for d in range(days):
        new_fish = groups[0]

        for x in range(8):
            groups[x] = groups[x + 1]

        groups[8] = new_fish
        groups[6] += new_fish

    result = sum(groups)
    print(result)

def day_seven():
    values, count = read_and_clean_file(".\data\day_seven_data.txt")
    positions = list(map(int, values[0].split(',')))

    min_cost = sys.maxsize
    for a in range(min(positions), max(positions)):
        cost = 0
        for p in positions:
            #cost += abs(p - a)
            cost += ((abs(p - a) ** 2) + abs(p - a)) // 2

        if(cost < min_cost):
            min_cost = cost

    print(min_cost)

import re
from collections import Counter

def determine_digits(patterns : list) -> list:
    count_parts = Counter(''.join(patterns))
    parts = ['' for x in range(7)]

    for n, v in count_parts.items():
        if v == 4:
            parts[4] = n
        elif v == 6:
            parts[1] = n
        elif v == 9:
            parts[5] = n

    parts[0] = [x for x in next(i for i in patterns if len(i) == 3) if x not in next(i for i in patterns if len(i) == 2)][0]
    for n, v in count_parts.items():
        if v == 8 and n != parts[0]:
            parts[2] = n

    f = next(i for i in patterns if len(i) == 4)
    parts[3] = re.sub('[' + parts[1] + parts[2] + parts[5] + ']', '', f)

    e = next(i for i in patterns if len(i) == 7)
    parts[6] = re.sub('[' + parts[0] + parts[1] + parts[2] + parts[3] + parts[4] + parts[5] + ']', '', e)

    return parts

def day_eight_a():
    values, count = read_and_clean_file(".\data\day_eight_data.txt")
    entries = [i.split('|') for i in values]

    v = 0
    for entry in entries:
        output = entry[1].strip().split(' ')

        for o in output:
            if len(o) == 2 or len(o) == 3 or len(o) == 4 or len(o) == 7:
                v += 1

    print(v)

def day_eight_b():
    values, count = read_and_clean_file(".\data\day_eight_data.txt")
    entries = [i.split('|') for i in values]

    s = 0

    for entry in entries:
        parts = determine_digits(entry[0].strip().split(' '))
        output = entry[1].strip().split(' ')

        c = ''
        for o in output:
            if(len(o) == 2):
                c += '1'
                continue
            if(len(o) == 4):
                c += '4'
                continue
            if(len(o) == 3):
                c += '7'
                continue
            if(len(o) == 7):
                c += '8'
                continue
            if(len(re.sub('[' + parts[0] + parts[1] + parts[2] + parts[4] + parts[5] + parts[6] + ']', '', o)) == 0):
                c += '0'
                continue
            if(len(re.sub('[' + parts[0] + parts[2] + parts[3] + parts[4] + parts[6] + ']', '', o)) == 0):
                c += '2'
                continue
            if(len(re.sub('[' + parts[0] + parts[2] + parts[3] + parts[5] + parts[6] + ']', '', o)) == 0):
                c += '3'
                continue
            if(len(re.sub('[' + parts[0] + parts[1] + parts[3] + parts[5] + parts[6] + ']', '', o)) == 0):
                c += '5'
                continue
            if(len(re.sub('[' + parts[0] + parts[1] + parts[3] + parts[4] + parts[5] + parts[6] + ']', '', o)) == 0):
                c += '6'
                continue
            if(len(re.sub('[' + parts[0] + parts[1] + parts[2] + parts[3] + parts[5] + parts[6] + ']', '', o)) == 0):
                c += '9'
                continue

        s += int(c)
    print(s)

def is_low_point(grid : list, x : int, y : int) -> bool:

    r = True

    v = grid[y][x]

    if(x - 1) >= 0:
        r = r and (v < grid[y][(x - 1)])
    if(y - 1) >= 0:
        r = r and (v < grid[(y - 1)][x])
    if(x + 1) < 100:
        r = r and (v < grid[y][(x + 1)])
    if(y + 1) < 100:
         r = r and (v < grid[(y + 1)][x])

    return r

nodes = []

def calculate_basin_size(grid : list, x : int, y : int) -> int: 
    nodes.append((x,y))

    inside = []

    while len(nodes) > 0:
        n = nodes.pop()
        if grid[n[1]][n[0]] != 9:
            if(n not in inside):
                inside.append(n)  
            next = [(n[0] - 1,n[1]),(n[0] + 1,n[1]),(n[0],n[1] - 1),(n[0],n[1] + 1)]
            for ne in next:
                if ne[0] >= 0 and ne[1] >= 0 and ne[0] < 100 and ne[1] < 100:
                    if ne not in inside:
                        nodes.append(ne)

    return len(inside)

def day_nine_a():
    values, count = read_and_clean_file(".\data\day_nine_data.txt")

    for i in range(count):
        values[i] = [int(x) for x in values[i]]

    r = 0

    for y in range(100):
        for x in range(100):
            if is_low_point(values, x, y):
                r += (values[y][x] + 1)

    print(r)

import heapq
import math

def day_nine_b():
    values, count = read_and_clean_file(".\data\day_nine_data.txt")

    for i in range(count):
        values[i] = [int(x) for x in values[i]]

    r = []

    for y in range(100):
        for x in range(100):
            if is_low_point(values, x, y):
                r.append(calculate_basin_size(values, x, y))

    print(math.prod(heapq.nlargest(3, r)))

import statistics

def day_ten():
    chunks, count = read_and_clean_file(".\data\day_ten_data.txt")
    for i in range(count):
        chunks[i] = [x for x in chunks[i]]

    corrupted_points = {')' : 3, ']' : 57, '}' : 1197, '>' : 25137}
    incomplete_points = {')' : 1, ']' : 2, '}' : 3, '>' : 4}
    pairs = {'{' : '}', '<' : '>', '[' : ']', '(' : ')'}

    corrupted_score = 0
    incomplete_scores = [] 

    for chunk in chunks:
        open_symbols = []
        is_corrupted = False
        for i in range(len(chunk)):
            symbol = chunk[i]
            if symbol in pairs:
                open_symbols.append(symbol)
            else:
                close_symbol = pairs[open_symbols.pop()]
                if close_symbol != symbol :
                    corrupted_score += corrupted_points[symbol]
                    is_corrupted  = True
                    break
        
        if not is_corrupted :
            score = 0
            while len(open_symbols) != 0:
                close_symbol = pairs[open_symbols.pop()]
                score = (score * 5) + incomplete_points[close_symbol]

            incomplete_scores.append(score)

    incomplete_score = statistics.median(incomplete_scores)
    
    print(f'Corrupted Score: {corrupted_score}')
    print(f'Incomplete Score: {incomplete_score}')


def day_eleven():
    grid, count = read_and_clean_file(".\data\day_eleven_data.txt")
    for i in range(count):
        grid[i] = [int(x) for x in grid[i]]
    
    flashes = 0

    for step in range(1000):

        # Increment all by one
        for y in range(10):
            for x in range(10):
                grid[y][x] += 1

        flash = []

        for y in range(10):
            for x in range(10):
                if grid[y][x] > 9:
                    flash.append((x, y))

        fired = [[False for x in range(10)] for i in range(10)]
        while len(flash) > 0:
            point = flash.pop()
            x = point[0]
            y = point[1]
            if not fired[y][x]:
                fired[y][x] = True
                neighbours = [(x - 1, y - 1),(x, y - 1),(x + 1, y - 1),(x - 1, y),(x + 1, y),(x - 1, y + 1),(x, y + 1),(x + 1, y + 1)]
                for n in neighbours:
                    if n[0] >= 0 and n[0] < 10 and n[1] >= 0 and n[1] < 10:
                        grid[n[1]][n[0]] += 1
                        if grid[n[1]][n[0]] > 9 and not fired[n[1]][n[0]]:
                            flash.append((n[0], n[1]))

        for y in range(10):
            for x in range(10):
                if fired[y][x]:
                    flashes += 1
                    grid[y][x] = 0
        
        local_flashes = sum(x.count(True) for x in fired)
        if local_flashes == 100:
            print(f"Sync Flash: {step + 1}")

    print(f'Complete with {flashes} flashes')


day_eleven()