import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygame
import sys
import time
import random
import os

from algoritmosGeneticos import (
    avaliar, gerar_populacao, crossover, mutacao, selecionar
)

# Inicializar pastas
os.makedirs("images", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Configurações
acoes = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'WEGE3.SA', 'ABEV3.SA']
inicio = "2023-01-01"
fim = "2024-01-01"
pop_size = 50
geracoes = 100
limite_risco = 0.20

# Pygame setup
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Evolução da Carteira - GA")
fonte = pygame.font.SysFont("Arial", 16)
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 200, 0)

def desenhar_grafico(pontos, geracao):
    tela.fill(branco)

    # Títulos dos eixos
    eixo_font = pygame.font.SysFont("Arial", 14)
    tela.blit(eixo_font.render("Retorno ↑", True, preto), (10, 30))
    tela.blit(eixo_font.render("→ Risco", True, preto), (largura - 120, altura - 30))

    # Eixos X e Y
    pygame.draw.line(tela, preto, (60, 20), (60, 550), 2)
    pygame.draw.line(tela, preto, (60, 550), (750, 550), 2)

    if not pontos:
        return

    # Escalas fixas baseadas nos limites do GA
    max_risco = 0.03
    max_retorno = 0.003

    # Grade de fundo
    for i in range(6):
        y = 550 - i * 100
        pygame.draw.line(tela, (220, 220, 220), (60, y), (750, y))
        tela.blit(fonte.render(f"{(i * max_retorno / 5):.2%}", True, preto), (10, y - 10))

    for i in range(7):
        x = 60 + i * 100
        pygame.draw.line(tela, (220, 220, 220), (x, 20), (x, 550))
        tela.blit(fonte.render(f"{(i * max_risco / 6):.2%}", True, preto), (x - 15, 555))

    # Desenha os pontos
    for i, (risco, retorno) in enumerate(pontos):
        x = 60 + (risco / max_risco) * 690
        y = 550 - (retorno / max_retorno) * 530
        pygame.draw.circle(tela, verde, (int(x), int(y)), 4)
        if i > 0:
            # linha entre os pontos
            risco_ant, ret_ant = pontos[i - 1]
            x_ant = 60 + (risco_ant / max_risco) * 690
            y_ant = 550 - (ret_ant / max_retorno) * 530
            pygame.draw.line(tela, (0, 180, 0), (int(x_ant), int(y_ant)), (int(x), int(y)), 1)

    # Geração atual
    texto = fonte.render(f"Geração: {geracao}", True, preto)
    tela.blit(texto, (630, 25))

    # Melhor ponto atual
    if pontos:
        risco, retorno = pontos[-1]
        texto2 = fonte.render(f"Melhor Retorno: {retorno:.2%}", True, preto)
        texto3 = fonte.render(f"Risco: {risco:.2%}", True, preto)
        tela.blit(texto2, (630, 45))
        tela.blit(texto3, (630, 65))

    pygame.display.flip()
    pygame.event.pump()

# Baixar dados

precos = yf.download(acoes, start=inicio, end=fim, auto_adjust=False)

# Verifica se o DataFrame está vazio
if precos.empty:
    raise ValueError("Falha ao baixar dados! Verifique os tickers ou conexão com a internet.")

# Verifica se é MultiIndex (múltiplas ações) e extrai 'Adj Close'
if isinstance(precos.columns, pd.MultiIndex):
    if 'Adj Close' in precos.columns.levels[0]:
        precos = precos['Adj Close']
    else:
        raise KeyError("'Adj Close' não encontrado nos dados baixados.")
else:
    if 'Adj Close' in precos.columns:
        precos = precos[['Adj Close']]
    else:
        raise KeyError("'Adj Close' não encontrado nos dados baixados.")

print("Dados baixados com sucesso:")
print(precos.head())
retornos = precos.pct_change().dropna()
media_retornos = retornos.mean()
cov_matrix = retornos.cov()

# Algoritmo Genético com pygame
def algoritmo_genetico():
    pop = gerar_populacao(pop_size, len(acoes))
    melhores_pesos = None
    historico = []

    for gen in range(geracoes):
        nova_pop = []
        for _ in range(pop_size):
            pais = random.sample(pop, 2)
            filho = crossover(pais[0], pais[1])
            filho = mutacao(filho)
            nova_pop.append(filho)

        pop = nova_pop
        melhores = selecionar(pop, media_retornos, cov_matrix, limite_risco)
        melhores_pesos = melhores[0]
        retorno = avaliar(melhores_pesos, media_retornos, cov_matrix, limite_risco)
        risco = np.sqrt(np.dot(melhores_pesos, np.dot(cov_matrix, melhores_pesos)))
        historico.append((risco, retorno))

        desenhar_grafico(historico, gen)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        time.sleep(0.1)

    return melhores_pesos, historico

# Executar
melhor, hist = algoritmo_genetico()
final_risco, final_retorno = hist[-1]

ret_diario = final_retorno
ret_mensal = (1 + ret_diario) ** 21 - 1
ret_anual = (1 + ret_diario) ** 252 - 1

risco_diario = final_risco
risco_mensal = risco_diario * np.sqrt(21)
risco_anual = risco_diario * np.sqrt(252)

plt.figure(figsize=(8, 6))
x, y = zip(*hist)
plt.plot(x, y, marker='o', linestyle='-', color='blue')
plt.title("Evolução da Carteira - Risco x Retorno")
plt.xlabel("Risco (Desvio Padrão)")
plt.ylabel("Retorno Esperado")
plt.grid(True)
plt.savefig("images/grafico_risco_retorno_final.png")
plt.close()

relatorio = f"""
Relatório Final - Otimização de Carteira com Algoritmo Genético

Melhores Pesos Encontrados:
----------------------------
"""
for nome, peso in zip(acoes, melhor):
    relatorio += f"{nome}: {peso:.2%}\n"

relatorio += f"""
Retorno Esperado da Carteira:
------------------------------
• Diário: {ret_diario:.2%}
• Mensal: {ret_mensal:.2%}
• Anual: {ret_anual:.2%}

Risco (Desvio Padrão da Carteira):
----------------------------------
• Diário: {risco_diario:.2%}
• Mensal: {risco_mensal:.2%}
• Anual: {risco_anual:.2%}

Explicações:
------------
• Retorno Esperado: ganho médio baseado nos retornos históricos dos ativos ponderados pelos pesos.
• Risco: volatilidade da carteira medida pelo desvio padrão. Quanto menor, mais estável.

Sobre os Pesos:
---------------
Atribuídos para maximizar o retorno dentro do limite de risco. A soma dos pesos é 100%.

Gráfico:
--------
Salvo em 'images/grafico_risco_retorno_final.png'. Mostra a evolução do algoritmo.

Conclusão:
----------
Carteira equilibrada para perfil moderado/agressivo.
"""

with open("output/relatorio_completo.txt", "w", encoding="utf-8") as f:
    f.write(relatorio)

pygame.quit()
