# 8-Puzzle Game

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2025.2  
**Professor:** André Luis Fonseca Faustino  
**Turma:** T04

## Integrantes do Grupo
* Otto Yshiro Osawa de Souza

## Descrição do Projeto
O projeto consiste em recriar o jogo 8-Puzzle e a partir disso, implementar um agente capaz de resolver de forma automatizada o jogo, mostrando uma descrição sobre a quantidade de movimentos e o tempo de execução de cada algoritmo de busca.
Este projeto é uma boa maneira de vizualizar a performance dos algoritmos de busca (A*, BFS e DFS).

## Guia de Instalação e Execução


### 1. Instalação das Dependências
Certifique-se de ter o **Python 3.3+** instalado. Clone o repositório e instale as bibliotecas listadas no `requirements.txt`:

```bash
# Clone o repositório
git clone https://github.com/ottoyshiro/8-puzzle-game

# Entre na pasta do projeto
cd src

# Crie um ambiente virtual
python -m venv nome_do_ambiente # (venv costuma ser o padrão)

# Ative o seu ambiente
nome_do_ambiente\Scripts\activate # (Windows)
source nome_do_ambiente/bin/activate # (Linux/MacOS)

# Após executar o comando, o nome do seu ambiente virtual (por exemplo, (nome_do_ambiente))
# aparecerá no início da linha do terminal, indicando que ele está ativo

# Instale as dependências dentro do ambiente virtual
pip install -r requirements.txt
````

### 2. Como Executar

Execute o comando abaixo no terminal para iniciar o jogo:

```bash
python main.py

# Para sair do ambiente virtual basta digitar no terminal
deactivate
```

## Estrutura dos Arquivos

A organização das pastas se encontra no seguinte formato:

  * `src/`: Código-fonte da aplicação.
  * `notebooks/`: Análises exploratórias e testes.
  * `assets/`: Imagens de resultados.

## Resultados e Demonstração

![Interface do jogo](https://raw.githubusercontent.com/ottoyshiro/8-puzzle-game/main/assets/arquivo.png)

![Interface com imagem](https://raw.githubusercontent.com/ottoyshiro/8-puzzle-game/main/assets/arquivo.png)

Obs.: Sempre que um jogo for concluído clique em reset para começar um novo jogo

## Referências

  * https://youtube.com/playlist?list=PLJ8PYFcmwFOxtJS4EZTGEPxMEo4YdbxdQ&si=2lpWflRYFfPqyuxK
  * https://www.geeksforgeeks.org/dsa/8-puzzle-problem-using-branch-and-bound
