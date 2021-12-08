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
    input_signals, output_signals = ([set(x.strip()) for x in s.split(" ")] for s in l.split(" | "))
    return SignalEntry(input_signals, output_signals)


def main():
    signal_entries = parse_args()
    output_digits = [get_output_digits(s) for s in signal_entries]
    part_1_answer = count_in_output_digits(output_digits, [1, 4, 7, 8])
    part_2_answer = sum_all_output_digits(output_digits)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def get_output_digits(signal_entry):
    known_signals = dict()
    all_signals = signal_entry.in_signals + signal_entry.out_signals
    for s in all_signals:
        if len(s) == 2:
            known_signals[1] = s
        elif len(s) == 3:
            known_signals[7] = s
        elif len(s) == 4:
            known_signals[4] = s
        elif len(s) == 7:
            known_signals[8] = s
    for s in all_signals:
        if len(s) == 5:
            if known_signals[4] and count_signals_in_common(s, known_signals[4]) == 2:
                known_signals[2] = s
                break
    for s in all_signals:
        if len(s) == 5:
            if known_signals[1] and count_signals_in_common(s, known_signals[1]) == 2:
                known_signals[3] = s
                break
            elif known_signals[7] and count_signals_in_common(s, known_signals[7]) == 3:
                known_signals[3] = s
                break
            elif known_signals[2] and count_signals_in_common(s, known_signals[2]) == 4:
                known_signals[3] = s
                break
    for s in all_signals:
        if len(s) == 5:
            if known_signals[2] and known_signals[3] and count_signals_in_common(s, known_signals[2]) != 5 and count_signals_in_common(s, known_signals[3]) != 5:
                known_signals[5] = s
                break
    for s in all_signals:
        if len(s) == 6:
            if known_signals[4] and count_signals_in_common(s, known_signals[4]) != 4\
                    and known_signals[7] and count_signals_in_common(s, known_signals[7]) == 3:
                known_signals[0] = s
                break
    for s in all_signals:
        if len(s) == 6:
            if known_signals[1] and count_signals_in_common(s, known_signals[1]) != 2:
                known_signals[6] = s
                break
            elif known_signals[7] and count_signals_in_common(s, known_signals[7]) != 3:
                known_signals[6] = s
                break
    for s in all_signals:
        if len(s) == 6:
            if known_signals[4] and count_signals_in_common(s, known_signals[4]) == 4:
                known_signals[9] = s
                break
    return [signal_to_digit(x, known_signals) for x in signal_entry.out_signals]


def count_signals_in_common(lhs, rhs):
    return len(lhs.intersection(rhs))


def signal_to_digit(signal, known_signals):
    for known_digit, known_signal in known_signals.items():
        if len(signal) == len(known_signal) and all(x in known_signal for x in signal):
            return known_digit
    raise Exception(f"signal_to_digit: Could not find digit for signal '{signal}'")


def reduce_possible_connections(potential_connections, valid_in_segments, valid_out_segments):
    for s in valid_in_segments:
        potential_connections[s] = potential_connections[s].intersection(valid_out_segments)


def count_in_output_digits(output_digits, target_digits):
    return sum(1 if x in target_digits else 0 for s in output_digits for x in s)


def sum_all_output_digits(output_digits):
    count = 0
    for x in output_digits:
        if len(x) != 4:
            raise Exception(f"sum_all_output_digits: There should be exactly 4 digits, found digits of {x}")
        count += x[0] * 1000 + x[1] * 100 + x[2] * 10 + x[3]
    return count


if __name__ == "__main__":
    main()
