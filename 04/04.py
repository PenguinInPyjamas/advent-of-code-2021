import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    input_lines = [x.strip() for x in open(args.input_file)]
    bingo_numbers = [int(x) for x in input_lines[0].split(",")]
    bingo_boards = parse_bingo_boards(input_lines[2:])
    return bingo_numbers, bingo_boards


def parse_bingo_boards(raw_board_lines):
    bingo_board_ints = [[int(x) for x in line.split(" ") if len(x) > 0] for line in raw_board_lines]
    bingo_boards = []
    current_bingo_board = []
    for line in bingo_board_ints:
        if len(line) == 0:
            bingo_boards.append(current_bingo_board)
            current_bingo_board = []
        else:
            current_bingo_board.append(line)
    bingo_boards.append(current_bingo_board)
    return bingo_boards


def main():
    bingo_numbers, bingo_boards = parse_args()

    bingo_scores = calculate_bingo_scores(bingo_numbers, bingo_boards)

    part_1_answer = bingo_scores[0]
    part_2_answer = bingo_scores[-1]
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def calculate_bingo_scores(numbers, boards):
    board_scores = []
    winning_location_groups = []
    for x in range(5):
        winning_location_groups.append([(x, y) for y in range(5)])
    for y in range(5):
        winning_location_groups.append([(x, y) for x in range(5)])

    called_numbers = set()
    remaining_boards = set(range(len(boards)))
    for last_called_number in numbers:
        called_numbers.add(last_called_number)
        finished_boards = set()
        for board_index in remaining_boards:
            if any(all(boards[board_index][x][y] in called_numbers for x, y in g) for g in winning_location_groups):
                finished_boards.add(board_index)
        for board_index in finished_boards:
            board_scores.append(calculate_score(called_numbers, last_called_number, boards[board_index]))
            remaining_boards.remove(board_index)
    return board_scores


def calculate_score(called_numbers, last_called_number, board):
    return sum(x for row in board for x in row if x not in called_numbers) * last_called_number


if __name__ == "__main__":
    main()
