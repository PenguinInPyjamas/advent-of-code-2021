import argparse
from collections import namedtuple

Command = namedtuple('Command', ['direction', 'magnitude'])
Location = namedtuple('Location', ['distance', 'depth', 'aim'])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    input_file_commands = [parse_command(x.strip()) for x in open(args.input_file)]
    return input_file_commands


def parse_command(s):
    direction, s_distance = s.split(" ")
    if direction not in ['forward', 'down', 'up']:
        raise Exception(f"Direction not valid ('{direction}')")
    return Command(direction, int(s_distance))


def follow_command_basic(location, command):
    if command.direction == 'forward':
        return Location(location.distance + command.magnitude, location.depth, location.aim)
    elif command.direction == 'down':
        return Location(location.distance, location.depth + command.magnitude, location.aim)
    elif command.direction == 'up':
        return Location(location.distance, location.depth - command.magnitude, location.aim)


def follow_command_with_aim(location, command):
    if command.direction == 'forward':
        return Location(location.distance + command.magnitude, location.depth + location.aim * command.magnitude, location.aim)
    elif command.direction == 'down':
        return Location(location.distance, location.depth, location.aim + command.magnitude)
    elif command.direction == 'up':
        return Location(location.distance, location.depth, location.aim - command.magnitude)


def follow_commands(initial_location, commands, use_aim=False):
    current_location = initial_location
    for c in commands:
        if use_aim:
            current_location = follow_command_with_aim(current_location, c)
        else:
            current_location = follow_command_basic(current_location, c)
    return current_location


def main():
    commands = parse_args()

    final_location_basic = follow_commands(Location(0, 0, 0), commands)
    final_location_with_aim = follow_commands(Location(0, 0, 0), commands, True)

    part_1_answer = final_location_basic.distance * final_location_basic.depth
    part_2_answer = final_location_with_aim.distance * final_location_with_aim.depth

    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


if __name__ == "__main__":
    main()
