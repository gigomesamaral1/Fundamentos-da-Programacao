

LETTERS = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# 2.1.1 - # minimo 1x1, maixmo até Z99
def eh_territorio(tab):
    return isinstance(tab, tuple) and 1 <= len(tab) <= 26 and \
        isinstance(tab[0], tuple) and 1 <= len(tab[0]) <= 99 and \
            all((type(v) == tuple and len(tab[0]) == len(v)) for v in tab) and \
            all((type(e) == int) and e in (0, 1) for v in tab for e in v)

# 2.1.2 - obtem ultima intersecao
def obtem_ultima_intersecao(board):
    if eh_territorio(board):
        v = LETTERS[len(board)-1]
        h = len(board[0])
        return v, h 
    raise ValueError('obtem_ultima_intersecao: argumento invalido')

# 2.1.3intersecao: de 'A1' até 'Z99'
def eh_intersecao(pos):
    return isinstance(pos, tuple) and len(pos) == 2 and \
        isinstance(pos[0], str) and pos[0] in LETTERS and \
            type(pos[1]) == int and 1 <= pos[1] <=99

# 2.1.4 eh_intersecao_valida - verfica se a intersecao está dentro do territorio
def eh_intersecao_valida(board, pos):
    if eh_territorio(board) and eh_intersecao(pos):
        last_pos = obtem_ultima_intersecao(board)
        return pos[0] <= last_pos[0] and pos[1] <= last_pos[1]
    raise ValueError('eh_intersecao_valida: argumentos invalidos')

# 2.1.5 - eh_intersecao_livre
def eh_intersecao_livre(board, pos):
    if eh_territorio(board) and eh_intersecao(pos) and eh_intersecao_valida(board, pos):
        v, h = LETTERS.index(pos[0]), pos[1]-1
        return board[v][h] == 0
    raise ValueError('eh_intersecao_livre: argumentos invalidos')

# 2.1.6 -  obtem\_intersecoes\_adjacentes    
def obtem_intersecoes_adjacentes(board, pos):
    move = {
        'U': lambda x: (x[0], x[1]+1),
        'D': lambda x: (x[0], x[1]-1),
        'L': lambda x: (('' if x[0] == 'A' else LETTERS[LETTERS.index(x[0])-1]), x[1]),
        'R': lambda x: (('' if x[0] == 'Z' else LETTERS[LETTERS.index(x[0])+1]), x[1]),
    }
    if eh_intersecao(pos) and eh_territorio(board):
        return tuple(move[d](pos) for d in ('D', 'L', 'R', 'U')
                     if eh_intersecao(move[d](pos)) and eh_intersecao_valida(board, move[d](pos)))
    raise ValueError('obtem_intersecoes_adjacentes: argumentos invalidos')

# 2.1.7 - ordena tuplo de interseções
def ordena_intersecoes(tup):
    if isinstance(tup, tuple) and all(eh_intersecao(i) for i in tup):
        return tuple(sorted(tup, key=lambda x:x[::-1]))
    raise ValueError('ordena_intersecoes: argumento invalido')

# 2.1.8 - territorio para str 
def territorio_para_str(tab):
    def obter_linha(tab, i):
        return tuple(tab[j][i] for j in range(len(tab)))
    if not eh_territorio(tab):
        raise ValueError('territorio_para_str: argumento invalido')
    
    n_v, n_h = len(tab), len(tab[0])
    cad = '   ' + ''.join(f'{l} ' for l in LETTERS[:n_v]).rstrip() + '\n' 
    for i in range(n_h):
        line = obter_linha(tab, n_h-i-1)
        cad += '{:>2} '.format(n_h-i)
        cad += ''.join('X ' if e else '. ' for e in line)
        cad += '{:>2}'.format(n_h-i) + '\n'
    cad += '   ' + ''.join(f'{l} ' for l in LETTERS[:n_v]).rstrip()
    
    return cad

# 2.2.1 - obtem\_cadeia(t,i)
def obtem_cadeia(board, pos):
    if not (eh_territorio(board) and eh_intersecao(pos) and eh_intersecao_valida(board, pos)):
        raise ValueError('obtem_cadeia: argumentos invalidos')
    state = eh_intersecao_livre(board, pos)
    chain, to_check = [], [pos]
    
    while to_check:
        pos = to_check.pop()
        chain.append(pos)
        for new_pos in obtem_intersecoes_adjacentes(board, pos):
            if eh_intersecao_livre(board, new_pos) == state and new_pos not in chain + to_check:
                to_check.append(new_pos)             
    return ordena_intersecoes(tuple(chain))

# 2.2.2 - obtem_vale(t,i)
def obtem_vale(board, pos):
    if not (eh_territorio(board) and eh_intersecao(pos) and eh_intersecao_valida(board, pos) and \
        not eh_intersecao_livre(board, pos)):
        raise ValueError('obtem_vale: argumentos invalidos')
    
    cadeia_montanhas = obtem_cadeia(board, pos)
    vale = []
    for pos in cadeia_montanhas:
        for new_pos in obtem_intersecoes_adjacentes(board, pos):
            if eh_intersecao_livre(board, new_pos) and new_pos not in vale:
                vale.append(new_pos)     
    return ordena_intersecoes(tuple(vale))
    
# 2.3.1 testa conexao
def verifica_conexao(board, pos1, pos2):
    if not (eh_territorio(board) and \
        eh_intersecao(pos1) and eh_intersecao_valida(board, pos1) and \
            eh_intersecao(pos2) and eh_intersecao_valida(board, pos2)):
        raise ValueError('verifica_conexao: argumentos invalidos')
    return pos2 in obtem_cadeia(board, pos1)
    
# 2.3.2 calcula\_numero\_montanhas
def calcula_numero_montanhas(board):
    if  not eh_territorio(board):
        raise ValueError('calcula_numero_montanhas: argumento invalido')
    return sum([sum(caminho) for caminho in board])
    
def aux_todas_cadeias(board):
    all_cadeias, cadeias_seen = [], ()
    last_pos = obtem_ultima_intersecao(board)
    last_h, last_v = LETTERS.index(last_pos[0]), last_pos[1]
    
    for h in LETTERS[:last_h+1]:
        for v in range(1, last_v+1):
            pos = h, v
            if (not eh_intersecao_livre(board, pos)) and pos not in cadeias_seen:
                this_cadeia = obtem_cadeia(board, pos)
                all_cadeias.append(this_cadeia)
                cadeias_seen += this_cadeia    
    return all_cadeias

# 2.3.3 calcula\_numero\_cadeias\_montanhas
def calcula_numero_cadeias_montanhas(board):
    if  not eh_territorio(board):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')       
    return len(aux_todas_cadeias(board))
    
# 2.3.4 calcula tamanho vales: territorio --> int
def calcula_tamanho_vales(board):
    if  not eh_territorio(board):
        raise ValueError('calcula_tamanho_vales: argumento invalido')
    
    valles = []
    for cadeia in aux_todas_cadeias(board):
        for pos in obtem_vale(board, cadeia[0]):
            if pos not in valles:
                valles.append(pos)
               
    return len(valles)
