import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [[int(x) for x in line.strip()] for line in open(args.input_file)]
    return parsed_lines


def main():
    risk_map = parse_args()
    part_1_answer = get_lowest_risk(risk_map)
    print(f"Part 1:\n{part_1_answer}\n")
    part_2_answer = get_lowest_risk(make_full_risk_map(risk_map))
    print(f"Part 2:\n{part_2_answer}")


def get_lowest_risk(risk_map):
    width = len(risk_map[0])
    height = len(risk_map)
    total_points = width * height
    cumulative_risk_by_point = {Point(0, 0): 0}
    remaining_points_to_calculate = {Point(0, 0)}
    while Point(width - 1, height - 1) not in cumulative_risk_by_point:
        p, risk = sorted([x for x in cumulative_risk_by_point.items()
                          if x[0] in remaining_points_to_calculate], key=lambda x: x[1])[0]
        adjacent_points = []
        if p.x - 1 >= 0:
            adjacent_points.append(Point(p.x - 1, p.y))
        if p.x + 1 < width:
            adjacent_points.append(Point(p.x + 1, p.y))
        if p.y - 1 >= 0:
            adjacent_points.append(Point(p.x, p.y - 1))
        if p.y + 1 < height:
            adjacent_points.append(Point(p.x, p.y + 1))
        for adjacent_point in adjacent_points:
            if adjacent_point not in cumulative_risk_by_point:
                cumulative_risk_by_point[adjacent_point] = risk + risk_map[adjacent_point.y][adjacent_point.x]
                remaining_points_to_calculate.add(adjacent_point)
                if len(cumulative_risk_by_point) % 1000 == 0:
                    print(f"\rCalculating... ({int(len(cumulative_risk_by_point) / total_points * 100)}%)", end="")
        remaining_points_to_calculate.remove(p)
    print("\r                     \r", end="")
    return cumulative_risk_by_point[Point(width - 1, height - 1)]


def make_full_risk_map(risk_map):
    h = len(risk_map)
    w = len(risk_map[0])
    return [[(risk_map[y % h][x % w] - 1 + int(x / w) + int(y / h)) % 9 + 1 for x in range(w * 5)] for y in range(h * 5)]


def print_map(risk_map):
    for y in range(len(risk_map)):
        for x in range(len(risk_map[y])):
            print(risk_map[y][x], end="")
        print("")
    print("")


if __name__ == "__main__":
    main()
