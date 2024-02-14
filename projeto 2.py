"""Go - Projeto 2 de Fundamentos da Programação 
"""

LETTERS = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

## TAD intersecao
def cria_intersecao(col, lin):
    if type(col) == str and len(col) == 1 and 'A' <= col <= 'S' \
        and type(lin) == int and  1 <= lin <= 19:
            return (col, lin)
        
    raise ValueError("cria_intersecao: argumentos invalidos") 

def obtem_col(pos):
    return pos[0]

def obtem_lin(pos):
    return pos[1]

def eh_intersecao(arg):
    return type(arg) == tuple and len(arg) == 2 \
        and type(arg[0]) == str and 'A' <= arg[0] <= 'S' \
            and type(arg[1]) == int and  1 <= arg[1] <= 19
            
def intersecoes_iguais(pos1, pos2):
    return eh_intersecao(pos1) and eh_intersecao(pos2) and obtem_col(pos1) == obtem_col(pos2) and obtem_lin(pos1) == obtem_lin(pos2)

def intersecao_para_str(pos):
    return f'{obtem_col(pos)}{obtem_lin(pos)}'

def str_para_intersecao(s):
    return cria_intersecao(s[0], int(s[1:]))

## FAN - TAD intersecao
def obtem_intersecoes_adjacentes(pos, last_pos):
    move = {
        'U': lambda x: 0 if obtem_lin(x) == obtem_lin(last_pos) else cria_intersecao(obtem_col(x), obtem_lin(x)+1),
        'D': lambda x: 0 if obtem_lin(x) == 1 else cria_intersecao(obtem_col(x), obtem_lin(x)-1),
        'L': lambda x: '' if obtem_col(x) == 'A' else cria_intersecao(LETTERS[LETTERS.index(obtem_col(x))-1], obtem_lin(x)),
        'R': lambda x: '' if obtem_col(x) == obtem_col(last_pos) else cria_intersecao(LETTERS[LETTERS.index(obtem_col(x))+1], obtem_lin(x))
    }
    
    return tuple(move[d](pos) for d in ('D', 'L', 'R', 'U') if move[d](pos))
    
def ordena_intersecoes(tup):
    return tuple(sorted(tup, key=lambda x:(obtem_lin(x), obtem_col(x))))

## TAD pedra
def cria_pedra_branca():
    return 'O'

def cria_pedra_preta():
    return 'X'

def cria_pedra_neutra():
    return '.'

def eh_pedra(arg):
    return arg in ('X', 'O', '.')
        
def eh_pedra_branca(arg):
    return eh_pedra(arg) and arg == 'O'

def eh_pedra_preta(arg):
    return eh_pedra(arg) and arg == 'X'

def pedras_iguais(p1, p2):
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2

def pedra_para_str(p):
    return p


## FAN pedra
def eh_pedra_jogador(pedra):
    return eh_pedra_branca(pedra) or eh_pedra_preta(pedra)


## TAD goban
def cria_goban_vazio(n):
    if type(n) == int and n in (9, 13, 19):
        return (n, {})
    
    raise ValueError('cria_goban_vazio: argumento invalido')    

def cria_goban(n, ib, ip):
    if type(n) == int and n in (9, 13, 19):
        goban = cria_goban_vazio(n)
        if type(n) == int and n in (9, 13, 19) and \
            type(ib) == tuple and all(eh_intersecao(i) and eh_intersecao_valida(goban, i) for i in ib) and \
                type(ip) == tuple and all(eh_intersecao(i) and eh_intersecao_valida(goban, i) for i in ip):
                    for i in ib: 
                        if eh_pedra_jogador(obtem_pedra(goban, i)):
                            raise ValueError('cria_goban: argumentos invalidos')   
                        coloca_pedra(goban, i, cria_pedra_branca())
                    
                    for i in ip: 
                        if eh_pedra_jogador(obtem_pedra(goban, i)):
                            raise ValueError('cria_goban: argumentos invalidos')  
                        coloca_pedra(goban, i, cria_pedra_preta())
                    return goban
    
    raise ValueError('cria_goban: argumentos invalidos')   

def cria_copia_goban(tab):
    return (tab[0], tab[1].copy())

def obtem_ultima_intersecao(tab):
    return cria_intersecao(LETTERS[tab[0]-1], tab[0])

def obtem_pedra(tab, pos):
    if pos in tab[1]:
        return tab[1][pos]
    else:
        return cria_pedra_neutra()


def obtem_cadeia(board, pos):
    
    state = obtem_pedra(board, pos)
    last = obtem_ultima_intersecao(board)
    
    chain, to_check = [], [pos]
    
    while to_check:
        pos = to_check.pop()
        chain.append(pos)
        for new_pos in obtem_intersecoes_adjacentes(pos, last):
            if pedras_iguais(obtem_pedra(board, new_pos), state) and new_pos not in chain + to_check:
                to_check.append(new_pos)
                
    return ordena_intersecoes(tuple(chain))



def coloca_pedra(tab, pos, pedra):
    tab[1][pos] = pedra
    return tab

def remove_pedra(tab, pos):
    if pos in tab[1]:
        del tab[1][pos]
    return tab

def remove_cadeia(tab, tuplo):
    for pos in tuplo:
        remove_pedra(tab, pos)
    return tab


def eh_goban(arg):
    return type(arg) == tuple and len(arg) == 2 and type(arg[0]) == int and arg[0] in (9, 13, 19) \
        and type(arg[1]) == dict and  all(eh_intersecao(k) for k in arg[1]) and \
            all(intersecao_dentro_limites(k, obtem_ultima_intersecao(arg)) for k in arg[1]) and \
                all(eh_pedra(arg[1][k]) for k in arg[1])
        # todaos os indexes são interseções, todas as intereseções são validas e todos os valores são pedras e todos 
        
def eh_intersecao_valida(tab, pos):
    return intersecao_dentro_limites(pos, obtem_ultima_intersecao(tab))

def gobans_iguais(g1, g2):
    if eh_goban(g1) and eh_goban(g2) and g1[0] == g2[0]: 
        if sorted(g1[1].keys()) == sorted(g2[1].keys()): # mesmas chaves
            return all(pedras_iguais(g1[1][k], g2[1][k]) for k in g1[1])
    return False

def goban_para_str(tab):    
    n_v, n_h = tab[0], tab[0]
    cad = '   ' + ''.join(f'{l} ' for l in LETTERS[:n_v]).rstrip() + '\n' 
    for i in range(n_h):
        cad += '{:>2} '.format(n_h-i)
        for j in LETTERS[:n_v]:
            cad += pedra_para_str(obtem_pedra(tab, cria_intersecao(j, n_h-i))) + ' '
        cad += '{:>2}'.format(n_h-i) + '\n'
        
    cad += '   ' + ''.join(f'{l} ' for l in LETTERS[:n_v]).rstrip()
    
    return cad
   
   
# Funcoes adicionais - nao do enunciado
def intersecao_dentro_limites(i1, i2):
    return 'A' <= obtem_col(i1) <= obtem_col(i2) and 1 <= obtem_lin(i1) <= obtem_lin(i2)


## FAN goban 

def obtem_adjacentes_diferentes(board, cadeia_pedras):
    
    if cadeia_pedras:
        state = obtem_pedra(board, cadeia_pedras[0])
        # eh_diferente = (lambda x:not pedras_iguais(x, neutral)) if pedras_iguais(state, neutral) else (lambda x: pedras_iguais(x, neutral))
        eh_diferente = (lambda x:not eh_pedra_jogador(x)) if eh_pedra_jogador(state) else eh_pedra_jogador
        
        liberdades = []
        
        for pos in cadeia_pedras:
            for new_pos in obtem_intersecoes_adjacentes(pos, obtem_ultima_intersecao(board)):
                if eh_diferente(obtem_pedra(board, new_pos)) and new_pos not in liberdades:
                    liberdades.append(new_pos)
                    
        return ordena_intersecoes(tuple(liberdades))
    return ()

def jogada(board, pos, pedra):
    coloca_pedra(board, pos, pedra)
    for new_pos in obtem_intersecoes_adjacentes(pos, obtem_ultima_intersecao(board)):
        outra_pedra = obtem_pedra(board, new_pos)
        if eh_pedra_jogador(outra_pedra) and not pedras_iguais(pedra, outra_pedra): #há uma pedra  adjacente de outro jogador
            cadeia = obtem_cadeia(board, new_pos)
            if len(obtem_adjacentes_diferentes(board, cadeia)) == 0:
                remove_cadeia(board, cadeia)
    return board
                    
def obtem_pedras_jogadores(board):
    num_b, num_p = 0, 0
    branca, preta = cria_pedra_branca(), cria_pedra_preta()
    
    # PERCORRER TODAS AS INTERSECOES
    last_pos = obtem_ultima_intersecao(board)
    last_h, last_v = LETTERS.index(obtem_col(last_pos)), obtem_lin(last_pos)
    
    for h in LETTERS[:last_h+1]:
        for v in range(1, last_v+1):
            pos = cria_intersecao(h, v)
            if pedras_iguais(branca, obtem_pedra(board, pos)):
                num_b+=1
            elif pedras_iguais(preta, obtem_pedra(board, pos)):
                num_p += 1
    return num_b, num_p



def obtem_territorios(board):
    
    all_cadeias, cadeias_seen = [], ()
    
    last_pos = obtem_ultima_intersecao(board)
    last_h, last_v = LETTERS.index(obtem_col(last_pos)), obtem_lin(last_pos)
    
    for h in LETTERS[:last_h+1]:
        for v in range(1, last_v+1):
            pos = cria_intersecao(h, v)
            if pedras_iguais(obtem_pedra(board, pos), cria_pedra_neutra()) and pos not in cadeias_seen:
                this_cadeia = obtem_cadeia(board, pos)
                all_cadeias.append(this_cadeia)
                cadeias_seen += this_cadeia
    
    # return all_cadeias            
    return tuple(sorted(all_cadeias, key=lambda x:(obtem_lin(x[0]), obtem_col(x[0]))))

    
def calcula_pontos(board):
    p_branco, p_preto =  obtem_pedras_jogadores(board)
    
    for territorio in obtem_territorios(board):
        limites = obtem_adjacentes_diferentes(board, territorio)
        if limites: #não pode ser vazio
            if all(eh_pedra_branca(obtem_pedra(board,i)) for i in limites):
                p_branco += len(territorio)
            elif all(eh_pedra_preta(obtem_pedra(board,i)) for i in limites):
                p_preto += len(territorio)
    return p_branco, p_preto 

def eh_jogada_legal(board, pos, pedra, last_board):
        
    if eh_intersecao_valida(board, pos) and \
        not eh_pedra_jogador(obtem_pedra(board, pos)): #intersecao valida, intersecao livre
            novo_board = cria_copia_goban(board)
            jogada(novo_board, pos, pedra)
            
            # verifica suicidio 
            if len(obtem_adjacentes_diferentes(novo_board, obtem_cadeia(novo_board, pos))) == 0:
                return False
            elif gobans_iguais(novo_board, last_board): # verifica Ko
                return False
            else:
                return True

    return False

def eh_cadeia_intercecao_ok(cad):
    return isinstance(cad,str) and ((len(cad) == 2 and 'A' <= cad[0] <= 'S' and cad[1] in '0123456789' and 1<= int(cad[1]) <= 9) \
        or (len(cad) == 3 and 'A' <= cad[0] <= 'S' and cad[1] == '1' \
            and cad[2] in '0123456789' and 1<= int(cad[1:]) <= 19)) 

def turno_jogador(current, pedra, last_board):
    jogada_legal = False
    while not jogada_legal:
        pos = input(f"Escreva uma intersecao ou 'P' para passar [{pedra_para_str(pedra)}]:")
        if pos == 'P':
            return False
        elif eh_cadeia_intercecao_ok(pos):
            pos = str_para_intersecao(pos)
            jogada_legal = eh_jogada_legal(current, pos, pedra, last_board)
            
    jogada(current, pos, pedra)
    return True



def go(n, ib, ip):
    
    if not (isinstance(ib, tuple) and isinstance(ip, tuple) and \
        all(eh_cadeia_intercecao_ok(i) for i in ib) and \
            all(eh_cadeia_intercecao_ok(i) for i in ip)):
        raise ValueError('go: argumentos invalidos')
    
    try:
        ib = tuple(str_para_intersecao(i) for i in ib)
        ip = tuple(str_para_intersecao(i) for i in ip)
        board = cria_goban(n, ib, ip) 
    except ValueError:
        raise ValueError('go: argumentos invalidos')

    score_msg = 'Branco (O) tem {} pontos\nPreto (X) tem {} pontos'    
    players = (cria_pedra_preta(), cria_pedra_branca())
    current = 0
    passed = [False, False]
    last_board = [cria_goban_vazio(n), cria_goban_vazio(n)]
    
    while not all(passed):
        print(score_msg.format(*calcula_pontos(board)))
        print(goban_para_str(board))
        
        last_board[current^1] = cria_copia_goban(board) 
        # print('Branco (O)' if pedras_iguais(players[current], cria_pedra_branca()) else 'Preto (X)' )
        passed[current] = not turno_jogador(board, players[current], last_board[current])
        
        current = current ^ 1 #xor
        # print()
        
    pontos = calcula_pontos(board)
    print(score_msg.format(*pontos))
    print(goban_para_str(board))
        
    return pontos[0] >= pontos[1]
 

eh_pedra(cria_pedra_branca())