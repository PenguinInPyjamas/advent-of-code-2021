import argparse
from collections import Counter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    diagnostic_report = [x.strip() for x in open(args.input_file)]
    return diagnostic_report


def main():
    report = parse_args()

    gamma, epsilon = calc_gamma_and_epsilon(report)
    oxy_rating = calc_oxy_gen_rating(report)
    c02_rating = calc_c02_scrub_rating(report)

    part_1_answer = gamma * epsilon
    part_2_answer = oxy_rating * c02_rating
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def calc_gamma_and_epsilon(report):
    # Assume all binary numbers are the same length
    gamma = [most_common_digit(report, i) for i in range(len(report[0]))]
    if None in gamma:
        raise Exception("calc_gamma_and_epsilon: most common digit could not be determined")
    epsilon = invert_binary(gamma)
    return binary_to_int(gamma), binary_to_int(epsilon)


def calc_life_support_rating(report, criteria):
    remaining_lines = set(report)
    # Assume all binary numbers are the same length
    for i in range(len(report[0])):
        if len(remaining_lines) > 1:
            mode_digit = most_common_digit(remaining_lines, i)
            incorrect_lines = set()
            for line in remaining_lines:
                if not criteria(line[i], mode_digit):
                    incorrect_lines.add(line)
            for line in incorrect_lines:
                remaining_lines.remove(line)
    if len(remaining_lines) != 1:
        raise Exception(f"calc_life_support_rating: Exactly 1 line should remain, instead found {len(remaining_lines)}")
    return binary_to_int(next(iter(remaining_lines)))


def calc_oxy_gen_rating(report):
    return calc_life_support_rating(report, lambda d, m: (d == m) if m else (d == '1'))


def calc_c02_scrub_rating(report):
    return calc_life_support_rating(report, lambda d, m: (d != m) if m else (d == '0'))


def most_common_digit(report, i):
    count_0 = 0
    count_1 = 0
    for line in report:
        if line[i] == '0':
            count_0 += 1
        elif line[i] == '1':
            count_1 += 1
        else:
            raise Exception(f"most_common_digit: Binary digit should be '0' or '1' but found '{line[i]}'")
    if count_1 > count_0:
        return '1'
    elif count_0 > count_1:
        return '0'
    else:
        return None


def invert_binary(b):
    return ['1' if c == '0' else ('0' if c == '1' else c) for c in b]


def binary_to_int(b):
    return sum([pow(2, i) if v == '1' else 0 for i, v in enumerate(reversed(b))])


if __name__ == "__main__":
    main()
