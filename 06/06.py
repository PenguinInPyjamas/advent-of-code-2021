import argparse
from collections import defaultdict
from itertools import islice


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    ints = [int(x) for x in next(open(args.input_file)).split(",")]
    return ints


def main():
    fish_ages = parse_args()

    simulation = simulate_fish(fish_ages)

    part_1_answer = count_fish(get_fish_counts_on_day(simulation, 80))
    part_2_answer = count_fish(get_fish_counts_on_day(simulation, 256 - 80))
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def simulate_fish(initial_state):
    fish_ages = defaultdict(lambda: 0)
    for x in initial_state:
        fish_ages[x] += 1
    while True:
        new_fish_ages = fish_ages.copy()
        for age in range(8):
            new_fish_ages[age] = fish_ages[age + 1]
        new_fish_ages[8] = fish_ages[0]
        new_fish_ages[6] += fish_ages[0]
        fish_ages = new_fish_ages
        yield fish_ages.copy()


def get_fish_counts_on_day(simulation, day):
    return next(islice(simulation, day - 1, day))


def count_fish(fish_ages_set):
    return sum(c for c in fish_ages_set.values())


if __name__ == "__main__":
    main()
