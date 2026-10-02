# -*- coding: utf-8 -*-
"""Folhas 01 (planta-chave), 06 (Cozinha), 07 (Area Gourmet e A.S.), 08 (detalhes) e 09 (loucas e metais)."""
import math
from am_base import *
import ampliacoes as AM
import am_banhos as BH

F = D.F
PT = PR.PT
COZ_SUP_FIM = 5.989        # fim da parede superior da cozinha (vidro), base
MURETA = (3.433, 16.016, 5.268, 16.125)
CHURR = (7.443, 7.827, 8.243, 8.727)          # churrasqueira no canto (leitura do caderno de revestimentos R00, E11/E12)
FAIXA_RP06 = (8.727, 11.477, 0.98, 1.48)      # faixa de travertino: y0, y1 ao longo da parede esquerda; h0, h1

def ponto_extra(s, v, p, tam=6.4):
    ex, ey = ponto_ampliado(s, v, p)
    nx, ny = NORMAL[p['parede']]
    pilula(s, ex + nx * 8, ey + ny * 8 + 2.4, p['cod'], tam)

# ================================================================== 06 COZINHA
def folha_cozinha():
    s = folha('Cozinha')
    titulo(s, ML, 92, 'A', 'Planta · pontos', 'Escala 1:50 · cotas em metros a partir da face da parede indicada')
    clip = (1.55, 13.30, 6.30, 18.02)
    v = Vista(ML + 8, 108, 50, clip[0], clip[1], clip=clip)
    pts = D.AMB['COZ']['pontos']
    AM.ampliacao(s, v, pts, tam_pil=6.0, cotas_cfg=[
        ('C1', 0, F['COZ_esq'] + 0.80, None, None, 1), ('C2', 0, F['COZ_esq'] + 1.05, None, None, 1),
        ('C3', 0, F['COZ_sup'] + 0.85, None, None, 1), ('C4', 0, 15.45, None, None, 1)])
    ponto_extra(s, v, G.FOGAO, 6.0)
    cota(s, v, G.FOGAO['cotas'][0], F['COZ_sup'] + 1.10, tam=6.4, ext_ate=F['COZ_sup'])
    s.text(v.X(1.70), v.Y(15.24), 'J02', 6.2, 700, COTA_TXT, anc='middle', rot=-90)
    s.text(v.X(4.35), v.Y(16.36), 'mureta h 1,00', 6.0, 600, COTA_TXT, anc='middle')
    AM.marca_vista(s, v, 3.0, 15.0, 'esq', 'B'); AM.marca_vista(s, v, 4.20, 14.85, 'sup', 'B')
    AM.marca_vista(s, v, 4.85, 15.62, 'inf', 'C')
    yplan = 108 + (clip[3] - clip[1]) * K50
    xr = ML + (clip[2] - clip[0]) * K50 + 30
    y = quadro_pts(s, xr, 84, MR, ['C1', 'C2', 'C3', 'C4', 'PG1'], extra={'PG1': G.FOGAO})
    sup = COZ_SUP_FIM - F['COZ_esq']
    itens = [
        ('Revestimento', 'RP07 cerâmica simples (fundo da marcenaria) na parede da janela e na parede superior, até o forro 2,85 (caderno R00).', 'D'),
        ('J02', '2,35 × 0,45, peitoril 1,10 (caderno de revestimentos R00): conferir no quadro de esquadrias.', 'C'),
        ('Mureta', 'Planta 29/09: %s × %s, h 1,00. Caderno R00: 1,90 × 0,15. RP02 nas faces norte e sul.'
         % (fmt(MURETA[2] - MURETA[0]), fmt(MURETA[3] - MURETA[1])), 'C'),
        ('Parede sup.', 'Planta 29/09: %s até o vidro; caderno R00: 4,25.' % fmt(sup), 'C'),
        ('Lava-louças', 'Água e esgoto pela face norte da mureta; ponto de água sem torneira própria (02/10).', 'D'),
        ('Gás', 'PG1 fogão: ver prancha de pontos de gás R02.', 'D'),
        ('Piso', 'P01 Santorini OFW NAT 90 × 90 (caderno de pisos R00).', 'D'),
        ('Bancada', 'Bancadas e marcenaria: projeto de marcenaria e marmoraria.', 'A'),
    ]
    y2 = quadro_itens(s, xr, y + 10, MR, 'Elementos', itens)
    # ---------------- B: paredes planificadas 1:50
    k = K50
    ytB = max(yplan, y2) + 30
    oyB = ytB + 30 + 2.85 * k
    titulo(s, ML, ytB, 'B', 'Parede da janela e parede superior · planificadas',
           'Escala 1:50 · vistas de dentro · alturas do piso acabado')
    L1 = F['COZ_inf'] - F['COZ_sup']
    segs = [(L1, 'parede da janela (esquerda)'), (sup, 'parede superior')]
    clad = [(0, L1, 0, 2.85, 'RP07'), (L1, L1 + sup, 0, 2.85, 'RP07')]
    j0, j1 = F['COZ_inf'] - 16.416, F['COZ_inf'] - 14.056
    elems = [('janela', j0, j1, 1.10, 1.55, 'J02 2,35 × 0,45 · peitoril 1,10')]
    ptsB = [(F['COZ_inf'] - p['y'], p) for p in pts if p['parede'] == 'esq']
    ptsB += [(L1 + p['x'] - F['COZ_esq'], p) for p in pts if p['parede'] == 'sup']
    ptsB.append((L1 + G.FOGAO['x'] - F['COZ_esq'], G.FOGAO))
    elevacao(s, ML + 44, oyB, k, segs, 2.85, pontos=ptsB, clad=clad, elems=elems, tam_m=3.6,
             niveis_extra=[1.10, 1.55])
    # ---------------- C: mureta 1:25
    k = K25
    ytC = oyB + 52
    oyC = ytC + 34 + 1.25 * k
    titulo(s, ML, ytC, 'C', 'Mureta do balcão · face voltada para o fogão', 'Escala 1:25 · vista do lado do fogão e da geladeira (face norte da planta)')
    Lm = MURETA[2] - MURETA[0]
    c4 = PT['C4']
    sm = MURETA[2] - c4['x']
    elevacao(s, ML + 44, oyC, k, [(Lm, 'face da mureta')], 1.00, pontos=[(sm, c4)], clad=[(0, Lm, 0, 1.00, 'RP02')],
             dims=[(0, sm, 'até a ponta do lado da sala'), (sm, Lm, 'até a ponta do lado da janela')], tam_m=4.2)
    xn = ML + 44 + Lm * k + 40
    paragrafo(s, xn, ytC + 50, 'C4 cotado na planta a 1,90 da parede da janela (eixo); fica a %s da ponta da mureta do lado da janela. '
              'Tomada da face do balcão afastada no mínimo 0,30 m dos pontos (Tomadas R05, item 13.5).' % fmt(Lm - sm),
              MR - xn, 6.6, 400, TINTA, entre=9.2)
    paragrafo(s, xn, ytC + 92, 'Topo e cabeceiras da mureta: acabamento a definir com a marmoraria.', MR - xn, 6.6, 400, TINTA, entre=9.2)
    notas(s, [
        ('C2', 'Cuba Deca Suprema 75 × 40 inox com misturador monocomando 2275.INX (AF/AQ). Registro 4900.INX105.PQ sob a bancada.', 'D'),
        ('C1', 'Filtro Purific Camadas 10 (torneira própria do fabricante), ponto a 1,00.', 'D'),
        ('C4', 'Lava-louças: ESG a 0,50 (padrão do escritório) e AF a 0,60 (caderno), na face da mureta.', 'D'),
        ('Elevação', 'Planificada: parede da janela vista de dentro (esquerda = parede inferior) e, em seguida, parede superior.', None),
        ('Geometria', 'Mureta e paredes medidas na planta de 29/09; o caderno de revestimentos R00 usa a geometria do DWG R01.', 'C'),
    ], escala=(K50, [0, 1, 2, 3, 4], '1/50'))
    carimbo3(s, 6, 'Cozinha', '1/50 e 1/25')
    return s.svg()

# ================================================================== 07 GOURMET + A.S.
def folha_gourmet_as():
    s = folha('Gourmet e A.S.')
    # ---------------- Gourmet
    titulo(s, ML, 92, 'A', 'Área Gourmet · planta', 'Escala 1:50')
    clip = (7.25, 7.62, 10.72, 12.55)
    v = Vista(ML + 8, 108, 50, clip[0], clip[1], clip=clip)
    AM.ampliacao(s, v, D.AMB['GOU']['pontos'], tam_pil=6.0, cotas_cfg=[('G1', 0, F['GOU_esq'] + 0.95, None, None, 1)])
    x0, y0, x1, y1 = CHURR
    s.rect(v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k, fill=tint(RP['RP06'][0], 0.35), stroke=TINTA, sw=0.6,
           extra='stroke-dasharray="3 1.6"')
    s.text(v.X(x1) + 4, v.Y((y0 + y1) / 2), 'churrasqueira', 6.0, 700, TINTA)
    s.text(v.X(x1) + 4, v.Y((y0 + y1) / 2) + 7.6, '0,90 × 0,80 · a confirmar', 5.8, 400, TINTA)
    s.rect(v.X(F['GOU_esq']), v.Y(FAIXA_RP06[0]), 0.05 * v.k, (FAIXA_RP06[1] - FAIXA_RP06[0]) * v.k, fill=RP['RP06'][0])
    AM.marca_vista(s, v, 8.9, 10.2, 'esq', 'B')
    yA = 108 + (clip[3] - clip[1]) * K50
    # elevacao 1:50 da parede esquerda
    k = K50
    Lg = F['GOU_inf'] - F['GOU_sup']
    oxB = ML + (clip[2] - clip[0]) * K50 + 62
    titulo(s, oxB - 34, 92, 'B', 'Área Gourmet · parede esquerda', 'Escala 1:50 · vista de dentro')
    oyB = 108 + 26 + 3.40 * k
    sc0, sc1 = F['GOU_inf'] - CHURR[3], F['GOU_inf'] - CHURR[1]
    sf0, sf1 = F['GOU_inf'] - FAIXA_RP06[1], F['GOU_inf'] - FAIXA_RP06[0]
    g1 = PT['G1']
    elevacao(s, oxB, oyB, k, [(Lg, 'parede esquerda')], 3.40, pontos=[(F['GOU_inf'] - g1['y'], g1)],
             clad=[(sf0, sf1, FAIXA_RP06[2], FAIXA_RP06[3], 'RP06'), (sc0, sc1, 0, 3.40, 'RP06')],
             elems=[('volume', sc0, sc1, 0, 3.40, 'churrasqueira\n(frente, 0,80\nà frente da parede)'),
                    ('texto', 0, sf0 + 0.6, 2.40, 0, 'pintura')],
             dims=[(0, sf0, ''), (sf0, sf1, 'faixa RP06'), (sc0, sc1, 'churrasq.')], tam_m=3.6,
             niveis_extra=[FAIXA_RP06[2], FAIXA_RP06[3]])
    xq = oxB + Lg * k + 22
    yq = quadro_pts(s, xq, 84, MR, ['G1'])
    quadro_itens(s, xq, yq + 8, MR, 'Elementos', [
        ('Faixa RP06', 'Travertino Rock Face 0,98–1,48, 2,75 junto à churrasqueira.', 'D'),
        ('Churrasq.', 'Frente 0,90 e lateral 0,80, RP06 (caderno R00). Posição a confirmar.', 'C'),
        ('Boca', '0,80 × 0,80: altura a confirmar.', 'C'),
        ('Pé-direito', '3,40 (caderno R00); sem forro de gesso.', 'D'),
        ('Piso', 'P02 Santorini SGR HARD.', 'D'),
        ('Bancada', 'Marmoraria.', 'A'),
    ], larg_txt=MR - xq - 128)
    # ---------------- A.S.
    yT = max(yA, oyB + 30, 470) + 22
    titulo(s, ML, yT, 'C', 'A.S. · Área de serviço · planta', 'Escala 1:50')
    clip = (1.62, 17.72, 4.85, 20.12)
    v = Vista(ML + 8, yT + 16, 50, clip[0], clip[1], clip=clip)
    AM.ampliacao(s, v, D.AMB['LAV']['pontos'], tam_pil=5.6)
    s.text(v.X(3.24), v.Y(19.05), 'cotas dos eixos na vista D', 5.8, 500, COTA_TXT, anc='middle')
    AM.marca_vista(s, v, 3.2, 18.35, 'inf', 'D')
    yC = yT + 16 + (clip[3] - clip[1]) * K50
    quadro_pts(s, ML, yC + 12, ML + 262, ['L1', 'L2', 'L3', 'L4', 'L5'])
    k = K25
    Ll = F['LAV_dir'] - F['LAV_esq']
    oxD = ML + 262 + 66
    titulo(s, oxD - 34, yT, 'D', 'A.S. · parede do tanque', 'Escala 1:25 · vista de dentro (esquerda = parede direita)')
    oyD = min(yT + 30 + 2.85 * k, 840)
    elevacao(s, oxD, oyD, k, [(Ll, 'parede inferior')], 2.85,
             pontos=[(F['LAV_dir'] - p['x'], p) for p in D.AMB['LAV']['pontos']],
             clad=[(0, Ll, 0, 2.85, 'RP02')], dims=[(0, Ll, 'parede inferior (divisa com a garagem)')],
             cotas_extra=[(Ll - 0.35, Ll, '0,35', 'L1 · da parede esquerda', 1), (0, 0.31, '0,31', 'L5 · da parede direita', 1),
                          (Ll - 0.64, Ll, '0,64', 'L2', 2), (Ll - 0.93, Ll, '0,93', 'L3', 3), (Ll - 1.70, Ll, '1,70', 'L4', 4)])
    notas(s, [
        ('Gourmet', 'Cuba Deca Suprema 50 × 40 inox; misturador de mesa AF/AQ (proposta Deca Flex Plus 2250.C, folha 09).', 'P'),
        ('Churrasq.', 'Posição lida no caderno de revestimentos R00 (E11/E12): no canto junto ao Banho 4. Não consta na planta de 29/09.', 'C'),
        ('A.S.', 'Tanque I.Corso 60 × 57; L1 e L3 ficam, uma será vedada depois. L2 só com o esgoto do tanque (R04).', 'D'),
        ('A.S.', 'RP02 em toda a parede inferior até o forro 2,85 (caderno R00). Piso P01.', 'D'),
        ('Ralos', 'Ralo de piso na A.S. e na Área Gourmet: não indicado nos arquivos nem solicitado (02/10).', None),
        ('Varal', 'Varal de parede Varal Mágico 120 cm: posição a definir (parede com estrutura para o peso).', 'A'),
    ], escala=(K25, [0, 0.5, 1, 1.5, 2], '1/25 (1/50: ×2)'))
    carimbo3(s, 7, 'Gourmet e A.S.', '1/50 e 1/25')
    return s.svg()

# ================================================================== 08 DETALHES
def seta(s, x0, y0, x1, y1, cor=TERRA, sw=0.7):
    s.line(x0, y0, x1, y1, stroke=cor, sw=sw)
    a = math.atan2(y1 - y0, x1 - x0)
    s.path('M%.2f %.2f L%.2f %.2f L%.2f %.2f Z' % (x1, y1, x1 - 5 * math.cos(a - 0.4), y1 - 5 * math.sin(a - 0.4),
                                                    x1 - 5 * math.cos(a + 0.4), y1 - 5 * math.sin(a + 0.4)), fill=cor)

def rotulo(s, x, y, txt, st=None, anc='start', tam=6.4):
    s.text(x, y, txt, tam, 500, TINTA, anc=anc)
    if st: chip(s, x + (largura(txt, tam, 500) + 4 if anc == 'start' else 4), y, st, 4.3)

def folha_detalhes():
    s = folha('Detalhes')
    # ---------------- A: ralo linear em planta (esquematico)
    titulo(s, ML, 92, 'A', 'Ralo linear · planta esquemática', 'Sem escala · vale para os 4 boxes')
    x0, y0, w, h = ML + 20, 118, 220, 150
    s.rect(x0 - 8, y0 - 8, w + 8, h + 16, fill=PAREDE)
    s.rect(x0, y0, w, h, fill=PAPEL)
    s.rect(x0, y0, 5, h, fill=tint(RP['RP04'][0], 0.6))
    s.rect(x0, y0, w, 4, fill=tint(RP['RP02'][0], 0.6)); s.rect(x0, y0 + h - 4, w, 4, fill=tint(RP['RP02'][0], 0.6))
    s.rect(x0 + 9, y0 + 8, 13, h - 16, fill='#ffffff', stroke=TINTA, sw=0.7)
    for yy in range(int(y0 + 10), int(y0 + h - 9), 3): s.line(x0 + 10.5, yy, x0 + 20.5, yy, stroke=TINTA, sw=0.25)
    s.rect(x0 + w - 3, y0, 3, h, fill='#5b8fa8')
    for yy in (y0 + 40, y0 + 75, y0 + 110): seta(s, x0 + w - 30, yy, x0 + 30, yy)
    rotulo(s, x0 + 60, y0 + 58, 'caimento i = a definir', 'A')
    rotulo(s, x0 + 30, y0 + h + 22, 'ralo linear junto à parede do fundo', 'D')
    rotulo(s, x0 + 30, y0 + h + 34, 'modelo, grelha e comprimento', 'A')
    s.text(x0 - 12, y0 + h / 2, 'fundo do box', 6.0, 600, COTA_TXT, anc='middle', rot=-90)
    s.text(x0 + w + 8, y0 + h / 2, 'vidro de correr', 6.0, 600, '#3d6b80', anc='middle', rot=-90)
    # ---------------- B: corte esquematico
    titulo(s, 330, 92, 'B', 'Ralo linear · corte esquemático', 'Sem escala · sem dimensionamento')
    bx, by = 350, 260
    s.rect(bx, by - 150, 18, 190, fill=PAREDE)
    s.rect(bx + 18, by - 150, 4, 150, fill=tint(RP['RP04'][0], 0.7))
    s.path('M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (bx + 18, by + 14, bx + 300, by + 14, bx + 300, by - 4, bx + 48, by + 2),
           fill='#d9d2c3', stroke=TINTA, sw=0.5)
    s.line(bx + 48, by + 2, bx + 300, by - 4, stroke='#2a6fb0', sw=1.0, dash='3 1.5')
    s.rect(bx + 24, by - 4, 22, 14, fill='#ffffff', stroke=TINTA, sw=0.8)
    s.rect(bx + 30, by + 10, 10, 22, fill='#ffffff', stroke=TINTA, sw=0.6)
    s.rect(bx + 18, by + 14, 300, 26, fill='#ebe5d8', stroke=TINTA, sw=0.4)
    s.text(bx + 170, by + 31, 'laje / base', 6.0, 400, COTA_TXT, anc='middle')
    seta(s, bx + 260, by - 18, bx + 80, by - 12)
    rotulo(s, bx + 120, by - 24, 'caimento para o ralo: i = a definir', 'A')
    rotulo(s, bx + 60, by + 56, 'ralo linear junto ao fundo · ligação ao esgoto: projeto hidrossanitário', 'A')
    rotulo(s, bx + 150, by - 46, 'impermeabilização (tracejado azul): sistema a definir', 'A')
    rotulo(s, bx + 30, by - 128, 'parede do fundo · revestimento até o forro 2,85', 'D')
    rotulo(s, bx + 160, by + 8, 'P01 90 × 90', 'D')
    # ---------------- C: box de correr
    yC = 352
    titulo(s, ML, yC, 'C', 'Box de correr · planta e vista esquemáticas', 'Sem escala · vão de cada banho na tabela')
    px, py, pw = ML + 20, yC + 36, 300
    s.rect(px - 10, py - 6, 10, 40, fill=PAREDE); s.rect(px + pw, py - 6, 10, 40, fill=PAREDE)
    s.rect(px, py + 4, pw * 0.55, 3, fill='#5b8fa8'); s.rect(px + pw * 0.45, py + 11, pw * 0.55, 3, fill='#5b8fa8')
    s.text(px + pw * 0.25, py, 'folha A', 6.2, 700, '#3d6b80', anc='middle')
    s.text(px + pw * 0.78, py + 25, 'folha B', 6.2, 700, '#3d6b80', anc='middle')
    seta(s, px + pw * 0.62, py + 31, px + pw * 0.92, py + 31, cor='#3d6b80', sw=0.5)
    seta(s, px + pw * 0.92, py + 31, px + pw * 0.62, py + 31, cor='#3d6b80', sw=0.5)
    s.text(px + pw / 2, py + 46, 'interior do box (ralo junto ao fundo)', 5.8, 400, COTA_TXT, anc='middle')
    rotulo(s, px, py + 62, 'uma folha fixa e uma de correr; qual é a fixa (A ou B)', 'A')
    # vista
    vx, vy = px, py + 200
    hh = 2.10 * 50; s.line(vx - 12, vy, vx + pw + 12, vy, stroke=PAREDE, sw=1.4)
    s.rect(vx, vy - hh, pw * 0.55, hh, fill='#dbe8ee', stroke='#5b8fa8', sw=0.9)
    s.rect(vx + pw * 0.45, vy - hh, pw * 0.55, hh, fill='#cfe0e8', stroke='#5b8fa8', sw=0.9, extra='fill-opacity="0.8"')
    s.line(vx - 10, vy, vx - 10, vy - hh, stroke=TERRA, sw=0.4)
    s.text(vx - 13, vy - hh / 2, 'h 2,10', 6.4, 700, '#7a3423', anc='middle', rot=-90)
    s.line(vx, vy - hh - 18, vx + pw, vy - hh - 18, stroke=COTA, sw=0.35, dash='2 1.5')
    s.text(vx + pw / 2, vy - hh - 22, 'forro +2,85 · o box não vai até o forro', 5.8, 600, COTA_TXT, anc='middle')
    rotulo(s, vx + 6, vy + 12, 'vidro temperado; ferragem e perfis: previsão cromada (lista de louças)', 'A')
    # tabela de vaos
    tx = ML + 360
    s.rect(tx, yC + 20, MR - tx, 170, fill='#ffffff', rx=12, stroke='#e2d8c3', sw=0.6)
    taloe(s, tx + 12, yC + 40, 'Vãos dos boxes', 11.5)
    cab = ['Banho', 'Vão (fundo)', 'Lateral', 'Caderno R00']
    xs = [tx + 12, tx + 150, tx + 225, tx + 300]
    for x, c in zip(xs, cab): caps(s, x, yC + 58, c, 5.4, TERRA, ls=0.8, peso=700)
    yy = yC + 74
    for kk in ('W01', 'W02', 'WSM', 'WEX'):
        b = BH.BANHOS[kk]; larg, prof = BH.dims(b)
        for x, c in zip(xs, [b['nome'], fmt(larg), fmt(prof), '%s × %s' % b['caderno']]):
            s.text(x, yy, c, 6.8, 600 if x == xs[0] else 400, TINTA)
        yy += 13
    paragrafo(s, xs[0], yy + 6, 'Planta de 29/09 (base das pranchas), medido entre as faces das paredes. Medir o vão '
              'executado antes de encomendar o vidro.', MR - tx - 24, 6.3, 400, TINTA, entre=8.8)
    chip(s, xs[0], yy + 34, 'C', 4.4)
    # ---------------- D: nicho 1:10
    yD = 640
    titulo(s, ML, yD, 'D', 'Nicho · corte', 'Escala 1:10 · caderno de revestimentos R00')
    k = 1000 / 10 * MM
    nx, base = ML + 70, yD + 250
    esp = 0.15
    s.rect(nx, base - 0.62 * k, esp * k, 0.62 * k, fill='#bdb5a6')
    s.rect(nx + (esp - 0.10) * k, base - 0.30 * k - 0.16 * k, 0.10 * k, 0.30 * k, fill=PAPEL, stroke=TINTA, sw=0.6)
    cr = tint(RP['RP04'][0], 0.7)
    n0, n1 = base - 0.46 * k, base - 0.16 * k                   # topo e base do nicho (pt)
    s.rect(nx + esp * k, base - 0.62 * k, 3, n0 - (base - 0.62 * k), fill=cr)
    s.rect(nx + esp * k, n1, 3, base - n1, fill=cr)
    s.rect(nx + (esp - 0.10) * k, n0, 3, n1 - n0, fill=cr)      # fundo do nicho
    s.rect(nx + (esp - 0.10) * k, n0, 0.10 * k + 3, 3, fill=cr)  # teto
    s.rect(nx + (esp - 0.10) * k, n1 - 3, 0.10 * k + 3, 3, fill=cr)  # base
    yb = base - 0.16 * k
    s.line(nx + esp * k + 40, yb, nx + esp * k + 4, yb, stroke=TERRA, sw=0.4)
    s.text(nx + esp * k + 44, yb + 2, 'base a 1,00 do piso acabado', 6.4, 700, '#7a3423')
    xd = nx + esp * k + 12
    s.line(xd, n0, xd, n1, stroke=TERRA, sw=0.4)
    for yy in (n0, n1): s.line(xd - 2.5, yy, xd + 2.5, yy, stroke=TERRA, sw=0.4)
    s.text(xd + 4, (n0 + n1) / 2 + 2.2, '0,30', 6.4, 700, '#7a3423')
    s.text(nx + esp * k + 44, (n0 + n1) / 2 + 2.2, 'nicho em toda a largura do fundo do box', 6.4, 400, TINTA)
    s.text(nx + (esp - 0.05) * k, yb + 12, '0,10', 6.4, 700, '#7a3423', anc='middle')
    s.text(nx + esp * k / 2, base + 12, 'parede ≈0,15', 6.0, 600, COTA_TXT, anc='middle')
    rotulo(s, nx + esp * k + 44, yb + 18, 'fundo, base, teto e laterais no revestimento da parede', 'D')
    rotulo(s, nx + esp * k + 44, yb + 31, 'profundidade 0,10 em parede de ≈0,15: conferir', 'C')
    # ---------------- E: acessorios (alturas propostas)
    xe = 420
    titulo(s, xe, yD, 'E', 'Acessórios · alturas propostas', 'Eixo da peça a partir do piso acabado · linha Deca You')
    ac = [('Papeleira', 0.60, 'ao lado da bacia, ao alcance de quem está sentado'),
          ('Porta-toalha de rosto', 1.10, 'junto à bancada da cuba'),
          ('Porta-toalha barra (banho)', 1.20, 'fora do box, próximo à saída; Suíte Master: barra dupla 60 cm, barra superior'),
          ('Cabide', 1.70, 'se a peça escolhida for cabide')]
    kk = 100
    gx, gb = xe + 30, yD + 230
    s.line(gx, gb, gx, gb - 2.0 * kk, stroke=COTA, sw=0.5)
    for h in (0, 0.5, 1.0, 1.5, 2.0):
        s.line(gx - 3, gb - h * kk, gx, gb - h * kk, stroke=COTA, sw=0.5)
        s.text(gx - 5, gb - h * kk + 2, fmt(h), 5.8, 500, COTA_TXT, anc='end')
    s.line(gx - 8, gb, gx + 360, gb, stroke=PAREDE, sw=1.2)
    for nome, h, obs in ac:
        yy = gb - h * kk
        dy = -16 if h == 1.20 else 0                                # 1,20 e 1,10 proximos: texto da barra acima
        s.line(gx, yy, gx + 18, yy, stroke=TERRA, sw=0.6); s.circle(gx + 20, yy, 2.2, fill=TERRA)
        if dy: s.line(gx + 22, yy, gx + 26, yy + dy + 2, stroke=TERRA, sw=0.4)
        s.text(gx + 27, yy + 2.2 + dy, '%s · %s' % (nome, fmt(h)), 6.8, 700, TINTA)
        s.text(gx + 27, yy + 10.5 + dy, obs, 5.9, 400, COTA_TXT)
    chip(s, gx + 220, gb - 1.95 * kk, 'P', 4.6)
    s.text(gx, gb + 14, 'Sem saboneteira (definido). Lixeira fora do escopo. Fixar em parede com bucha adequada ao revestimento.', 6.0, 400, TINTA)
    notas(s, [
        ('Impermeab.', 'Sistema, extensão e altura de subida nas paredes do box e no piso dos banhos e da A.S.: a definir pelo '
                       'responsável técnico (NBR 9575 e NBR 9574).', 'A'),
        ('Desnível', 'Desnível entre o piso do box e o do banho e soleira do box: a definir com o ralo escolhido.', 'A'),
        ('Ralo', 'Linear, junto ao fundo do box, nos 4 banhos (02/10). Não há ralo fora do box.', 'D'),
        ('Box', 'Correr, 2 folhas (1 fixa + 1 de correr), h 2,10, não vai até o forro (02/10).', 'D'),
        ('Acessórios', 'Alturas propostas pelo escritório (liberado pelo cliente em 02/10): confirmar com as peças Deca You.', 'P'),
        ('Escopo', 'Desenhos esquemáticos de localização: não substituem o projeto hidrossanitário nem o de impermeabilização.', None),
    ])
    carimbo3(s, 8, 'Detalhes', 'indicadas')
    return s.svg()

# ================================================================== 09 LOUCAS E METAIS
LOUCAS = [
    ('Banhos Suíte 1 e Suíte 2 · por banho (×2)', [
        ('B1.1/B2.1', 'Kit chuveiro de parede com desviador e ducha manual', 'Deca · Acqua Plus', '—', 'Cromado', '1', 'D'),
        ('B1.1/B2.1', 'Acabamento de registro · misturador de duas alavancas', 'Deca · Level', '4900.C26.GD', 'Cromado', '1 conj.', 'D'),
        ('B1.2/B2.2', 'Ducha higiênica com registro e derivação', 'Deca · Level', '1984.C26.ACT', 'Cromado', '1', 'D'),
        ('B1.3/B2.3', 'Bacia com caixa acoplada + assento original', 'Roca · ONA', '—', 'Padrão', '1', 'D'),
        ('B1.4/B2.4', 'Cuba de embutir retangular 50 × 40', 'Deca', '—', 'Branca', '1', 'D'),
        ('B1.4/B2.4', 'Misturador de mesa bica baixa (AF/AQ) · substitui torneira 1193.C26', 'Deca · Level', '2875.C26', 'Cromado', '1', 'P'),
        ('B1.4/B2.4', 'Válvula de escoamento click · engates flexíveis (2 por misturador)', 'Deca', '1601.C.CLI · 4607.C.030/040', 'Cromado', '1 + 2', 'P'),
        ('—', 'Porta-toalha barra simples · porta-toalha de rosto/cabide · papeleira', 'Deca · You', '—', 'Cromado', '1 cada', 'D'),
    ]),
    ('Banho Suíte Master', [
        ('BM.1', 'Kit chuveiro Acqua Plus + acabamento misturador duas alavancas', 'Deca', '4900.C26.GD', 'Cromado', '1', 'D'),
        ('BM.2', 'Ducha higiênica com registro e derivação', 'Deca · Level', '1984.C26.ACT', 'Cromado', '1', 'D'),
        ('BM.3', 'Bacia com caixa acoplada + assento original', 'Roca · ONA', '—', 'Padrão', '1', 'D'),
        ('BM.4', 'Cuba de embutir 50 × 40 (1 cuba, 02/10)', 'Deca', '—', 'Branca', '1', 'D'),
        ('BM.4', 'Misturador de mesa bica baixa (AF/AQ) · substitui 1193.C26', 'Deca · Level', '2875.C26', 'Cromado', '1', 'P'),
        ('BM.4', 'Válvula click · engates flexíveis', 'Deca', '1601.C.CLI · 4607.C.030/040', 'Cromado', '1 + 2', 'P'),
        ('—', 'Porta-toalha barra dupla 60 cm', 'Deca · You', '2042.C104.060', 'Cromado', '1', 'D'),
        ('—', 'Porta-toalha de rosto/cabide · papeleira', 'Deca · You', '—', 'Cromado', '1 cada', 'D'),
    ]),
    ('Banho 4', [
        ('B4.1', 'Kit chuveiro Acqua Plus + acabamento misturador duas alavancas', 'Deca', '4900.C26.GD', 'Cromado', '1', 'D'),
        ('B4.2', 'Ducha higiênica com registro e derivação', 'Deca · Level', '1984.C26.ACT', 'Cromado', '1', 'D'),
        ('B4.3', 'Bacia com caixa acoplada + assento original', 'Roca · ONA', '—', 'Padrão', '1', 'D'),
        ('B4.4', 'Cuba de apoio/sobrepor retangular (cor verde fosco a confirmar na loja)', 'Deca · Slim', '—', 'Verde fosco', '1', 'C'),
        ('B4.4', 'Misturador de mesa bica alta (AF/AQ) · substitui Tube 1198.GF.TUB.MT', 'Deca · Unic', '2885.GF90.MT', 'Dark Antracite', '1', 'P'),
        ('B4.4', 'Válvula click (cromada, decisão do cliente) · engates flexíveis', 'Deca', '1601.C.CLI · 4607.C.030/040', 'Cromado', '1 + 2', 'P'),
        ('—', 'Porta-toalha barra simples · rosto/cabide · papeleira', 'Deca · You', '—', 'Cromado', '1 cada', 'D'),
    ]),
    ('Cozinha', [
        ('C2', 'Cuba de embutir 75 × 40 inox', 'Deca · Suprema', 'CC67075INX', 'Inox', '1', 'D'),
        ('C2', 'Misturador monocomando de mesa', 'Deca', '2275.INX', 'Inox', '1', 'D'),
        ('C2', 'Registro de gaveta, acabamento quadrado (sob a bancada)', 'Deca', '4900.INX105.PQ', 'Inox', '1', 'D'),
        ('C2', 'Sifão articulado 1½" + engates (referência de mercado)', 'Deca', '1682.C.112', 'Cromado/inox', '1 kit', 'C'),
        ('C1', 'Filtro/purificador com torneira própria', 'Purific · Camadas 10', '—', 'a escolher', '1', 'D'),
        ('C4', 'Lava-louças: só ponto de água e esgoto (sem torneira independente)', '—', '—', '—', '—', 'D'),
    ]),
    ('Área Gourmet', [
        ('G1', 'Cuba de embutir 50 × 40 inox', 'Deca · Suprema', 'CC66050INX', 'Inox', '1', 'D'),
        ('G1', 'Misturador de mesa bica móvel (AF/AQ) · substitui torneira 1167.C21', 'Deca · Flex Plus', '2250.C', 'Cromado', '1', 'P'),
        ('G1', 'Registro de gaveta, acabamento', 'Deca · Level', '4900.C26.GD', 'Cromado', '1', 'D'),
        ('G1', 'Sifão articulado 1½" + engates (referência de mercado)', 'Deca', '1682.C.112', 'Cromado/inox', '1 kit', 'C'),
    ]),
    ('A.S. · Área de serviço', [
        ('L2', 'Tanque moldado 60 × 57, 39 L', 'I.Corso · Premium', '—', 'Branco', '1', 'D'),
        ('L1·L3', 'Torneira de parede bica longa (uma das duas será vedada)', 'Deca · Link', '1178.C.LNK', 'Cromado', '1', 'D'),
        ('L4', 'Registro/torneira da máquina de lavar', '—', '—', 'Cromado', '1', 'A'),
        ('—', 'Varal de parede sanfonado 7 varetas, 120 cm', 'Varal Mágico', '—', 'Alumínio branco', '1', 'D'),
    ]),
    ('Áreas externas e boxes', [
        ('X1·X2', 'Kit chuveirão de parede, só água fria, com acabamento de registro', 'Deca + kit', 'a fechar', 'Cromado', '1', 'C'),
        ('X3·X4', 'Torneira de jardim com adaptador para mangueira (lista: qtd 1; pontos: 2)', 'Deca · Izy', '1153.C37', 'Cromado', '2', 'C'),
        ('Boxes', 'Vidro temperado de correr e ferragem dos 4 boxes (folha 08)', '—', '—', 'Cromado (previsão)', '4', 'A'),
    ]),
]

def folha_loucas():
    s = folha('Louças e metais')
    s.text(ML, 86, 'Lista técnica de compras de 25/09/2026 atualizada com as decisões de 02/10/2026. O código vale pela '
           'referência de cada linha; confirmar disponibilidade e acabamento na loja.', 6.8, 400, TINTA)
    cols = [(ML + 8, 'Ponto', None), (ML + 54, 'Item', 296), (ML + 360, 'Marca · linha', 92), (ML + 458, 'Referência', 112),
            (ML + 576, 'Acabamento', 66), (ML + 646, 'Qtd.', 34), (MR - 8, 'Status', None)]
    y = 106
    s.rect(ML, y, MR - ML, 16, fill=OLIVA, rx=4)
    for x, c, _ in cols: caps(s, x, y + 10.6, c, 5.4, CREME, ls=0.8, peso=700, anc='end' if c == 'Status' else 'start')
    y += 30
    for grupo, linhas in LOUCAS:
        taloe(s, ML + 8, y, grupo, 10.5, TERRA) if aloe_ok(grupo) else s.text(ML + 8, y, grupo, 9.6, 700, TERRA)
        y += 7
        s.line(ML, y, MR, y, stroke=TERRA, sw=0.5); y += 11
        for i, ln in enumerate(linhas):
            alt = 1
            partes = []
            for (x, c, w), val in zip(cols[:-1], ln[:-1]):
                partes.append(quebrar(val, w, 6.5, 400) if w else [val])
            alt = max(len(p) for p in partes)
            if i % 2 == 0: s.rect(ML, y - 8.6, MR - ML, alt * 8.8 + 4.4, fill='#efe8da')
            for (x, c, w), pl in zip(cols[:-1], partes):
                for j, t in enumerate(pl):
                    s.text(x, y + j * 8.8, t, 6.5, 700 if c == 'Ponto' else 400, TINTA)
            chip(s, MR - 8, y + 0.4, ln[-1], 4.2, anc='end')
            y += alt * 8.8 + 4.4
        y += 9
    notas(s, [
        ('Misturadores', 'Lavatórios e Área Gourmet passam a ter AF e AQ (02/10): as torneiras só de água fria da lista foram '
                         'trocadas por misturadores da mesma família (proposta do escritório). Confirmar preço e prazo.', 'P'),
        ('Engates', 'Cada misturador de mesa usa 2 engates flexíveis (AF e AQ): quantidade dobrada em relação à lista.', 'P'),
        ('Banho 4', 'Unic 2885.GF90.MT em Dark Antracite (alternativa: Duna Clássica 1877.GF64.MT). Válvula click cromada.', 'P'),
        ('Bacias', 'Roca ONA com caixa acoplada: dispensa válvula de descarga. Ponto AF a 0,30 a conferir na ficha técnica.', 'C'),
        ('Pendentes', 'Sifões compatíveis com as cubas Suprema, kit da ducha externa e registro da máquina: lista de controle de 25/09.', 'A'),
        ('Quantidade', 'Torneira de jardim: a lista prevê 1, mas há 2 pontos (X3 e X4, mantidos em 02/10).', 'C'),
    ], status_leg=True)
    carimbo3(s, 9, 'Louças e metais', 'sem escala')
    return s.svg()

# ================================================================== 01 PLANTA-CHAVE
FOLHAS = [('01', 'Planta-chave, índice e legenda', '1/100'), ('02', 'Banho Suíte 1', '1/25'), ('03', 'Banho Suíte 2', '1/25'),
          ('04', 'Banho Suíte Master', '1/25'), ('05', 'Banho 4', '1/25'), ('06', 'Cozinha', '1/50 · 1/25'),
          ('07', 'Área Gourmet e A.S.', '1/50 · 1/25'), ('08', 'Detalhes: ralo, box, nicho, acessórios', 'indicadas'),
          ('09', 'Louças e metais', '—')]
CHAVE = [('02', (2.445, 8.748, 5.26, 10.265)), ('03', (2.453, 7.079, 5.26, 8.639)), ('04', (0.423, 0.376, 2.406, 3.83)),
         ('05', (7.443, 6.275, 10.504, 7.737)), ('06', (1.85, 13.531, 5.989, 17.764)), ('07', (7.443, 7.827, 10.50, 12.362)),
         ('07', (1.85, 17.905, 4.625, 19.935))]

def folha_chave():
    s = folha('Planta-chave e índice')
    titulo(s, ML, 92, 'A', 'Planta-chave', 'Escala 1:100 · áreas molhadas e número da folha')
    clip = (0.15, 0.10, 12.0, 20.45)
    v = Vista(ML + 6, 106, 100, clip[0], clip[1], clip=clip)
    for _, (x0, y0, x1, y1) in CHAVE:
        s.rect(v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k, fill=tint(TERRA, 0.16))
    desenhar_base(s, v)
    for k_ in D.ORDEM:
        if k_ == 'EXT': continue
        for p in D.AMB[k_]['pontos']:
            if p.get('ralo'): AM.desenhar_ralo(s, v, p['ralo'])
            ponto_simples(s, v, p)
    for t, rx, ry, rot in PR.ROTULOS:
        if rx < clip[2]: s.text(v.X(rx), v.Y(ry), t, 5.6, 600, COTA_TXT, anc='middle', ls=0.6, rot=rot or None)
    for n, (x0, y0, x1, y1) in CHAVE:
        s.rect(v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k, stroke=TERRA, sw=0.7, rx=3, extra='stroke-dasharray="3 1.6"')
        selo(s, v.X(x1) - 2, v.Y(y0) + 2, n, 7.4, tam=7.0)
    xr = 410
    # indice
    s.rect(xr, 84, MR - xr, 196, fill=OLIVA, rx=12)
    taloe(s, xr + 12, 103, 'Índice', 11.5, CREME)
    y = 124
    for n, t, e in FOLHAS:
        s.text(xr + 12, y, n, 8, 700, CREME); s.text(xr + 36, y, t, 7.4, 500, CREME)
        s.text(MR - 12, y, e, 6.8, 300, CREME, anc='end'); y += 16.6
    # legenda
    y0 = 292
    s.rect(xr, y0, MR - xr, 300, fill='#ffffff', rx=12, stroke='#e2d8c3', sw=0.6)
    taloe(s, xr + 12, y0 + 19, 'Legenda', 11.5)
    yy = y0 + 38
    for t in ('AF', 'AQ', 'ESG', 'RG', 'SC', 'GAS'):
        marcador(s, xr + 18, yy - 2.4, t, 3.8); s.text(xr + 28, yy, D.TIPOS[t][1], 6.6, 400, TINTA); yy += 12.4
    marcador(s, xr + 18, yy - 2.4, 'RG', 3.8, tracejado=True); s.text(xr + 28, yy, 'Ponto com eixo sem cota', 6.6, 400, TINTA); yy += 12.4
    pilula(s, xr + 22, yy, 'B1.3', 5.6); s.text(xr + 36, yy, 'Código do ponto (= pranchas R04)', 6.6, 400, TINTA); yy += 12.4
    s.rect(xr + 10, yy - 5.5, 22, 5, fill='#ffffff', stroke=TINTA, sw=0.5); s.text(xr + 38, yy, 'Ralo linear (indicativo)', 6.6, 400, TINTA); yy += 12.4
    s.rect(xr + 10, yy - 4.5, 22, 2.2, fill='#5b8fa8'); s.text(xr + 38, yy, 'Vidro do box (de correr)', 6.6, 400, TINTA); yy += 12.4
    s.rect(xr + 10, yy - 5.5, 22, 5, fill=tint(TERRA, 0.16), stroke=TERRA, sw=0.6, extra='stroke-dasharray="3 1.6"')
    s.text(xr + 38, yy, 'Área detalhada · nº da folha', 6.6, 400, TINTA); yy += 12.4
    # revestimentos (coluna 2 da legenda)
    xx, yy2 = xr + 200, y0 + 38
    caps(s, xx, yy2 - 2, 'Revestimentos de parede', 5.4, TERRA, ls=0.8, peso=700); yy2 += 10
    for cod, (cor, nome, ref) in RP.items():
        if cod == 'RP03' or True:
            s.rect(xx, yy2 - 7, 14, 9, fill=cor, rx=2)
            s.text(xx + 19, yy2 - 1, cod + ' ' + nome, 6.2, 600, TINTA)
            s.text(xx + 19, yy2 + 6.6, ref, 5.6, 400, COTA_TXT); yy2 += 18
    caps(s, xr + 12, y0 + 232, 'Status das informações', 5.4, TERRA, ls=0.8, peso=700)
    desc = {'D': 'consta nos arquivos ou foi definido pelo cliente', 'P': 'proposta do escritório: aprovar',
            'A': 'falta definição: não executar sem ela', 'C': 'há divergência entre arquivos: conferir'}
    yy = y0 + 246
    for kk in 'DPAC':
        chip(s, xr + 12, yy, kk, 4.4); s.text(xr + 72, yy, desc[kk], 6.4, 400, TINTA); yy += 12
    # observacoes gerais
    y1 = y0 + 312
    quadro_itens(s, xr, y1, MR, 'Observações gerais', [
        ('Escopo', 'Detalhamento arquitetônico das áreas molhadas: pontos, box, ralo, nicho, revestimentos e louças. '
                   'Não é projeto hidrossanitário nem de impermeabilização.', None),
        ('Base', 'Planta de 29/09 (Tomadas R05 / Pontos Hidráulicos). Pontos e alturas iguais às pranchas hidráulicas R04.', None),
        ('Alturas', 'Do piso acabado. Forro +2,85 nos banhos, cozinha e A.S. (caderno de forro R01).', None),
        ('Fontes', 'Revestimentos de parede e piso R00, forro R01, lista de louças e metais (25/09), decisões do cliente de 30/09 e 02/10.', None),
        ('Nomes', 'Ambientes com os nomes da planta elétrica (decisão de 02/10).', None),
    ])
    notas(s, [
        ('Vãos', 'Os cadernos de revestimento R00 e o de forro usam a geometria do DWG R01 (boxes de 0,90; Banho 4 com 3,30). '
                 'Este caderno segue a planta de 29/09: revisar quantitativos.', 'C'),
        ('Forro R01', 'Diz "revestimento cerâmico total nos banhos"; a definição de 02/10 é revestir só o box.', 'C'),
        ('CAU', 'Cadernos de piso e parede R00 trazem A269382-8; o correto é A263982-8.', 'C'),
        ('Registros', 'Chuveiros: afastamento entre registros AF/AQ já executados a medir em obra.', 'C'),
        ('Roca ONA', 'Altura do ponto AF (0,30) a conferir na ficha técnica.', 'C'),
        ('Box', 'Lado da folha fixa e ferragem.', 'A'),
        ('Ralo', 'Modelo, comprimento, caimento e desnível; impermeabilização pelo responsável técnico.', 'A'),
        ('Gourmet', 'Posição da churrasqueira e altura da boca (caderno R00: a confirmar).', 'C'),
    ], titulo='Pendências e divergências', escala=(K100, [0, 1, 2, 3, 4, 5], '1/100'))
    carimbo3(s, 1, 'Planta-chave e índice', '1/100')
    return s.svg()
