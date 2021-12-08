import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    ints = [int(x) for x in next(open(args.input_file)).split(",")]
    return ints


def main():
    crab_positions = parse_args()

    part_1_answer = get_simple_crab_fuel_cost(crab_positions, median_average(crab_positions))
    part_2_answer = get_advanced_crab_fuel_cost(crab_positions, advanced_crab_metric(crab_positions))
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def get_simple_crab_fuel_cost(positions, target_position):
    return sum(abs(p - target_position) for p in positions)


def get_advanced_crab_fuel_cost(positions, target_position):
    return sum(sum(range(abs(p - target_position) + 1)) for p in positions)


def median_average(ints):
    return sorted(ints)[int(len(ints) / 2)]


def advanced_crab_metric(ints):
    best_int = 0
    least_fuel_used = get_advanced_crab_fuel_cost(ints, best_int)
    for i in range(1, max(ints) + 1):
        fuel_used = get_advanced_crab_fuel_cost(ints, i)
        if fuel_used < least_fuel_used:
            best_int = i
            least_fuel_used = fuel_used
    return best_int


if __name__ == "__main__":
    main()
