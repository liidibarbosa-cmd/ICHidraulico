# -*- coding: utf-8 -*-
"""Pranchas 02 (Cozinha, Area Gourmet, A.S.) e 03 (Banhos): ampliacoes 1:25 + vistas."""
from svgkit import *
from planta import *
import dados_pontos as D
import pranchas as PR

PT = PR.PT
F = D.F

# ------------------------------------------------------------------ helpers de ampliacao
def ampliacao(s, v, pontos, pilulas=None, cotas_cfg=(), nomes=None, tam_pil=6.8):
    """desenha base recortada, pontos (pilhas), pilulas de codigo e cotas.
    pilulas: {cod: (dx, dy) em pt a partir do fim da pilha} (default: logo apos a pilha).
    cotas_cfg: lista de (cod, i_cota, desloc_m, ext_de_m, ext_ate_m, lado_txt).
    nomes: {cod: (tx_m, ty_m, anc)} para etiqueta completa (peca + alturas)."""
    desenhar_base(s, v)
    for cod, i, desloc, e1, e2, lado in cotas_cfg:
        p = PT[cod]; c = p['cotas'][i]
        if e2 is None: e2 = p['y'] if c['eixo'] == 'x' else p['x']
        cota(s, v, c, desloc, tam=7.6, ext_de=e1, ext_ate=e2, lado_txt=lado)
    for p in pontos:
        ex, ey = ponto_ampliado(s, v, p)
        nx, ny = NORMAL[p['parede']]
        if nomes and p['cod'] in nomes:
            tx, ty, anc = nomes[p['cod']]
            etiqueta(s, ex, ey, v.X(tx), v.Y(ty), p, anc=anc, tam=7.2)
            continue
        dx, dy = (pilulas or {}).get(p['cod'], (0, 0))
        px, py = ex + nx * 8 + dx, ey + ny * 8 + dy
        if dx or dy: s.line(ex, ey, px - (nx * 3), py - ny * 3, stroke=TINTA, sw=0.3)
        pilula(s, px, py + 2.4, p['cod'], tam_pil)

def titulo_vista(s, x, y, num, titulo, sub):
    s.circle(x + 10, y - 5, 10, fill=TERRA)
    s.text(x + 10, y - 1.2, num, 10.5, 'aloe', CREME, anc='middle')
    s.text(x + 26, y, titulo, 15, 'aloe', TINTA)
    s.text(x + 26, y + 13.5, sub, 9.5, 600, COTA_TXT)

def marca_vista(s, v, x, y, direcao, rot):
    """seta de vista: triangulo apontando para a parede das pecas."""
    X, Y = v.P(x, y)
    dx, dy = {'sup': (0, -1), 'inf': (0, 1), 'esq': (-1, 0), 'dir': (1, 0)}[direcao]
    px, py = -dy, dx
    a = (X + dx * 7, Y + dy * 7); b = (X + px * 6, Y + py * 6); c = (X - px * 6, Y - py * 6)
    s.path('M%.2f %.2f L%.2f %.2f L%.2f %.2f Z' % (a + b + c), fill=TINTA)
    s.circle(X - dx * 5, Y - dy * 5, 7.5, fill='#ffffff', stroke=TINTA, sw=0.6)
    s.text(X - dx * 5, Y - dy * 5 + 2.6, rot, 7, 700, TINTA, anc='middle')

def vista(s, ox, oy, escala, comp, pts_s, alt_max=2.40, niveis=None, rotulos=True, esq_txt='', dir_txt=''):
    """elevacao esquematica da parede das pecas. pts_s: lista de (s_m, ponto). comp: comprimento
    da parede (m) entre faces. oy = linha do piso (pt)."""
    k = 1000 / escala * MM
    X = lambda sm: ox + sm * k
    Y = lambda h: oy - h * k
    s.rect(X(0), Y(alt_max), comp * k, alt_max * k, fill='#fbf8f1', stroke=TINTA, sw=0.35)
    s.rect(X(-0.12), Y(alt_max), 0.12 * k, alt_max * k, fill=PAREDE)
    s.rect(X(comp), Y(alt_max), 0.12 * k, alt_max * k, fill=PAREDE)
    s.line(X(-0.3), oy, X(comp + 0.3), oy, stroke=PAREDE, sw=1.4)
    if esq_txt: s.text(X(0), oy + 10, esq_txt, 6.6, 600, COTA_TXT)
    if dir_txt: s.text(X(comp), oy + 10, dir_txt, 6.6, 600, COTA_TXT, anc='end')
    alturas = set()
    marcas = []
    rot_pts = []
    for sm, p in pts_s:
        grupos = {}
        for t, h, f in p['serv']:
            hv = 0.0 if h == 'piso' else float(h.replace(',', '.'))
            grupos.setdefault(hv, []).append((t, h))
        for hv, lst in grupos.items():
            alturas.add(hv)
            n = len(lst)
            for i, (t, h) in enumerate(lst):
                cx = X(sm) + (i - (n - 1) / 2) * 9.2
                marcas.append((cx, Y(hv) if hv > 0 else oy - 4.8, t, p['esquematico']))
        rot_pts.append((X(sm), max(grupos), p['cod']))
    # niveis (cotas de altura, estilo ordenada, a esquerda)
    xo = X(-0.12) - 12
    s.line(xo, oy, xo, Y(max(alturas)), stroke=COTA, sw=0.35)
    niv = [hv for hv in sorted(alturas) if hv > 0]
    ys = [Y(h) for h in niv]
    # espalha os rotulos (min. 8,4 pt) de baixo para cima
    lab = []
    for yy in ys:
        lab.append(min(yy, lab[-1] - 8.4) if lab else min(yy, oy - 6))
    for hv, yy, ly in zip(niv, ys, lab):
        s.line(xo - 2, yy, X(comp), yy, stroke=COTA, sw=0.3, dash='1 1.4')
        s.circle(xo, yy, 1.15, fill=COTA)
        s.line(xo - 2, yy, xo - 7, ly, stroke=COTA, sw=0.3)
        s.text(xo - 8, ly + 2.6, ('%.2f' % hv).replace('.', ','), 7.4, 600, COTA_TXT, anc='end')
    s.circle(xo, oy, 1.15, fill=COTA)
    s.text(xo - 8, oy + 2.6, '0,00', 7.4, 600, COTA_TXT, anc='end')
    # etiquetas numa faixa no alto (2,30 / 2,20), alternando quando os eixos estao proximos
    nivel_ant, x_ant = 1, -999
    for xx, hmax, cod in sorted(rot_pts):
        nivel = 1 - nivel_ant if xx - x_ant < 26 else 0
        hy = alt_max - 0.10 - nivel * 0.13
        s.line(xx, oy, xx, Y(hy) + 4, stroke=COTA, sw=0.35, dash='2 1.3')
        if rotulos: pilula(s, xx, Y(hy) + 2.2, cod, 6.2)
        nivel_ant, x_ant = nivel, xx
    for cx, cy, t, esq in marcas:
        marcador(s, cx, cy, t, 4.4, tracejado=esq)

def quadro_pontos(s, x0, y0, x1, y1, grupos, titulo='Pontos e alturas', quadro='1', entre=41.5):
    c = painel(s, x0, y0, x1, y1, TERRA, titulo, quadro)
    s.text(838, y0 + 48, 'CÓD.', 9.5, 700, c); s.text(876, y0 + 48, 'PEÇA · EIXO', 9.5, 700, c)
    s.text(1208, y0 + 48, 'ALTURAS (m) · FONTE', 9.5, 700, c, anc='end')
    y = y0 + 70
    for nome, cods, nota in grupos:
        s.text(838, y, nome.upper(), 10, 700, CREME, ls=1.4)
        s.line(838 + largura(nome.upper(), 10, 700, 1.4) + 8, y - 3.5, 1208, y - 3.5, stroke=CREME, sw=0.4, extra='opacity="0.45"')
        y += 17
        for cod in cods:
            p = PT[cod]
            s.text(838, y, cod, 11, 700, c)
            s.text(876, y, p['peca'], 11.2, 600, c)
            s.text(876, y + 13.2, p['eixo_txt'], 9.6, 300, c)
            xx = 876
            for t, h, f in p['serv']:
                marcador(s, xx + 4.2, y + 24.2, t, 4.2, tracejado=p['esquematico'])
                s.text(xx + 11.5, y + 27.4, h, 9.8, 600, c)
                w = largura(h, 9.8, 600)
                s.text(xx + 12.5 + w, y + 24.4, f, 6.6, 700, c)
                xx += 11.5 + w + 16
            y += entre
        if nota:
            y = paragrafo(s, 876, y - 6, nota, 330, 9.4, 400, c, entre=12.4) + 8
        y += 4
    return y

def quadro_revisoes(s, x0, y0, x1, y1, grupos, quadro='1A'):
    c = painel(s, x0, y0, x1, y1, OLIVA, 'Revisões sobre o caderno', quadro)
    s.text(838, y0 + 48, 'PEÇA', 9.5, 700, c); s.text(1080, y0 + 48, 'CADERNO', 9.5, 700, c, anc='end')
    s.text(1208, y0 + 48, 'PLANTA 29/09', 9.5, 700, c, anc='end')
    y = y0 + 68
    for nome, linhas in grupos:
        s.text(838, y, nome.upper(), 9.6, 700, c, ls=1.3); y += 15.5
        for peca, a, b in linhas:
            s.text(838, y, peca, 10.4, 400, c); s.text(1080, y, a, 10.4, 300, c, anc='end'); s.text(1208, y, b, 10.4, 700, c, anc='end')
            y += 14.6
        y += 5
    paragrafo(s, 838, y + 2, 'Eixos em metros. Vale a Planta Pontos Hidráulicos (decisão do cliente, 30/09/2026).', 370, 9.8, 400, c, entre=13)
    return y

# ------------------------------------------------------------------ PRANCHA 02
def prancha02():
    s = Svg(); moldura(s)
    # Cozinha 1:25
    vc = Vista(40, 88, 25, 1.55, 13.30, clip=(1.55, 13.30, 6.02, 18.02))
    titulo_vista(s, 40, 58, '1', 'Cozinha', 'Escala 1:25 · pontos C1 a C4')
    ampliacao(s, vc, D.AMB['COZ']['pontos'],
              cotas_cfg=[('C1', 0, 2.30, None, None, 1), ('C2', 0, 2.62, None, None, 1),
                         ('C3', 0, 13.98, None, None, 1), ('C4', 0, 15.50, None, None, 1)],
              nomes={'C1': (2.95, 17.05, 'start'), 'C2': (2.95, 15.02, 'start'), 'C3': (4.05, 14.40, 'start'),
                     'C4': (4.30, 15.62, 'start')})
    s.text(vc.X(1.63), vc.Y(14.6), 'JANELA', 6.4, 600, COTA_TXT, rot=-90, anc='middle')
    # Gourmet 1:25
    vg = Vista(582, 88, 25, 6.95, 7.70, clip=(6.95, 7.70, 8.55, 12.55))
    titulo_vista(s, 582, 58, '2', 'Área Gourmet', 'Escala 1:25 · ponto G1')
    ampliacao(s, vg, D.AMB['GOU']['pontos'], cotas_cfg=[('G1', 0, 8.22, None, None, 1)],
              nomes={'G1': (7.62, 10.12, 'start')})
    s.text(vg.X(8.0), vg.Y(9.0), 'área gourmet', 7, 500, COTA_TXT, anc='middle')
    # Lavanderia 1:25
    vl = Vista(40, 728, 25, 1.55, 17.80, clip=(1.55, 17.80, 4.90, 21.10))
    titulo_vista(s, 40, 698, '3', 'A.S. · Área de serviço', 'Escala 1:25 · pontos L1 a L5')
    ampliacao(s, vl, D.AMB['LAV']['pontos'],
              cotas_cfg=[('L1', 0, 20.28, 19.95, None, 1), ('L2', 0, 20.48, 20.28, None, 1), ('L3', 0, 20.68, 20.48, None, 1),
                         ('L4', 0, 20.88, 20.68, None, 1), ('L5', 0, 20.28, 19.95, None, 1)])
    marca_vista(s, vl, 3.25, 18.25, 'inf', 'V1')
    comp = F['LAV_dir'] - F['LAV_esq']
    pts_s = [(F['LAV_dir'] - p['x'], p) for p in D.AMB['LAV']['pontos']]
    titulo_vista(s, 452, 818, 'V1', 'Vista da parede do tanque', 'Escala 1:25 · do interior (espelhada em relação à planta)')
    vista(s, 490, 1040, 25, comp, pts_s, alt_max=1.45, esq_txt='parede direita', dir_txt='parede esquerda')
    PR.titulo_desenho(s, 28, 1101, '02', 'Ampliações · cozinha · gourmet · lavanderia', 'Escala 1:25 · plotagem em A2 · cotas em metros a partir da face da parede indicada')
    barra_escala(s, 29, 1134.4, vc.k, [0, 0.5, 1, 1.5, 2])
    # coluna 2
    quadro_pontos(s, COL2[0], TOPO, COL2[1], 706.0, [
        ('Cozinha', ['C1', 'C2', 'C3', 'C4'], None),
        ('Área Gourmet', ['G1'], None),
        ('A.S. · Área de serviço', ['L1', 'L2', 'L3', 'L4', 'L5'], None)], titulo='Pontos e alturas')
    quadro_revisoes(s, COL2[0], 720.0, COL2[1], BASE, [
        ('Cozinha', D.REVISOES['COZ']), ('A.S.', D.REVISOES['LAV'])])
    # coluna 3
    PR.legenda(s, planta_geral=False)
    PR.observacoes(s, [
        ('Cozinha', 'Filtro e cuba na parede da janela. Geladeira a 3,60 da parede da janela, na parede superior. '
                    'Lava-louças: água e esgoto saem pela face norte da mureta do balcão (1,83 × 0,11 m), a 1,90 da parede da janela (R02).'),
        ('Lava-louças', 'Tomada da face do balcão afastada no mínimo 0,30 m dos pontos de água e esgoto (Tomadas R05, item 13.5).'),
        ('Área Gourmet', 'Cuba a 1,75 da parede inferior; fecha com os 2,80 até a parede superior do caderno. Misturador Deca Flex Plus (AF/AQ).'),
        ('A.S.', 'Posições conforme a planta de 29/09. Tanque único I.Corso: L1 e L3 ficam por ora; uma será vedada depois. '
                 'L2 = torneira da lava e seca Brastemp. Tanquinho cotado pela parede direita.'),
        ('Alturas', 'Do piso acabado ao eixo. A letra ao lado de cada altura indica a fonte (Quadro 1B da prancha 01).'),
        ('Escopo', 'Localização de pontos. Diâmetros, trajetos e declividades: projeto hidrossanitário.'),
    ])
    PR.cabec_carimbo(s, 'Pontos hidráulicos · ampliações', '1:25 · folha A2', 2, (113.386 / 2, 2, '0 — 2 m'))
    return s.svg()

# ------------------------------------------------------------------ PRANCHA 03
def prancha03():
    s = Svg(); moldura(s)
    # WC Suite Master
    vm = Vista(40, 88, 25, 0.20, 0.18, clip=(0.20, 0.18, 2.62, 4.02))
    titulo_vista(s, 40, 58, '6', 'Banho Suíte Master', 'Escala 1:25 · pontos BM.1 a BM.5')
    ampliacao(s, vm, D.AMB['WSM']['pontos'],
              cotas_cfg=[('BM.2', 0, 1.32, None, None, 1), ('BM.3', 0, 1.58, None, None, 1), ('BM.4', 0, 1.84, None, None, 1),
                         ('BM.1', 0, 1.32, None, None, 1)])
    marca_vista(s, vm, 2.05, 2.75, 'esq', 'V2')
    # WC 02 + WC 01
    vw = Vista(350, 88, 25, 2.25, 6.95, clip=(2.25, 6.95, 5.45, 10.42))
    titulo_vista(s, 350, 58, '4', 'Banhos Suíte 1 e Suíte 2', 'Escala 1:25 · pontos B1.1 a B1.5 e B2.1 a B2.5 (espelhado)')
    ptsw = D.AMB['W01']['pontos'] + D.AMB['W02']['pontos']
    ampliacao(s, vw, ptsw,
              cotas_cfg=[('B1.1', 0, 9.72, None, None, 1), ('B1.4', 0, 9.72, None, None, 1), ('B1.3', 0, 9.92, None, None, 1),
                         ('B1.2', 0, 10.12, None, None, 1),
                         ('B2.1', 0, 7.68, None, None, -1), ('B2.4', 0, 7.68, None, None, -1), ('B2.3', 0, 7.48, None, None, -1),
                         ('B2.2', 0, 7.28, None, None, -1)])
    s.text(vw.X(2.55), vw.Y(10.15), 'BANHO SUÍTE 1', 8, 700, COTA_TXT, ls=1)
    s.text(vw.X(2.55), vw.Y(7.30), 'BANHO SUÍTE 2', 8, 700, COTA_TXT, ls=1)
    marca_vista(s, vw, 5.0, 9.45, 'sup', 'V3'); marca_vista(s, vw, 5.0, 7.95, 'inf', 'V4')
    # WC Externo
    ve = Vista(40, 600, 25, 7.25, 6.12, clip=(7.25, 6.12, 10.70, 7.92))
    titulo_vista(s, 40, 570, '7', 'Banho 4', 'Escala 1:25 · pontos B4.1 a B4.5')
    ampliacao(s, ve, D.AMB['WEX']['pontos'],
              cotas_cfg=[('B4.2', 0, 6.42, None, None, 1), ('B4.3', 0, 6.62, None, None, 1),
                         ('B4.1', 0, 6.82, None, None, 1), ('B4.4', 0, 6.82, None, None, 1)])
    marca_vista(s, ve, 10.15, 7.05, 'inf', 'V5')
    # vistas 1:50
    def vw_(n, tit, ox, oy, amb, sfun, comp, e, d):
        titulo_vista(s, ox - 20, oy - 2.4 * 56.69 - 28, n, tit, 'Escala 1:50 · do interior · alturas do piso acabado')
        vista(s, ox, oy, 50, comp, [(sfun(p), p) for p in D.AMB[amb]['pontos']], esq_txt=e, dir_txt=d)
    vw_('V2', 'Banho Suíte Master', 530, 800, 'WSM', lambda p: F['WSM_inf'] - p['y'], F['WSM_inf'] - F['WSM_sup'], 'parede inferior', 'parede superior')
    vw_('V3', 'Banho Suíte 1', 70, 1048, 'W01', lambda p: p['x'] - F['W01_esq'], F['W01_dir'] - F['W01_esq'], 'esquerda', 'direita')
    vw_('V4', 'Banho Suíte 2', 330, 1048, 'W02', lambda p: F['W02_dir'] - p['x'], F['W02_dir'] - F['W02_esq'], 'direita', 'esquerda')
    vw_('V5', 'Banho 4', 590, 1048, 'WEX', lambda p: F['WEX_dir'] - p['x'], F['WEX_dir'] - F['WEX_esq'], 'direita', 'esquerda')
    PR.titulo_desenho(s, 28, 1101, '03', 'Ampliações · banheiros', 'Plantas 1:25 · vistas 1:50 · plotagem em A2 · cotas em metros a partir da face da parede indicada')
    barra_escala(s, 29, 1134.4, vm.k, [0, 0.5, 1, 1.5, 2])
    # coluna 2
    quadro_pontos(s, COL2[0], TOPO, COL2[1], BASE, [
        ('Banho Suíte 1', ['B1.1', 'B1.2', 'B1.3', 'B1.4', 'B1.5'], None),
        ('Banho Suíte 2 (espelhado)', ['B2.1', 'B2.2', 'B2.3', 'B2.4', 'B2.5'], None),
        ('Banho Suíte Master', ['BM.1', 'BM.2', 'BM.3', 'BM.4', 'BM.5'], None),
        ('Banho 4', ['B4.1', 'B4.2', 'B4.3', 'B4.4', 'B4.5'], None)], titulo='Pontos e alturas', entre=40.6)
    # coluna 3
    PR.legenda(s, planta_geral=False)
    PR.observacoes(s, [
        ('Chuveiro', 'Kit Acqua Plus: saída a 2,10; misturador de duas alavancas (AF/AQ) a 1,10, já executado: afastamento a medir em obra.'),
        ('Bacia', 'Roca ONA com caixa acoplada: alimentação a 0,30 (conferir na ficha da Roca) e esgoto no piso. Sem válvula de descarga.'),
        ('Registro geral', 'A 0,55, dentro do armário da bancada. Eixo sem cota (marcador tracejado): definir com a marcenaria.'),
        ('Referências', 'Banhos Suíte 1, Suíte 2 e Banho 4: chuveiro pela parede esquerda, demais peças pela direita. Banho Suíte Master: '
                        'peças pela parede superior, chuveiro pela inferior. Vistas esquemáticas: eixos e alturas, sem louças.'),
    ], y1=640.0, tam=10.6)
    c = painel(s, COL3[0], 654.0, COL3[1], 913.0, CREME, 'Revisões sobre o caderno', '3A')
    s.text(1263, 697, 'PEÇA', 8.4, 700, TINTA, ls=1); s.text(1540, 697, 'CADERNO', 8.4, 700, TINTA, ls=1, anc='end')
    s.text(1638, 697, 'PLANTA', 8.4, 700, TINTA, ls=1, anc='end')
    yy = 716
    for nome, linhas in (('Banhos Suíte 1 e 2', D.REVISOES['W01']), ('Banho Suíte Master', D.REVISOES['WSM']), ('Banho 4', D.REVISOES['WEX'])):
        s.text(1263, yy, nome, 9.2, 700, TERRA); yy += 12.4
        for peca, x_, y_ in linhas:
            s.text(1263, yy, peca, 9, 400, TINTA); s.text(1540, yy, x_, 9, 300, TINTA, anc='end'); s.text(1638, yy, y_, 9, 700, TINTA, anc='end')
            yy += 11.4
        yy += 3
    paragrafo(s, 1263, yy + 4, 'Vale a planta de 29/09. Nos Banhos Suíte 1/2 a soma das cotas do caderno (2,90) excedia a largura do ambiente.', 375, 8.6, 500, COTA_TXT, entre=11)
    PR.cabec_carimbo(s, 'Pontos hidráulicos · banheiros', '1:25 e 1:50 · folha A2', 3, (113.386 / 2, 2, '0 — 2 m (1:25)'))
    return s.svg()
