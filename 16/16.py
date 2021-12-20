import argparse
from collections import namedtuple
from functools import reduce

Packet = namedtuple("Packet", ["version", "type_id", "value", "remaining_transmission"])
TYPE_SUM = ['0', '0', '0']
TYPE_PRODUCT = ['0', '0', '1']
TYPE_MIN = ['0', '1', '0']
TYPE_MAX = ['0', '1', '1']
TYPE_LITERAL = ['1', '0', '0']
TYPE_GREATER_THAN = ['1', '0', '1']
TYPE_LESS_THAN = ['1', '1', '0']
TYPE_EQUAL_TO = ['1', '1', '1']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [line.strip() for line in open(args.input_file)]
    return parsed_lines[0]


def main():
    transmission_hex = parse_args()
    transmission_bin = []
    for hex_digit in transmission_hex:
        transmission_bin += hex_to_binary(hex_digit)
    decoded_packets = [x for x in parse_transmission(transmission_bin)]
    part_1_answer = count_version_numbers(decoded_packets)
    part_2_answer = calculate_packet_value(decoded_packets[0])
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def parse_transmission(transmission):
    remaining_transmission = [x for x in transmission]
    while len(remaining_transmission) > 6:
        version_bits = remaining_transmission[0:3]
        type_bits = remaining_transmission[3:6]
        remaining_transmission = remaining_transmission[6:]
        if type_bits == TYPE_LITERAL:
            value_bits = []
            while True:
                end_of_value = remaining_transmission[0] == '0'
                value_bits += remaining_transmission[1:5]
                remaining_transmission = remaining_transmission[5:]
                if end_of_value:
                    break
            yield Packet(version_bits, type_bits, bin_to_dec(value_bits), remaining_transmission)
        else:
            length_type_id = remaining_transmission[0]
            remaining_transmission = remaining_transmission[1:]
            if length_type_id == '0':
                len_sub_packet_bits = bin_to_dec(remaining_transmission[:15])
                remaining_transmission = remaining_transmission[15:]
                sub_packets = [x for x in parse_transmission(remaining_transmission[:len_sub_packet_bits])]
                remaining_transmission = remaining_transmission[len_sub_packet_bits:]
                yield Packet(version_bits, type_bits, sub_packets, remaining_transmission)
            else:
                num_sub_packets = bin_to_dec(remaining_transmission[:11])
                remaining_transmission = remaining_transmission[11:]
                parse_remaining_transmission = parse_transmission(remaining_transmission)
                sub_packets = [next(parse_remaining_transmission) for _ in range(num_sub_packets)]
                remaining_transmission = sub_packets[-1].remaining_transmission
                yield Packet(version_bits, type_bits, sub_packets, remaining_transmission)


def calculate_packet_value(packet):
    _, type_bits, value, _ = packet
    if type_bits == TYPE_SUM:
        return sum(calculate_packet_value(p) for p in value)
    if type_bits == TYPE_PRODUCT:
        return reduce(lambda x, y: x * y, (calculate_packet_value(p) for p in value), 1)
    if type_bits == TYPE_MIN:
        return reduce(min, (calculate_packet_value(p) for p in value))
    if type_bits == TYPE_MAX:
        return reduce(max, (calculate_packet_value(p) for p in value))
    if type_bits == TYPE_LITERAL:
        return value
    if type_bits == TYPE_GREATER_THAN:
        return 1 if calculate_packet_value(value[0]) > calculate_packet_value(value[1]) else 0
    if type_bits == TYPE_LESS_THAN:
        return 1 if calculate_packet_value(value[0]) < calculate_packet_value(value[1]) else 0
    if type_bits == TYPE_EQUAL_TO:
        return 1 if calculate_packet_value(value[0]) == calculate_packet_value(value[1]) else 0
    raise Exception(f"calculate_packets_value: Type bits were invalid: '{type_bits}'")


def count_version_numbers(packets):
    count = 0
    for version, type_bits, value, _ in packets:
        count += bin_to_dec(version)
        if type_bits != TYPE_LITERAL:
            count += count_version_numbers(value)
    return count


def hex_to_binary(x):
    if x == "A":
        x = 10
    if x == "B":
        x = 11
    if x == "C":
        x = 12
    if x == "D":
        x = 13
    if x == "E":
        x = 14
    if x == "F":
        x = 15
    else:
        x = int(x)
    binary_digits = bin(x)[2:]
    return ["0" for _ in range(3 - (len(binary_digits) - 1) % 4)] + list(binary_digits)


def bin_to_hex(x):
    hex_digits = hex(int(x[0]) * 8 + int(x[1]) * 4 + int(x[2]) * 2 + int(x[3]) * 1)[2:]
    return ["0" for _ in range(3 - (len(hex_digits) - 1) % 4)] + list(hex_digits)


def bin_to_dec(x):
    return sum(2**index * int(digit) for index, digit in enumerate(reversed(x)))


def bin_to_str(x):
    out = ""
    for c in x:
        out += c
    return out


if __name__ == "__main__":
    main()
