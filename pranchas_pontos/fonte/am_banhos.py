# -*- coding: utf-8 -*-
"""Folhas 02 a 05 do caderno de areas molhadas: banhos (planta 1:25 + box/paredes planificados 1:25)."""
import math
from am_base import *
import ampliacoes as AM

F = D.F
VIDRO = '#5b8fa8'
ALT = 2.85            # forro +2,85 nos banhos (Caderno de forro R01)
H_BOX, H_NICHO, PEIT_J04, H_J04 = 2.10, (1.00, 1.30), 1.50, 0.60

# Geometria medida na base (planta de Tomadas R05 = planta de pontos 29/09). Segmentos da elevacao
# planificada: (P0, P1, rotulo) na face da parede, da esquerda para a direita vista de dentro.
BANHOS = {
    'W01': dict(n=2, cod='B1', nome='Banho Suíte 1', fundo='RP04', clip=(2.20, 8.56, 5.50, 10.46),
        box=(2.445, 8.748, 3.308, 10.265), lado_fundo='esq', vidro=('x', 3.3355, 8.748, 10.265),
        segs=[((3.308, 10.265), (2.445, 10.265), 'lateral do box'), ((2.445, 10.265), (2.445, 8.748), 'fundo do box'),
              ((2.445, 8.748), (5.26, 8.748), 'parede das peças')], ip=2, box_ip=(0.0, 0.863),
        janela=((2.445, 10.011), (2.445, 9.015)), cotas=[('B1.1', 0.50), ('B1.4', 0.50), ('B1.3', 0.63), ('B1.2', 0.76)],
        vista=(3.05, 9.80, 'esq'), caderno=('1,50', '0,90'), espelho=None),
    'W02': dict(n=3, cod='B2', nome='Banho Suíte 2', fundo='RP04', clip=(2.20, 6.89, 5.50, 8.83),
        box=(2.453, 7.079, 3.293, 8.639), lado_fundo='esq', vidro=('x', 3.3285, 7.079, 8.639),
        segs=[((5.26, 8.639), (2.453, 8.639), 'parede das peças'), ((2.453, 8.639), (2.453, 7.079), 'fundo do box'),
              ((2.453, 7.079), (3.293, 7.079), 'lateral do box')], ip=0, box_ip=(1.967, 2.807),
        janela=((2.453, 8.349), (2.453, 7.361)), cotas=[('B2.1', -0.50), ('B2.4', -0.50), ('B2.3', -0.63), ('B2.2', -0.76)],
        vista=(3.05, 7.45, 'esq'), caderno=('1,50', '0,90'), espelho='Espelhado em relação ao Banho Suíte 1.'),
    'WSM': dict(n=4, cod='BM', nome='Banho Suíte Master', fundo='RP03', clip=(0.20, 0.27, 2.62, 3.96),
        box=(0.423, 2.846, 2.40, 3.83), lado_fundo='inf', vidro=('y', 2.8225, 0.423, 2.40),
        segs=[((2.40, 2.846), (2.40, 3.83), 'lateral do box'), ((2.40, 3.83), (0.423, 3.83), 'fundo do box'),
              ((0.423, 3.83), (0.423, 0.376), 'parede das peças')], ip=2, box_ip=(0.0, 0.984),
        janela=((1.568, 3.83), (0.58, 3.83)), cotas=[('BM.1', 0.50), ('BM.2', 0.50), ('BM.3', 0.63), ('BM.4', 0.76)],
        vista=(2.12, 3.12, 'inf'), caderno=('1,95', '0,90'), espelho=None),
    'WEX': dict(n=5, cod='B4', nome='Banho 4', fundo='RP05', clip=(7.22, 6.08, 10.76, 7.93),
        box=(7.443, 6.275, 8.239, 7.737), lado_fundo='esq', vidro=('x', 8.2745, 6.275, 7.737),
        segs=[((10.504, 7.737), (7.443, 7.737), 'parede das peças'), ((7.443, 7.737), (7.443, 6.275), 'fundo do box'),
              ((7.443, 6.275), (8.239, 6.275), 'lateral do box')], ip=0, box_ip=(2.265, 3.061),
        janela=None, cotas=[('B4.1', -0.50), ('B4.4', -0.50), ('B4.3', -0.63), ('B4.2', -0.76)],
        vista=(8.00, 6.60, 'esq'), caderno=('1,40', '0,90'), espelho=None),
}

def comp(seg):
    (x0, y0), (x1, y1), _ = seg
    return math.hypot(x1 - x0, y1 - y0)

def s_de(b, i, x, y):
    """posicao (m) na elevacao planificada de um ponto (x, y) da face do segmento i."""
    acc = sum(comp(sg) for sg in b['segs'][:i])
    (x0, y0), (x1, y1), _ = b['segs'][i]
    L = comp(b['segs'][i]); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    return acc + (x - x0) * ux + (y - y0) * uy

def dims(b):
    x0, y0, x1, y1 = b['box']
    if b['lado_fundo'] in ('esq', 'dir'): return y1 - y0, x1 - x0       # largura (fundo), profundidade (lateral)
    return x1 - x0, y1 - y0

# ------------------------------------------------------------------ planta
def planta_box(s, v, b, rotulos=True):
    x0, y0, x1, y1 = b['box']
    cor = tint(RP['RP02'][0], 0.9); corf = tint(RP[b['fundo']][0], 0.9)
    e = 0.035                                  # faixa de indicacao da face revestida
    lf = b['lado_fundo']
    # laterais e fundo revestidos (faixa colorida junto a face)
    if lf == 'esq':
        s.rect(v.X(x0), v.Y(y0), e * v.k, (y1 - y0) * v.k, fill=corf)
        s.rect(v.X(x0), v.Y(y0), (x1 - x0) * v.k, e * v.k, fill=cor)
        s.rect(v.X(x0), v.Y(y1 - e), (x1 - x0) * v.k, e * v.k, fill=cor)
    else:
        s.rect(v.X(x0), v.Y(y1 - e), (x1 - x0) * v.k, e * v.k, fill=corf)
        s.rect(v.X(x0), v.Y(y0), e * v.k, (y1 - y0) * v.k, fill=cor)
        s.rect(v.X(x1 - e), v.Y(y0), e * v.k, (y1 - y0) * v.k, fill=cor)
    rl = [p for p in D.AMB[b['k']]['pontos'] if p.get('ralo')][0]['ralo']   # ralo linear (pontos R04)
    # caimento: seta para o ralo
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if lf == 'esq':
        sg = 1 if b['segs'][b['ip']][0][1] < cy else -1          # seta do lado oposto a parede das pecas
        a, bb = (cx + 0.18, cy + sg * 0.36), (rl[2] + 0.05, cy + sg * 0.36)
    else:
        a, bb = (cx + 0.30, cy - 0.30), (cx + 0.30, rl[1] - 0.05)
    s.line(v.X(a[0]), v.Y(a[1]), v.X(bb[0]), v.Y(bb[1]), stroke=TERRA, sw=0.6)
    ang = math.atan2(v.Y(bb[1]) - v.Y(a[1]), v.X(bb[0]) - v.X(a[0]))
    px, py = v.X(bb[0]), v.Y(bb[1])
    s.path('M%.2f %.2f L%.2f %.2f L%.2f %.2f Z' % (px, py, px - 5 * math.cos(ang - 0.4), py - 5 * math.sin(ang - 0.4),
                                                      px - 5 * math.cos(ang + 0.4), py - 5 * math.sin(ang + 0.4)), fill=TERRA)
    if rotulos:
        tx, ty = (v.X(a[0]) + v.X(bb[0])) / 2, (v.Y(a[1]) + v.Y(bb[1])) / 2
        if lf == 'esq': s.text(tx, ty + 7.5, 'i = a definir', 5.6, 700, TERRA, anc='middle')
        else: s.text(tx - 4, ty + 2, 'i = a definir', 5.6, 700, TERRA, anc='end')
    # vidro de correr: 2 folhas (1 fixa + 1 de correr), lado da fixa a definir
    eixo, c, a0, a1 = b['vidro']
    L = a1 - a0; sob = 0.06
    f1 = (a0, a0 + L / 2 + sob / 2); f2 = (a0 + L / 2 - sob / 2, a1)
    for (p0, p1), d in ((f1, -0.018), (f2, 0.018)):
        if eixo == 'x': s.rect(v.X(c + d) - 1.1, v.Y(p0), 2.2, (p1 - p0) * v.k, fill=VIDRO)
        else: s.rect(v.X(p0), v.Y(c + d) - 1.1, (p1 - p0) * v.k, 2.2, fill=VIDRO)
    if rotulos:
        if eixo == 'x':
            pecas_acima = b['segs'][b['ip']][0][1] < (a0 + a1) / 2
            X = v.X(c) + 9; Ym = v.Y(a0 + (0.80 if pecas_acima else 0.18) * (a1 - a0))
            s.text(X, Ym - 4, 'box de correr', 5.8, 700, '#3d6b80')
            s.text(X, Ym + 3.6, '2 folhas · h 2,10', 5.6, 400, '#3d6b80')
            s.text(X, Ym + 11.2, 'lado da fixa: a definir', 5.6, 400, '#3d6b80')
        else:
            Xm = v.X((a0 + a1) / 2); Yv = v.Y(c) - 6
            s.text(Xm, Yv, 'box de correr · 2 folhas (1 fixa + 1 de correr) · h 2,10 · lado da fixa: a definir', 5.6, 600, '#3d6b80', anc='middle')
    # nicho no fundo (indicacao tracejada na parede)
    return rl

def folha_banho(k_amb):
    b = BANHOS[k_amb]; b['k'] = k_amb; amb = D.AMB[k_amb]
    larg, prof = dims(b)
    s = folha(b['nome'])
    # ------------------------------ planta 1:25
    cx0, cy0, cx1, cy1 = b['clip']
    pw, ph = (cx1 - cx0) * K25, (cy1 - cy0) * K25
    titulo(s, ML, 92, 'A', 'Planta · pontos e box', 'Escala 1:25 · cotas em metros a partir da face da parede indicada')
    v = Vista(ML + 8, 108, 25, cx0, cy0, clip=b['clip'])
    cfg = []
    for cod, d in b['cotas']:
        p = PR.PT[cod]; c = p['cotas'][0]
        face = p['y'] if c['eixo'] == 'x' else p['x']
        cfg.append((cod, 0, face + d, None, None, 1 if d > 0 else -1))
    AM.ampliacao(s, v, amb['pontos'], cotas_cfg=cfg)
    planta_box(s, v, b)
    vx, vy, vd = b['vista']
    AM.marca_vista(s, v, vx, vy, vd, 'B')
    s.text(v.X((b['box'][0] + b['box'][2]) / 2) if b['lado_fundo'] == 'inf' else v.X(b['box'][0]) + 14,
           v.Y(b['box'][1]) + 12 if b['lado_fundo'] == 'esq' else v.Y((b['box'][1] + b['box'][3]) / 2) - 8,
           'BOX', 6.4, 700, TINTA, anc='middle' if b['lado_fundo'] == 'inf' else 'start', ls=1.4)
    yplan = 108 + ph
    # ------------------------------ quadros a direita
    xr = ML + pw + 26
    y = quadro_pts(s, xr, 84, MR, [p['cod'] for p in amb['pontos']])
    itens = [
        ('Box', 'Vidro de correr, 2 folhas (1 fixa + 1 de correr), h 2,10 do piso acabado; não vai até o forro.', 'D'),
        ('Folha fixa', 'Lado da folha fixa, ferragem e perfis (lista de louças: previsão cromada).', 'A'),
        ('Vão do box', 'Fundo %s × lateral %s (planta 29/09). Caderno de revestimentos R00: %s × %s.'
         % (fmt(larg), fmt(prof), b['caderno'][0], b['caderno'][1]), 'C'),
        ('Ralo', 'Linear, junto à parede do fundo do box; não há ralo fora do box. Modelo, comprimento e caimento a definir.', 'D'),
        ('Revestimento', 'Box: laterais RP02 e fundo %s até o forro (2,85). Demais paredes em pintura: ducha higiênica, bacia e cuba na pintura.' % b['fundo'], 'D'),
        ('Nicho', '0,30 × 0,10, base a 1,00, em toda a largura do fundo (caderno R00). Parede de ≈0,15 na planta: conferir a profundidade.', 'C'),
    ]
    if b['janela']: itens.append(('Janela J04', '1,00 × 0,60, peitoril 1,50 (02/10), no fundo do box.', 'D'))
    itens += [('Piso', 'P01 Santorini OFW NAT 90 × 90 (caderno de pisos R00), inclusive no box.', 'D'),
              ('Bancada', 'Bancada da cuba: prancha de marmoraria (a desenvolver).', 'A'),
              ('Acessórios', 'Alturas propostas na folha 08.', 'P')]
    y2 = quadro_itens(s, xr, y + 10, MR, 'Elementos', itens)
    # ------------------------------ elevacao planificada
    segs = [(comp(sg), sg[2]) for sg in b['segs']]
    oy = 892.0                                  # piso da elevacao (mesma posicao nas 4 folhas)
    ytit = oy - 30 - ALT * K25
    assert max(yplan, y2) < ytit - 6, ('sobreposicao', k_amb, yplan, y2, ytit)
    titulo(s, ML, ytit, 'B', 'Box e parede das peças · planificados',
           'Escala 1:25 · vistos de dentro, da esquerda para a direita · alturas do piso acabado')
    ip = b['ip']; acc = [0]
    for c, _ in segs: acc.append(acc[-1] + c)
    clad = []
    for i, sg in enumerate(b['segs']):
        if i == ip: clad.append((acc[i] + b['box_ip'][0], acc[i] + b['box_ip'][1], 0, ALT, 'RP02'))
        elif sg[2] == 'fundo do box': clad.append((acc[i], acc[i + 1], 0, ALT, b['fundo']))
        else: clad.append((acc[i], acc[i + 1], 0, ALT, 'RP02'))
    ifun = [i for i, sg in enumerate(b['segs']) if sg[2] == 'fundo do box'][0]
    elems = [('nicho', acc[ifun], acc[ifun + 1], H_NICHO[0], H_NICHO[1], 'nicho 0,30 × 0,10'),
             ('ralo', acc[ifun] + 0.05, acc[ifun + 1] - 0.05, 0, 0, '')]
    if b['janela']:
        (ax, ay), (bx, by) = b['janela']
        s0, s1 = sorted((s_de(b, ifun, ax, ay), s_de(b, ifun, bx, by)))
        elems.append(('janela', s0, s1, PEIT_J04, PEIT_J04 + H_J04, 'J04 1,00 × 0,60\npeitoril 1,50'))
    # linhas do vidro (onde o box encontra as paredes)
    ivid = [acc[ip] + b['box_ip'][0] if b['box_ip'][0] > 0 else acc[ip] + b['box_ip'][1]]
    ilat = [i for i, sg in enumerate(b['segs']) if sg[2] == 'lateral do box'][0]
    ivid.append(acc[ilat] if ilat < ifun else acc[ilat + 1])
    for sv in ivid:
        elems.append(('vidro', sv, 1 if sv < acc[-1] / 2 else -1, 0, H_BOX, 'vidro h 2,10'))
    # pintura
    pa, pb = (acc[ip] + b['box_ip'][1], acc[ip + 1]) if b['box_ip'][0] == 0 else (acc[ip], acc[ip] + b['box_ip'][0])
    elems.append(('texto', pa, pb, 1.90, 0, 'pintura'))
    elems.append(('texto', pa, pb, 1.78, 0, 'bancada: ver marmoraria'))
    pts = [(s_de(b, ifun if p.get('ralo') else ip, p['x'], p['y']), p) for p in amb['pontos']]
    k = K25
    largura_el = acc[-1] * k
    ox = max(ML + 44, (ML + MR) / 2 - largura_el / 2 + 10)
    dd = []
    for i, (c, rot) in enumerate(segs):
        if i == ip:
            dd += [(acc[ip] + b['box_ip'][0], acc[ip] + b['box_ip'][1], 'lateral do box (peças)'), (pa, pb, 'pintura (peças)')]
        else: dd.append((acc[i], acc[i + 1], rot))
    elevacao(s, ox, oy, k, segs, ALT, pontos=pts, clad=clad, elems=elems, dims=dd,
             niveis_extra=[H_NICHO[0], H_NICHO[1], H_BOX] + ([PEIT_J04] if b['janela'] else []))
    # ------------------------------ notas
    nt = [
        ('Chuveiro', 'Kit Deca Acqua Plus + misturador de duas alavancas (Level 4900). Registros AF/AQ já executados: '
                     'afastamento entre eles a medir em obra.', 'C'),
        ('Bacia', 'Roca ONA com caixa acoplada, sem válvula de descarga. AF a 0,30 até conferir na ficha da Roca.', 'C'),
        ('RG', 'Registro geral dentro do armário da bancada, eixo sem cota (marcador tracejado): definir com a marcenaria.', 'A'),
        ('Pontos', 'Posições e alturas iguais às pranchas de pontos hidráulicos R04 (cotas da planta de 29/09).', 'D'),
        ('Vão', 'Vão do box medido na planta de 29/09 (base das pranchas). O caderno de revestimentos R00 usa a '
                'geometria do DWG R01: quantitativos de RP02/%s a revisar.' % b['fundo'], 'C'),
        ('Ralo', 'Desenho indicativo: comprimento, grelha, caimento e desnível do box conforme fabricante e projeto '
                 'hidrossanitário (folha 08).', 'A'),
    ]
    if b['espelho']: nt.insert(0, ('Espelho', b['espelho'], None))
    notas(s, nt, escala=(K25, [0, 0.5, 1, 1.5, 2], '1/25'))
    carimbo3(s, b['n'], b['nome'], '1/25')
    return s.svg()
