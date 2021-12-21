import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Area = namedtuple("Area", ["x_start", "y_start", "x_end", "y_end"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    line = [line for line in open(args.input_file)][0]
    x1 = int(line.split("=")[1].split("..")[0])
    x2 = int(line.split("..")[1].split(",")[0])
    y1 = int(line.split("=")[2].split("..")[0])
    y2 = int(line.split("..")[2].strip())
    return Area(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))


def main():
    target_area = parse_args()
    trajectories = find_trajectories(target_area)
    part_1_answer = max(location.y for trajectory in trajectories for location, _ in trajectory)
    part_2_answer = len(trajectories)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def find_trajectories(target_area):
    trajectories = []
    for y in range(target_area.y_start, 300):
        for x in range(1, target_area.x_end + 1):
            trajectory_generator = simulate_probe(Point(x, y))
            trajectory = []
            for location, velocity in trajectory_generator:
                if location.x > target_area.x_end or (location.y < target_area.y_start and velocity.y < 0):
                    break
                trajectory.append((location, velocity))
                if target_area.x_start <= location.x <= target_area.x_end \
                        and target_area.y_start <= location.y <= target_area.y_end:
                    trajectories.append(trajectory)
                    break
    return trajectories


def simulate_probe(velocity):
    probe_location = Point(0, 0)
    while True:
        probe_location = Point(probe_location.x + velocity.x, probe_location.y + velocity.y)
        if velocity.x > 0:
            velocity = Point(velocity.x - 1, velocity.y)
        elif velocity.x < 0:
            velocity = Point(velocity.x + 1, velocity.y)
        velocity = Point(velocity.x, velocity.y - 1)
        yield probe_location, velocity


if __name__ == "__main__":
    main()
