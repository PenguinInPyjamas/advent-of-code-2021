import argparse
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    parsed_lines = [line.strip().split("-") for line in open(args.input_file)]
    return parsed_lines


def main():
    vertices = get_vertices(parse_args())
    part_1_answer = len(get_exit_paths(vertices, False))
    part_2_answer = len(get_exit_paths(vertices))
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def get_vertices(paths):
    vertices = defaultdict(lambda: set())
    for lhs, rhs in paths:
        vertices[lhs].add(rhs)
        vertices[rhs].add(lhs)
    return vertices


def get_exit_paths(vertices, second_visit_available=True, current_vertex="start", visited_vertices=None):
    if current_vertex == "end":
        return [[]]
    if current_vertex.islower():
        if visited_vertices:
            if current_vertex in visited_vertices:
                second_visit_available = False
            else:
                visited_vertices = visited_vertices.copy()
                visited_vertices.add(current_vertex)
        else:
            visited_vertices = {current_vertex}
    if second_visit_available:
        next_vertices = vertices[current_vertex].difference({"start"})
    else:
        next_vertices = vertices[current_vertex].difference(visited_vertices.union(["start"]))
    return [[x] + path
            for x in next_vertices
            for path in get_exit_paths(vertices, second_visit_available, x, visited_vertices)]


if __name__ == "__main__":
    main()
