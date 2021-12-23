import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()
    lines = [line.strip() for line in open(args.input_file)]
    enhancement_algorithm = [c == "#" for c in lines[0]]
    image = [[c == "#" for c in line] for line in lines[2:]]
    return enhancement_algorithm, image


def main():
    enhancement_algorithm, image = parse_args()
    enhancement = run_enhancement(image, enhancement_algorithm)
    enhancement_results = [next(enhancement) for _ in range(51)]
    part_1_answer = sum(1 if c else 0 for row in enhancement_results[2] for c in row)
    part_2_answer = sum(1 if c else 0 for row in enhancement_results[50] for c in row)
    print(f"Part 1:\n{part_1_answer}\n\nPart 2:\n{part_2_answer}")


def run_enhancement(image, enhancement_algorithm, background=False):
    image = image.copy()
    while True:
        yield image
        new_image = [[is_new_pixel_lit(image, enhancement_algorithm, x, y, background)
                      for x in range(-2, len(image[0]) + 2)] for y in range(-2, len(image) + 2)]
        background = is_new_pixel_lit([], enhancement_algorithm, 0, 0, background)
        image = new_image


def is_new_pixel_lit(image, enhancement_algorithm, x, y, background):
    binary = []
    for yi in range(y-1, y+2):
        for xi in range(x-1, x+2):
            if 0 <= yi < len(image) and 0 <= xi < len(image[0]):
                binary.append(image[yi][xi])
            else:
                binary.append(background)
    enhancement_index = sum(x * (2**i) for i, x in enumerate(reversed(binary)))
    return enhancement_algorithm[enhancement_index]


def image_to_string(image):
    return "\n".join("".join("#" if c else "." for c in row) for row in image)


if __name__ == "__main__":
    main()
