
import numpy as np
import random

def avaliar(pesos, media_retornos, cov_matrix, limite_risco):
    pesos = np.array(pesos)  
    retorno = np.dot(pesos, media_retornos)
    risco = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))
    if risco > limite_risco:
        return -1
    return retorno

def gerar_populacao(n, qtd_acoes):
    return [normalizar(np.random.rand(qtd_acoes)) for _ in range(n)]

def normalizar(v):
    soma = sum(v)
    return [x / soma for x in v]

def crossover(p1, p2):
    alpha = random.random()
    filho = [alpha * a + (1 - alpha) * b for a, b in zip(p1, p2)]
    return normalizar(filho)

def mutacao(p, taxa=0.1):
    if random.random() < taxa:
        i = random.randint(0, len(p)-1)
        p[i] += random.uniform(-0.05, 0.05)
        p = normalizar(p)
    return p

def selecionar(pop, media_retornos, cov_matrix, limite_risco):
    return sorted(pop, key=lambda x: avaliar(x, media_retornos, cov_matrix, limite_risco), reverse=True)[:2]
