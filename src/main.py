import pygame
import tkinter as tk
from tkinter import filedialog
import time
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import heapq
import random
from sys import exit
from collections import deque

# ---------------------------
# Helpers / Algorithms (8-puzzle)
# ---------------------------

def manhattan(tab, objetivo):
    """Calcula a heurística de Manhattan para o 8-puzzle."""
    h = 0
    for idx, val in enumerate(tab):
        if val == 0:
            continue
        target_idx = val - 1
        cur_r, cur_c = divmod(idx, 3)
        tar_r, tar_c = divmod(target_idx, 3)
        h += abs(cur_r - tar_r) + abs(cur_c - tar_c)
    return h

def reconstruir_caminho(pai, estado):
 """Reconstrói o caminho do estado inicial ao estado dado usando o dicionário pai."""
 caminho = []
 atual = estado
	
 while atual is not None:
  caminho.append(list(atual))
  atual = pai[atual]
 return caminho[::-1]
	
def gerar_vizinhos(estado):
 """Gera estados vizinhos trocando o 0 com seus vizinhos em representação linear."""
 estado = list(estado)
 zero_index = estado.index(0)
 linha, coluna = zero_index//3, zero_index%3
	
 moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
 vizinhos = []
	
 for mx, my in moves:
  n_linha, n_coluna = linha+mx, coluna+my
  if 0 <= n_linha < 3 and 0 <= n_coluna < 3:
   n_index = n_linha*3 + n_coluna
   novo = estado.copy()
   novo[zero_index], novo[n_index] = novo[n_index], novo[zero_index]
   vizinhos.append(tuple(novo))
 return vizinhos

# ---------------------------
# Algorithms (8-puzzle)
# ---------------------------

def a_star(inicial, objetivo):
    """A* para o 8-puzzle em representação linear."""
    inicial = tuple(inicial)
    objetivo = tuple(objetivo)

    open_heap = []
    g_n = {inicial: 0}
    h_0 = manhattan(inicial, objetivo)
    heapq.heappush(open_heap, (h_0, 0, inicial))

    visitados = set()
    pai = {inicial: None}

    while open_heap:
        f, g, estado = heapq.heappop(open_heap)

        if estado in visitados:
            continue

        if estado == objetivo:
            return reconstruir_caminho(pai, estado)

        visitados.add(estado)

        for viz in gerar_vizinhos(estado):
            new_g = g + 1

            if viz in visitados:
                continue

            if new_g < g_n.get(viz, float('inf')):
                g_n[viz] = new_g
                h = manhattan(viz, objetivo)
                pai[viz] = estado
                heapq.heappush(open_heap, (new_g + h, new_g, viz))

    return None

def bfs_algorithm(inicial, objetivo):
 """BFS para o 8-puzzle em representação linear."""
 inicial = tuple(inicial)
 objetivo = tuple(objetivo)
 fila = deque()
 fila.append(inicial)
 visitados = set([inicial])
 pai = {inicial: None}
	
 while fila:
  estado = fila.popleft()
  
  if estado == objetivo:
   return reconstruir_caminho(pai, estado)
   
  for vizinho in gerar_vizinhos(estado):
   if vizinho not in visitados:
    visitados.add(vizinho)
    pai[vizinho] = estado
    fila.append(vizinho)
   
 return None

def dfs_algorithm(inicial, objetivo):
 """DFS para o 8-puzzle em representação linear."""
 inicial = tuple(inicial)
 objetivo = tuple(objetivo)
	
 pilha = deque()
 visitados = set([inicial])
	
 pilha.append(inicial)
 pai = {inicial: None}
	
 while pilha:
  estado = pilha.pop()
  
  if estado == objetivo:
   return reconstruir_caminho(pai, estado)
  
  for vizinho in reversed(gerar_vizinhos(estado)):
   if vizinho not in visitados:
    visitados.add(vizinho)
    pilha.append(vizinho)
    pai[vizinho] = estado
 return None

# ---------------------------
# Util: load imagem + 
# resolvibilidade + 
# shuffle
# ---------------------------

def carregar_imagem():
    """Abre diálogo para carregar imagem e retorna o caminho do arquivo."""
    root = tk.Tk()
    root.withdraw()

    global file_path

    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All Files", "*.*")]
    )

    if file_path:
        return file_path
    else:
        return None

def imagem_para_tabuleiro(imagem_path):
    """Carrega a imagem e divide em tiles para o tabuleiro."""
    global tile_images, main_image

    main_image = pygame.image.load(imagem_path).convert()
    main_image = pygame.transform.scale(main_image, (3*TILE_SIZE, 3*TILE_SIZE))

    tile_images = {}
    index = 1
    for row in range(3):
        for col in range(3):
            tile = main_image.subsurface(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if index <= 8:
                tile_images[index] = tile
            index += 1

def eh_resolvivel(tab_linear):
    """Verifica se o tabuleiro linear é resolvível."""
    arr = [x for x in tab_linear if x != 0]
    inversoes = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inversoes += 1
    return (inversoes % 2) == 0

def shuffle_tabuleiro(tab_in):
    """Retorna uma nova lista embaralhada resolvível (não altera tab_in)."""
    novo = tab_in[:]
    while True:
        random.shuffle(novo)
        if eh_resolvivel(novo) and novo != tab_in:
            return novo[:]

# ---------------------------
# Pygame / UI
# ---------------------------

pygame.init()
WIDTH, HEIGHT = 820, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Game")
FONT_BIG = pygame.font.SysFont('arial', 43, bold=True)
FONT_SMALL = pygame.font.SysFont('arial', 20, bold=True)
WHITE = (255,255,255)
BG = (20, 20, 20)
BLUE = (0, 110, 255)
MAGENTA = (190, 0, 190)
LARANJA = (230, 140, 0)
GRAY = (100, 100, 100)
FPS = 60

# grid visual: usa tamanho 100x100 por tile (3x3) e deixa margem
TILE_SIZE = 80
TILE_PADDING = 5
GRID_ORIGIN = (10, 10) # x,y
# botãoes à direita
BTN_X = 410
BTN_WIDTH, BTN_HEIGHT = 100, 44

# estado inicial (linear)
tabuleiro = [1, 2, 3, 4, 5, 0, 6, 7, 8] 
objetivo = [1,2,3,4,5,6,7,8,0]

def atualizar_grid_rects(tab_linear):
    """Retorna lista de pygame.Rect (ou None) correspondente ao board linear."""
    rects = []
    for i, val in enumerate(tab_linear):
        x = GRID_ORIGIN[0] + (i % 3) * (TILE_SIZE + TILE_PADDING)
        y = GRID_ORIGIN[1] + (i // 3) * (TILE_SIZE + TILE_PADDING)
        if val != 0:
            rects.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
        else:
            rects.append(None)
    return rects

grid_pecas = atualizar_grid_rects(tabuleiro)

# controle de animação do A*
animando = False
anim_frames = [] # lista de estados lineares
anim_index = 0
anim_interval = 300 # ms entre frames
last_anim_time = 0
mostrar_relatorio = False
mov = 0
player_mov = 0
bfs_time = 0
a_star_time = 0
jogo_concluido = False
bloqueio_input = False

clock = pygame.time.Clock()

def desenhar(imagem_path=None):
    """Desenha o estado atual na tela."""
    relatorio = ""
    SCREEN.fill(BG)
    if imagem_path and main_image:
        # desenhar tiles com imagem
        for i, val in enumerate(tabuleiro):
            x = GRID_ORIGIN[0] + (i % 3) * (TILE_SIZE + TILE_PADDING)
            y = GRID_ORIGIN[1] + (i // 3) * (TILE_SIZE + TILE_PADDING)
            if val != 0:
                tile_img = tile_images.get(val)
                if tile_img:
                    SCREEN.blit(tile_img, (x, y))
            else:
                # desenha retângulo vazio sutil
                pygame.draw.rect(SCREEN, (50,50,50), (x, y, TILE_SIZE, TILE_SIZE))
    else:
        # desenhar tiles sem imagem
        for i, val in enumerate(tabuleiro):
            x = GRID_ORIGIN[0] + (i % 3) * (TILE_SIZE + TILE_PADDING)
            y = GRID_ORIGIN[1] + (i // 3) * (TILE_SIZE + TILE_PADDING)
            if val != 0:
                # contorno + número
                pygame.draw.rect(SCREEN, BLUE, (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)
                text = FONT_BIG.render(str(val), True, WHITE)
                tr = text.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
                SCREEN.blit(text, tr)
            else:
                # desenha retângulo vazio sutil
                pygame.draw.rect(SCREEN, (50,50,50), (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)

    # botões
    btn_resolver = pygame.Rect(BTN_X, 20, BTN_WIDTH, BTN_HEIGHT)
    btn_resolver_BFS = pygame.Rect(BTN_X+120, 20, BTN_WIDTH, BTN_HEIGHT)
    btn_resolver_DFS = pygame.Rect(BTN_X+240, 20, BTN_WIDTH, BTN_HEIGHT)
    btn_shuffle = pygame.Rect(BTN_X, 90, BTN_WIDTH, BTN_HEIGHT)
    btn_escolher_imagem = pygame.Rect(BTN_X+120, 90, BTN_WIDTH, BTN_HEIGHT)
    btn_recomecar = pygame.Rect(BTN_X+240, 90, BTN_WIDTH, BTN_HEIGHT)
    

    pygame.draw.rect(SCREEN, BLUE, btn_resolver, border_radius=8)
    pygame.draw.rect(SCREEN, BLUE, btn_resolver_BFS, border_radius=8)
    pygame.draw.rect(SCREEN, BLUE, btn_resolver_DFS, border_radius=8)
    pygame.draw.rect(SCREEN, MAGENTA, btn_shuffle, border_radius=8)
    pygame.draw.rect(SCREEN, GRAY, btn_escolher_imagem, border_radius=8)
    
    SCREEN.blit(FONT_SMALL.render("A*", True, WHITE), (BTN_X + 15, 30))
    SCREEN.blit(FONT_SMALL.render("BFS", True, WHITE), (BTN_X + 135, 30))
    SCREEN.blit(FONT_SMALL.render("DFS", True, WHITE), (BTN_X + 255, 30))
    SCREEN.blit(FONT_SMALL.render("Shuffle", True, WHITE), (BTN_X + 15, 100))
    SCREEN.blit(FONT_SMALL.render("Image", True, WHITE), (BTN_X + 135, 100))
    if jogo_concluido:
      pygame.draw.rect(SCREEN, LARANJA, btn_recomecar, border_radius=8)
      SCREEN.blit(FONT_SMALL.render("Restart", True, WHITE), (BTN_X + 255, 100))

    # info
    info = "Resolvendo..." if animando else ""
    SCREEN.blit(FONT_SMALL.render(info, True, WHITE), (BTN_X, 160))
    if mostrar_relatorio:
      relatorio_linhas = []

      # Caso só IA tenha resolvido
      if player_mov == 0 and mov > 0:
          relatorio_linhas.append(f"IA movimentos: {mov - 1}")
          tempo = bfs_time if bfs_time > 0 else a_star_time
          relatorio_linhas.append(f"Tempo: {tempo:.5f}s")

      # Caso só o player tenha resolvido
      elif mov == 0 and player_mov > 0:
          relatorio_linhas.append(f"Player movimentos: {player_mov}")

      # Caso ambos tenham feito movimentos
      else:
          relatorio_linhas.append(f"Player movimentos: {player_mov}")
          relatorio_linhas.append(f"IA movimentos: {mov - 1}")
          relatorio_linhas.append(f"Total movimentos: {player_mov + mov - 1}")

          tempo = bfs_time if bfs_time > 0 else a_star_time
          if tempo > 0:
              relatorio_linhas.append(f"Tempo IA: {tempo:.5f}s")
      relatorio = "\n".join(relatorio_linhas) if relatorio_linhas else ""

    draw_multiline_text(SCREEN, relatorio, BTN_X, 180, FONT_SMALL, (255,255,255))
    pygame.display.flip()
    
def draw_multiline_text(surface, text, x, y, font, color):
    """Desenha texto multilinha em surface a partir de (x,y)."""
    linhas = text.split("\n")
    for i, linha in enumerate(linhas):
        img = font.render(linha, True, color)
        surface.blit(img, (x, y + i * (img.get_height() + 5)))
           

# ---------------------------
# Loop principal
# ---------------------------

running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN and event.button == 1 and not bloqueio_input:
            mx, my = event.pos
            # botões
            btn_resolver = pygame.Rect(BTN_X, 20, BTN_WIDTH, BTN_HEIGHT)
            btn_resolver_BFS = pygame.Rect(BTN_X+120, 20, BTN_WIDTH, BTN_HEIGHT)
            btn_resolver_DFS = pygame.Rect(BTN_X+240, 20, BTN_WIDTH, BTN_HEIGHT)
            btn_shuffle = pygame.Rect(BTN_X, 90, BTN_WIDTH, BTN_HEIGHT)
            btn_escolher_imagem = pygame.Rect(BTN_X+120, 90, BTN_WIDTH, BTN_HEIGHT)
            btn_recomecar = pygame.Rect(BTN_X+240, 90, BTN_WIDTH, BTN_HEIGHT)
           

            if btn_resolver.collidepoint(mx, my) and not animando:
                # rodar A*
                inicial = tabuleiro[:]
                inicio = time.time()
                resultado = a_star(inicial, objetivo)
                a_star_time = time.time() - inicio
                if resultado:
                    # converter
                    anim_frames = resultado
                    anim_index = 0
                    animando = True
                    last_anim_time = pygame.time.get_ticks()
                    mov = len(resultado)
                    mostrar_relatorio = True
                else:
                    print("Sem solução encontrada (improvável).")
                continue
                
            if btn_resolver_BFS.collidepoint(mx, my) and not animando:
                # rodar BFS
                inicial = tabuleiro[:]
                inicio = time.time()
                resultado = bfs_algorithm(inicial, objetivo)
                bfs_time = time.time() - inicio
                if resultado:
                    # converter
                    anim_frames = resultado
                    anim_index = 0
                    animando = True
                    last_anim_time = pygame.time.get_ticks()
                    mov = len(resultado)
                    mostrar_relatorio = True
                else:
                    print("Sem solução encontrada (improvável).")
                continue
            if btn_resolver_DFS.collidepoint(mx, my) and not animando:
                # rodar DFS
                inicial = tabuleiro[:]
                inicio = time.time()
                resultado = dfs_algorithm(inicial, objetivo)
                dfs_time = time.time() - inicio
                if resultado:
                    # converter
                    anim_frames = resultado
                    anim_index = 0
                    animando = True
                    last_anim_time = pygame.time.get_ticks()
                    mov = len(resultado)
                    mostrar_relatorio = True
                else:
                    print("Sem solução encontrada (improvável).")
                continue
            
            if btn_shuffle.collidepoint(mx, my) and not animando:
                tabuleiro = shuffle_tabuleiro(tabuleiro)
                grid_pecas = atualizar_grid_rects(tabuleiro)
                mov = 0
                player_mov = 0
                jogo_concluido = False
                bloqueio_input = False
                continue
            
            if btn_escolher_imagem.collidepoint(mx, my) and not animando:
                imagem_path = carregar_imagem()
                if imagem_path:
                    imagem_para_tabuleiro(imagem_path)
                continue
              

            # se está animando, ignora cliques no tabuleiro
            if animando:
                continue

            # clique no tabuleiro: procura rect clicado
            clicked_index = None
            for idx, rect in enumerate(grid_pecas):
                if rect is not None and rect.collidepoint(mx, my):
                    clicked_index = idx
                    break

            if clicked_index is not None:
                # verificar vizinhança do espaço vazio
                zero_idx = tabuleiro.index(0)
                r0, c0 = divmod(zero_idx, 3)
                ri, ci = divmod(clicked_index, 3)
                if abs(r0 - ri) + abs(c0 - ci) == 1:
                    # troca simples: atualiza tabuleiro e recalcula grid
                    tabuleiro[zero_idx], tabuleiro[clicked_index] = tabuleiro[clicked_index], tabuleiro[zero_idx]
                    grid_pecas = atualizar_grid_rects(tabuleiro)
                    player_mov += 1
                # caso contrário, ignore clique
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
          mx, my = event.pos
          btn_recomecar = pygame.Rect(BTN_X+240, 90, BTN_WIDTH, BTN_HEIGHT)
          if jogo_concluido:
                if btn_recomecar.collidepoint(mx, my):
                    tabuleiro = shuffle_tabuleiro(tabuleiro)
                    grid_pecas = atualizar_grid_rects(tabuleiro)
                    mov = 0
                    player_mov = 0
                    jogo_concluido = False
                    bloqueio_input = False
                    mostrar_relatorio = False
                continue
    # animação do A*: trocar estados a cada intervalo
    if animando:
        now = pygame.time.get_ticks()
        if now - last_anim_time >= anim_interval:
            if anim_index < len(anim_frames):
                tabuleiro = anim_frames[anim_index][:]
                grid_pecas = atualizar_grid_rects(tabuleiro)
                anim_index += 1
                last_anim_time = now
            else:
                animando = False
                anim_frames = []
                anim_index = 0
                # garantir grid final sincronizado
                grid_pecas = atualizar_grid_rects(tabuleiro)
    if tabuleiro == objetivo:
      mostrar_relatorio = True
      jogo_concluido = True
      bloqueio_input = True
    else:
      jogo_concluido = False
      bloqueio_input = False
     
    desenhar(file_path if 'file_path' in globals() else None)

# final cleanup
pygame.quit()
exit()