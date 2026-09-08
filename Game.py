import pygame
import random

pygame.init()

# Configurações da tela
LARGURA = 400
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Entre Nuvens e Estrelas")

# Cores
BRANCO = (255, 255, 255)
ROXO_ESCURO = (20, 15, 32)
LILAS_VITORIA = (208, 195, 241)

# Fonte
fonte = pygame.font.SysFont(None, 36)

# Jogador
TAM_PLAYER = (70, 70)
jogador = pygame.Rect(160, 500, *TAM_PLAYER)  # Centralizado horizontalmente
vel_jogador = 5

# Obstáculos e boosts
TAM_OBS = 50
TAM_BOOST = 50
vel_obs = 4
tempo_spawn = 30
obstaculos = []
boosts = []

# Controle de tempo e jogo
clock = pygame.time.Clock()
frames = 0
tempo_vitoria = 30
rodando = True
game_over = False
venceu = False

# Carregar imagens
img_fundo = pygame.image.load("imagens/fundo1.png").convert()
img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))

img_player = pygame.image.load("imagens/player.png").convert_alpha()
img_player = pygame.transform.scale(img_player, TAM_PLAYER)

img_obs = pygame.image.load("imagens/nuvem-obstaculo.png").convert_alpha()
img_obs = pygame.transform.scale(img_obs, (TAM_OBS, TAM_OBS))

img_boost = pygame.image.load("imagens/bonus.png").convert_alpha()
img_boost = pygame.transform.scale(img_boost, (TAM_BOOST, TAM_BOOST))

# Função para desenhar texto centralizado
def desenha_texto(texto, cor, y):
    surf = fonte.render(texto, True, cor)
    rect = surf.get_rect(center=(LARGURA // 2, y))
    TELA.blit(surf, rect)

# Loop principal
while rodando:
    clock.tick(60)
    TELA.blit(img_fundo, (0, 0))

    if not game_over and not venceu:
        frames += 1
        segundos = frames // 60

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and jogador.left > 0:
            jogador.x -= vel_jogador
        if keys[pygame.K_RIGHT] and jogador.right < LARGURA:
            jogador.x += vel_jogador

        # Aumenta a velocidade dos obstáculos a cada 5 segundos
        if frames % (60 * 5) == 0:
            vel_obs += 0.5

        # Spawn de obstáculos e boosts
        if frames % tempo_spawn == 0:
            x = random.randint(0, LARGURA - TAM_OBS)
            obstaculos.append(pygame.Rect(x, -TAM_OBS, TAM_OBS, TAM_OBS))
            if random.randint(1, 5) == 1:
                x_boost = random.randint(0, LARGURA - TAM_BOOST)
                boosts.append(pygame.Rect(x_boost, -TAM_BOOST, TAM_BOOST, TAM_BOOST))

        # Movimento dos obstáculos e boosts
        for obs in obstaculos:
            obs.y += vel_obs
        for boost in boosts:
            boost.y += vel_obs

        # Colisão com obstáculos
        for obs in obstaculos:
            if jogador.colliderect(obs):
                game_over = True

        # Colisão com boosts
        novos_boosts = []
        for b in boosts:
            if jogador.colliderect(b):
                vel_obs = max(2, vel_obs - 1)
            else:
                novos_boosts.append(b)
        boosts = novos_boosts

        # Remover objetos
        obstaculos = [obs for obs in obstaculos if obs.y < ALTURA]
        boosts = [b for b in boosts if b.y < ALTURA]

        # Verifica vitória
        if segundos >= tempo_vitoria:
            venceu = True

        # Desenhar elementos
        TELA.blit(img_player, jogador)
        for obs in obstaculos:
            TELA.blit(img_obs, obs)
        for boost in boosts:
            TELA.blit(img_boost, boost)

        tempo_txt = fonte.render(f"Tempo: {segundos}s", True, BRANCO)
        TELA.blit(tempo_txt, (10, 10))

    elif venceu:
        desenha_texto("Você Venceu!!", LILAS_VITORIA, ALTURA // 2)
        desenha_texto("Pressione R para jogar de novo", BRANCO, ALTURA // 2 + 40)

    else:
        desenha_texto("Game Over", ROXO_ESCURO, ALTURA // 2)
        desenha_texto("Pressione R para jogar de novo", BRANCO, ALTURA // 2 + 40)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            jogador = pygame.Rect(160, 500, *TAM_PLAYER)
            obstaculos = []
            boosts = []
            vel_obs = 4
            frames = 0
            game_over = False
            venceu = False

    pygame.display.update()

pygame.quit()
