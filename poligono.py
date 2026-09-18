# https://claude.ai/artifact/4Gip9cfzwttoTiakYRH6rZ

import math
import matplotlib.pyplot as plt

def centroide(vertices):
    n = len(vertices)
    cx = sum(x for x, _ in vertices) / n
    cy = sum(y for _, y in vertices) / n
    return cx, cy

def transladar(vertices, destino_x, destino_y):
    cx, cy = centroide(vertices)
    dx, dy = destino_x - cx, destino_y - cy
    return [(x + dx, y + dy) for x, y in vertices]

def escalar(vertices, fator_x, fator_y):
    cx, cy = centroide(vertices)
    return [(cx + (x - cx) * fator_x, cy + (y - cy) * fator_y) for x, y in vertices]

def rotacionar(vertices, angulo_graus):
    cx, cy = centroide(vertices)
    ang = math.radians(angulo_graus)
    seno, cosseno = math.sin(ang), math.cos(ang)
    novos = []
    for x, y in vertices:
        vx, vy = x - cx, y - cy
        novos.append((
            cx + vx * cosseno - vy * seno,
            cy + vx * seno + vy * cosseno,
        ))
    return novos






janela = {'xmin': -15, 'xmax': 15, 'ymin': -15, 'ymax': 15}

def _expandir_janela(xs, ys):
    margem = 5
    janela['xmin'] = min(janela['xmin'], min(xs) - margem)
    janela['xmax'] = max(janela['xmax'], max(xs) + margem)
    janela['ymin'] = min(janela['ymin'], min(ys) - margem)
    janela['ymax'] = max(janela['ymax'], max(ys) + margem)

def desenhar(vertices):
    xs = [p[0] for p in vertices]
    ys = [p[1] for p in vertices]

    plt.clf()
    eixo = plt.gca()
    eixo.fill(xs, ys, color='steelblue', alpha=0.6, edgecolor='navy', linewidth=2)

    _expandir_janela(xs, ys)
    eixo.set_xlim(janela['xmin'], janela['xmax'])
    eixo.set_ylim(janela['ymin'], janela['ymax'])

    eixo.axhline(0, color='black', linewidth=1)
    eixo.axvline(0, color='black', linewidth=1)

    cx, cy = centroide(vertices)
    eixo.plot(cx, cy, marker='x', color='red', markersize=8)

    eixo.grid(color='lightgray', linestyle='--', linewidth=0.5)
    eixo.set_aspect('equal', adjustable='box')
    eixo.set_title(f"Poligono ({len(vertices)} vertices)")

    plt.draw()
    plt.pause(0.1)






def ler_vertice(indice):
    while True:
        entrada = input(f"Vertice {indice} (x,y): ")
        partes = entrada.split(',')
        if len(partes) == 2:
            try:
                return float(partes[0]), float(partes[1])
            except ValueError:
                pass
        print("Formato invalido, use: x,y")

def ler_poligono():
    while True:
        try:
            n = int(input("Quantos vertices tem o poligono? (minimo 3): "))
            if n >= 3:
                break
        except ValueError:
            pass
        print("Digite um numero inteiro >= 3.")
    return [ler_vertice(i + 1) for i in range(n)]

def executar_comando(comando, vertices):
    """Despachante: interpreta a string e chama a transformacao certa."""
    partes = [p.strip() for p in comando.split(',')]
    acao = partes[0].upper()
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
        vertices = escalar(vertices, *valores)
        print(f"-> Escalado (Sx={valores[0]}, Sy={valores[1]})")
    elif acao == 'R' and len(valores) == 1:
        vertices = rotacionar(vertices, valores[0])
        print(f"-> Rotacionado {valores[0]} graus")
    else:
        print("Comando desconhecido. Use: T,x,y | E,sx,sy | R,angulo")
        return vertices

    desenhar(vertices)
    return vertices

def main():
    plt.ion()
    print("=== TRANSFORMACOES GEOMETRICAS EM POLIGONOS ===")
    vertices = ler_poligono()
    desenhar(vertices)

    print("\nComandos:\n  T,x,y     -> translada o centro para (x,y)\n"
          "  E,sx,sy   -> escala pelos fatores sx e sy\n"
          "  R,angulo  -> rotaciona (graus, sentido anti-horario)\n"
          "  SAIR")
    while True:
        comando = input("\nComando: ").strip()
        if comando.upper() == "SAIR":
            break
        vertices = executar_comando(comando, vertices)

if __name__ == "__main__":
    main()
