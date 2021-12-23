import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    lines = [line.strip() for line in open(args.input_file)]
    return int(lines[0].split(": ")[1]), int(lines[1].split(": ")[1])


def main():
    player_1_start, player_2_start = parse_args()
    simple_game_results = list(play_dirac_dice([player_1_start, player_2_start]))
    part_1_answer = min(simple_game_results[-1]) * len(simple_game_results) * 3

    quantum_game_results = get_quantum_dirac_dice_results([player_1_start, player_2_start])
    part_2_answer = max(quantum_game_results)

    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def play_dirac_dice(start_positions):
    positions = start_positions.copy()
    scores = [0, 0]
    player_num = -1

    def dice_roll_generator():
        while True:
            for x in range(1, 101):
                yield x
    dice_rolls = dice_roll_generator()

    while scores[0] < 1000 and scores[1] < 1000:
        player_num = (player_num + 1) % 2
        rolls = [next(dice_rolls), next(dice_rolls), next(dice_rolls)]
        positions[player_num] = (positions[player_num] + sum(rolls) - 1) % 10 + 1
        scores[player_num] += positions[player_num]
        yield scores


# Pre-calculated results of rolling 3 d3s
quantum_dice_results = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def get_quantum_dirac_dice_results(start_positions):
    won_games = [0, 0]
    game_state_counts = dict(((p1_pos, p2_pos, p1_score, p2_score), 0)
                             for p1_pos in range(1, 11) for p2_pos in range(1, 11)
                             for p1_score in range(21) for p2_score in range(21))
    game_state_counts[(start_positions[0], start_positions[1], 0, 0)] = 1
    turn_player = -1
    while any(count > 0 for count in game_state_counts.values()):
        turn_player = (turn_player + 1) % 2
        new_game_state_counts = dict(((p1_pos, p2_pos, p1_score, p2_score), 0)
                                     for p1_pos in range(1, 11) for p2_pos in range(1, 11)
                                     for p1_score in range(21) for p2_score in range(21))
        for roll_value, roll_count in quantum_dice_results.items():
            for game_state_values, game_state_count in game_state_counts.items():
                p1_pos, p2_pos, p1_score, p2_score = game_state_values
                if turn_player == 0:
                    new_pos = (p1_pos + roll_value - 1) % 10 + 1
                    new_score = p1_score + new_pos
                    if new_score >= 21:
                        won_games[0] += game_state_count * roll_count
                    else:
                        new_game_state_counts[(new_pos, p2_pos, new_score, p2_score)] += game_state_count * roll_count
                else:
                    new_pos = (p2_pos + roll_value - 1) % 10 + 1
                    new_score = p2_score + new_pos
                    if new_score >= 21:
                        won_games[1] += game_state_count * roll_count
                    else:
                        new_game_state_counts[(p1_pos, new_pos, p1_score, new_score)] += game_state_count * roll_count
        game_state_counts = new_game_state_counts
    return won_games


if __name__ == "__main__":
    main()
