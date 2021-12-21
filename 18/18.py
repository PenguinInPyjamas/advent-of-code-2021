import argparse
from functools import reduce


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [parse_snail_number(line.strip()) for line in open(args.input_file)]
    return parsed_lines


def parse_snail_number(s):
    if s[0] == "[":
        s_split = s[1:-1].split(",")
        for i in range(1, len(s_split)):
            left_string = ",".join(s_split[:i])
            right_string = ",".join(s_split[i:])
            if left_string.count('[') == left_string.count(']') and right_string.count('[') == right_string.count(']'):
                return parse_snail_number(left_string), parse_snail_number(right_string)
        raise Exception(f"parse_snail_number: Couldn't parse snail number '{s}'")
    return int(s)


def main():
    snail_numbers = parse_args()
    snail_numbers_sum = reduce(add_snail_numbers, snail_numbers)
    snail_number_pairs = [(snail_numbers[x], snail_numbers[y]) for x in range(len(snail_numbers))
                      for y in range(len(snail_numbers)) if x is not y]
    part_1_answer = calculate_magnitude(snail_numbers_sum)
    part_2_answer = max(calculate_magnitude(add_snail_numbers(x, y)) for x, y in snail_number_pairs)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def add_snail_numbers(x, y):
    return reduce_snail_number((x, y))


def calculate_magnitude(snail_number):
    if type(snail_number) is not tuple:
        return snail_number
    else:
        return 3 * calculate_magnitude(snail_number[0]) + 2 * calculate_magnitude(snail_number[1])


def reduce_snail_number(snail_number):
    if type(snail_number) is not tuple:
        return snail_number
    else:
        x, y = snail_number
    while True:
        explode_result = reduce_explode((x, y))
        if explode_result:
            if type(explode_result[0]) is tuple:
                x, y = explode_result[0]
                continue
            else:
                raise Exception(f"reduce_snail_number: reduce_explode somehow resulted in single value")
        split_result = reduce_split((x, y))
        if split_result:
            x, y = split_result
            continue
        break
    return x, y


def reduce_explode(snail_number, layer=0):
    if type(snail_number) is tuple:
        if layer >= 4:
            return 0, snail_number[0], snail_number[1]
        if type(snail_number[0]) is tuple:
            left_result = reduce_explode(snail_number[0], layer + 1)
            if left_result:
                new_left_num, left_remainder, right_remainder = left_result
                return (new_left_num, add_to_snail_number_left(snail_number[1], right_remainder)), left_remainder, 0
        if type(snail_number[1]) is tuple:
            right_result = reduce_explode(snail_number[1], layer + 1)
            if right_result:
                new_right_num, left_remainder, right_remainder = right_result
                return (add_to_snail_number_right(snail_number[0], left_remainder), new_right_num), 0, right_remainder
    return None


def add_to_snail_number_left(snail_number, x):
    if type(snail_number) is tuple:
        return add_to_snail_number_left(snail_number[0], x), snail_number[1]
    else:
        return snail_number + x


def add_to_snail_number_right(snail_number, x):
    if type(snail_number) is tuple:
        return snail_number[0], add_to_snail_number_right(snail_number[1], x)
    else:
        return snail_number + x


def reduce_split(snail_number):
    if type(snail_number) is not tuple:
        if snail_number >= 10:
            x = int(snail_number / 2)
            y = snail_number - x
            return x, y
        else:
            return None
    else:
        x, y = snail_number
        left_result = reduce_split(x)
        if left_result:
            return left_result, y
        else:
            right_result = reduce_split(y)
            return (x, right_result) if right_result else None


def test_explode():
    assert reduce_explode((((((9, 8), 1), 2), 3), 4))[0] == ((((0, 9), 2), 3), 4)
    assert reduce_explode((7, (6, (5, (4, (3, 2))))))[0] == (7, (6, (5, (7, 0))))
    assert reduce_explode(((6, (5, (4, (3, 2)))), 1))[0] == ((6, (5, (7, 0))), 3)
    assert reduce_explode(((3, (2, (1, (7, 3)))), (6, (5, (4, (3, 2))))))[0] == ((3, (2, (8, 0))), (9, (5, (4, (3, 2)))))
    assert reduce_explode(((3, (2, (8, 0))), (9, (5, (4, (3, 2))))))[0] == ((3, (2, (8, 0))), (9, (5, (7, 0))))


def test_add():
    assert reduce(add_snail_numbers, [(1, 1), (2, 2), (3, 3), (4, 4)]) == ((((1, 1), (2, 2)), (3, 3)), (4, 4))
    assert reduce(add_snail_numbers, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]) == ((((3, 0), (5, 3)), (4, 4)), (5, 5))


if __name__ == "__main__":
    main()
