# 🧬 Tech Challenge - Otimização de Carteira com Algoritmo Genético

Este projeto foi desenvolvido como parte do Tech Challenge da FIAP, com o objetivo de aplicar algoritmos genéticos para otimizar uma carteira de investimentos com ativos da B3. A proposta é encontrar a melhor alocação entre risco e retorno utilizando dados históricos reais.

---

## 📁 Estrutura do Projeto

```
tech-challenge-carteira/
├── images/                           # Gráficos de risco × retorno
├── output/                           # Relatório completo com análise da carteira ótima
├── main.py                           # Script principal (algoritmo + visualização com pygame)
├── algoritmosGeneticos.py            # Módulo com as funções do algoritmo genético
├── requirements.txt                  # Dependências do projeto
└── README.md                         # Documentação do projeto
```

---

## 📈 Sobre os Dados

- Os dados são obtidos automaticamente via a biblioteca `yfinance`, com preços **diários ajustados** entre `2023-01-01` e `2024-01-01`.
- São considerados os seguintes ativos da B3:
  - PETR4.SA
  - VALE3.SA
  - ITUB4.SA
  - BBDC4.SA
  - WEGE3.SA
  - ABEV3.SA

Com esses dados, são calculados:
- **Retornos médios diários**
- **Matriz de covariância** entre os ativos (base para o cálculo do risco da carteira)

---

## ⚙️ Como Executar o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/Phellype-Guilherme/Tech-Challenge-2-IA-FIAP
cd Tech-Challenge-2-IA-FIAP
```

2. Instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

3. Execute o script principal:
```bash
python main.py
```

Durante a execução, o algoritmo será visualizado em tempo real via `Pygame`.

---

## 🎮 Visualização em Tempo Real

Ao executar o projeto, uma janela será aberta com:

- Gráfico interativo de **Risco × Retorno** por geração
- Exibição da **melhor carteira atual**
- Geração em tempo real dos pontos da evolução do algoritmo

---

## 📊 Saídas Geradas

- **`images/grafico_risco_retorno_final.png`**: gráfico final com o histórico da evolução da carteira.
- **`output/relatorio_completo.txt`**: relatório com:
  - Pesos da carteira ótima
  - Retorno esperado e risco em:
    - Termos **diários**, **mensais** e **anuais**
  - Explicações sobre os conceitos utilizados (retorno, risco, pesos)

---

## 🧠 Técnicas Utilizadas

- Algoritmo Genético com:
  - Seleção dos melhores indivíduos
  - Crossover com média ponderada
  - Mutação com normalização
- Avaliação com base em:
  - **Retorno esperado** (média ponderada dos retornos históricos)
  - **Risco** (desvio padrão calculado a partir da matriz de covariância)
- Visualização interativa com `pygame`
- Exportação de gráfico com `matplotlib`

---

## 📚 Bibliotecas Utilizadas

- `yfinance` – Download de dados da B3
- `pandas` e `numpy` – Manipulação de dados e cálculos estatísticos
- `pygame` – Visualização gráfica do processo evolutivo
- `matplotlib` – Gráficos estáticos salvos no diretório `images`

---

## 👥 Autor

**Phellype Guilherme Pereira da Silva**  
**RM:** 361625  
**Projeto: Fase 2 - Pós Tech FIAP - Inteligência Artificial**

---