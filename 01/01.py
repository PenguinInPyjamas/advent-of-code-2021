import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    input_file_ints = [int(x.strip()) for x in open(args.input_file)]
    return input_file_ints


def main():
    depth_values = parse_args()

    part_1_answer = count_num_depth_increases(depth_values)
    part_2_answer = count_sliding_window_increases(depth_values, 3)

    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def count_num_depth_increases(depth_values):
    num_times_depth_increased = 0
    previous_depth = depth_values[1]
    for current_depth in depth_values:
        if current_depth > previous_depth:
            num_times_depth_increased += 1
        previous_depth = current_depth
    return num_times_depth_increased


def count_sliding_window_increases(depth_values, window_size):
    if window_size <= 0:
        raise Exception(f"Window size must be above 0 (was '{window_size}')")

    num_times_depth_increased = 0
    previous_sliding_window_value = sum(depth_values[:window_size])
    for i in range(window_size, len(depth_values)):
        current_sliding_window_value = sum(depth_values[i + 1 - window_size:i + 1])
        if current_sliding_window_value > previous_sliding_window_value:
            num_times_depth_increased += 1
        previous_sliding_window_value = current_sliding_window_value
    return num_times_depth_increased


if __name__ == "__main__":
    main()
