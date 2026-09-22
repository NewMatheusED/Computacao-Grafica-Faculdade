import math
from PIL import Image
from traca_reta import bresenham_line, midpoint_line


LARGURA, ALTURA = 600, 600
COR_FUNDO = (255, 255, 255)
COR_PREENCHIMENTO = (70, 130, 180)
COR_ARESTA = (0, 0, 128)
COR_CENTROIDE = (200, 0, 0)


def centroide(vertices):
    n = len(vertices)
    cx = sum(x for x, _ in vertices) / n
    cy = sum(y for _, y in vertices) / n
    return cx, cy


def transladar(vertices, destino_x, destino_y):
    cx, cy = centroide(vertices)
    dx, dy = destino_x - cx, destino_y - cy
    return [(x + dx, y + dy) for x, y in vertices]


def escalar(vertices, fator_x, fator_y, pivo=None):
    """Escala em torno do pivo: translada o pivo pra origem, escala, translada de volta.
    pivo=None usa o centroide do quadrilatero; pivo=(0, 0) usa a origem da tela."""
    px, py = pivo if pivo is not None else centroide(vertices)
    return [(px + (x - px) * fator_x, py + (y - py) * fator_y) for x, y in vertices]


def rotacionar(vertices, angulo_graus, pivo=None):
    """Rotaciona em torno do pivo: translada o pivo pra origem, aplica a matriz de
    rotacao, translada de volta. pivo=None usa o centroide; pivo=(0, 0) usa a origem da tela."""
    px, py = pivo if pivo is not None else centroide(vertices)
    ang = math.radians(angulo_graus)
    seno, cosseno = math.sin(ang), math.cos(ang)
    novos = []
    for x, y in vertices:
        vx, vy = x - px, y - py
        novos.append((
            px + vx * cosseno - vy * seno,
            py + vx * seno + vy * cosseno,
        ))
    return novos


def _pintar(pixels, x, y, cor):
    """Escreve um pixel se ele cair dentro da tela (origem no canto superior esquerdo, Y para baixo)."""
    if 0 <= x < LARGURA and 0 <= y < ALTURA:
        pixels[x, y] = cor


def _desenhar_arestas(pixels, vertices_int):
    n = len(vertices_int)
    for i in range(n):
        x1, y1 = vertices_int[i]
        x2, y2 = vertices_int[(i + 1) % n]
        for x, y in bresenham_line(x1, y1, x2, y2):
            _pintar(pixels, x, y, COR_ARESTA)


def _preencher_scanline(pixels, vertices):
    """Preenchimento por varredura (scan-line): para cada linha da tela, acha as
    interseccoes da reta y=cte com as arestas do poligono e pinta entre pares."""
    ys = [y for _, y in vertices]
    n = len(vertices)

    for y in range(math.floor(min(ys)), math.ceil(max(ys)) + 1):
        interseccoes = []
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            if y1 == y2:
                continue  # aresta horizontal nao contribui para a varredura
            if min(y1, y2) <= y < max(y1, y2):
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                interseccoes.append(x)

        interseccoes.sort()
        for i in range(0, len(interseccoes) - 1, 2):
            x_ini = round(interseccoes[i])
            x_fim = round(interseccoes[i + 1])
            for x in range(x_ini, x_fim + 1):
                _pintar(pixels, x, y, COR_PREENCHIMENTO)


def desenhar(vertices, caminho="poligono.png", mostrar=True):
    img = Image.new("RGB", (LARGURA, ALTURA), COR_FUNDO)
    pixels = img.load()

    _preencher_scanline(pixels, vertices)

    vertices_int = [(round(x), round(y)) for x, y in vertices]
    _desenhar_arestas(pixels, vertices_int)

    cx, cy = centroide(vertices)
    cx, cy = round(cx), round(cy)
    for dx in range(-3, 4):
        _pintar(pixels, cx + dx, cy, COR_CENTROIDE)
        _pintar(pixels, cx, cy + dx, COR_CENTROIDE)

    img.save(caminho)
    if mostrar:
        img.show()
    return img


def ler_ponto(indice):
    while True:
        entrada = input(f"P{indice} (x,y): ")
        partes = entrada.split(',')
        if len(partes) == 2:
            try:
                return float(partes[0]), float(partes[1])
            except ValueError:
                pass
        print("Formato invalido, use: x,y")


def ler_quadrilatero():
    print(f"Digite as coordenadas na tela ({LARGURA}x{ALTURA}, origem no canto")
    print("superior esquerdo, eixo Y crescendo para baixo).")
    return [ler_ponto(i + 1) for i in range(4)]


def executar_comando(comando, vertices):
    """Despachante: interpreta a string e chama a transformacao certa.
    E e R aceitam uma letra de pivot: O (origem da tela, 0,0) ou C
    (centroide, padrao)."""
    partes = [p.strip() for p in comando.split(',')]
    acao = partes[0].upper()

    pivo_letra = 'C'
    if len(partes) > 1 and partes[-1].upper() in ('O', 'C'):
        pivo_letra = partes[-1].upper()
        partes = partes[:-1]
    pivo = (0, 0) if pivo_letra == 'O' else None
    nome_pivo = "origem da tela (0,0)" if pivo_letra == 'O' else "centroide"

    try:
        valores = [float(p) for p in partes[1:]]
    except ValueError:
        print("Erro: parametros numericos invalidos.")
        return vertices

    if acao == 'T' and len(valores) == 2:
        vertices = transladar(vertices, *valores)
        cx, cy = centroide(vertices)
        print(f"-> Transladado para centro ({cx:.2f}, {cy:.2f})")
    elif acao == 'E' and len(valores) == 2:
        vertices = escalar(vertices, *valores, pivo=pivo)
        print(f"-> Escalado (Sx={valores[0]}, Sy={valores[1]}) em relacao a: {nome_pivo}")
    elif acao == 'R' and len(valores) == 1:
        vertices = rotacionar(vertices, valores[0], pivo=pivo)
        print(f"-> Rotacionado {valores[0]} graus em relacao a: {nome_pivo}")
    else:
        print("Comando desconhecido. Use: T,x,y | E,sx,sy[,O|C] | R,angulo[,O|C]")
        return vertices

    desenhar(vertices)
    return vertices


def main():
    print("=== RASTERIZACAO E TRANSFORMACAO DE QUADRILATEROS ===")
    vertices = ler_quadrilatero()
    desenhar(vertices)

    print("\nComandos:\n  T,x,y          -> translada o centro para (x,y)\n"
          "  E,sx,sy[,O|C]  -> escala pelos fatores sx e sy\n"
          "  R,angulo[,O|C] -> rotaciona (graus, sentido horario na tela)\n"
          "                    pivot: O=origem da tela (0,0), C=centroide (padrao)\n"
          "  SAIR")
    while True:
        comando = input("\nComando: ").strip()
        if comando.upper() == "SAIR":
            break
        vertices = executar_comando(comando, vertices)


if __name__ == "__main__":
    main()
