def read_and_clean_file(filename: str) -> tuple[list[str], int]:
    lines = []
    with open(filename, "r") as file:
        lines = file.readlines()

    line_count = len(lines)
    for x in range(line_count):
        lines[x] = lines[x].strip()

    return lines, line_count