import argparse
from collections import namedtuple
from collections import defaultdict
from itertools import repeat


Point = namedtuple("Point", ['x', 'y'])
VentLine = namedtuple("VentLine", ['start', 'end'])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    input_lines = [x.strip() for x in open(args.input_file)]
    vent_lines = [parse_input_line(x) for x in input_lines]
    return vent_lines


def parse_input_line(s):
    points = s.split(" -> ")
    sx1, sy1 = points[0].split(",")
    sx2, sy2 = points[1].split(",")
    return VentLine(Point(int(sx1), int(sy1)), Point(int(sx2), int(sy2)))


def main():
    vent_lines = parse_args()

    part_1_answer = count_overlaps(vent_lines)
    part_2_answer = count_overlaps(vent_lines, True)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def count_overlaps(vents, count_diagonals=False):
    overlap_counts = defaultdict(lambda: 0)
    for v in vents:
        if not count_diagonals and v.start.x != v.end.x and v.start.y != v.end.y:
            continue

        if v.start.x == v.end.x:
            xs = repeat(v.start.x)
        elif v.start.x < v.end.x:
            xs = range(v.start.x, v.end.x + 1)
        else:
            xs = range(v.start.x, v.end.x - 1, -1)

        if v.start.y == v.end.y:
            ys = repeat(v.start.y)
        elif v.start.y < v.end.y:
            ys = range(v.start.y, v.end.y + 1)
        else:
            ys = range(v.start.y, v.end.y - 1, -1)

        for x, y in zip(xs, ys):
            overlap_counts[Point(x, y)] += 1
    return sum(1 if x > 1 else 0 for x in overlap_counts.values())


def print_counts(overlap_counts, x_max=9, y_max=9):
    print("Overlap counts:")
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            count = overlap_counts[Point(x, y)]
            print(count if count > 0 else '.', end='')
        print('')
    print('')


if __name__ == "__main__":
    main()
