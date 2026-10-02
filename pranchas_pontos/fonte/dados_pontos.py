# -*- coding: utf-8 -*-
"""Pontos hidraulicos - Residencia Ivan e Ana Neris - Nova Odessa, SP.

Coordenadas em metros no sistema da base (base.json): origem no canto superior esquerdo do
raster da planta de tomadas, x para a direita, y para baixo (mesma orientacao das pranchas de
eletrica e da planta de pontos hidraulicos).

POSICAO EM PLANTA: Planta Pontos Hidraulicos (LayOut, folha 07, Rev. 01, 29/09/2026) - vale
sobre o caderno quando houver divergencia (decisao do cliente, 30/09/2026). Cada ponto e
posicionado pela face da parede de referencia usada na propria planta + a cota publicada.

ALTURAS (a partir do piso acabado), com a fonte de cada valor:
  C = Caderno Detalhamento Residencia IC - Hidraulica Detalhe, Rev. 02 (24/09/2026)
  D = Definicao do cliente em 30/09/2026 (respostas as duvidas desta prancha)
  P = Padrao do escritorio: valores do R02 (28/09/2026), confirmados pelo cliente em 30/09/2026
  A = Adotado a partir do padrao do chuveiro (saida 2,10 / registro 1,10) - CONFIRMAR
"""

REV = 'R02'
DATA = '02/10/2026'
PROJETO = 'Residência Ivan e Ana Neris'
ENDERECO = 'Nova Odessa – SP'
RESP = ['Lidiane Barbosa · CAU A290220-6', 'Isadora Ferrari · CAU A263982-8']

FONTES = {
    'C': 'Caderno Hidráulica Detalhe · Rev. 02 · 24/09/2026',
    'D': 'Definição do cliente · 30/09 e 02/10/2026',
    'P': 'Padrão do escritório (R02) · confirmado em 30/09/2026',
    'A': 'Adotado do padrão do chuveiro · confirmar',
}

# servicos: tipo -> (sigla, nome, cor, cor do texto)
TIPOS = {
    'SC':  ('S',  'Saída de chuveiro (misturada)', None, '#ffffff'),
    'AF':  ('F',  'Água fria',                    '#1f45b5', '#ffffff'),
    'AQ':  ('Q',  'Água quente',                  '#d42a1e', '#ffffff'),
    'ESG': ('E',  'Esgoto',                       '#e3a64a', '#22251a'),
    'VD':  ('V',  'Válvula de descarga',          '#2f9e44', '#ffffff'),
    'RG':  ('R',  'Registro geral',               '#e8cf1f', '#22251a'),
}
SIGLA_TXT = {'SC': 'Saída', 'AF': 'AF', 'AQ': 'AQ', 'ESG': 'ESG', 'VD': 'VD', 'RG': 'RG'}

# ---------------------------------------------------------------------------------------
# Faces de parede (m) medidas na base vetorizada (geom.face).
F = dict(
    WSM_esq=0.423, WSM_sup=0.376, WSM_inf=3.830,
    W01_esq=2.445, W01_dir=5.260, W01_sup=8.748, W01_inf=10.265,
    W02_esq=2.453, W02_dir=5.260, W02_inf=8.639, W02_sup=7.079,
    WEX_esq=7.443, WEX_dir=10.504, WEX_inf=7.737, WEX_sup=6.275,
    COZ_esq=1.850, COZ_sup=13.531, COZ_inf=17.764,
    GOU_esq=7.443, GOU_sup=7.827, GOU_inf=12.362,
    LAV_esq=1.850, LAV_dir=4.625, LAV_inf=19.935, LAV_sup=17.905,
    MURO=0.270, CASA_ext=10.622,           # muro (face interna) e face externa da parede da casa (lado piscina)
    MURETA_n=16.016,                       # face norte da mureta do balcao da cozinha (1,83 x 0,11 m, DWG Prefeitura)
    COZ_ext=1.709, PORTAO=19.920,           # corredor externo: face externa da parede da cozinha; face do portao
    SALA_ext=11.633, RECUO_sup=15.929,      # recuo junto a sala
)

def cota(eixo, de, ate, txt, ref):
    return dict(eixo=eixo, de=de, ate=ate, txt=txt, ref=ref)

def P(cod, peca, x, y, parede, serv, cotas, eixo_txt, nota=None, esquematico=False):
    """parede: lado da parede em que o ponto esta ('esq','dir','sup','inf') visto de dentro
    do ambiente, ou None (ponto fora de parede, ex. ilha)."""
    return dict(cod=cod, peca=peca, x=round(x, 4), y=round(y, 4), parede=parede, serv=serv,
                cotas=cotas, eixo_txt=eixo_txt, nota=nota, esquematico=esquematico)

# servicos padrao dos banheiros
def chuveiro(): return [('SC', '2,10', 'C'), ('AF', '1,10', 'C'), ('AQ', '1,10', 'C')]
def ducha():    return [('AF', '0,50', 'P')]
def bacia():    return [('AF', '0,30', 'P'), ('ESG', 'piso', 'C')]          # caixa acoplada Roca ONA: sem VD (R02)
def cuba(af_fonte='C'): return [('AF', '0,60', af_fonte), ('AQ', '0,60', 'D'), ('ESG', '0,50', 'P')]
def rg(fonte='P'): return [('RG', '0,55', fonte)]

NOTA_CHUV = ('Kit Deca Acqua Plus + misturador de duas alavancas (Deca 4900). Registros AF/AQ já executados: '
             'afastamento lateral entre eles a medir em obra.')
NOTA_BACIA = 'Caixa acoplada Roca ONA: sem válvula de descarga. Altura do ponto AF (0,30) a conferir na ficha da Roca.'
NOTA_RG = 'Eixo sem cota: dentro do armário da bancada. Definir com a marcenaria.'

AMB = {}

# ---------------------------------------------------------------- Cozinha
AMB['COZ'] = dict(nome='Cozinha', sigla='COZ', pontos=[
    P('C1', 'Filtro', F['COZ_esq'], F['COZ_inf'] - 1.01, 'esq',
      [('AF', '1,00', 'C')],
      [cota('y', F['COZ_inf'], F['COZ_inf'] - 1.01, '1,01', 'parede inferior')],
      '1,01 da parede inferior'),
    P('C2', 'Cuba da pia · misturador monocomando', F['COZ_esq'], F['COZ_inf'] - 2.16, 'esq',
      [('AF', '0,50', 'D'), ('AQ', '0,50', 'C'), ('ESG', '0,35', 'C')],
      [cota('y', F['COZ_inf'], F['COZ_inf'] - 2.16, '2,16', 'parede inferior')],
      '2,16 da parede inferior'),
    P('C3', 'Geladeira', F['COZ_esq'] + 3.60, F['COZ_sup'], 'sup',
      [('AF', '1,25', 'C')],
      [cota('x', F['COZ_esq'], F['COZ_esq'] + 3.60, '3,60', 'parede da janela')],
      '3,60 da parede da janela (esquerda)', nota='Cota de 3,60 definida pelo cliente em 30/09 (planta: 3,59).'),
    P('C4', 'Lava-louças · face da mureta', F['COZ_esq'] + 1.90, F['MURETA_n'], 'inf',
      [('AF', '0,60', 'C'), ('ESG', '0,50', 'P')],
      [cota('x', F['COZ_esq'], F['COZ_esq'] + 1.90, '1,90', 'parede da janela')],
      '1,90 da parede da janela · na face norte da mureta do balcão (≈0,32 da ponta)',
      nota='Água e esgoto saem pela mureta do balcão (decisão de 02/10). Ponto de água sem torneira própria. '
           'Tomada da face do balcão afastada no mínimo 0,30 m (Tomadas R05, item 13.5).'),
])

# ---------------------------------------------------------------- Gourmet
AMB['GOU'] = dict(nome='Área Gourmet', sigla='GOU', pontos=[
    P('G1', 'Cuba · misturador de mesa', F['GOU_esq'], F['GOU_inf'] - 1.75, 'esq',
      [('AF', '0,50', 'D'), ('AQ', '0,50', 'C'), ('ESG', '0,50', 'D')],
      [cota('y', F['GOU_inf'], F['GOU_inf'] - 1.75, '1,75', 'parede inferior')],
      '1,75 da parede inferior (2,80 até a superior, conforme caderno)'),
])

# ---------------------------------------------------------------- Lavanderia
L = F['LAV_esq']
AMB['LAV'] = dict(nome='A.S. · Área de serviço', sigla='LAV', pontos=[
    P('L1', 'Torneira de parede · tanque', L + 0.35, F['LAV_inf'], 'inf',
      [('AF', '1,00', 'P')], [cota('x', L, L + 0.35, '0,35', 'parede esquerda')], '0,35 da parede esquerda',
      nota='Tanque único I.Corso: uma das duas torneiras (L1 ou L3) será vedada depois.'),
    P('L2', 'Torneira · lava e seca Brastemp', L + 0.64, F['LAV_inf'], 'inf',
      [('AF', '1,00', 'C'), ('ESG', '0,50', 'P')], [cota('x', L, L + 0.64, '0,64', 'parede esquerda')],
      '0,64 da parede esquerda (meio das torneiras)', nota='Ponto da lava e seca Brastemp (02/10); eixo no meio das torneiras (30/09).'),
    P('L3', 'Torneira de parede · tanque', L + 0.93, F['LAV_inf'], 'inf',
      [('AF', '1,00', 'P')], [cota('x', L, L + 0.93, '0,93', 'parede esquerda')], '0,93 da parede esquerda',
      nota='Tanque único I.Corso: uma das duas torneiras (L1 ou L3) será vedada depois.'),
    P('L4', 'Máquina de lavar roupas', L + 1.70, F['LAV_inf'], 'inf',
      [('AF', '0,70', 'C'), ('ESG', '0,60', 'P')], [cota('x', L, L + 1.70, '1,70', 'parede esquerda')], '1,70 da parede esquerda'),
    P('L5', 'Tanquinho', F['LAV_dir'] - 0.31, F['LAV_inf'], 'inf',
      [('AF', '0,70', 'C'), ('ESG', '0,50', 'P')], [cota('x', F['LAV_dir'], F['LAV_dir'] - 0.31, '0,31', 'parede direita')],
      '0,31 da parede direita'),
])

# ---------------------------------------------------------------- Banheiros
def wc_horizontal(sig, nome, esq, dir_, face, lado, ch, du, ba, cu, rg_fonte='P', af_cuba='C', pref=''):
    """Banheiro com as pecas numa parede horizontal (face y=face). ch = cota do chuveiro a
    partir da parede esquerda; du, ba, cu = cotas a partir da parede direita."""
    return dict(nome=nome, sigla=sig, pontos=[
        P(pref + '1', 'Chuveiro', esq + ch, face, lado, chuveiro(),
          [cota('x', esq, esq + ch, '%.2f' % ch, 'parede esquerda')], '%s da parede esquerda' % ('%.2f' % ch), nota=NOTA_CHUV),
        P(pref + '2', 'Ducha higiênica', dir_ - du, face, lado, ducha(),
          [cota('x', dir_, dir_ - du, '%.2f' % du, 'parede direita')], '%s da parede direita' % ('%.2f' % du)),
        P(pref + '3', 'Bacia sanitária', dir_ - ba, face, lado, bacia(),
          [cota('x', dir_, dir_ - ba, '%.2f' % ba, 'parede direita')], '%s da parede direita' % ('%.2f' % ba), nota=NOTA_BACIA),
        P(pref + '4', 'Cuba · misturador de mesa', dir_ - cu, face, lado, cuba(af_cuba),
          [cota('x', dir_, dir_ - cu, '%.2f' % cu, 'parede direita')], '%s da parede direita' % ('%.2f' % cu)),
        P(pref + '5', 'Registro geral', dir_ - cu - 0.30, face, lado, rg(rg_fonte), [], 'sem cota · dentro do armário',
          nota=NOTA_RG, esquematico=True),
    ])

def fmt(v): return ('%.2f' % v).replace('.', ',')

def _fix(amb):
    for p in amb['pontos']:
        for c in p['cotas']: c['txt'] = c['txt'].replace('.', ',')
        p['eixo_txt'] = p['eixo_txt'].replace('.', ',')
    return amb

AMB['W01'] = _fix(wc_horizontal('W01', 'Banho Suíte 1', F['W01_esq'], F['W01_dir'], F['W01_sup'], 'sup',
                                0.44, 1.66, 1.48, 0.56, pref='B1.'))
AMB['W02'] = _fix(wc_horizontal('W02', 'Banho Suíte 2', F['W02_esq'], F['W02_dir'], F['W02_inf'], 'inf',
                                0.44, 1.66, 1.48, 0.56, pref='B2.'))
AMB['W02']['nota'] = 'Espelhado em relação ao Banho Suíte 1 (mesmas cotas, peças na parede comum).'
AMB['WEX'] = _fix(wc_horizontal('WEX', 'Banho 4', F['WEX_esq'], F['WEX_dir'], F['WEX_inf'], 'inf',
                                0.54, 1.95, 1.73, 1.11, rg_fonte='C', af_cuba='D', pref='B4.'))
AMB['WEX']['pontos'][3]['peca'] = 'Cuba de sobrepor · misturador bica alta'
AMB['WEX']['pontos'][3]['nota'] = 'AF a 0,60 (mesma altura dos demais banhos), decisão mantida em 30/09. Misturador AF/AQ (02/10).'

# WC Suite Master: pecas na parede esquerda (vertical)
x0 = F['WSM_esq']; sup = F['WSM_sup']; inf = F['WSM_inf']
AMB['WSM'] = dict(nome='Banho Suíte Master', sigla='WSM', pontos=[
    P('BM.1', 'Chuveiro', x0, inf - 0.53, 'esq', chuveiro(),
      [cota('y', inf, inf - 0.53, '0,53', 'parede inferior')], '0,53 da parede inferior', nota=NOTA_CHUV),
    P('BM.2', 'Ducha higiênica', x0, sup + 0.26, 'esq', ducha(),
      [cota('y', sup, sup + 0.26, '0,26', 'parede superior')], '0,26 da parede superior'),
    P('BM.3', 'Bacia sanitária', x0, sup + 0.49, 'esq', bacia(),
      [cota('y', sup, sup + 0.49, '0,49', 'parede superior')], '0,49 da parede superior', nota=NOTA_BACIA),
    P('BM.4', 'Cuba · misturador de mesa', x0, sup + 1.62, 'esq', cuba(),
      [cota('y', sup, sup + 1.62, '1,62', 'parede superior')], '1,62 da parede superior'),
    P('BM.5', 'Registro geral', x0, sup + 1.32, 'esq', rg('P'), [], 'sem cota · dentro do armário',
      nota=NOTA_RG, esquematico=True),
])

# ---------------------------------------------------------------- Areas externas
AMB['EXT'] = dict(nome='Áreas externas', sigla='EXT', pontos=[
    P('X1', 'Ducha da piscina (água fria)', F['CASA_ext'] + 2.57, F['MURO'], 'sup',
      [('AF', '2,10', 'D')], [cota('x', F['CASA_ext'], F['CASA_ext'] + 2.57, '2,57', 'face externa da Suíte Master')],
      '2,57 da face externa da parede da Suíte Master · no muro', nota='Saída da ducha (kit chuveirão só água fria). Altura confirmada em 02/10.'),
    P('X2', 'Registro da ducha da piscina', F['CASA_ext'] + 3.07, F['MURO'], 'sup',
      [('AF', '1,10', 'D')], [cota('x', F['CASA_ext'], F['CASA_ext'] + 3.07, '3,07', 'face externa da Suíte Master')],
      '3,07 da face externa da parede da Suíte Master · no muro', nota='Registro da ducha. Altura confirmada em 02/10.'),
    P('X3', 'Torneira de jardim · corredor externo', F['COZ_ext'], F['PORTAO'] - 2.70, 'dir',
      [('AF', '0,50', 'D')], [cota('y', F['PORTAO'], F['PORTAO'] - 2.70, '2,70', 'portão do corredor')],
      '2,70 do alinhamento do portão · face externa da parede da cozinha'),
    P('X4', 'Torneira de jardim · recuo da sala', F['SALA_ext'] + 0.98, F['RECUO_sup'], 'sup',
      [('AF', '0,50', 'D')], [cota('x', F['SALA_ext'], F['SALA_ext'] + 0.98, '0,98', 'face externa da sala')],
      '0,98 da face externa da parede da sala'),
])

ORDEM = ['COZ', 'GOU', 'LAV', 'W01', 'W02', 'WSM', 'WEX', 'EXT']

# ---------------------------------------------------------------- Piscina (Vallauris iGUi)
# Implantacao medida na planta de layout (DETALHAMENTO A2 - LAYOUT, Rev. 01, 01/05/2026, 1:75):
# borda externa a 3,63 m da face externa da parede da Suite Master e a 1,50 m do muro.
# Conferencia: a ducha no layout fica a 2,55 m da mesma face (planta de pontos: 2,57).
PISCINA = dict(
    modelo='Vallauris · iGUi', ext=(3.39, 7.45), interna=(2.99, 7.05), prof=1.41, borda=0.20,
    x=F['CASA_ext'] + 3.63, y=F['MURO'] + 1.50,       # canto superior esquerdo da borda externa
    afast_fachada='3,63', afast_muro='1,50',
    casa_maquinas=(20.27, 0.48, 21.64, 1.85), g7=(20.36, 0.67, 21.11, 1.22), trocador=(21.15, 0.67, 21.55, 1.62),
    qc_max=(20.25, 0.26, 20.60, 0.37),
)

# Divergencias entre caderno (Rev. 02, 24/09) e planta (29/09): vale a planta (decisao 30/09).
REVISOES = {
    'LAV': [('Torneira · tanque', '0,40', '0,35'), ('Torneira · tanque', '1,00', '0,93'),
            ('Máquina de lavar', '1,80', '1,70'), ('Tanquinho', '2,55 (esq.)', '0,31 (dir.)')],
    'W01': [('Ducha higiênica', '1,20 (esq.)', '1,66 (dir.)'), ('Bacia', '1,40 (esq.)', '1,48 (dir.)'),
            ('Cuba', '2,35 (esq.)', '0,56 (dir.)'), ('Chuveiro', '0,45', '0,44')],
    'WSM': [('Ducha higiênica', '0,25', '0,26'), ('Bacia', '0,45', '0,49'), ('Cuba', '1,60', '1,62'),
            ('Chuveiro (da inferior)', '0,55', '0,53')],
    'WEX': [('Chuveiro', '0,55', '0,54'), ('Bacia (da dir.)', '1,75', '1,73'), ('Torneira (da dir.)', '1,15', '1,11')],
    'COZ': [('Filtro', '1,00', '1,01'), ('Cuba', '2,15', '2,16'), ('Lava-louças', '0,40 da borda da ilha', '1,90 · 2,30 das paredes')],
}
