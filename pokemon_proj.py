import random
import pygame
import sys

pygame.init()
pygame.font.init()

LARGURA_TILE = 32
ALTURA_TILE = 32
LARGURA_TELA = 12 * LARGURA_TILE
ALTURA_TELA = 20 * ALTURA_TILE
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Pokémon Route 1")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 16)
fonte_grande = pygame.font.SysFont("Arial", 24, bold=True)

IMAGENS_TILES = {
    ' ': pygame.image.load("imagens_pokemon/chao_pokemon.png/chao_poktest.png"),
    'A': pygame.image.load("imagens_pokemon/arvore_pokemon.png/arvore_pokemontest.png"),
    'E': pygame.image.load("imagens_pokemon/elevacao_pokemon.png/elevacao_pokemontest.png"),
    'G': pygame.image.load("imagens_pokemon/grama_pokemon.png/grama_poktest.png")
}

for chave in IMAGENS_TILES:
    IMAGENS_TILES[chave] = pygame.transform.scale(IMAGENS_TILES[chave], (LARGURA_TILE, ALTURA_TILE))

img_jogador_frente = pygame.transform.scale(pygame.image.load("imagens_pokemon/jogador_de_frente.png/jogador_pokemontest.png"), (LARGURA_TILE, ALTURA_TILE))
img_jogador_costas = pygame.transform.scale(pygame.image.load("imagens_pokemon/jogador_de_costas_pokemon.png/jogador_de_costas_poktest.png"), (LARGURA_TILE, ALTURA_TILE))
img_jogador_atual = img_jogador_frente

IMAGENS_POKEMONS = {
    "Ratata": pygame.image.load("imagens_pokemon/ratata_pok.png/ratata_poktest.png"),
    "Pidgey": pygame.image.load("imagens_pokemon/pidgey_pok.png/pidgey_poktest.png"),
    "Weedle": pygame.image.load("imagens_pokemon/weedle_pok.png/weedle_poktest.png"),
    "Caterpie": pygame.image.load("imagens_pokemon/caterpie_pok.png/caterpie_poktest.png"),
    "Paras": pygame.image.load("imagens_pokemon/paras_pok.png/paras_poktest.png"),
    "Charmander": pygame.image.load("imagens_pokemon/charmander_pok.png/charmander_poktest2.png"),
    "Bulbasaur": pygame.image.load("imagens_pokemon/bulbasaur_pok.png/bulbasaur_poktest.png"),
    "Squirtle": pygame.image.load("imagens_pokemon/squirtle_pok.png/squirtel_poktest.png"),
    "Pikachu": pygame.image.load("imagens_pokemon/pikachu_pok.png/pikachu_poktest.png"),
    "Evee": pygame.image.load("imagens_pokemon/eevee_pok.png/eevee_poktest.png")
}

for pkmn in IMAGENS_POKEMONS:
    IMAGENS_POKEMONS[pkmn] = pygame.transform.scale(IMAGENS_POKEMONS[pkmn], (64, 64))

x, y = 19, 6
especies = list(IMAGENS_POKEMONS.keys())
pokedex = {}

estado_jogo = "MENU_INICIAL"  
pokemon_atual = None
mensagem_batalha = ""
frames_bump = 0  

# --- CORREÇÃO: VARIÁVEIS DA POKÉDEX INICIALIZADAS ---
indice_pokedex = 0
visualizar_detalhes = False

matriz_mapa = [
    ['A','A','A','A','A',' ',' ','A','A','A','A','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A'],
    ['A',' ',' ',' ','A',' ',' ',' ',' ',' ',' ','A'],
    ['A','E','E','E','A','E','E','E','G','G','G','A'],
    ['A',' ',' ',' ','A','E','E','E','G','G','G','A'],
    ['A','E','E','E','A','G','G','G','G','G','G','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ','G','G','G','A'],
    ['A','A','E','E','E','A','A','A','G','G','G','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A'],
    ['A','E',' ','E','E',' ','E','E','E','E','E','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A'],
    ['A','A','A','A','A','A','G','G','G','E','E','A'],
    ['A',' ',' ',' ',' ',' ','G','G','G',' ',' ','A'],
    ['A',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','A'],
    ['A','E','E',' ',' ','E','E','E','E','E','E','A'],
    ['A',' ','G','G','G','G',' ',' ','G','G','G','A'],
    ['A','G','G','G',' ',' ',' ','G','G',' ',' ','A'],
    ['A','A','A','A','A','A','G','A','A','A','A','A']
]

def desenhar_mapa():
    tela.fill((0, 0, 0))
    for l in range(len(matriz_mapa)):
        for c in range(len(matriz_mapa[l])):
            caractere = matriz_mapa[l][c]
            tela.blit(IMAGENS_TILES[' '], (c * LARGURA_TILE, l * ALTURA_TILE))

            if caractere != ' ':
                tela.blit(IMAGENS_TILES[caractere], (c * LARGURA_TILE, l * ALTURA_TILE))

    tela.blit(img_jogador_atual, (y * LARGURA_TILE, x * ALTURA_TILE))
    
    global frames_bump
    if frames_bump > 0:
        txt_bump = fonte_grande.render("BUMP!", True, (255, 0, 0))
        tela.blit(txt_bump, (LARGURA_TELA // 2 - txt_bump.get_width() // 2, 50))
        frames_bump -= 1

def pokemon_apareceu():
    global estado_jogo, pokemon_atual, message_batalha, mensagem_batalha
    if random.random() < 0.25:
        estado_jogo = "BATALHA"
        pokemon_atual = random.choice(especies)
        mensagem_batalha = f"Um {pokemon_atual} selvagem apareceu! \n[1] Capturar  |  [2] Correr"

def tentar_mover(dx, dy):
    global x, y, img_jogador_atual, frames_bump
    novo_x = x + dx
    novo_y = y + dy

    if dx > 0: img_jogador_atual = img_jogador_frente
    elif dx < 0: img_jogador_atual = img_jogador_costas

    if 0 <= novo_x < len(matriz_mapa) and 0 <= novo_y < len(matriz_mapa[0]):
        bloco = matriz_mapa[novo_x][novo_y]
        if bloco != 'E' and bloco != 'A':
            x = novo_x
            y = novo_y
            if bloco == 'G':
                pokemon_apareceu()
        else:
            frames_bump = 15

def desenhar_menu_inicial():
    tela.fill((10, 30, 50))
    titulo = fonte_grande.render("POKÉMON RPG", True, (255, 215, 0))
    instrucao1 = fonte.render("Pressione [ESPAÇO] para Iniciar", True, (255, 255, 255))
    instrucao2 = fonte.render("[C] Como Jogar", True, (0, 255, 255))
    instrucao3 = fonte.render("Pressione [ESC] ou [0] para Sair", True, (200, 200, 200))
    
    tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 150))
    tela.blit(instrucao1, (LARGURA_TELA // 2 - instrucao1.get_width() // 2, 280))
    tela.blit(instrucao2, (LARGURA_TELA // 2 - instrucao2.get_width() // 2, 330))
    tela.blit(instrucao3, (LARGURA_TELA // 2 - instrucao3.get_width() // 2, 380))

def desenhar_como_jogar():
    tela.fill((15, 15, 30))
    titulo = fonte_grande.render("COMO JOGAR", True, (0, 255, 255))
    tela.blit(titulo, (20, 40))
    
    instrucoes = [
        "Seta para Cima - Andar para Cima",
        "Seta para Baixo - Andar para Baixo",
        "Seta Esquerda - Andar para Esquerda",
        "Seta Direita - Andar para Direita",
        "",
        "[M] ou [9] - Abrir Menu de Opções",
        "Dentro da Grama (G) surgem Pokémons.",
        "Em Batalha: [1] Captura, [2] Foge.",
        "",
        "Pressione [BACKSPACE] para Voltar"
    ]
    
    linha_y = 100
    for texto in instrucoes:
        render_txt = fonte.render(texto, True, (255, 255, 255))
        tela.blit(render_txt, (20, linha_y))
        linha_y += 30

def desenhar_menu_opcoes():
    tela.fill((30, 40, 50))
    titulo = fonte_grande.render("MENU DO JOGO", True, (255, 215, 0))
    tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 100))
    
    opcoes = [
        "[5] Abrir Pokédex",
        "[M] Voltar ao Jogo",
        "[0] Sair do Jogo"
    ]
    
    linha_y = 220
    for texto in opcoes:
        render_txt = fonte.render(texto, True, (255, 255, 255))
        tela.blit(render_txt, (LARGURA_TELA // 2 - render_txt.get_width() // 2, linha_y))
        linha_y += 45

def desenhar_tela_batalha():
    tela.fill((40, 40, 40))
    if pokemon_atual in IMAGENS_POKEMONS:
        img = IMAGENS_POKEMONS[pokemon_atual]
        tela.blit(img, (LARGURA_TELA // 2 - 32, ALTURA_TELA // 2 - 80))

    linhas = mensagem_batalha.split('\n')
    for i, linha in enumerate(linhas):
        txt = fonte.render(linha, True, (255, 255, 255))
        tela.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, ALTURA_TELA // 2 + 20 + (i * 25)))

def desenhar_tela_pokedex():
    tela.fill((25, 25, 35))
    titulo = fonte_grande.render("POKÉDEX SISTEMA", True, (255, 215, 0))
    titulo_rect = titulo.get_rect(topleft=(20, 20))
    tela.blit(titulo, titulo_rect)
    
    controles = "Setas: Navegar | [D]: Ver Detalhes | [X]: Apagar | [BACKSPACE]: Sair"
    txt_ctrl = fonte.render(controles, True, (0, 255, 255))
    tela.blit(txt_ctrl, (20, 55))
    
    lista_pokemons = list(pokedex.keys())
    
    if not lista_pokemons:
        txt = fonte.render("Nenhum registro encontrado.", True, (150, 150, 150))
        tela.blit(txt, (20, 120))
        return

    global indice_pokedex
    if indice_pokedex >= len(lista_pokemons):
        indice_pokedex = max(0, len(lista_pokemons) - 1)

    linha_y = 100
    for i, pkmn in enumerate(lista_pokemons):
        prefixo = "-> " if i == indice_pokedex else "   "
        cor = (255, 255, 0) if i == indice_pokedex else (255, 255, 255)
        
        txt_nome = fonte.render(f"{prefixo}{pkmn}", True, cor)
        tela.blit(txt_nome, (20, line_y := linha_y))
        linha_y += 30

    if visualizar_detalhes and lista_pokemons:
        pkmn_selecionado = lista_pokemons[indice_pokedex]
        stats = pokedex[pkmn_selecionado]
        
        pygame.draw.rect(tela, (45, 45, 60), (15, 380, LARGURA_TELA - 30, 220))
        
        if pkmn_selecionado in IMAGENS_POKEMONS:
            tela.blit(IMAGENS_POKEMONS[pkmn_selecionado], (30, 400))
            
        txt_detalhe_nome = fonte_grande.render(pkmn_selecionado, True, (255, 215, 0))
        tela.blit(txt_detalhe_nome, (110, 400))
        
        txt_hp = fonte.render(f"HP: {stats['HP']}", True, (255, 255, 255))
        txt_atk = fonte.render(f"Atk: {stats['Atk']}", True, (255, 255, 255))
        txt_def = fonte.render(f"Def: {stats['Def']}", True, (255, 255, 255))
        
        tela.blit(txt_hp, (110, 440))
        tela.blit(txt_atk, (110, 465))
        tela.blit(txt_def, (110, 490))

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        elif evento.type == pygame.KEYDOWN:
            # --- ADICIONADO: BOTÃO GLOBAL DE FECHAR (ESC, 0 OU 0 DO NUMPAD) ---
            if evento.key in (pygame.K_ESCAPE, pygame.K_0, pygame.K_KP0):
                rodando = False
            
            if estado_jogo == "MENU_INICIAL":
                if evento.key == pygame.K_SPACE:
                    estado_jogo = "EXPLORANDO"
                elif evento.key == pygame.K_c:
                    estado_jogo = "COMO_JOGAR"
            
            elif estado_jogo == "COMO_JOGAR":
                if evento.key == pygame.K_BACKSPACE:
                    estado_jogo = "MENU_INICIAL"
            
            elif estado_jogo == "EXPLORANDO":
                if evento.key == pygame.K_UP:    tentar_mover(-1, 0)
                elif evento.key == pygame.K_DOWN:  tentar_mover(1, 0)
                elif evento.key == pygame.K_LEFT:  tentar_mover(0, -1)
                elif evento.key == pygame.K_RIGHT: tentar_mover(0, 1)
                elif evento.key == pygame.K_m or evento.key == pygame.K_KP9 or evento.key == pygame.K_9:     
                    estado_jogo = "MENU_OPCOES"
            
            elif estado_jogo == "MENU_OPCOES":
                if evento.key == pygame.K_5 or evento.key == pygame.K_KP5:
                    estado_jogo = "POKEDEX"
                    visualizar_detalhes = False
                elif evento.key == pygame.K_m:
                    estado_jogo = "EXPLORANDO"
            
            elif estado_jogo == "POKEDEX":
                lista_pkmn = list(pokedex.keys())
                if evento.key == pygame.K_BACKSPACE:
                    estado_jogo = "MENU_OPCOES"
                elif lista_pkmn:
                    if evento.key == pygame.K_UP:
                        indice_pokedex = (indice_pokedex - 1) % len(lista_pkmn)
                        visualizar_detalhes = False
                    elif evento.key == pygame.K_DOWN:
                        indice_pokedex = (indice_pokedex + 1) % len(lista_pkmn)
                        visualizar_detalhes = False
                    elif evento.key == pygame.K_d:
                        visualizar_detalhes = True
                    elif evento.key == pygame.K_x:
                        pkmn_para_deletar = lista_pkmn[indice_pokedex]
                        del pokedex[pkmn_para_deletar]
                        visualizar_detalhes = False
                        
            elif estado_jogo == "BATALHA":
                if evento.key == pygame.K_1 or evento.key == pygame.K_KP1:
                    if pokemon_atual in pokedex:
                        mensagem_batalha = f"{pokemon_atual} já foi capturado antes!\n\nPressione [ESPAÇO] para continuar."
                    else:
                        pokedex[pokemon_atual] = {
                            "HP": random.randint(10, 100), "Atk": random.randint(10, 100), "Def": random.randint(10, 100)
                        }
                        mensagem_batalha = f"{pokemon_atual} capturado com sucesso!\n\nPressione [ESPAÇO] para continuar."
                    estado_jogo = "FIM_BATALHA"
                elif evento.key == pygame.K_2 or evento.key == pygame.K_KP2:
                    estado_jogo = "EXPLORANDO"
                    
            elif estado_jogo == "FIM_BATALHA":
                if evento.key == pygame.K_SPACE:
                    estado_jogo = "EXPLORANDO"

    if estado_jogo == "MENU_INICIAL":
        desenhar_menu_inicial()
    elif estado_jogo == "COMO_JOGAR":
        desenhar_como_jogar()
    elif estado_jogo == "EXPLORANDO":
        desenhar_mapa()
    elif estado_jogo == "MENU_OPCOES":
        desenhar_menu_opcoes()
    elif estado_jogo == "POKEDEX":
        desenhar_tela_pokedex()
    elif estado_jogo in ("BATALHA", "FIM_BATALHA"):
        desenhar_tela_batalha()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()