from PIL import Image, ImageDraw

TAMANHO_CELULA = 40
COR_AMBOS = (100, 100, 100)
COR_SO_BRESENHAM = (30, 100, 220)
COR_SO_MIDPOINT = (230, 120, 20)


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


def midpoint_line(x1, y1, x2, y2):
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
            if d < 0:
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
            if d < 0:
                d += incr_e
            else:
                d += incr_ne
                x += step_x
            y += step_y
            points.append((x, y))

    return points


def visualizar_comparacao(p1, p2, caminho="comparacao_algoritmos.png", mostrar=True):
    pontos_bresenham = set(bresenham_line(*p1, *p2))
    pontos_midpoint = set(midpoint_line(*p1, *p2))
    todos = pontos_bresenham | pontos_midpoint

    margem = 1
    x_min = min(x for x, _ in todos) - margem
    x_max = max(x for x, _ in todos) + margem
    y_min = min(y for _, y in todos) - margem
    y_max = max(y for _, y in todos) + margem
    colunas, linhas = x_max - x_min + 1, y_max - y_min + 1

    altura_legenda = 90
    img = Image.new("RGB", (colunas * TAMANHO_CELULA, linhas * TAMANHO_CELULA + altura_legenda), "white")
    desenho = ImageDraw.Draw(img)

    for gx in range(colunas + 1):
        px = gx * TAMANHO_CELULA
        desenho.line([(px, 0), (px, linhas * TAMANHO_CELULA)], fill="lightgray")
    for gy in range(linhas + 1):
        py = gy * TAMANHO_CELULA
        desenho.line([(0, py), (colunas * TAMANHO_CELULA, py)], fill="lightgray")

    ambos = pontos_bresenham & pontos_midpoint
    so_bresenham = pontos_bresenham - pontos_midpoint
    so_midpoint = pontos_midpoint - pontos_bresenham

    for conjunto, cor in [(ambos, COR_AMBOS), (so_bresenham, COR_SO_BRESENHAM), (so_midpoint, COR_SO_MIDPOINT)]:
        for x, y in conjunto:
            px, py = (x - x_min) * TAMANHO_CELULA, (y - y_min) * TAMANHO_CELULA
            desenho.rectangle([px + 2, py + 2, px + TAMANHO_CELULA - 2, py + TAMANHO_CELULA - 2], fill=cor)

    y_legenda = linhas * TAMANHO_CELULA + 10
    for texto, cor in [("Ambos escolhem", COR_AMBOS),
                        ("So Bresenham (d<=0 -> E)", COR_SO_BRESENHAM),
                        ("So Ponto Medio (d<0 -> E)", COR_SO_MIDPOINT)]:
        desenho.rectangle([10, y_legenda, 30, y_legenda + 20], fill=cor)
        desenho.text((40, y_legenda + 3), texto, fill="black")
        y_legenda += 25

    img.save(caminho)
    if mostrar:
        img.show()
    return img, so_bresenham, so_midpoint


def _parse_point(texto):
    x, y = texto.replace("(", "").replace(")", "").split(",")
    return int(x), int(y)


if __name__ == "__main__":
    print("Comparacao visual: Bresenham x Ponto Medio")
    print("(Enter sem digitar nada usa o exemplo (0,0)->(2,1), que ja diverge)")
    entrada_a = input("Ponto A (x,y) [Enter=0,0]: ").strip()
    entrada_b = input("Ponto B (x,y) [Enter=2,1]: ").strip()
    a = _parse_point(entrada_a) if entrada_a else (0, 0)
    b = _parse_point(entrada_b) if entrada_b else (2, 1)

    _, so_bresenham, so_midpoint = visualizar_comparacao(a, b)
    if so_bresenham or so_midpoint:
        print(f"Divergencia! So Bresenham escolheu: {sorted(so_bresenham)}")
        print(f"             So Ponto Medio escolheu: {sorted(so_midpoint)}")
    else:
        print("Os dois algoritmos escolheram exatamente os mesmos pixels para essa reta.")
