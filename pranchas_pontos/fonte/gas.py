# -*- coding: utf-8 -*-
"""Prancha de pontos de gas (GLP) - Residencia Ivan e Ana Neris - 01/01, A2 paisagem, mesmo padrao
grafico das pranchas hidraulicas/eletrica. Gera gas.html.

Definicoes do cliente (01/10/2026): abrigo de GLP com 2 botijoes P13 sob as condensadoras C1 e C2,
na projecao delas; unico ponto de consumo: fogao da cozinha, eixo a 1,36 da parede da janela, a 0,60
do piso acabado. Condensadoras e tomadas: prancha de Tomadas R05 (posicao das condensadoras A CONFIRMAR
no caderno de ar condicionado)."""
import os
from svgkit import *
from planta import *
import dados_pontos as D
import pranchas as PR
import ampliacoes as AM

DATA = '02/10/2026'
GAS = '#f0b400'
D.TIPOS['GAS'] = ('G', 'Gás (GLP)', GAS, TINTA)
D.SIGLA_TXT['GAS'] = 'Gás'
F = D.F

# condensadoras (hachura da prancha de Tomadas R05, em metros na base)
COND = {'C1': (1.718, 7.161, 2.117, 8.163), 'C2': (1.718, 9.158, 2.117, 10.160)}
TOM_C = [(2.10, 8.473), (2.10, 8.848)]          # tomadas das condensadoras (cotas 1,40 da eletrica), h 1,50
FOGAO = dict(cod='PG1', peca='Fogão de piso 5 bocas', x=F['COZ_esq'] + 1.36, y=F['COZ_sup'], parede='sup',
             serv=[('GAS', '0,60', 'D')], esquematico=False,
             cotas=[dict(eixo='x', de=F['COZ_esq'], ate=F['COZ_esq'] + 1.36, txt='1,36', ref='parede da janela')],
             eixo_txt='1,36 da parede da janela · parede superior da cozinha')
MURO_CORR = 0.321                               # face do muro no corredor externo (base)

def hachura(s, v, r, cor=TINTA, passo=0.10, sw=0.3):
    x0, y0, x1, y1 = r
    cid = s.uid('hc')
    s.defs.append('<clipPath id="%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/></clipPath>'
                  % (cid, v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k))
    s.group('clip-path="url(#%s)"' % cid)
    t = -(y1 - y0)
    while t < (x1 - x0):
        s.line(v.X(x0 + t), v.Y(y1), v.X(x0 + t + (y1 - y0)), v.Y(y0), stroke=cor, sw=sw)
        t += passo
    s.end()

def abrigo(s, v, rotulos=True, botijoes=True):
    for nome, r in COND.items():
        x0, y0, x1, y1 = r
        s.rect(v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k, fill='#fdf1c8', stroke=GAS, sw=0.9)
        hachura(s, v, r, cor='#b9a46a', passo=0.10 if v.k > 50 else 0.16, sw=0.25)
        s.rect(v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k, stroke=TINTA, sw=0.45, extra='stroke-dasharray="3 1.6"')
        if botijoes:
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            s.circle(v.X(cx), v.Y(cy), 0.165 * v.k, fill='#ffffff', stroke=GAS, sw=0.9, dash='2 1.2')
            if v.k > 50:
                s.text(v.X(cx), v.Y(cy) + 2.6, 'P13', 7.2, 700, TINTA, anc='middle')
        if rotulos and v.k > 50:
            s.text(v.X(x0) - 4, v.Y((y0 + y1) / 2) + 2.5, nome, 8.5, 700, TINTA, anc='end')

def tomadas_ref(s, v, tam=4.2):
    for x, y in TOM_C:
        X, Y = v.P(x, y)
        s.rect(X - tam, Y - tam, 2 * tam, 2 * tam, fill='#ffffff', stroke=TERRA, sw=0.6)
        s.text(X, Y + tam * 0.55, 'C', tam * 1.45, 700, TERRA, anc='middle')

def legenda_gas(s):
    x0, x1 = COL3
    painel(s, x0, TOPO, x1, 306.1, CREME, 'Legenda', '2')
    xa, xb, yy = 1263.0, 1459.0, 78.0
    itens_a = [
        (lambda x, y: marcador(s, x + 5, y - 3.2, 'GAS', 4.6), 'Ponto de gás (GLP)'),
        (lambda x, y: (s.rect(x - 2, y - 8, 24, 9, fill='#fdf1c8', stroke=GAS, sw=0.9)), 'Abrigo de GLP'),
        (lambda x, y: s.circle(x + 6, y - 3.4, 4.6, fill='#ffffff', stroke=GAS, sw=0.9, dash='2 1.2'), 'Botijão P13 (esquemático)'),
        (lambda x, y: (s.rect(x - 2, y - 8, 24, 9, stroke=TINTA, sw=0.45, extra='stroke-dasharray="3 1.6"'),
                       [s.line(x - 2 + i, y + 1, x + 7 + i, y - 8, stroke='#b9a46a', sw=0.3) for i in (0, 5, 10, 15)]), 'Condensadora (projeção)'),
        (lambda x, y: (s.rect(x + 1.8, y - 7.4, 8.4, 8.4, fill='#ffffff', stroke=TERRA, sw=0.6),
                       s.text(x + 6, y - 0.8, 'C', 6.1, 700, TERRA, anc='middle')), 'Tomada da condensadora'),
    ]
    itens_b = [
        (lambda x, y: pilula(s, x + 9, y, 'PG1', 6.4), 'Código do ponto'),
        (lambda x, y: selo(s, x + 5, y - 3.2, '1', 5.6, tam=6.6), 'Ampliação'),
        (lambda x, y: (s.line(x - 2, y - 3.2, x + 22, y - 3.2, stroke=COTA, sw=0.35), s.circle(x - 2, y - 3.2, 1.1, fill=COTA),
                       s.circle(x + 22, y - 3.2, 1.1, fill=COTA), s.text(x + 10, y - 5.4, '1,00', 6.5, 500, COTA_TXT, anc='middle')), 'Cota em metros'),
        (lambda x, y: s.rect(x - 2, y - 6, 24, 5.2, fill=PAREDE), 'Alvenaria'),
        (lambda x, y: s.rect(x - 2, y - 6, 24, 5.2, fill=JANELA), 'Janela / vidro'),
    ]
    for i, (fn, t) in enumerate(itens_a):
        fn(xa, yy + i * 18.6); s.text(xa + 31.8, yy + i * 18.6, t, 9.6, 400, TINTA)
    for i, (fn, t) in enumerate(itens_b):
        fn(xb, yy + i * 18.6); s.text(xb + 32, yy + i * 18.6, t, 9.6, 400, TINTA)
    s.text(xa, yy + 5 * 18.6 + 6, 'Altura do piso acabado ao eixo do ponto. Cores: amarelo = gás (NBR 6493).', 8.6, 500, COTA_TXT)

def prancha_gas():
    s = Svg(); moldura(s)
    # ---------------- 1. planta de localizacao 1:100
    v = Vista(44, 100, 100, 0.0, 5.6, clip=(0.0, 5.6, 12.6, 21.2))
    AM.titulo_vista(s, 40, 58, '1', 'Planta de localização', 'Escala 1:100 · abrigo de GLP e ponto do fogão')
    desenhar_base(s, v)
    abrigo(s, v, rotulos=False, botijoes=False)
    marcador(s, v.X(FOGAO['x']), v.Y(FOGAO['y']) + 6, 'GAS', 3.8)
    for t, x, y, rot in (('CORREDOR EXTERNO', 1.02, 12.6, -90), ('COZINHA', 3.9, 15.3, 0), ('BANHO SUÍTE 2', 3.7, 7.6, 0), ('BANHO SUÍTE 1', 3.7, 9.6, 0),
                         ('A.S.', 3.2, 18.8, 0), ('SALA', 9.3, 14.5, 0)):
        s.text(v.X(x), v.Y(y), t, 6.6, 600, COTA_TXT, anc='middle', ls=0.9, rot=rot or None)
    for num, (a, b, c, d) in (('2', (1.6, 6.9, 2.5, 10.4)), ('3', (1.72, 13.42, 4.8, 14.3))):
        s.rect(v.X(a), v.Y(b), (c - a) * v.k, (d - b) * v.k, stroke=TERRA, sw=0.6, rx=4, extra='stroke-dasharray="3 1.6"')
        selo(s, v.X(c), v.Y(b), num, 7.2, tam=8.2)
    pilula(s, v.X(1.0), v.Y(8.66) + 2.4, 'AB', 6.6)
    pilula(s, v.X(FOGAO['x']), v.Y(13.98) + 2.4, 'PG1', 6.6)

    # ---------------- 2. abrigo 1:25
    va = Vista(430, 100, 25, 0.15, 6.85, clip=(0.15, 6.85, 2.75, 10.45))
    AM.titulo_vista(s, 430, 58, '2', 'Abrigo de GLP · corredor externo', 'Escala 1:25 · sob as condensadoras C1 e C2')
    desenhar_base(s, va)
    abrigo(s, va)
    tomadas_ref(s, va)
    s.text(va.X(1.0), va.Y(8.65), 'CORREDOR EXTERNO', 7.4, 600, COTA_TXT, anc='middle', ls=1, rot=-90)
    s.text(va.X(2.62), va.Y(7.9), 'BANHO SUÍTE 2', 7.4, 700, COTA_TXT, anc='middle', rot=-90)
    s.text(va.X(2.62), va.Y(9.6), 'BANHO SUÍTE 1', 7.4, 700, COTA_TXT, anc='middle', rot=-90)
    for nome, (x0, y0, x1, y1) in COND.items():
        cota(s, va, dict(eixo='y', de=y0, ate=y1, txt='1,00*'), 1.45, tam=7.6, ext_de=x0, ext_ate=x0)
    x0, y0, x1, y1 = COND['C1']
    cota(s, va, dict(eixo='x', de=x0, ate=x1, txt='0,40*'), 8.32, tam=7.4, ext_de=y1, ext_ate=y1, lado_txt=-1)
    for nome, (x0, y0, x1, y1) in COND.items():
        s.line(va.X(1.30), va.Y(8.66) + (-4 if nome == 'C1' else 6), va.X(x0), va.Y((y0 + y1) / 2), stroke=TINTA, sw=0.35)
        s.circle(va.X(x0), va.Y((y0 + y1) / 2), 0.9, fill=TINTA)
    pilula(s, va.X(1.30), va.Y(8.66) + 2.4, 'AB', 7.4)
    paragrafo(s, 430, 532, '* Projeção das condensadoras na prancha de Tomadas R05 (1,00 × 0,40 cada). Dimensões finais do abrigo, '
              'porta e ventilação a definir. Tomadas C a 1,50 m, acima do abrigo (Tomadas R05, item 10).', 300, 8.2, 500, COTA_TXT, entre=10.6)

    # ---------------- 3. cozinha 1:25 (parede do fogao)
    vc = Vista(40, 650, 25, 1.55, 13.25, clip=(1.55, 13.25, 4.85, 14.55))
    AM.titulo_vista(s, 40, 618, '3', 'Cozinha · parede do fogão', 'Escala 1:25 · ponto PG1')
    desenhar_base(s, vc)
    ex, ey = ponto_ampliado(s, vc, FOGAO)
    cota(s, vc, FOGAO['cotas'][0], 14.12, tam=7.6, ext_ate=F['COZ_sup'])
    etiqueta(s, ex, ey, vc.X(3.55), vc.Y(14.35), FOGAO, tam=7.2)
    s.text(vc.X(1.63), vc.Y(14.25), 'JANELA', 6.4, 600, COTA_TXT, rot=-90, anc='middle')
    marca = AM.marca_vista(s, vc, 2.6, 14.3, 'sup', 'V1')

    # ---------------- 4. vista da parede do fogao 1:25
    k = 113.386; ox, oy = 460, 1052
    AM.titulo_vista(s, 440, 760, 'V1', 'Vista da parede do fogão', 'Escala 1:25 · do interior · alturas do piso acabado')
    L, Hm = 2.60, 2.30
    s.rect(ox, oy - Hm * k, L * k, Hm * k, fill='#fbf8f1', stroke=TINTA, sw=0.35)
    s.rect(ox - 0.12 * k, oy - Hm * k, 0.12 * k, Hm * k, fill=PAREDE)
    s.line(ox - 0.3 * k, oy, ox + L * k + 0.1 * k, oy, stroke=PAREDE, sw=1.4)
    s.path('M%.2f %.2f l4 6 l-8 6 l8 6 l-4 6' % (ox + L * k, oy - Hm * k), stroke=TINTA, sw=0.5)
    s.text(ox, oy + 10, 'parede da janela', 6.6, 600, COTA_TXT)
    s.text(ox + L * k, oy + 10, 'continua', 6.6, 600, COTA_TXT, anc='end')
    xe = ox + 1.36 * k
    s.line(xe, oy, xe, oy - 2.2 * k, stroke=COTA, sw=0.35, dash='2 1.3')
    # cota horizontal 1,36
    s.line(ox, oy - 2.18 * k, xe, oy - 2.18 * k, stroke=COTA, sw=0.35)
    s.circle(ox, oy - 2.18 * k, 1.15, fill=COTA); s.circle(xe, oy - 2.18 * k, 1.15, fill=COTA)
    s.text((ox + xe) / 2, oy - 2.18 * k - 2.6, '1,36', 7.6, 600, COTA_TXT, anc='middle')
    # niveis
    xo = ox - 0.12 * k - 12
    s.line(xo, oy, xo, oy - 2.065 * k, stroke=COTA, sw=0.35)
    for h, lab in ((0.30, '0,30'), (0.60, '0,60'), (2.065, '2,065')):
        yy = oy - h * k
        s.line(xo - 2, yy, xe + 30, yy, stroke=COTA, sw=0.3, dash='1 1.4')
        s.circle(xo, yy, 1.15, fill=COTA)
        s.text(xo - 4, yy + 2.6, lab, 7.4, 600, COTA_TXT, anc='end')
    s.circle(xo, oy, 1.15, fill=COTA); s.text(xo - 4, oy + 2.6, '0,00', 7.4, 600, COTA_TXT, anc='end')
    marcador(s, xe, oy - 0.60 * k, 'GAS', 5.0)
    pilula(s, xe + 24, oy - 0.60 * k + 2.4, 'PG1', 6.8)
    for h, t in ((0.30, 'tomada de acendimento 0,30'), (2.065, 'tomada da coifa 2,065')):
        yy = oy - h * k
        s.path('M%.2f %.2f l5 -8 l-10 0 Z' % (xe, yy + 4), fill='#ffffff', stroke=TERRA, sw=0.6)
        s.text(xe + 9, yy + 2.5, t + ' (Tomadas R05)', 6.8, 600, TERRA)
    PR.titulo_desenho(s, 28, 1101, '01', 'Pontos de gás · GLP', 'Plotagem em A2 · cotas em metros a partir da face da parede indicada')
    barra_escala(s, 29, 1134.4, k, [0, 0.5, 1, 1.5, 2])

    # ---------------- coluna 2
    x0, x1 = COL2
    c = painel(s, x0, TOPO, x1, 474.0, TERRA, 'Pontos de gás', '1')
    s.text(838, 82, 'CÓD.', 9.5, 700, c); s.text(876, 82, 'ITEM · POSIÇÃO', 9.5, 700, c); s.text(1208, 82, 'ALTURA', 9.5, 700, c, anc='end')
    y = 108
    s.text(838, y, 'AB', 12, 700, c); s.text(876, y, 'Abrigo de GLP · 2 botijões P13', 12, 600, c); s.text(1208, y, 'piso', 12, 700, c, anc='end')
    y = paragrafo(s, 876, y + 15, 'No recuo do corredor externo, sob as condensadoras C1 e C2, na projeção de cada uma (1,00 × 0,40, '
                  'conforme a prancha de Tomadas R05). Disposição dos botijões esquemática. Dimensões finais, porta, ventilação e '
                  'fixação a definir com o fornecedor e o responsável técnico.', 320, 10.6, 300, c, entre=13.6) + 12
    s.text(838, y, 'PG1', 12, 700, c); s.text(876, y, 'Fogão de piso 5 bocas · cozinha', 12, 600, c); s.text(1208, y, '0,60 m', 12, 700, c, anc='end')
    y = paragrafo(s, 876, y + 15, '1,36 da parede da janela, na parede superior da cozinha: mesmo eixo do fogão e da coifa na prancha de '
                  'Tomadas R05. Altura definida pelo cliente em 01/10/2026.', 320, 10.6, 300, c, entre=13.6) + 14
    s.line(838, y - 6, 1208, y - 6, stroke=CREME, sw=0.4, extra='opacity="0.5"')
    y = paragrafo(s, 838, y + 10, 'Único ponto de consumo: cooktop do gourmet, secadora e trocador da piscina são elétricos e a '
                  'churrasqueira é a carvão (Tomadas R05 e definições de 30/09). Trajeto da tubulação, diâmetros, regulador e '
                  'registros: projeto de gás (NBR 15526), por profissional habilitado.', 370, 10.4, 400, c, entre=13.8)
    c = painel(s, x0, 488.0, x1, 786.0, OLIVA, 'Compatibilização', '1A')
    y = 534
    for tit, txt in (('Condensadoras', 'C1 e C2 (Gree G-Max multisplit 48.000 BTU/h) acima do abrigo. Altura de instalação e suporte '
                                      'a definir; localização ainda A CONFIRMAR no caderno de ar condicionado.'),
                     ('Tomadas C', 'Pontos de força das condensadoras a 1,50 m, entre C1 e C2 (Tomadas R05, item 10).'),
                     ('Janelas', 'As janelas J04 (peitoril 1,50) dos Banhos Suíte 1 e Suíte 2 ficam atrás das condensadoras.'),
                     ('Fogão', 'Tomada de acendimento a 0,30 e tomada da coifa a 2,065 no mesmo eixo do ponto de gás '
                               '(Tomadas R05, itens 13.1 e 13.7).')):
        s.text(838, y, tit, 11, 700, c)
        y = paragrafo(s, 952, y, txt, 256, 10.2, 300, c, entre=13.2) + 9
    c = painel(s, x0, 800.0, x1, BASE, CLARO, 'Verificar antes de executar', '1B')
    y = 848
    for txt in ('Afastamentos e ventilação do abrigo de GLP em relação a fontes de ignição (condensadoras e tomadas C), '
                'aberturas (janelas dos WCs), ralos e caixas, conforme NBR 13523, NBR 15526 e IT 28 do Corpo de Bombeiros de SP.',
                'Acesso para troca dos botijões e circulação livre no corredor externo.',
                'Afastamento entre o ponto de gás do fogão e a tomada de acendimento logo abaixo, no mesmo eixo.'):
        s.circle(842, y - 4, 2.2, fill=TERRA)
        y = paragrafo(s, 852, y, txt, 356, 10.4, 400, TINTA, entre=13.6) + 8

    # ---------------- coluna 3
    legenda_gas(s)
    PR.observacoes(s, [
        ('Escopo', 'Localização do abrigo de GLP e do ponto de consumo. Não é projeto de gás: rede interna, diâmetros, trajeto, '
                   'regulador, registros, teste de estanqueidade e ventilação seguem o projeto de gás do responsável técnico.'),
        ('Abrigo', 'Dois botijões P13 sob as condensadoras C1 e C2, na projeção delas. Posição das condensadoras conforme a prancha '
                   'de Tomadas R05; o caderno de ar condicionado ainda indica localização a confirmar.'),
        ('Fogão', 'Ponto de gás a 0,60 do piso acabado, no eixo de 1,36 da parede da janela. Conexão do fogão conforme o fabricante.'),
        ('Alturas e cotas', 'Alturas do piso acabado ao eixo. Cotas em metros, a partir da face da parede indicada. '
                            'Conferir as medidas no local.'),
        ('Normas', 'NBR 15526 (redes de distribuição interna de gases combustíveis), NBR 13523 (central de GLP) e '
                   'IT 28 do Corpo de Bombeiros do Estado de São Paulo.'),
    ])
    carimbo(s, PR.LOGO, 'Pontos de gás (GLP)', '1:100 e 1:25 · folha A2', '01/01', 'R02', DATA, (113.386 / 2, 2, '0 — 2 m (1:25)'),
            projeto=D.PROJETO, endereco=D.ENDERECO, resp=D.RESP)
    return s.svg()

if __name__ == '__main__':
    open(os.path.join(AQUI, 'gas.html'), 'w').write(PR.html([prancha_gas()]))
    print('ok')
