import argparse
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [[int(x) for x in line.strip()] for line in open(args.input_file)]
    return parsed_lines


def main():
    height_map = parse_args()
    low_points = get_low_points(height_map)
    basins = get_basins(low_points, height_map)
    part_1_answer = get_risk_level(low_points, height_map)
    part_2_answer = get_basin_score(basins)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def get_low_points(height_map):
    low_points = []
    for y in range(len(height_map)):
        for x in range(len(height_map[y])):
            if x > 0 and height_map[y][x-1] <= height_map[y][x]:
                continue
            if x < len(height_map[y]) - 1 and height_map[y][x+1] <= height_map[y][x]:
                continue
            if y > 0 and height_map[y-1][x] <= height_map[y][x]:
                continue
            if y < len(height_map) - 1 and height_map[y+1][x] <= height_map[y][x]:
                continue
            low_points.append(Point(x, y))
    return low_points


def get_basins(low_points, height_map):
    basins = []
    for initial_point in low_points:
        this_basin = {initial_point}
        already_checked = set()
        while True:
            new_points = set()
            for x, y in this_basin - already_checked:
                if x > 0 and height_map[y][x] < height_map[y][x - 1] < 9:
                    new_points.add(Point(x - 1, y))
                if x < len(height_map[y]) - 1 and height_map[y][x] < height_map[y][x + 1] < 9:
                    new_points.add(Point(x + 1, y))
                if y > 0 and height_map[y][x] < height_map[y-1][x] < 9:
                    new_points.add(Point(x, y - 1))
                if y < len(height_map) - 1 and height_map[y][x] < height_map[y+1][x] < 9:
                    new_points.add(Point(x, y + 1))
                already_checked.add(Point(x, y))
            if len(new_points) > 0:
                for p in new_points:
                    this_basin.add(p)
            else:
                basins.append(this_basin)
                break
    return basins


def get_risk_level(low_points, height_map):
    return sum(height_map[y][x] + 1 for x, y in low_points)


def get_basin_score(basins):
    basin_sizes = sorted(len(b) for b in basins)
    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


if __name__ == "__main__":
    main()
