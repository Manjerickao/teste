# Desafio do Fazendeiro - Erick Nicolas

# Fiz meu codigo dividido em 4 partes, sendo uma para vereficar o estado,
# outra para as ações, outra para a decisão e a ultima para o caminho(BFS).
# Sobre a condicao 4 do problema 2 onde a ovelha pode pular o bote,
# eu interpretei que ela so poderia pular em um momento que fosse selecionada para para se transportata,
# decidi colocar um numero randomico para decidir com chances de 20% para isso ocorrer
# vou chamar de situacao 2.4 no codigo
#

from collections import deque
import random

 # Verifica se o estado é válido e é pssível proseguir
def verefica_estado(estado):
    if estado[0] != estado[1] and estado[1] == estado[2]:  # lobo vs ovelha
        return False
    elif estado[0] != estado[2] and estado[2] == estado[3]:  # ovelha vs repolho
        return False
    elif estado[1] == estado[4] and estado[0] != estado[4] and estado[2] != estado[4] and estado[3] != estado[4]:  # lobo vs cachorro
        return False
    else:
        return True

# Ações possíveis: mover para frente/traz o fazendeiro , o lobo, a ovelha, o repolho ou o cachorro
def leva_fazendeiro(estado):
    estado[0] = 'd'
    return estado

def traz_fazendeiro(estado):
    estado[0] = 'e'
    return estado

def leva_lobo(estado):
    estado[0] = 'd'
    estado[1] = 'd'
    return estado

def traz_lobo(estado):
    estado[0] = 'e'
    estado[1] = 'e'
    return estado

def leva_ovelha(estado):
    # Situação 2.4: sorteia o número aleatório para decidir se a ovelha pula do bote
    chance_ovelha_pular_bote = random.randint(1, 5)
    # Se a ovelha pular do bote, retorna o estado atual sem alterações
    if chance_ovelha_pular_bote == 1:
        print("A ovelha pulou do bote!")
        return estado
    estado[0] = 'd'
    estado[2] = 'd'
    return estado

# fiz a mesma coisa nessa funcao
def traz_ovelha(estado):
    chance_ovelha_pular_bote = random.randint(1, 5)
    if chance_ovelha_pular_bote == 1:
        print("A ovelha pulou do bote!")
        return estado
    estado[0] = 'e'
    estado[2] = 'e'
    return estado

def leva_repolho(estado):
    estado[0] = 'd'
    estado[3] = 'd'
    return estado

def traz_repolho(estado):
    estado[0] = 'e'
    estado[3] = 'e'
    return estado

def leva_cachorro(estado):
    estado[0] = 'd'
    estado[4] = 'd'
    return estado

def traz_cachorro(estado):
    estado[0] = 'e'
    estado[4] = 'e'
    return estado   

# Função que gera uma lista de todos os próximos estados válidos a partir do estado atual
def toma_decisao(estado):
    proximos_estados = []
    for i in range(len(estado)):
        estado_test = estado.copy()
        if i == 0:
            if estado[i] == 'e':
                estado_test = leva_fazendeiro(estado_test)
                print("leva fazendeiro")
            else:
                estado_test = traz_fazendeiro(estado_test)
                print("traz fazendeiro")
        elif i == 1:
            if estado[i] == 'e':
                estado_test = leva_lobo(estado_test)
                print("leva lobo")
            else:
                estado_test = traz_lobo(estado_test)
                print("traz lobo")
        # acao da ovelha
        elif i == 2:
            if estado[i] == 'e':
                # afim de saber se a ovelha pulou do bote e salvei uma copia da lista atual
                # para comparar depois se ocorreu ou nao alteracao, caso nao orrcoeu alteracao na acao da ovelha
                # o estado inicial é retornado para avisar que a busca deve comecar desde o inicio
                estado_test2 = estado_test.copy()
                estado_test = leva_ovelha(estado_test)
                if estado_test == estado_test2:
                    return estado
                print("leva ovelha")
            else:
                # mesma coisa da acao de cima, so que agora a ovelha esta voltando
                estado_test2 = estado_test.copy()
                estado_test = traz_ovelha(estado_test)
                if estado_test == estado_test2:
                    return estado
                print("traz ovelha")
        elif i == 3:
            if estado[i] == 'e':
                estado_test = leva_repolho(estado_test)
                print("leva repolho")
            else:   
                estado_test = traz_repolho(estado_test)
                print("traz repolho")
        elif i == 4:
            if estado[i] == 'e':
                estado_test = leva_cachorro(estado_test)
                print("leva cachorro")
            else:
                estado_test = traz_cachorro(estado_test)
                print("traz cachorro")

        # Adiciona o estado à lista se for válido
        if verefica_estado(estado_test):
            proximos_estados.append(estado_test)

    return proximos_estados

def melhor_caminho(s0, goal):
    # Busca em largura (BFS) adaptada
    fila = deque([[s0]])
    visitados = set()  
    while fila:
        caminho = fila.popleft()  
        no = caminho[-1]  
        if no == goal:
            return caminho 

        if tuple(no) not in visitados:
            #salva o estado atual paara saber se ocorreu problema com a ovelha
            #se depois da tomada de decicao o resultado por igual a o estado anterior   
            #significa que a ovelha morreu e o laco de repeticao deve ser reiniciado desde o comeco do problema
            estado_atual = no
            proximos_estados = toma_decisao(no)  
            if proximos_estados == estado_atual:
                print("tentar novamente pois ovelha morreu")
                continue
            for proximo_estado in proximos_estados:
                novo_caminho = list(caminho)
                novo_caminho.append(proximo_estado)
                fila.append(novo_caminho)

    return None  

# Estado inicial e objetivo
s0 = ['e', 'e', 'e', 'e', 'e']  
G = ['d', 'd', 'd', 'd', 'd']  

# Encontra o melhor caminho
caminho = melhor_caminho(s0, G)
if caminho:
    print("Caminho encontrado:")
    for passo, estado in enumerate(caminho):
        print(f"Passo {passo}: {estado}")
else:
    print("Nenhuma solução encontrada.")
