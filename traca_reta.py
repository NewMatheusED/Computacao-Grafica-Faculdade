def bresenham_line(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    dx, dy = abs(dx), abs(dy)

    x, y = x1, y1
    points = [(x, y)]

    if dx >= dy:
        d = 2 * dy - dx
        incr_e, incr_ne = 2 * dy, 2 * (dy - dx)
        for _ in range(dx):
            if d <= 0:
                d += incr_e
            else:
                d += incr_ne
                y += step_y
            x += step_x
            points.append((x, y))
    else:
        d = 2 * dx - dy
        incr_e, incr_ne = 2 * dx, 2 * (dx - dy)
        for _ in range(dy):
            if d <= 0:
                d += incr_e
            else:
                d += incr_ne
                x += step_x
            y += step_y
            points.append((x, y))

    return points


def draw_line_matrix(a, b, size=None):
    x1, y1 = a
    x2, y2 = b
    if size is None:
        size = max(x1, y1, x2, y2) + 1

    matrix = [[0] * size for _ in range(size)]
    for x, y in bresenham_line(x1, y1, x2, y2):
        matrix[y][x] = 1
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print("".join(f"[{v}]" for v in row))


def _parse_point(texto):
    x, y = texto.replace("(", "").replace(")", "").split(",")
    return int(x), int(y)


if __name__ == "__main__":

    a = _parse_point(input("Ponto A (x,y): "))
    b = _parse_point(input("Ponto B (x,y): "))

    print_matrix(draw_line_matrix(a, b))
