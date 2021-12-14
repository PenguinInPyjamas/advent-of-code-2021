import argparse
from itertools import takewhile


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [[int(c) for c in line.strip()] for line in open(args.input_file)]
    return parsed_lines


def main():
    octopuses = parse_args()
    simulation = simulate_octopuses(octopuses)
    flash_counts = [x for x in takewhile(lambda x: x < 100, simulation)]
    part_1_answer = sum(flash_counts[:100])
    part_2_answer = len(flash_counts) + 1
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def simulate_octopuses(original_octopuses):
    octopuses = [[x for x in y] for y in original_octopuses]
    while True:
        flashes = set()
        num_flashes = 0
        for y in range(10):
            for x in range(10):
                octopuses[y][x] += 1
                if octopuses[y][x] == 10:
                    flashes.add((x, y))
        while len(flashes) > 0:
            num_flashes += len(flashes)
            new_flashes = set()
            for flash_x, flash_y in flashes:
                for y in range(max(0, flash_y-1), min(flash_y+2, 10)):
                    for x in range(max(0, flash_x-1), min(flash_x+2, 10)):
                        if x != flash_x or y != flash_y:
                            octopuses[y][x] += 1
                            if octopuses[y][x] == 10:
                                new_flashes.add((x, y))
            flashes = new_flashes
        for y in range(10):
            for x in range(10):
                if octopuses[y][x] >= 10:
                    octopuses[y][x] = 0
        yield num_flashes


if __name__ == "__main__":
    main()
