from aoc_helper import read_and_clean_file
from collections import Counter
from itertools import chain, zip_longest

lines, line_count = read_and_clean_file(".\data\day_14_data.txt")

template = lines[0]
rules = dict(x.split(' -> ') for x in lines[2:])

char_count = Counter(template)
template_pairs = Counter()

for i in range(len(template) - 1):
    template_pairs[template[i] + template[i + 1]] += 1

for _ in range(40):
    additional = Counter()
    for key, value in template_pairs.items():
        if key in rules:
            additional[key[0] + rules[key]] += value
            additional[rules[key] + key[1]] += value
            char_count[rules[key]] += value

    template_pairs = additional

result = max(char_count.values()) - min(char_count.values())
print(result)