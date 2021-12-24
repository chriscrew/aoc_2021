from aoc_helper import read_and_clean_file
from collections import Counter

class Node: 
    def __init__(self, name):
        self.name = name
        self.large = name.isupper()
        self.connections = []


lines, line_count = read_and_clean_file(".\data\day_twelve_data.txt")
connections = [x.split('-') for x in lines]

nodes = {}

# Create Tree
for c in connections:
    if c[0] not in nodes:
        nodes[c[0]] = Node(c[0])
    if c[1] not in nodes:
        nodes[c[1]] = Node(c[1])

    f = nodes[c[0]]
    t = nodes[c[1]]
    if t.name != 'start':
        f.connections.append(t)
    if f.name != 'start':
        t.connections.append(f)

nodes['end'].connections.clear()

start_node = nodes['start']
end_node = nodes['end']

def find(node: Node, path : list[str]):
    global found
    path.append(node.name)

    for n in node.connections:
        if n.name == 'end':
            found += 1
            continue
        if not n.large:
            has_been = path.count(n.name) > 0
            if has_been:
                small_visted_twice = len([c for c in Counter(path) if c.islower() and Counter(path)[c] == 2]) > 0
                if small_visted_twice:
                    continue

        find(n, path.copy())

found = 0
find(start_node, [])
print(f'Paths Found: {found}')