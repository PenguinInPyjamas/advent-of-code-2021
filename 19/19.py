import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    lines = [line.strip() for line in open(args.input_file) if line[0:3] != "---"]
    locations = []
    scanners = []
    for line in lines:
        if len(line) == 0:
            scanners.append(locations)
            locations = []
            continue
        locations.append(tuple(int(x) for x in line.split(",")))
    scanners.append(locations)
    return scanners


def main():
    unaligned_scanners = parse_args()
    aligned_scanners, scanner_locations = align_scanners(unaligned_scanners)
    unique_beacons = set(x for scanner in aligned_scanners for x in scanner)
    part_1_answer = len(unique_beacons)
    part_2_answer = max(manhattan_distance(scanner_locations[x], scanner_locations[y])
                        for x in range(len(scanner_locations)) for y in range(x + 1, len(scanner_locations)))
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def align_scanners(unaligned_scanners):
    aligned_scanners = [unaligned_scanners[0]]
    unchecked_aligned_scanners = [unaligned_scanners[0]]
    scanner_locations = [(0, 0, 0)]
    remaining_scanner_indices = set(range(1, len(unaligned_scanners)))
    while len(unchecked_aligned_scanners) > 0:
        print(f"\r{len(aligned_scanners)} of {len(unaligned_scanners)} complete...", end='')
        new_aligned_scanners = []
        for positions in unchecked_aligned_scanners:
            aligned_scanner_indices = set()
            for i in remaining_scanner_indices:
                offset = get_offset(positions, unaligned_scanners[i])
                if offset:
                    aligned_scanner = [apply_offset(offset, x) for x in unaligned_scanners[i]]
                    aligned_scanners.append(aligned_scanner)
                    scanner_locations.append(offset[1])
                    new_aligned_scanners.append(aligned_scanner)
                    aligned_scanner_indices.add(i)
            for i in aligned_scanner_indices:
                remaining_scanner_indices.remove(i)
        unchecked_aligned_scanners = new_aligned_scanners
    print("\r                              \r", end='')
    return aligned_scanners, scanner_locations


def get_offset(original_positions, new_positions):
    for rot_x, rot_y, rot_z in ((x, y, z) for x in range(4) for y in range(4) for z in range(4)):
        rotated_positions = [rotate_multiple(p, rot_x, rot_y, rot_z) for p in new_positions]
        for original_position in original_positions:
            for rotated_position in rotated_positions:
                offset_translation = minus_positions(original_position, rotated_position)
                num_matching_points = sum(1 if add_positions(rp, offset_translation) in original_positions
                                          else 0 for rp in rotated_positions)
                if num_matching_points >= 12:
                    return (rot_x, rot_y, rot_z), offset_translation
    return None


def apply_offset(offset, p):
    return add_positions(rotate_multiple(p, offset[0][0], offset[0][1], offset[0][2]), offset[1])


def rot_90(p, axis):
    if axis == 0:
        return p[0], p[2], -p[1]
    if axis == 1:
        return -p[2], p[1], p[0]
    if axis == 2:
        return -p[1], p[0], p[2]
    raise Exception(f"rot_90: bad axis '{axis}'")


def rotate_multiple(p, x_rot_num, y_rot_num, z_rot_num):
    for _ in range(x_rot_num):
        p = rot_90(p, 0)
    for _ in range(y_rot_num):
        p = rot_90(p, 1)
    for _ in range(z_rot_num):
        p = rot_90(p, 2)
    return p


def add_positions(x, y):
    return x[0] + y[0], x[1] + y[1], x[2] + y[2]


def minus_positions(x, y):
    return x[0] - y[0], x[1] - y[1], x[2] - y[2]


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])


if __name__ == "__main__":
    main()
