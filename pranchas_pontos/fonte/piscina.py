# -*- coding: utf-8 -*-
"""Prancha 04: Piscina Vallauris (iGUi) - implantacao, esquema funcional dos pontos, modelo e cortes.
Geometria do modelo redesenhada a partir do desenho tecnico iGUi 'VALLAURIS 01/01' (vetores do PDF,
escala 45,71 pt/m conferida pelas cotas: 7,45 x 3,39 externa, 7,05 x 2,99 interna, 1,41 de profundidade)."""
import os
import pymupdf as fitz
from svgkit import *
from planta import *
import dados_pontos as D
import pranchas as PR
import ampliacoes as AM

IGUI = os.path.join(AQUI, '..', '..', 'referencias', 'pdfs_originais', 'VALLAURIS - IGUI.pdf')
K_IG = 322.32 / 7.05          # pt do PDF iGUi por metro
AZUL = '#4d85a8'

def linhas_igui(caixa, cores, larg_min=None):
    d = fitz.open(IGUI); p = d[0]; out = []
    x0, y0, x1, y1 = caixa
    for dr in p.get_drawings():
        col = tuple(round(c, 2) for c in (dr.get('color') or ()))
        r = dr['rect']
        if col not in cores or not (r.x0 >= x0 and r.x1 <= x1 and r.y0 >= y0 and r.y1 <= y1): continue
        if larg_min is not None and (dr.get('width') or 0) < larg_min: continue
        for it in dr['items']:
            if it[0] == 'l': out.append((it[1].x, it[1].y, it[2].x, it[2].y))
    return out

def desenhar_igui(s, linhas, ox, oy, orig, escala, cor=TINTA, sw=0.6):
    k = 1000 / escala * MM / K_IG
    for a, b, c, d in linhas:
        s.line(ox + (a - orig[0]) * k, oy + (b - orig[1]) * k, ox + (c - orig[0]) * k, oy + (d - orig[1]) * k, stroke=cor, sw=sw)
    return lambda x, y: (ox + x * K_IG * k, oy + y * K_IG * k)   # metros a partir da origem -> pt

def cota_simples(s, x1, y1, x2, y2, txt, lado=1, tam=7.4, cor=COTA_TXT):
    s.line(x1, y1, x2, y2, stroke=COTA, sw=0.35)
    s.circle(x1, y1, 1.1, fill=COTA); s.circle(x2, y2, 1.1, fill=COTA)
    if abs(y1 - y2) < 0.01:
        s.text((x1 + x2) / 2, y1 - 2.6 if lado > 0 else y1 + tam + 1, txt, tam, 600, cor, anc='middle')
    else:
        s.text(x1 - 2.6 if lado > 0 else x1 + tam + 1, (y1 + y2) / 2, txt, tam, 600, cor, anc='middle', rot=-90)

def caixa(s, x, y, w, h, t1, t2=None, fundo='#ffffff', borda=TINTA, cor=TINTA):
    s.rect(x, y, w, h, fill=fundo, stroke=borda, sw=0.6, rx=5)
    s.text(x + w / 2, y + (h / 2 + 3 if not t2 else h / 2 - 1.5), t1, 8.2, 700, cor, anc='middle')
    if t2: s.text(x + w / 2, y + h / 2 + 9, t2, 7, 400, cor, anc='middle')

def seta(s, x1, y1, x2, y2, txt=None, cor=TINTA, dash=None, lado=-1):
    s.line(x1, y1, x2, y2, stroke=cor, sw=0.7, dash=dash)
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 5
    s.path('M%.2f %.2f L%.2f %.2f L%.2f %.2f Z' % (x2, y2, x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4),
                                                  x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4)), fill=cor)
    if txt:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(y2 - y1) < 1: s.text(mx, my + (-4 if lado < 0 else 10), txt, 7, 600, cor, anc='middle')
        else: s.text(mx + 4, my + 2.5, txt, 7, 600, cor)

def prancha04():
    s = Svg(); moldura(s)
    P_ = D.PISCINA
    # ---------------- 1. implantacao 1:100
    v = Vista(46, 112, 100, 9.9, -1.3, clip=(9.9, -1.3, 23.95, 10.05))
    AM.titulo_vista(s, 40, 58, '1', 'Implantação da piscina', 'Escala 1:100 · * cotas medidas na planta de layout (01/05/2026) · a conferir')
    desenhar_base(s, v)
    x, y, w, l = PR.piscina_planta(s, v)
    s.text(v.X(x + w / 2), v.Y(y + l / 2), 'PISCINA', 7.5, 700, AZUL, anc='middle', ls=1.2)
    s.text(v.X(x + w / 2), v.Y(y + l / 2) + 10, 'Vallauris', 7, 500, AZUL, anc='middle')
    s.text(v.X(x + w / 2), v.Y(y + l / 2) + 19, '3,39 × 7,45', 7, 500, AZUL, anc='middle')
    cm = P_['casa_maquinas']
    s.text(v.X(cm[0]) - 4, v.Y(cm[1]) + 8, 'Casa de máquinas G7', 6.6, 600, TERRA, anc='end')
    s.text(v.X(cm[0]) - 4, v.Y(cm[1]) + 16, 'ref. Tomadas R05 (quadro 1C)', 6.4, 500, TERRA, anc='end')
    # cotas de implantacao (a conferir)
    cota_simples(s, v.X(D.F['CASA_ext']), v.Y(9.75), v.X(x), v.Y(9.75), P_['afast_fachada'] + '*', tam=7.2, cor=TERRA)
    s.line(v.X(D.F['CASA_ext']), v.Y(4.0), v.X(D.F['CASA_ext']), v.Y(9.9), stroke=COTA, sw=0.35)
    s.line(v.X(x), v.Y(y + l), v.X(x), v.Y(9.9), stroke=COTA, sw=0.35)
    cota_simples(s, v.X(x + w / 2), v.Y(D.F['MURO']), v.X(x + w / 2), v.Y(y), P_['afast_muro'] + '*', lado=-1, tam=7.2, cor=TERRA)
    # ducha X1 / registro X2
    X1, X2 = PR.PT['X1'], PR.PT['X2']
    for p in (X1, X2): ponto_ampliado(s, v, p, r=3.6, afast=5.2, passo=7.6, eixo=False)
    cota(s, v, X1['cotas'][0], -0.42, tam=7, ext_de=None, ext_ate=D.F['MURO'])
    cota(s, v, X2['cotas'][0], -0.85, tam=7, ext_de=None, ext_ate=D.F['MURO'])
    s.line(v.X(D.F['CASA_ext']), v.Y(D.F['MURO']), v.X(D.F['CASA_ext']), v.Y(-0.9), stroke=COTA, sw=0.35)
    PR.etq(s, v.X(X1['x']), v.Y(0.45), v.X(11.0), v.Y(1.35), X1)
    PR.etq(s, v.X(X2['x']), v.Y(0.45), v.X(17.9), v.Y(-0.75), X2)

    # ---------------- 2. esquema funcional (sem escala)
    ex, ey = 500, 92
    AM.titulo_vista(s, ex, 58, '2', 'Esquema dos pontos', 'Sem escala · funcional · não indica trajeto nem diâmetro')
    s.rect(ex, ey, 300, 300, fill=CLARO, rx=10)
    caixa(s, ex + 14, ey + 18, 118, 34, 'Rede de água fria', 'alimentação da casa')
    caixa(s, ex + 168, ey + 18, 118, 34, 'Registro independente', 'junto ao skimmer (PVC)', borda=D.TIPOS['AF'][2])
    caixa(s, ex + 168, ey + 84, 118, 34, 'Skimmer filtrante', 'reposição de nível (G7)', borda=AZUL)
    caixa(s, ex + 14, ey + 84, 118, 34, 'Piscina Vallauris', 'iGUi', fundo='#e6f2fa', borda=AZUL)
    caixa(s, ex + 168, ey + 150, 118, 34, 'Casa de máquinas G7', 'filtro e bomba iGUi', borda=TERRA)
    caixa(s, ex + 14, ey + 150, 118, 34, 'Dispositivo de retorno', 'na parede da piscina', borda=AZUL)
    caixa(s, ex + 168, ey + 216, 118, 34, 'Rede de esgoto', 'ladrão do skimmer', borda=D.TIPOS['ESG'][2])
    caixa(s, ex + 14, ey + 216, 118, 34, 'Grelha', 'dreno do G7 · a definir', borda=D.TIPOS['ESG'][2])
    seta(s, ex + 132, ey + 35, ex + 168, ey + 35, cor=D.TIPOS['AF'][2])
    seta(s, ex + 227, ey + 52, ex + 227, ey + 84, 'AF', cor=D.TIPOS['AF'][2])
    seta(s, ex + 132, ey + 101, ex + 168, ey + 101, 'água', cor=AZUL)
    seta(s, ex + 227, ey + 118, ex + 227, ey + 150, cor=AZUL)
    seta(s, ex + 168, ey + 167, ex + 132, ey + 167, 'retorno', cor=AZUL, lado=-1)
    seta(s, ex + 73, ey + 150, ex + 73, ey + 118, cor=AZUL)
    s.path('M%.2f %.2f L%.2f %.2f' % (ex + 286, ey + 101, ex + 293, ey + 101), stroke=D.TIPOS['ESG'][2], sw=0.7)
    s.line(ex + 293, ey + 101, ex + 293, ey + 233, stroke=D.TIPOS['ESG'][2], sw=0.7, dash='3 1.5')
    seta(s, ex + 293, ey + 233, ex + 286, ey + 233, cor=D.TIPOS['ESG'][2])
    s.text(ex + 296, ey + 170, 'ladrão 3/4"', 7, 600, D.TIPOS['ESG'][2], rot=90, anc='middle')
    seta(s, ex + 168, ey + 184, ex + 105, ey + 216, cor=D.TIPOS['ESG'][2], dash='3 1.5')
    s.text(ex + 150, ey + 208, 'dreno', 7, 600, D.TIPOS['ESG'][2])
    paragrafo(s, ex + 14, ey + 268, 'Itens conforme a prancha de Tomadas R05 (quadro 1C) e o sistema G7 da iGUi.', 280, 7.8, 500, COTA_TXT, entre=10)

    # ---------------- 3. modelo Vallauris - planta 1:50
    my = 540
    AM.titulo_vista(s, 40, my - 62, '3', 'Modelo Vallauris · planta', 'Escala 1:50 · redesenhado do desenho técnico iGUi (01/01)')
    L_pl = linhas_igui((230, 55, 600, 230), {(0.0, 0.0, 0.0)}, larg_min=0.3)
    ox, oy = 70, my
    M = desenhar_igui(s, L_pl, ox, oy, (240.96, 65.92), 50)
    s.rect(ox + 0.2 * 56.693, oy + 0.2 * 56.693, 7.05 * 56.693, 2.99 * 56.693, fill='#e6f2fa', extra='fill-opacity="0.55"')
    desenhar_igui(s, L_pl, ox, oy, (240.96, 65.92), 50)
    k = 56.693
    # cotas (m)
    cota_simples(s, ox, oy - 26, ox + 7.45 * k, oy - 26, '7,45 (externa)')
    cota_simples(s, ox + 0.2 * k, oy - 12, ox + 7.25 * k, oy - 12, '7,05 (interna)')
    cota_simples(s, ox - 14, oy, ox - 14, oy + 3.39 * k, '3,39')
    cota_simples(s, ox + 7.45 * k + 14, oy + 0.2 * k, ox + 7.45 * k + 14, oy + 3.19 * k, '2,99', lado=-1)
    xs = [0.2, 5.53, 5.84, 6.31, 6.78, 7.25]
    for a, b in zip(xs, xs[1:]):
        cota_simples(s, ox + a * k, oy + 3.39 * k + 13, ox + b * k, oy + 3.39 * k + 13, ('%.2f' % (b - a)).replace('.', ','), lado=-1, tam=6.8)
    s.text(ox + 2.8 * k, oy + 1.72 * k, 'fundo −1,41', 8, 700, AZUL, anc='middle')
    s.text(ox + 6.29 * k, oy + 1.25 * k, '−0,94', 7.2, 700, AZUL, anc='middle')
    s.text(ox + 6.29 * k, oy + 2.95 * k, 'escada', 7.2, 600, TERRA, anc='middle')
    s.text(ox + 7.02 * k, oy + 0.55 * k, 'banco', 7.2, 600, TERRA, anc='middle')
    s.text(ox + 7.02 * k, oy + 0.72 * k, '−0,47', 6.6, 600, AZUL, anc='middle')
    # ---------------- 4/5. cortes 1:50
    cy = 872
    AM.titulo_vista(s, 40, cy - 34, '4', 'Corte longitudinal', 'Escala 1:50 · iGUi')
    L_lg = linhas_igui((221, 376, 599, 460), {(0.0, 0.15, 0.58)}) + linhas_igui((221, 376, 599, 460), {(0.0, 0.0, 0.0)}, larg_min=0.3)
    desenhar_igui(s, L_lg, 70, cy, (240.96, 384.4), 50, cor=TINTA, sw=0.55)
    s.line(70 + 0.2 * k, cy + 0.15 * k, 70 + 7.25 * k, cy + 0.15 * k, stroke=AZUL, sw=0.5, dash='3 1.5')
    s.text(70 + 3.4 * k, cy + 0.15 * k - 3, 'nível da água −0,15', 7, 600, AZUL, anc='middle')
    cota_simples(s, 70 - 12, cy, 70 - 12, cy + 1.41 * k, '1,41')
    s.text(70 + 5.9 * k, cy + 0.94 * k + 10, '−0,94', 7, 600, COTA_TXT, anc='middle')
    s.text(70 + 6.99 * k, cy + 0.47 * k + 10, '−0,47', 7, 600, COTA_TXT, anc='middle')
    AM.titulo_vista(s, 555, cy - 34, '5', 'Corte transversal', 'Escala 1:50 · iGUi')
    L_tr = linhas_igui((606, 257, 776, 341), {(0.0, 0.58, 0.29)}) + linhas_igui((606, 257, 776, 341), {(0.0, 0.0, 0.0)}, larg_min=0.3)
    desenhar_igui(s, L_tr, 590, cy, (618.0, 264.16), 50, cor=TINTA, sw=0.55)
    cota_simples(s, 590, cy + 1.41 * k + 12, 590 + 3.39 * k, cy + 1.41 * k + 12, '3,39', lado=-1)
    s.text(590 + 3.0 * k, cy + 0.9 * k, 'escada', 7, 600, TERRA, anc='middle')
    s.text(590 + 3.0 * k, cy + 0.9 * k + 9, '4 × 0,31', 6.6, 500, TERRA, anc='middle')
    PR.titulo_desenho(s, 28, 1101, '04', 'Piscina Vallauris · pontos hidráulicos', 'Implantação 1:100 · modelo e cortes 1:50 · plotagem em A2')
    barra_escala(s, 29, 1134.4, k, [0, 1, 2, 3, 4])

    # ---------------- coluna 2
    c = painel(s, COL2[0], TOPO, COL2[1], 640.0, TERRA, 'Pontos da piscina', '1')
    s.text(838, 82, 'Nº', 9.5, 700, c); s.text(876, 82, 'ITEM · ORIGEM DA INFORMAÇÃO', 9.5, 700, c)
    s.text(1208, 82, 'POSIÇÃO', 9.5, 700, c, anc='end')
    itens = [
        ('X1', 'Ducha de água fria', 'Saída a 2,10 m* · 2,57 da face externa da Suíte Master, no muro. Planta de pontos (29/09).', 'cotada'),
        ('X2', 'Registro da ducha', 'A 1,10 m* · 3,07 da mesma face, no muro. Planta de pontos (29/09).', 'cotada'),
        ('P1', 'Reposição de água (AF)', 'Registro independente junto ao skimmer, em PVC (Tomadas R05, quadro 1C).', 'iGUi'),
        ('P2', 'Skimmer filtrante', 'Sistema G7 da iGUi.', 'iGUi'),
        ('P3', 'Dispositivo de retorno', 'Sistema G7 da iGUi; ligação à casa de máquinas.', 'iGUi'),
        ('P4', 'Ladrão 3/4" do skimmer', 'Para a rede de esgoto (Tomadas R05, quadro 1C).', 'iGUi'),
        ('P5', 'Dreno do G7', 'Para a grelha (Tomadas R05, quadro 1C). Grelha não localizada nos arquivos.', 'a definir'),
        ('G7', 'Casa de máquinas', 'Canto superior do lote, junto ao muro, como na prancha de Tomadas R05.', 'ref. elétrica'),
    ]
    y = 108
    for cod, nome, txt, pos in itens:
        s.text(838, y, cod, 12, 700, c); s.text(876, y, nome, 12, 600, c); s.text(1208, y, pos, 10, 700, c, anc='end')
        y = paragrafo(s, 876, y + 15, txt, 320, 10.6, 300, c, entre=13.6) + 11
    paragrafo(s, 838, y + 4, '* Alturas da ducha adotadas do padrão do chuveiro: confirmar. Pontos P1 a P5 sem cota: posição, trajeto e '
              'diâmetro conforme a instaladora iGUi e o projeto hidrossanitário.', 370, 10.2, 400, c, entre=13.6)
    c = painel(s, COL2[0], 654.0, COL2[1], BASE, OLIVA, 'Modelo Vallauris', '1A')
    dados = [('Fabricante', 'iGUi · desenho técnico Vallauris 01/01'), ('Medidas externas', '7,45 × 3,39 m (borda de 0,20)'),
             ('Medidas internas', '7,05 × 2,99 m'), ('Profundidade', '1,41 m no fundo'), ('Plataforma', '0,96 m a −0,94 m'),
             ('Banco', '0,47 m a −0,47 m'), ('Escada', '4 degraus de 0,31 m · largura 0,80 m'), ('Nível da água', '0,15 m abaixo da borda'),
             ('Estrutura', 'Mão francesa ao longo da borda e reforços a cada 45 cm, em média (iGUi)'),
             ('Implantação', 'Borda externa a 3,63 m da fachada da Suíte Master e a 1,50 m do muro, medidas na planta de layout (01/05/2026) · a conferir'),
             ('Orientação', 'Lado da escada e do banco a definir com a iGUi')]
    y = 700
    for a_, b_ in dados:
        s.text(838, y, a_, 10.4, 700, c)
        y = paragrafo(s, 960, y, b_, 248, 10.4, 300, c, entre=13.4) + 6
    # ---------------- coluna 3
    PR.legenda(s, planta_geral=False, extra=[])
    PR.observacoes(s, [
        ('Escopo', 'Localização dos pontos hidráulicos ligados à piscina. Instalação, tubulação e equipamentos conforme o manual '
                   'da iGUi e o projeto hidrossanitário.'),
        ('Implantação', 'Posição da piscina medida graficamente na planta de layout (Rev. 01). Conferir no local e com o projeto de '
                        'implantação antes da escavação.'),
        ('Ducha', 'Ducha de água fria com registro próprio, no muro, entre a casa e a piscina.'),
        ('Elétrica', 'Q.C. MAX, conduítes e trocador de calor conforme a prancha de Tomadas R05 (quadro 1C). '
                     'Equipotencialização da piscina conforme NBR 5410.'),
        ('Normas', 'NBR 10339 (piscinas) e NBR 5626 (água fria e água quente).'),
    ])
    PR.cabec_carimbo(s, 'Pontos hidráulicos · piscina', '1:100 e 1:50 · folha A2', 4, (56.693 / 2, 4, '0 — 4 m (1:50)'))
    return s.svg()
