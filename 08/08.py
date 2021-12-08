import argparse
from collections import namedtuple

SignalEntry = namedtuple("SignalEntry", ["in_signals", "out_signals"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [parse_input_line(x) for x in open(args.input_file)]
    return parsed_lines


def parse_input_line(l):
    input_signals, output_signals = ([x.strip() for x in s.split(" ")] for s in l.split(" | "))
    return SignalEntry(input_signals, output_signals)


def main():
    signal_entries = parse_args()
    output_digits = [get_correct_output_signal(s) for s in signal_entries]
    part_1_answer = count_in_output_digits(output_digits, [1, 4, 7, 8])
    part_2_answer = None
    # part_2_answer = sum_output_digits(output_digits)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def get_correct_output_signal(signal_entry):
    unknown_output_signals = set(signal_entry.out_signals)
    known_output_digits = []
    potential_connections = dict((c, "abcdefg") for c in "abcdefg")
    for s in signal_entry.out_signals:
        if len(s) == 2:
            if s in unknown_output_signals:
                unknown_output_signals.remove(s)
            known_output_digits.append(1)
        elif len(s) == 3:
            if s in unknown_output_signals:
                unknown_output_signals.remove(s)
            known_output_digits.append(7)
        elif len(s) == 4:
            if s in unknown_output_signals:
                unknown_output_signals.remove(s)
            known_output_digits.append(4)
        elif len(s) == 7:
            if s in unknown_output_signals:
                unknown_output_signals.remove(s)
            known_output_digits.append(8)
    return known_output_digits


def count_in_output_digits(output_digits, target_digits):
    return sum(1 if x in target_digits else 0 for s in output_digits for x in s)


def sum_output_digits(output_digits):
    return sum(x for l in output_digits for x in l)


if __name__ == "__main__":
    main()
