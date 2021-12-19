import argparse
from collections import namedtuple
from collections import defaultdict

Rule = namedtuple("Rule", ["left", "right", "new_middle"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    lines = [line.strip() for line in open(args.input_file)]
    template = lines[0]
    rules = [Rule(line[0], line[1], line[-1]) for line in lines[2:]]
    return template, rules


def main():
    template, rules = parse_args()

    polymerization = run_polymerization(template, rules)
    for _ in range(9):
        next(polymerization)
    polymerization_stage_10 = next(polymerization)

    efficient_polymerization = run_polymerization_efficiently(template, rules)
    for _ in range(39):
        next(efficient_polymerization)
    polymerization_stage_40 = next(efficient_polymerization)

    stage_10_elements_by_quantity = count_elements_in_polymer(polymerization_stage_10)
    part_1_answer = stage_10_elements_by_quantity[0][1] - stage_10_elements_by_quantity[-1][1]
    stage_40_elements_by_quantity = sorted(list(polymerization_stage_40.items()), key=lambda x: x[1], reverse=True)
    part_2_answer = stage_40_elements_by_quantity[0][1] - stage_40_elements_by_quantity[-1][1]
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def run_polymerization(initial_state, rules):
    polymer = initial_state
    while True:
        new_polymer = []
        for i in range(len(polymer) - 1):
            new_polymer.append(polymer[i])
            for left, right, new_middle in rules:
                if polymer[i] == left and polymer[i + 1] == right:
                    new_polymer.append(new_middle)
                    break
        new_polymer.append(polymer[-1])
        polymer = new_polymer
        yield polymer


def run_polymerization_efficiently(initial_state, raw_rules):
    rules = {}
    for left, right, middle in raw_rules:
        rules[left + right] = [left + middle, middle + right]

    element_pair_counts = defaultdict(lambda: 0)
    for i in range(len(initial_state) - 1):
        element_pair_counts[initial_state[i] + initial_state[i + 1]] += 1

    element_counts = defaultdict(lambda: 0)
    for element in initial_state:
        element_counts[element] += 1

    while True:
        new_element_pair_counts = defaultdict(lambda: 0)
        for pair, count in element_pair_counts.items():
            if pair in rules:
                element_counts[rules[pair][0][-1]] += element_pair_counts[pair]
                for new_element_pair in rules[pair]:
                    new_element_pair_counts[new_element_pair] += element_pair_counts[pair]
            else:
                new_element_pair_counts[pair] += element_pair_counts[pair]
        element_pair_counts = new_element_pair_counts
        yield element_counts


def count_elements_in_polymer(polymer):
    counts = defaultdict(lambda: 0)
    for element in polymer:
        counts[element] += 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    main()
