import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Instruction = namedtuple("Instruction", ["axis", "position"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    lines = [line for line in open(args.input_file)]
    split_index = lines.index("\n")
    dot_locations = [Point(int(line.split(",")[0]), int(line.split(",")[1])) for line in lines[:split_index]]
    instructions = [Instruction(line[11], int(line[13:])) for line in lines[split_index + 1:]]
    return dot_locations, instructions


def main():
    dots, instructions = parse_args()
    new_dot_locations = fold_paper(dots, instructions[0])
    print(f"Part 1:\n{len(new_dot_locations)}\n")
    for i in instructions[1:]:
        new_dot_locations = fold_paper(new_dot_locations, i)
    print("Part 2:")
    print_paper(new_dot_locations, 40, 6)


def fold_paper(dots, instruction):
    new_dots = set()
    for x, y in dots:
        if instruction.axis == "x":
            if x < instruction.position:
                new_dots.add(Point(x, y))
            else:
                new_dots.add(Point(2 * instruction.position - x, y))
        elif instruction.axis == "y":
            if y < instruction.position:
                new_dots.add(Point(x, y))
            else:
                new_dots.add(Point(x, (2 * instruction.position) - y))
        else:
            raise Exception(f"Axis of fold was not 'x' or 'y' (was '{instruction.axis}')")
    return new_dots


def print_paper(dots, length, height):
    for x in range(length + 2):
        print(".", end="")
    print("")
    for y in range(height):
        print(".", end="")
        for x in range(length):
            print("#" if Point(x, y) in dots else " ", end="")
        print(".", end="\n")
    for x in range(length + 2):
        print(".", end="")
    print("")


if __name__ == "__main__":
    main()
