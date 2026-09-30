# -*- coding: utf-8 -*-
"""Prancha 02 — Cortineiros iluminados CT1 (suíte master) e CT2 (estar/jantar)."""
from base import *
from dados_forro import *
from secao import *
import p01_planta as P1

TOTAL_N = TOTAL


# ------------------------------------------------------------------ planta ampliada
def planta_ampliada(v, cid, esc, ox, oy, reg, ct, extra=None):
    x0, y0, x1, y1 = reg
    pl = Planta(esc, ox, oy, x0, y0)
    W, H = pl.mm(x1 - x0), pl.mm(y1 - y0)
    v.add(f'<clipPath id="{cid}"><rect x="{ox}" y="{oy}" width="{W}" height="{H}"/></clipPath><g clip-path="url(#{cid})">')
    P1.fill_ambientes(v, pl)
    P1.luminarias(v, pl, s=1.0, rot=True)
    P1.cortineiros(v, pl, [ct])
    paredes(v, pl)
    # testeira (face interna) em traço forte
    for (a0, b0, a1, b1) in ct['faixas']:
        if (a1 - a0) < (b1 - b0):
            p, q = pl.P(a0, b0), pl.P(a0, b1)
        else:
            p, q = pl.P(a0, b1), pl.P(a1, b1)
        v.line(*p, *q, C['ink'], 0.6)
    if extra:
        extra(v, pl)
    v.add('</g>')
    return pl


def corte_cortineiro(v, ox, y_forro, forro, laje_z, cod, fonte, esq_top, esq_nome, numeros=True):
    """Corte transversal do cortineiro, escala 1:5. x = 0 na face da parede acabada."""
    k = 200.0
    s = Secao(5, ox, y_forro + forro * k)
    zb = forro - 0.26                      # base do desenho
    # parede / esquadria
    if esq_top > zb + 0.02:
        parede(v, s, -0.17, 0.0, esq_top, laje_z)
        x, y, w, h = s.R(-0.17, zb, 0.0, esq_top)
        v.rect(x + w * 0.35, y, w * 0.3, h, fill='#eef3f5', stroke=C['aco'], sw=0.3)
        v.rect(x + w * 0.2, y, w * 0.6, 1.6, fill=C['aco'])
        quebra_h(v, x - 1, x + w + 1, y + h)
        v.text(x + w / 2, y + h - 3, 'esquadria', size=5.0, weight=600, cor=C['muted'], rot=-90)
    else:
        parede(v, s, -0.17, 0.0, zb, laje_z)
    laje(v, s, -0.17, 0.56, laje_z)
    # forro
    chapa(v, s, 0.20 + T_CHAPA, forro, 0.56, forro + T_CHAPA)
    quebra_v(v, s.P(0.56, 0)[0], s.P(0, forro + 0.03)[1], s.P(0, forro - 0.02)[1])
    # testeira
    chapa(v, s, 0.20, forro, 0.20 + T_CHAPA, laje_z)
    perfil_u(v, s, 0.20 + T_CHAPA, laje_z - 0.03, 0.20 + T_CHAPA + 0.028, laje_z, 'esq')
    perfil_u(v, s, 0.20 + T_CHAPA, forro + T_CHAPA, 0.20 + T_CHAPA + 0.028, laje_z - 0.03, 'esq')
    # estrutura do forro (simbólica) + pendurais
    for xp in (0.33, 0.49):
        perfil_u(v, s, xp, forro + T_CHAPA, xp + 0.05, forro + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.025, forro + T_CHAPA + 0.022, laje_z)
    # cantoneira na aresta
    cantoneira(v, s, 0.20, forro, dx=1, dz=1, L=0.025)
    # fundo do cortineiro (laje pintada)
    a, b = s.P(0.0, laje_z), s.P(0.20, laje_z)
    v.line(a[0], a[1] + 0.3, b[0], b[1] + 0.3, C['rust'], 0.5, dash='1.4 0.7')
    # zona do trilho
    zt0 = laje_z - 0.035
    x, y, w, h = s.R(0.02, zt0, 0.145, laje_z)
    v.rect(x, y, w, h, fill='#efe9d9', stroke=C['grey'], sw=0.25, dash='1 0.6')
    tx, ty, tw, th = s.R(0.065, laje_z - 0.022, 0.095, laje_z)
    v.rect(tx, ty, tw, th, fill=C['aco'])
    v.text(x + w / 2, y + h + 3.6, 'trilho', size=4.8, weight=600, cor=C['muted'])
    # cortina
    cortina(v, s, 0.08, laje_z - 0.022, zb + 0.01)
    # fonte de luz
    fz = laje_z - 0.012
    x, y, w, h = s.R(0.152, laje_z - 0.06, 0.198, laje_z - 0.004)
    v.rect(x, y, w, h, fill='#fde6bf', stroke=C['luz'], sw=0.25, dash='1 0.6')
    if 'Tubo' in fonte:
        c = s.P(0.178, laje_z - 0.033)
        v.circle(*c, 0.013 * k, fill='#fff6df', stroke=C['luz'], sw=0.35)
        src = c
    else:
        p = [s.P(0.19, laje_z - 0.02), s.P(0.19, laje_z - 0.045), s.P(0.172, laje_z - 0.045)]
        v.poly(p, stroke=C['aco'], sw=0.5, close=False)
        v.rect(*s.P(0.1805, laje_z - 0.026), 0.8, 0.012 * k * 0.5, fill=C['luz'])
        src = s.P(0.182, laje_z - 0.03)
    cone_luz(v, [src, s.P(0.095, laje_z - 0.03), s.P(0.04, forro - 0.24), s.P(0.19, forro - 0.24)])
    # cotas
    v.cota(*s.P(0.0, forro - 0.07), *s.P(0.20, forro - 0.07), off=0, txt='20 cm', size=6.6, ext=False,
           cor=C['luz'], tcor=C['luz'], weight=800)
    v.line(*s.P(0.0, forro - 0.09), *s.P(0.0, forro - 0.05), C['luz'], 0.2)
    v.line(*s.P(0.20, forro - 0.09), *s.P(0.20, forro), C['luz'], 0.2)
    v.text(*s.P(0.10, forro - 0.115), 'vão livre', size=5.2, weight=600, cor=C['luz'])
    h_cm = int(round((laje_z - forro) * 100))
    v.cota(*s.P(0.42, forro), *s.P(0.42, laje_z), off=0, txt=f'{h_cm} cm', size=6.2, ext=False)
    # níveis
    xm = s.P(0.60, 0)[0]
    marca_nivel(v, xm, s.P(0, forro)[1], f'+{br(forro)} forro')
    marca_nivel(v, xm, s.P(0, laje_z)[1], f'+{br(laje_z)} laje')
    # chamadas numeradas
    if numeros:
        R = lambda x, z: s.P(x, z)
        L = s.P(-0.17, 0)[0]
        call(v, *R(-0.08, laje_z + 0.06), L - 8, R(0, laje_z + 0.06)[1], 1)
        call(v, *R(-0.005, forro - 0.18), L - 8, R(0, forro - 0.18)[1], 2)
        call(v, *R(0.10, laje_z + 0.0015), R(0.10, 0)[0] + 2, R(0, laje_z + 0.19)[1], 3)
        call(v, *R(0.08, laje_z - 0.01), R(0.02, 0)[0], R(0, laje_z + 0.19)[1] + 0.0, 4)
        call(v, *R(0.08, forro - 0.20), L - 8, R(0, forro - 0.235)[1], 5)
        call(v, *R(0.175, laje_z - 0.03), R(0.25, 0)[0], R(0, laje_z + 0.19)[1], 6)
        call(v, *R(0.206, (forro + laje_z) / 2), R(0.30, 0)[0], R(0, laje_z + 0.19)[1], 7)
        call(v, *R(0.215, laje_z - 0.015), R(0.35, 0)[0], R(0, laje_z + 0.19)[1], 8)
        call(v, *R(0.201, forro - 0.001), R(0.27, 0)[0], R(0, forro - 0.16)[1], 9)
        call(v, *R(0.40, forro + 0.006), R(0.50, 0)[0], R(0, forro - 0.16)[1], 10)
        call(v, *R(0.505, forro + 0.04), R(0.47, 0)[0], R(0, laje_z + 0.19)[1], 11)
    return s


def perspectiva(v, ox, oy):
    """Perspectiva do corte do cortineiro (esquemática, suíte master)."""
    F, Lz = FORRO_ALA, LAJE_ALA
    p = Persp(10, ox, oy + (F - 0.45) * 100)
    D = 0.6
    zb = F - 0.45
    p.caixa(v, -0.17, zb, 0.0, Lz, 0, D, 'url(#hAlv)', side='#f4f1e8', faces='fs')
    p.caixa(v, 0.20 + T_CHAPA, F, 0.62, F + T_CHAPA, 0, D, C['gesso'], top='#ffffff', side='#eeebe2')
    p.caixa(v, 0.20, F, 0.20 + T_CHAPA, Lz, 0, D, C['gesso'], side='#f8f5ec', faces='fs')
    # fonte de luz (linha brilhante) na testeira
    a, b = p.P(0.185, 0, Lz - 0.03), p.P(0.185, D, Lz - 0.03)
    v.line(*a, *b, C['luz2'], 2.2, cap='round')
    v.line(*a, *b, C['luz'], 0.6, cap='round')
    # trilho
    a, b = p.P(0.08, 0, Lz - 0.012), p.P(0.08, D, Lz - 0.012)
    v.line(*a, *b, C['aco'], 1.0)
    # cortina (superfície)
    pts = []
    n = 12
    for i in range(n + 1):
        y = D * i / n
        pts.append(p.P(0.08 + (0.012 if i % 2 else -0.012), y, Lz - 0.02))
    for i in range(n, -1, -1):
        y = D * i / n
        pts.append(p.P(0.08 + (0.012 if i % 2 else -0.012), y, zb + 0.02))
    v.poly(pts, fill='#f3f1ea', stroke='#b3afa1', sw=0.15, op=0.75)
    for i in range(0, n + 1, 2):
        y = D * i / n
        v.line(*p.P(0.08 - 0.012, y, Lz - 0.02), *p.P(0.08 - 0.012, y, zb + 0.02), '#c3bfb2', 0.15)
    # luz lavando a cortina
    v.poly([p.P(0.10, 0, Lz - 0.03), p.P(0.10, D, Lz - 0.03), p.P(0.10, D, zb + 0.15), p.P(0.10, 0, zb + 0.15)],
           fill='url(#gLuz)', op=0.8)
    p.caixa(v, -0.17, Lz, 0.62, Lz + 0.12, 0, D, 'url(#hLaje)', top='#dedad0', side='#cfcbbf', faces='fts')
    # rótulos
    lbl = [((0.20, 0.0, F + 0.07), 'testeira'), ((0.40, 0.0, F), 'forro'), ((0.10, D, Lz - 0.012), 'trilho'),
           ((0.185, D * 0.7, Lz - 0.03), 'fonte de luz'), ((0.08, 0.2, zb + 0.25), 'cortina'), ((-0.08, 0, zb + 0.3), 'parede')]
    for (x, y, z), t in lbl:
        q = p.P(x, y, z)
        v.circle(*q, 0.45, fill=C['ink'])
    q = p.P(0.20, 0, F + 0.07); v.line(*q, q[0] + 16, q[1] + 10, C['ink'], 0.18); v.text(q[0] + 16.5, q[1] + 11, 'testeira', size=5.6, weight=600, anchor='start')
    q = p.P(0.40, 0, F); v.line(*q, q[0] + 8, q[1] + 8, C['ink'], 0.18); v.text(q[0] + 8.5, q[1] + 9, 'forro', size=5.6, weight=600, anchor='start')
    q = p.P(0.10, D, Lz - 0.012); v.line(*q, q[0] + 4, q[1] - 12, C['ink'], 0.18); v.text(q[0] + 4.5, q[1] - 12.5, 'trilho', size=5.6, weight=600, anchor='start')
    q = p.P(0.185, D * 0.7, Lz - 0.03); v.line(*q, q[0] + 22, q[1] - 6, C['luz'], 0.18); v.text(q[0] + 22.5, q[1] - 6.5, 'fonte de luz', size=5.6, weight=700, cor=C['luz'], anchor='start')
    q = p.P(0.08, 0.2, zb + 0.25); v.line(*q, q[0] - 10, q[1] + 10, C['ink'], 0.18); v.text(q[0] - 10.5, q[1] + 12.5, 'cortina', size=5.6, weight=600, anchor='end')
    q = p.P(-0.08, 0, zb + 0.3); v.line(*q, q[0] - 6, q[1] - 10, C['ink'], 0.18); v.text(q[0] - 6.5, q[1] - 11, 'parede', size=5.6, weight=600, anchor='end')


def canto_L(v, ox, oy):
    """C3 — canto em L do CT2 (planta 1:10)."""
    x0, y0 = 11.50, 12.12
    pl = Planta(10, ox, oy, x0, y0)
    W = pl.mm(0.78)
    v.add(f'<clipPath id="cpC3"><rect x="{ox}" y="{oy}" width="{W}" height="{W}"/></clipPath><g clip-path="url(#cpC3)">')
    a, b = pl.P(x0, y0), pl.P(12.08, 12.35)
    v.rect(a[0], a[1], pl.mm(0.78), pl.mm(12.35 - y0), fill=C['ink'])
    a = pl.P(12.08, y0)
    v.rect(a[0], a[1], pl.mm(0.2), pl.mm(0.78), fill=C['ink'])
    # forro (fora do cortineiro)
    a = pl.P(x0, 12.55 + T_CHAPA)
    v.rect(a[0], a[1], pl.mm(11.88 - T_CHAPA - x0), pl.mm(0.5), fill=C['st'])
    # vão
    v.poly([pl.P(x0, 12.35), pl.P(12.08, 12.35), pl.P(12.08, 12.90), pl.P(11.88, 12.90), pl.P(11.88, 12.55), pl.P(x0, 12.55)],
           fill=C['cort_fill'])
    # testeira em L
    v.poly([pl.P(x0, 12.55), pl.P(11.88, 12.55), pl.P(11.88, 12.90), pl.P(11.88 - T_CHAPA, 12.90),
            pl.P(11.88 - T_CHAPA, 12.55 + T_CHAPA), pl.P(x0, 12.55 + T_CHAPA)], fill='url(#hGesso)', stroke=C['ink'], sw=0.3)
    # zona do trilho (curva)
    r0, r1 = 0.02, 0.145
    c = pl.P(12.08, 12.35)
    v.path(f'M{pl.P(x0,12.35+0.08)[0]:.2f},{pl.P(x0,12.35+0.08)[1]:.2f} L{pl.P(11.93,12.43)[0]:.2f},{pl.P(11.93,12.43)[1]:.2f} '
           f'Q{pl.P(12.0,12.43)[0]:.2f},{pl.P(12.0,12.43)[1]:.2f} {pl.P(12.0,12.50)[0]:.2f},{pl.P(12.0,12.50)[1]:.2f} '
           f'L{pl.P(12.0,12.90)[0]:.2f},{pl.P(12.0,12.90)[1]:.2f}', stroke=C['aco'], sw=0.8)
    # fonte de luz contínua
    v.poly([pl.P(x0, 12.53), pl.P(11.86, 12.53), pl.P(11.86, 12.90)], stroke=C['luz'], sw=0.9, close=False, dash='2 0.8')
    v.add('</g>')
    v.rect(ox, oy, W, W, stroke=C['grey2'], sw=0.2)
    v.text(*pl.P(11.66, 12.26), 'parede', size=5.0, weight=600, cor='#fff')
    v.text(*pl.P(11.60, 12.78), 'forro', size=5.6, weight=600, anchor='start')
    for i, (t, cor) in enumerate((('trilho: curva ou emenda a 90°, conforme o sistema escolhido', C['aco']),
                                  ('fonte de luz contínua, contornando o canto', C['luz']),
                                  ('testeira em L, com cantoneira na aresta', C['ink']))):
        v.text(ox, oy + W + 4.5 + i * 2.9, t, size=5.2, weight=600, anchor='start', cor=cor)
    v.cota(*pl.P(11.88, 12.95), *pl.P(12.08, 12.95), off=0, txt='20', size=5.8, ext=False, cor=C['luz'], tcor=C['luz'])
    v.cota(*pl.P(11.55, 12.35), *pl.P(11.55, 12.55), off=0, txt='20', size=5.8, ext=False, cor=C['luz'], tcor=C['luz'])


def cabeceira(v, ox, oy):
    """C4 — cabeceira (início) do CT2 na parede superior, a 1,75 m da parede da cozinha (planta 1:10)."""
    x0, y0 = 8.20, 12.12
    pl = Planta(10, ox, oy, x0, y0)
    W, H = pl.mm(0.78), pl.mm(0.62)
    v.add(f'<clipPath id="cpC4"><rect x="{ox}" y="{oy}" width="{W}" height="{H}"/></clipPath><g clip-path="url(#cpC4)">')
    a = pl.P(x0, y0)
    v.rect(a[0], a[1], W, pl.mm(12.35 - y0), fill=C['ink'])
    a = pl.P(x0, 12.35)
    v.rect(a[0], a[1], W, H, fill=C['st'])
    v.poly([pl.P(8.58, 12.35), pl.P(9.2, 12.35), pl.P(9.2, 12.55), pl.P(8.58, 12.55)], fill=C['cort_fill'])
    v.poly([pl.P(8.58 - T_CHAPA, 12.35), pl.P(8.58, 12.35), pl.P(8.58, 12.55), pl.P(9.2, 12.55), pl.P(9.2, 12.55 + T_CHAPA),
            pl.P(8.58 - T_CHAPA, 12.55 + T_CHAPA)], fill='url(#hGesso)', stroke=C['ink'], sw=0.3)
    v.line(*pl.P(8.62, 12.43), *pl.P(9.2, 12.43), C['aco'], 0.8)
    v.circle(*pl.P(8.62, 12.43), 0.7, fill=C['aco'])
    v.line(*pl.P(8.60, 12.53), *pl.P(9.2, 12.53), C['luz'], 0.9, dash='2 0.8')
    v.add('</g>')
    v.rect(ox, oy, W, H, stroke=C['grey2'], sw=0.2)
    v.cota(*pl.P(8.20, 12.62), *pl.P(8.58, 12.62), off=0, txt='← 1,75 da parede da cozinha', size=5.0, ext=False)
    v.cota(*pl.P(8.45, 12.35), *pl.P(8.45, 12.55), off=0, txt='20', size=5.8, ext=False, cor=C['luz'], tcor=C['luz'])
    q = pl.P(8.58, 12.46)
    v.text(q[0] + 16, q[1] + 25, 'fechamento lateral (cabeceira)', size=5.2, weight=700, anchor='start')
    v.text(q[0] + 16, q[1] + 28, 'em chapa, mesmo acabamento da testeira', size=5.0, weight=400, anchor='start', cor=C['muted'])
    v.text(*pl.P(8.95, 12.27), 'parede superior do estar', size=5.0, weight=600, cor='#fff')


def prancha():
    v = SVG()
    # ---- plantas ampliadas 1:50
    ct1, ct2 = CORTINEIROS

    def ex1(v, pl):
        v.corte_marca(*pl.P(10.55, 1.25), *pl.P(12.3, 1.25), 'C1', '02', lado=-1)
        P = pl.P
        v.cota(*P(11.28, 3.30), *P(11.48, 3.30), off=0, txt='0,20', size=5.6, ext=False, cor=C['luz'], tcor=C['luz'])
        v.cota(*P(11.10, 0.15), *P(11.10, 3.65), off=0, txt='3,50', size=5.8, ext=False)
        v.text(*P(8.9, 2.1), 'SUÍTE MASTER · forro +2,85', size=6.0, weight=700)
        v.text(*P(8.9, 2.45), 'P10 · porta de correr veneziana 2,50 × 2,10', size=5.0, weight=400, cor=C['muted'])
    planta_ampliada(v, 'cpA', 50, 14, 26, (6.72, -0.05, 12.40, 3.85), ct1, ex1)
    mini_titulo(v, 14, 115, 'CT1', 'Cortineiro · suíte master', 'planta 1:50', 'L08 fita LED')

    def ex2(v, pl):
        P = pl.P
        v.corte_marca(*P(11.0, 17.9), *P(12.75, 17.9), 'C2', '02', lado=-1)
        v.chamada(*P(12.45, 12.0), 'C3', '02')
        v.chamada(*P(8.58, 12.95), 'C4', '02')
        v.cota(*P(6.83, 12.95), *P(8.58, 12.95), off=0, txt='1,75', size=5.8, ext=False)
        v.cota(*P(8.58, 13.3), *P(12.08, 13.3), off=0, txt='3,50', size=5.8, ext=False)
        v.cota(*P(11.55, 12.35), *P(11.55, 20.35), off=0, txt='8,00', size=5.8, ext=False)
        v.cota(*P(11.88, 19.9), *P(12.08, 19.9), off=0, txt='0,20', size=5.6, ext=False, cor=C['luz'], tcor=C['luz'])
        v.text(*P(9.2, 16.9), 'ESTAR / JANTAR · forro +3,40', size=6.0, weight=700)
        v.text(*P(9.2, 17.25), 'P05 (2×) 3,00 × 2,10 · J01 2,50 × 2,50', size=5.0, weight=400, cor=C['muted'])
        P1.cassete(v, pl)
    planta_ampliada(v, 'cpB', 50, 14, 132, (6.72, 12.10, 12.40, 20.55), ct2, ex2)
    mini_titulo(v, 14, 309, 'CT2', 'Cortineiro · estar / jantar', 'planta 1:50', 'L09 Tuboled')

    # ---- cortes 1:5
    corte_cortineiro(v, 178, 104, FORRO_ALA, LAJE_ALA, 'C1', 'fita', 2.10, 'P10')
    mini_titulo(v, 146, 166, 'C1', 'Corte do cortineiro · suíte master', 'escala 1:5', 'entreforro 15 cm')
    corte_cortineiro(v, 178, 292, FORRO_ESTAR, LAJE_ESTAR, 'C2', 'Tuboled', 3.00, 'J01')
    mini_titulo(v, 146, 355, 'C2', 'Corte do cortineiro · estar / jantar', 'escala 1:5', 'entreforro 30 cm')

    # ---- perspectiva e detalhes em planta 1:10
    perspectiva(v, 334, 118)
    mini_titulo(v, 330, 150, '3D', 'Como funciona', 'perspectiva do corte · sem escala')
    canto_L(v, 334, 172)
    mini_titulo(v, 330, 266, 'C3', 'Canto em L · CT2', 'planta 1:10')
    cabeceira(v, 334, 284)
    mini_titulo(v, 330, 358, 'C4', 'Cabeceira · CT2', 'planta 1:10')

    escala_grafica(v, 14, 400, 50, 3, [0, 0.5, 1, 2, 3])
    v.text(14, 397, 'plantas 1:50', size=5.8, weight=600, anchor='start', cor=C['muted'])
    escala_grafica(v, 150, 400, 5, 0.3, [0, 0.1, 0.2, 0.3])
    v.text(150, 397, 'cortes 1:5', size=5.8, weight=600, anchor='start', cor=C['muted'])

    itens = [
        (1, 'Laje pré-fabricada = fundo do cortineiro', 'Regularizar e pintar em branco fosco no trecho do vão.', 'prop'),
        (2, 'Parede acabada', 'Referência para medir o vão livre de 20 cm (após reboco/pintura).', 'doc'),
        (3, 'Trilho da cortina, fixado na laje', 'Tipo, quantidade e posição a definir com o fornecedor da cortina.', 'pend'),
        (4, 'Espaço reservado para o trilho', 'Faixa junto à parede; manter livre de fixações do forro.', 'prop'),
        (5, 'Cortina', 'Tipo a definir com o fornecedor.', 'pend'),
        (6, 'Fonte de luz na face interna da testeira', 'CT1: fita LED em perfil · CT2: Tuboled. Voltada para a cortina, escondida pela testeira. Modelo a definir com a loja.', 'prop'),
        (7, 'Testeira em chapa de gesso até a laje', 'Fecha o entreforro e esconde a fonte. Mesma placa do forro.', 'prop'),
        (8, 'Perfil de fixação da testeira', 'Guia na laje e montante vertical. Tipo e fixação conforme fabricante.', 'prop'),
        (9, 'Cantoneira de proteção da aresta', 'Aresta inferior da testeira; massa e pintura por cima.', 'prop'),
        (10, 'Forro em chapa de gesso ST', 'Espessura conforme fabricante.', 'doc'),
        (11, 'Estrutura e pendurais do forro', 'Perfis, pendurais, fixações e espaçamentos conforme manual do fabricante.', 'pend'),
    ]
    pill = {'doc': '<span class="pill doc">DOC</span>', 'prop': '<span class="pill prop">PROPOSTA</span>',
            'pend': '<span class="pill pend">A DEFINIR</span>'}
    lista = ''.join(f'<tr><td style="width:6mm"><b style="display:inline-flex;width:4.4mm;height:4.4mm;border-radius:50%;background:#22251a;color:#fff;align-items:center;justify-content:center;font-size:6.4pt;font-family:Outfit">{n}</b></td>'
                    f'<td><b style="font-weight:600">{t}</b><span class="s">{d}</span></td><td style="text-align:right">{pill[k]}</td></tr>'
                    for n, t, d, k in itens)
    seq = ['Concluir e testar elétrica (pontos e circuitos da fonte) e ar-condicionado no entreforro.',
           'Marcar na laje a linha da testeira: 20 cm da parede acabada, em toda a extensão.',
           'Fixar o trilho (ou a base do trilho) na laje, antes de fechar a testeira.',
           'Montar a estrutura do forro e a testeira; aplicar cantoneira na aresta.',
           'Tratar juntas, lixar e pintar; pintar o fundo (laje) em branco fosco.',
           'Instalar fonte de luz e driver; testar; instalar a cortina.']
    q1 = box(438, 12, 146, 206, 'b-creme', 'Componentes', 'QUADRO 1', f'<table>{lista}</table>'
             '<div style="font-weight:700;font-size:7.4pt;letter-spacing:.8pt;margin-top:3.5mm">SEQUÊNCIA DE EXECUÇÃO <span class="pill prop">PROPOSTA</span></div>'
             '<ol style="margin:1.6mm 0 0 4.2mm;font-size:7.4pt;font-weight:300;line-height:1.3">' + ''.join(f'<li style="margin-bottom:.6mm">{t}</li>' for t in seq) + '</ol>')
    obs = [
        ('Vão livre de 20 cm', 'Decisão de 30/09/2026. Medido da parede acabada à face interna da testeira, em toda a extensão.'),
        ('Comprimentos', 'CT1: parede inteira, 3,50 m. CT2: em L, 3,50 m na parede superior (a partir de 1,75 m da parede da cozinha) + 8,00 m na lateral. Conforme DWG.'),
        ('Luz', 'A fonte fica no alto do vão, voltada para a cortina, e não aparece de quem está no ambiente. Deixar o driver dentro do cortineiro, acessível pelo vão.'),
        ('Manutenção', 'Fonte, driver e trilho acessíveis por baixo, pelo vão de 20 cm. Não há alçapão.'),
        ('Conferir', 'Topo da esquadria abaixo do forro: J01 a 3,00 m (caderno de esquadrias); o DWG indica 2,50 m.'),
    ]
    q3 = box(438, 222, 146, 101, 'b-bege', 'Observações', 'QUADRO 2',
             '<div class="obs small">' + ''.join(f'<div class="i"><span class="t">{t}</span><p>{p}</p></div>' for t, p in obs) + '</div>')
    extra = q1 + q3 + carimbo(438, 327, 146, 83, 'Cortineiros', '1:50 · 1:10 · 1:5', 2, TOTAL_N) + \
        titulo(150, 381, '02', 'Cortineiros iluminados', 'CT1 suíte master · CT2 estar/jantar · vão livre 20 cm · cotas em metros (plantas) e centímetros (cortes)')
    return pagina(str(v), extra)
