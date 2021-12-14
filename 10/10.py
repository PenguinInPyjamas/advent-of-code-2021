import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [line.strip() for line in open(args.input_file)]
    return parsed_lines


def main():
    lines = parse_args()
    corrupted_line_scores = [get_corrupted_line_score(x) for x in lines]
    incomplete_line_scores = [get_incomplete_line_score(x) for x in lines if get_corrupted_line_score(x) == 0]
    part_1_answer = sum(corrupted_line_scores)
    part_2_answer = sorted(incomplete_line_scores)[int(len(incomplete_line_scores) / 2)]
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def get_corrupted_line_score(line):
    reduced_line = reduce_line(line)
    for i in range(len(reduced_line) - 1):
        if reduced_line[i+1] == ")" and reduced_line[i] in ["[", "{", "<"]:
            return 3
        if reduced_line[i+1] == "]" and reduced_line[i] in ["(", "{", "<"]:
            return 57
        if reduced_line[i+1] == "}" and reduced_line[i] in ["(", "[", "<"]:
            return 1197
        if reduced_line[i+1] == ">" and reduced_line[i] in ["(", "[", "{"]:
            return 25137
    return 0


def get_incomplete_line_score(line):
    reduced_line = reduce_line(line)
    score = 0
    for c in reversed(reduced_line):
        score *= 5
        if c == "(":
            score += 1
        if c == "[":
            score += 2
        if c == "{":
            score += 3
        if c == "<":
            score += 4
    return score


def reduce_line(line):
    reduced_line = line
    while len(reduced_line) > 1:
        for i in range(len(reduced_line) - 1):
            if reduced_line[i:i+2] in ["()", "[]", "{}", "<>"]:
                reduced_line = reduced_line[:i] + reduced_line[i+2:]
                break
        else:
            break
    return reduced_line


if __name__ == "__main__":
    main()
