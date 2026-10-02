# -*- coding: utf-8 -*-
"""Gera pranchas.html: 4 pranchas A2 paisagem de pontos hidraulicos no padrao da eletrica.
  01/04 Planta geral de pontos (1:100)
  02/04 Ampliacoes: Cozinha, Area Gourmet, A.S. (1:25)
  03/04 Ampliacoes: Banheiros (1:25) + vistas das paredes hidraulicas (1:50)
  04/04 Piscina Vallauris (implantacao 1:100, modelo 1:50, pontos)
"""
import base64, os
from svgkit import *
from planta import *
import dados_pontos as D

LOGO = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(AQUI, 'img', 'logo_duas.png'), 'rb').read()).decode()
TOTAL = 4
PT = {p['cod']: p for k in D.ORDEM for p in D.AMB[k]['pontos']}

def cabec_carimbo(s, planta_txt, escala_txt, n, barra):
    carimbo(s, LOGO, planta_txt, escala_txt, '%02d/%02d' % (n, TOTAL), D.REV, D.DATA, barra,
            projeto=D.PROJETO, endereco=D.ENDERECO, resp=D.RESP)

# ------------------------------------------------------------------ legenda (quadro 2)
def legenda(s, y1=306.1, planta_geral=True, extra=None):
    x0, x1 = COL3
    painel(s, x0, TOPO, x1, y1, CREME, 'Legenda', '2')
    yy = 78.0; xa, xb = 1263.0, 1459.0
    col = []
    for t in ('AF', 'AQ', 'ESG', 'RG', 'SC'):
        col.append((lambda s, x, y, t=t: marcador(s, x + 5, y - 3.2, t, 4.6), D.TIPOS[t][1]))
    col2 = []
    if planta_geral:
        col2.append((lambda s, x, y: ponto_simples_leg(s, x + 5, y - 3.2), 'Eixo de ponto (planta geral)'))
    col2 += [
        (lambda s, x, y: marcador(s, x + 5, y - 3.2, 'RG', 4.6, tracejado=True), 'Ponto com eixo sem cota'),
        (lambda s, x, y: pilula(s, x + 9, y, 'B1.3', 6.4), 'Código do ponto'),
        (lambda s, x, y: selo(s, x + 5, y - 3.2, '4', 5.6, tam=6.6), 'Ampliação (Quadro 1)'),
        (lambda s, x, y: (s.line(x - 2, y - 3.2, x + 22, y - 3.2, stroke=COTA, sw=0.35), s.circle(x - 2, y - 3.2, 1.1, fill=COTA),
                          s.circle(x + 22, y - 3.2, 1.1, fill=COTA), s.text(x + 10, y - 5.4, '1,00', 6.5, 500, COTA_TXT, anc='middle')), 'Cota em metros'),
        (lambda s, x, y: s.rect(x - 2, y - 6, 24, 5.2, fill=PAREDE), 'Alvenaria'),
        (lambda s, x, y: s.rect(x - 2, y - 6, 24, 5.2, fill=JANELA), 'Janela / vidro'),
        (lambda s, x, y: (s.rect(x - 2, y - 6, 24, 5.2, fill='#ffffff', stroke=TINTA, sw=0.5),
                          [s.line(x + i * 2.4, y - 5.4, x + i * 2.4, y - 1.4, stroke=TINTA, sw=0.25) for i in range(9)]), 'Ralo linear (indicativo)'),
    ]
    if extra: col2 += extra
    for i, (fn, txt) in enumerate(col):
        fn(s, xa, yy + i * 18.6); s.text(xa + 31.8, yy + i * 18.6, txt, 9.6, 400, TINTA)
    for i, (fn, txt) in enumerate(col2):
        fn(s, xb, yy + i * 18.6); s.text(xb + 32, yy + i * 18.6, txt, 9.6, 400, TINTA)
    yl = yy + max(len(col), len(col2)) * 18.6 + 2
    s.text(xa, yl, 'Letra no círculo = serviço. Altura do piso acabado ao eixo do ponto.', 8.6, 500, COTA_TXT)

def ponto_simples_leg(s, x, y):
    s.circle(x, y, 2.6, fill='#ffffff', stroke=TINTA, sw=0.5)
    s.line(x - 3.8, y, x + 3.8, y, stroke=TINTA, sw=0.35); s.line(x, y - 3.8, x, y + 3.8, stroke=TINTA, sw=0.35)

def observacoes(s, itens, y0=320.4, y1=912.7, quadro='3', tam=11.2):
    x0, x1 = COL3
    painel(s, x0, y0, x1, y1, CLARO, 'Observações técnicas', quadro)
    y = y0 + 47
    for i, (tit, txt) in enumerate(itens):
        s.text(x0 + 16, y, '%d. %s' % (i + 1, tit), 12, 700, TERRA)
        y = paragrafo(s, x0 + 16, y + 16, txt, x1 - x0 - 34, tam, 400, TINTA, entre=tam * 1.36) + 8
    return y

def fontes_quadro(s, x0, y0, x1, y1, quadro, titulo='Fontes das alturas', fundo=CLARO, notas=None):
    c = painel(s, x0, y0, x1, y1, fundo, titulo, quadro)
    y = y0 + 50
    for k in ('C', 'D', 'P'):
        s.circle(x0 + 24, y - 3.8, 7.2, fill=TERRA if fundo != TERRA else CREME)
        s.text(x0 + 24, y - 0.4, k, 9, 700, CREME if fundo != TERRA else TERRA, anc='middle')
        y = paragrafo(s, x0 + 40, y, D.FONTES[k], x1 - x0 - 58, 11, 400, c) + 6
    if notas:
        y += 4
        for n in notas:
            y = paragrafo(s, x0 + 16, y, n, x1 - x0 - 34, 10.2, 400, c, entre=13.6) + 4
    return y

# ------------------------------------------------------------------ PRANCHA 01
ROTULOS = [  # (texto, x, y, rot)
    ('BANHO', 1.42, 2.4, 0), ('SUÍTE MASTER', 1.42, 2.7, 0), ('SUÍTE MASTER', 8.3, 2.1, 0), ('BANHO SUÍTE 2', 3.45, 7.55, 0), ('BANHO SUÍTE 1', 3.45, 9.55, 0),
    ('BANHO 4', 9.35, 6.62, 0), ('COZINHA', 4.6, 14.05, 0), ('ÁREA GOURMET', 9.0, 9.2, 0), ('A.S.', 3.3, 18.55, 0),
    ('CORREDOR EXTERNO', 1.02, 11.5, -90), ('RECUO', 14.2, 16.62, 0), ('SALA', 9.5, 14.2, 0),
]
AMPL = [  # (num, rotulo, (x0,y0,x1,y1) m, prancha, posicao do selo (x,y) m)
    ('1', 'Cozinha', (1.72, 13.42, 6.05, 17.88), '02', (6.05, 13.42)),
    ('2', 'Área Gourmet', (7.34, 9.95, 8.05, 11.25), '02', (8.05, 9.95)),
    ('3', 'A.S.', (1.72, 17.88, 4.72, 20.05), '02', (4.72, 17.88)),
    ('4', 'Banho Suíte 1', (2.35, 8.67, 5.36, 10.36), '03', (5.36, 10.36)),
    ('5', 'Banho Suíte 2', (2.35, 6.98, 5.36, 8.72), '03', (5.36, 6.98)),
    ('6', 'Banho Suíte Master', (0.32, 0.28, 2.5, 3.92), '03', (2.5, 0.28)),
    ('7', 'Banho 4', (7.34, 6.18, 10.6, 7.84), '03', (10.6, 6.18)),
]

def pontos_ext_planta(s, v):
    """X1..X4 com marcador colorido, codigo, altura e cotas (so aparecem nesta prancha e na 04)."""
    X1, X2, X3, X4 = PT['X1'], PT['X2'], PT['X3'], PT['X4']
    for p in (X1, X2, X3, X4):
        ponto_ampliado(s, v, p, r=3.6, afast=5.2, passo=7.6, eixo=False)
    # cotas X1/X2 (acima do muro, a partir da face externa da Suite Master)
    cota(s, v, X1['cotas'][0], -0.42, tam=7, ext_de=None, ext_ate=D.F['MURO'])
    cota(s, v, X2['cotas'][0], -0.85, tam=7, ext_de=None, ext_ate=D.F['MURO'])
    s.line(v.X(D.F['CASA_ext']), v.Y(D.F['MURO']), v.X(D.F['CASA_ext']), v.Y(-0.9), stroke=COTA, sw=0.35)
    for p, dx, dy in ((X1, -0.2, -2.3), (X2, 0.6, -1.55)):
        ax, ay = v.X(p['x']), v.Y(p['y']) + 2
        etq(s, ax, ay - 2, v.X(p['x'] + dx), v.Y(dy), p)
    # X3 corredor externo: cota vertical a partir do portao
    cota(s, v, X3['cotas'][0], 0.72, tam=7, ext_de=1.1, ext_ate=1.45)
    etq(s, v.X(1.55), v.Y(17.22), v.X(0.7), v.Y(22.3), X3)
    # X4 recuo da sala
    cota(s, v, X4['cotas'][0], 16.45, tam=7, ext_de=16.2, ext_ate=16.1)
    etq(s, v.X(12.62), v.Y(16.15), v.X(15.9), v.Y(17.7), X4)

def etq(s, ax, ay, tx, ty, p, tam=7.2):
    s.line(ax, ay, tx, ty - 2, stroke=TINTA, sw=0.35); s.circle(ax, ay, 0.9, fill=TINTA)
    xa, xb = pilula(s, tx, ty + 0.5, p['cod'], tam, anc='start')
    s.text(xb + 3, ty + 0.5, p['peca'], tam, 600, TINTA)
    s.text(xb + 3, ty + 0.5 + tam * 1.3, txt_alturas(p) + (' (confirmar)' if any(f == 'A' for _, _, f in p['serv']) else ''),
           tam * 0.95, 400, TINTA)

def piscina_planta(s, v, rotulos=True):
    P_ = D.PISCINA; w, l = P_['ext']; b = P_['borda']
    x, y = P_['x'], P_['y']
    s.rect(v.X(x), v.Y(y), w * v.k, l * v.k, fill='#e6f2fa', stroke='#4d85a8', sw=0.7)
    s.rect(v.X(x + b), v.Y(y + b), (w - 2 * b) * v.k, (l - 2 * b) * v.k, stroke='#4d85a8', sw=0.45)
    cm = P_['casa_maquinas']
    s.rect(v.X(cm[0]), v.Y(cm[1]), (cm[2] - cm[0]) * v.k, (cm[3] - cm[1]) * v.k, fill='#fcf2e6', stroke=TERRA, sw=0.6, extra='stroke-dasharray="3 1.5"')
    g = P_['g7']; s.rect(v.X(g[0]), v.Y(g[1]), (g[2] - g[0]) * v.k, (g[3] - g[1]) * v.k, fill='#f2f2ed', stroke=TINTA, sw=0.4, extra='stroke-dasharray="2 1.2"')
    s.text(v.X((g[0] + g[2]) / 2), v.Y((g[1] + g[3]) / 2) + 2.2, 'G7', 6.2, 700, TINTA, anc='middle')
    return x, y, w, l

def prancha01():
    s = Svg(); moldura(s)
    v = Vista(89.0, 127.0, 100)
    desenhar_base(s, v)
    # piscina (posicao a conferir) e casa de maquinas
    x, y, w, l = piscina_planta(s, v)
    s.text(v.X(x + w / 2), v.Y(y + l / 2) - 6, 'PISCINA', 7.5, 700, '#4d85a8', anc='middle', ls=1.2)
    s.text(v.X(x + w / 2), v.Y(y + l / 2) + 5, 'Vallauris · iGUi', 7, 500, '#4d85a8', anc='middle')
    s.text(v.X(x + w / 2), v.Y(y + l / 2) + 14, 'ver prancha 04', 7, 500, '#4d85a8', anc='middle')
    cm = D.PISCINA['casa_maquinas']
    s.text(v.X(cm[0]) - 4, v.Y(cm[1]) + 8, 'Casa de máquinas', 6.4, 600, TERRA, anc='end')
    s.text(v.X(cm[0]) - 4, v.Y(cm[1]) + 16, '(ref. Tomadas R05)', 6.4, 500, TERRA, anc='end')
    # rotulos de ambientes
    for t, rx, ry, rot in ROTULOS:
        s.text(v.X(rx), v.Y(ry), t, 6.6, 600, COTA_TXT, anc='middle', ls=0.9, rot=rot or None)
    # ampliacoes
    for num, nome, (a, b, c, d), pr, (sx, sy) in AMPL:
        s.rect(v.X(a), v.Y(b), (c - a) * v.k, (d - b) * v.k, stroke=TERRA, sw=0.6, rx=4, extra='stroke-dasharray="3 1.6"')
        selo(s, v.X(sx), v.Y(sy), num, 7.2, tam=8.2)
    # pontos internos
    for k in D.ORDEM:
        if k == 'EXT': continue
        for p in D.AMB[k]['pontos']:
            if p.get('ralo'):
                import ampliacoes as _AM; _AM.desenhar_ralo(s, v, p['ralo'])
            ponto_simples(s, v, p)
    pontos_ext_planta(s, v)
    titulo_desenho(s, 28, 1101, '01', 'Planta de pontos hidráulicos', 'Escala 1:100 · plotagem em A2 · posições conforme Planta Pontos Hidráulicos (29/09/2026)')
    barra_escala(s, 29, 1134.4, v.k, [0, 1, 2, 3, 4, 6, 8])

    # ---- coluna 2
    x0, x1 = COL2
    c = painel(s, x0, TOPO, x1, 530.0, TERRA, 'Pontos por ambiente', '1')
    s.text(838, 74 + 8, 'Nº', 9.5, 700, c); s.text(876, 82, 'AMBIENTE · PONTOS', 9.5, 700, c)
    s.text(1208, 82, 'PRANCHA', 9.5, 700, c, anc='end')
    linhas = [('1', 'Cozinha', 'C1 a C4 · filtro, cuba, geladeira e lava-louças (mureta)', '02'),
              ('2', 'Área Gourmet', 'G1 · cuba com misturador', '02'),
              ('3', 'A.S. · Área de serviço', 'L1 a L5 · torneiras e esgoto do tanque, máquina, tanquinho', '02'),
              ('4', 'Banho Suíte 1', 'B1.1 a B1.6 · chuveiro, ducha higiênica, bacia, cuba, registro, ralo', '03'),
              ('5', 'Banho Suíte 2', 'B2.1 a B2.6 · espelhado em relação ao Banho Suíte 1', '03'),
              ('6', 'Banho Suíte Master', 'BM.1 a BM.6 · chuveiro, ducha higiênica, bacia, cuba, registro, ralo', '03'),
              ('7', 'Banho 4', 'B4.1 a B4.6 · chuveiro, ducha, bacia, cuba de sobrepor, registro, ralo', '03'),
              ('8', 'Piscina', 'Ducha e registro (X1, X2), skimmer, retorno, reposição, ladrão, dreno', '04')]
    y = 108
    for num, amb, desc, pr in linhas:
        s.circle(846, y - 4, 9, fill=CREME); s.text(846, y - 0.2, num, 10, 700, TERRA, anc='middle')
        s.text(876, y, amb, 12, 600, c); s.text(1208, y, pr, 12, 700, c, anc='end')
        y = paragrafo(s, 876, y + 15, desc, 300, 11, 300, c) + 13
    y += 2
    s.line(838, y - 10, 1208, y - 10, stroke=CREME, sw=0.4, extra='opacity="0.5"')
    paragrafo(s, 838, y + 4, 'Planta: selos em terracota indicam a ampliação de cada ambiente; o círculo com cruz marca o eixo de cada ponto. '
              'Pontos externos X1 a X4 cotados nesta prancha (Quadro 1A).', 370, 10.5, 400, c, entre=14)

    c = painel(s, x0, 544.0, x1, 868.0, OLIVA, 'Pontos externos', '1A')
    s.text(838, 590, 'Nº', 9.5, 700, c); s.text(876, 590, 'PONTO · POSIÇÃO', 9.5, 700, c); s.text(1208, 590, 'ALTURA', 9.5, 700, c, anc='end')
    y = 613
    for cod in ('X1', 'X2', 'X3', 'X4'):
        p = PT[cod]
        s.text(838, y, cod, 12, 700, c); s.text(876, y, p['peca'], 12, 600, c)
        alt = p['serv'][0][1] + ' m' + ('*' if p['serv'][0][2] == 'A' else '')
        s.text(1208, y, alt, 12, 700, c, anc='end')
        y = paragrafo(s, 876, y + 15, p['eixo_txt'] + '.', 300, 11, 300, c) + 12
    paragrafo(s, 838, y + 2, 'Ducha de água fria junto à piscina (kit chuveirão só água fria): saída 2,10 e registro 1,10, confirmados em 02/10/2026.', 370, 10.2, 400, c, entre=13.6)

    fontes_quadro(s, x0, 882.0, x1, BASE, '1B', notas=[
        'Cada altura nos quadros das pranchas 02 a 04 traz a letra da sua fonte. Posições: Planta Pontos Hidráulicos (29/09/2026).',
        'R02 (02/10/2026): bacias Roca ONA com caixa acoplada (sem válvula de descarga); lavatórios e gourmet com misturador AF/AQ; '
        'lava-louças na face da mureta; nomes dos ambientes conforme a elétrica; CAU corrigido. R03: água fria do L2 eliminada. R04: L2 só com o esgoto do tanque; ralos lineares dos boxes (B1.6, B2.6, BM.6, B4.6).'])

    # ---- coluna 3
    legenda(s)
    observacoes(s, [
        ('Escopo', 'Prancha de localização de pontos. Não é projeto de dimensionamento: diâmetros, trajetos, declividades, ventilação, '
                   'caixas e ramais seguem o projeto hidrossanitário do responsável técnico.'),
        ('Posições', 'Cotas em metros, a partir da face da parede indicada em cada ponto. Os pontos dos ambientes estão cotados nas '
                     'ampliações (pranchas 02 e 03); os externos, nesta prancha.'),
        ('Alturas', 'Do piso acabado ao eixo do ponto. A fonte de cada valor está no Quadro 1B.'),
        ('Chuveiros', 'Kit Deca Acqua Plus com misturador de duas alavancas (água quente e fria); registros já executados. Sem chuveiro elétrico.'),
        ('Registro geral', 'Dentro do armário da bancada de cada banheiro, a 0,55 m. Eixo sem cota: definir com a marcenaria.'),
        ('Compatibilização', 'Pontos elétricos conforme a prancha de Tomadas R05. Manter no mínimo 0,30 m entre tomadas e pontos de '
                             'água e esgoto. Conferir as medidas no local antes de fechar as paredes.'),
        ('Normas', 'NBR 5626 (água fria e água quente), NBR 8160 (esgoto sanitário) e NBR 10339 (piscinas).'),
    ])
    cabec_carimbo(s, 'Pontos hidráulicos · geral', '1:100 · folha A2', 1, (28.3465 * 5 / 5, 5, '0 — 5 m'))
    return s.svg()

# ------------------------------------------------------------------ HTML
def html(folhas):
    ff = ''
    for w in (300, 400, 500, 600, 700):
        ff += "@font-face{font-family:'Manrope';font-weight:%d;src:url('fonts/manrope-latin-%d-normal.woff2') format('woff2');}\n" % (w, w)
    ff += "@font-face{font-family:'Aloevera';font-weight:700;src:url('fonts/aloevera-bold-dup.ttf') format('truetype');}\n"
    corpo = '\n'.join('<section class="folha">%s</section>' % f for f in folhas)
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Pontos hidráulicos · Residência IC</title><style>%s'
            '@page{size:594mm 420mm;margin:0}html,body{margin:0;padding:0;background:#fff}'
            'section.folha{width:594mm;height:420mm;overflow:hidden;page-break-after:always;break-after:page}'
            'section.folha svg{display:block}text{font-kerning:normal}</style></head><body>%s</body></html>' % (ff, corpo))

if __name__ == '__main__':
    import sys
    import ampliacoes
    folhas = [prancha01(), ampliacoes.prancha02(), ampliacoes.prancha03()]
    try:
        import piscina
        folhas.append(piscina.prancha04())
    except ImportError:
        pass
    open(os.path.join(AQUI, 'pranchas.html'), 'w').write(html(folhas))
    print('folhas:', len(folhas))
