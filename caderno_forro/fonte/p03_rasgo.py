# -*- coding: utf-8 -*-
"""Prancha 03 — Rasgo de luz RG1 (circulação)."""
from base import *
from dados_forro import *
from secao import *
import p01_planta as P1

R = RASGO
LARG = RASGO_LARG
AF = RASGO_AFAST


def planta(v, ox, oy):
    reg = (5.85, 3.45, 8.45, 12.62)
    pl = Planta(50, ox, oy, reg[0], reg[1])
    W, H = pl.mm(reg[2] - reg[0]), pl.mm(reg[3] - reg[1])
    v.add(f'<clipPath id="cpR"><rect x="{ox}" y="{oy}" width="{W}" height="{H}"/></clipPath><g clip-path="url(#cpR)">')
    P1.fill_ambientes(v, pl)
    P1.rasgo(v, pl)
    P1.alcapoes(v, pl)
    paredes(v, pl)
    v.add('</g>')
    P = pl.P
    v.cota(*P(6.83, 4.35), *P(6.83 + AF, 4.35), off=0, txt='0,15', size=5.4, ext=False)
    v.cota(*P(R['x0'], 4.85), *P(R['x1'], 4.85), off=0, txt='0,12', size=5.4, ext=False, cor=C['luz'], tcor=C['luz'])
    v.cota(*P(6.83, 11.95), *P(8.04, 11.95), off=0, txt='1,20', size=5.6, ext=False)
    v.cota(*P(7.72, R['y0']), *P(7.72, R['y1']), off=0, txt='8,20', size=6.0, ext=False, cor=C['luz'], tcor=C['luz'])
    v.cota(*P(7.30, 3.80), *P(7.30, R['y0']), off=0, txt='0,10', size=5.0, ext=False)
    v.cota(*P(7.30, R['y1']), *P(7.30, 12.20), off=0, txt='0,10', size=5.0, ext=False)
    v.cota(*P(6.13, 10.40), *P(6.83, 10.40), off=0, txt='0,70', size=5.0, ext=False)
    v.corte_marca(*P(6.25, 5.2), *P(8.35, 5.2), 'R1', '03', lado=-1)
    v.corte_marca(*P(7.04, 10.75), *P(7.04, 12.55), 'R2', '03', lado=1)
    v.text(*P(7.48, 8.1), 'CIRCULAÇÃO', size=6.0, weight=700, rot=-90)
    v.text(*P(7.78, 8.1), 'forro +2,85 · placa ST', size=5.0, weight=500, cor=C['muted'], rot=-90)
    v.text(*P(4.95, 8.30), 'banhos', size=5.4, weight=600, cor=C['ru_txt'])
    v.text(*P(4.60, 5.3), 'SUÍTE 2', size=5.4, weight=600, cor=C['muted'])
    v.text(*P(4.60, 11.7), 'SUÍTE 1', size=5.4, weight=600, cor=C['muted'])
    v.text(*P(8.28, 3.6), 'suíte master', size=5.0, weight=600, cor=C['muted'], anchor='end')
    v.text(*P(7.45, 12.55), 'estar / jantar', size=5.0, weight=600, cor=C['muted'])
    a = P(ALCAPOES[0]['x'] + 0.25, ALCAPOES[0]['y'])
    v.seta_nota(*a, a[0] + 16, a[1] - 6, C['prop'])
    v.text(a[0] + 16.5, a[1] - 6.5, 'AL1 · alçapão (se a', size=5.2, weight=700, cor=C['prop'], anchor='start')
    v.text(a[0] + 16.5, a[1] - 3.9, 'fonte for externa)', size=5.2, weight=700, cor=C['prop'], anchor='start')
    return pl


def corte_transversal(v, ox, y_forro):
    F, Lz = FORRO_ALA, LAJE_ALA
    k = 200.0
    s = Secao(5, ox, y_forro + F * k)
    zb = F - 0.26
    x0, x1 = AF, AF + LARG
    parede(v, s, -0.17, 0.0, zb, Lz)
    laje(v, s, -0.17, 0.62, Lz)
    chapa(v, s, 0.0, F, x0, F + T_CHAPA)                      # faixa junto à parede
    chapa(v, s, x1, F, 0.62, F + T_CHAPA)                     # forro
    quebra_v(v, s.P(0.62, 0)[0], s.P(0, F + 0.03)[1], s.P(0, F - 0.02)[1])
    chapa(v, s, x0 - T_CHAPA, F, x0, Lz)                      # lateral esquerda do rasgo
    chapa(v, s, x1, F, x1 + T_CHAPA, Lz)                      # lateral direita
    perfil_u(v, s, x0 - T_CHAPA - 0.028, F + T_CHAPA, x0 - T_CHAPA, Lz, 'dir')
    perfil_u(v, s, x1 + T_CHAPA, F + T_CHAPA, x1 + T_CHAPA + 0.028, Lz, 'esq')
    for xp in (0.40, 0.54):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.05, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.025, F + T_CHAPA + 0.022, Lz)
    perfil_u(v, s, 0.0, F + T_CHAPA, 0.03, F + T_CHAPA + 0.022, 'cima')
    cantoneira(v, s, x0, F, dx=-1, dz=1, L=0.02)
    cantoneira(v, s, x1, F, dx=1, dz=1, L=0.02)
    a, b = s.P(x0, Lz), s.P(x1, Lz)
    v.line(a[0], a[1] + 0.3, b[0], b[1] + 0.3, C['rust'], 0.5, dash='1.4 0.7')
    # Tuboled
    xc = (x0 + x1) / 2
    zr = s.R(x0 + 0.01, Lz - 0.045, x1 - 0.01, Lz)
    v.rect(*zr, fill='#fde6bf', stroke=C['luz'], sw=0.25, dash='1 0.6')
    c = s.P(xc, Lz - 0.03)
    v.rect(c[0] - 3, c[1] - 6, 6, 3.2, fill=C['aco'])
    v.circle(*c, 0.013 * k, fill='#fff6df', stroke=C['luz'], sw=0.35)
    cone_luz(v, [s.P(x0 + 0.005, Lz - 0.03), s.P(x1 - 0.005, Lz - 0.03), s.P(x1 + 0.12, zb + 0.01), s.P(x0 - 0.12, zb + 0.01)])
    # cotas
    v.cota(*s.P(0.0, F - 0.05), *s.P(x0, F - 0.05), off=0, txt='15', size=6.4, ext=False)
    v.cota(*s.P(x0, F - 0.05), *s.P(x1, F - 0.05), off=0, txt='12', size=6.6, ext=False, cor=C['luz'], tcor=C['luz'], weight=800)
    for xx in (0.0, x0, x1):
        v.line(*s.P(xx, F - 0.07), *s.P(xx, F), C['grey'], 0.15)
    v.cota(*s.P(0.47, F), *s.P(0.47, Lz), off=0, txt='15 cm', size=6.2, ext=False)
    xm = s.P(0.66, 0)[0]
    marca_nivel(v, xm, s.P(0, F)[1], f'+{br(F)} forro')
    marca_nivel(v, xm, s.P(0, Lz)[1], f'+{br(Lz)} laje')
    Rr = lambda x, z: s.P(x, z)
    L = s.P(-0.17, 0)[0]
    top = Rr(0, Lz + 0.19)[1]
    call(v, *Rr(-0.08, Lz + 0.06), L - 8, Rr(0, Lz + 0.06)[1], 1)
    call(v, *Rr(-0.005, F - 0.15), L - 8, Rr(0, F - 0.15)[1], 2)
    call(v, *Rr(0.07, F + 0.006), Rr(0.02, 0)[0], top, 3)
    call(v, *Rr(x0 - 0.006, (F + Lz) / 2), Rr(0.10, 0)[0], top, 4)
    call(v, *Rr(xc, Lz - 0.03), Rr(0.21, 0)[0], top, 5)
    call(v, *Rr(xc, Lz + 0.001), Rr(0.27, 0)[0], top, 6)
    call(v, *Rr(x1 + 0.002, F), Rr(0.32, 0)[0], Rr(0, F - 0.16)[1], 7)
    call(v, *Rr(0.44, F + 0.006), Rr(0.52, 0)[0], Rr(0, F - 0.16)[1], 8)
    call(v, *Rr(0.565, F + 0.05), Rr(0.40, 0)[0], top, 9)
    return s


def corte_extremidade(v, ox, y_forro):
    """R2 — corte longitudinal na extremidade do rasgo junto à porta do estar (1:5)."""
    F, Lz = FORRO_ALA, LAJE_ALA
    k = 200.0
    s = Secao(5, ox, y_forro + F * k)
    zb = F - 0.26
    # u = distância a partir da face da verga (porta do estar), para a esquerda do desenho = interior da circulação
    # desenho: verga à direita (x=0.45..0.60), circulação à esquerda
    xv = 0.45
    x, y, w, h = s.R(xv, zb, xv + 0.15, Lz)
    v.rect(x, y, w, h, fill='url(#hAlv)', stroke=C['ink'], sw=0.35)
    quebra_h(v, x - 1, x + w + 1, y + h)
    v.text(x + w / 2, y + h - 3, 'verga · porta P06', size=5.0, weight=600, cor=C['muted'], rot=-90)
    laje(v, s, -0.05, xv + 0.15, Lz)
    # forro após o rasgo (junto à verga): 10 cm
    chapa(v, s, xv - 0.10, F, xv, F + T_CHAPA)
    chapa(v, s, xv - 0.10 - T_CHAPA, F, xv - 0.10, Lz)          # fechamento da ponta
    perfil_u(v, s, xv - 0.10, F + T_CHAPA, xv - 0.10 + 0.028, Lz, 'esq')
    cantoneira(v, s, xv - 0.10 - T_CHAPA, F, dx=1, dz=1, L=0.02)
    # tubo ao longo do rasgo (vista)
    a, b = s.P(-0.05, Lz - 0.03), s.P(xv - 0.10 - T_CHAPA - 0.03, Lz - 0.03)
    v.rect(a[0], a[1] - 0.013 * k, b[0] - a[0], 0.026 * k, fill='#fff6df', stroke=C['luz'], sw=0.35)
    v.rect(b[0], b[1] - 3.2, 3.2, 6.4, fill=C['aco'])
    cone_luz(v, [s.P(-0.05, Lz - 0.04), s.P(xv - 0.13, Lz - 0.04), s.P(xv - 0.11, zb + 0.01), s.P(-0.05, zb + 0.01)])
    # lateral do rasgo ao fundo (em vista)
    x, y, w, h = s.R(-0.05, F, xv - 0.10 - T_CHAPA, Lz)
    v.rect(x, y, w, h, fill='none', stroke=C['grey'], sw=0.2)
    v.line(*s.P(-0.05, F), *s.P(xv - 0.10 - T_CHAPA, F), C['ink'], 0.35)
    quebra_v(v, s.P(-0.05, 0)[0], s.P(0, Lz + 0.14)[1], s.P(0, F - 0.02)[1])
    v.cota(*s.P(xv - 0.10, F - 0.05), *s.P(xv, F - 0.05), off=0, txt='10', size=6.4, ext=False)
    v.line(*s.P(xv - 0.10, F - 0.07), *s.P(xv - 0.10, F), C['grey'], 0.15)
    v.line(*s.P(xv, F - 0.07), *s.P(xv, F), C['grey'], 0.15)
    t = s.P(0.02, F - 0.12)
    v.text(t[0], t[1], 'fechamento da ponta em chapa + cantoneira', size=5.4, weight=700, anchor='start')
    v.text(t[0], t[1] + 2.6, 'tubo termina antes da ponta: ajustar à modulação', size=5.0, weight=400, anchor='start', cor=C['muted'])
    v.text(t[0], t[1] + 4.9, 'dos tubos escolhidos (sem trecho escuro)', size=5.0, weight=400, anchor='start', cor=C['muted'])
    xm = s.P(0.64, 0)[0]
    marca_nivel(v, xm, s.P(0, F)[1], f'+{br(F)} forro')
    marca_nivel(v, xm, s.P(0, Lz)[1], f'+{br(Lz)} laje')


def perspectiva(v, ox, oy, sc=46.0):
    """Perspectiva interna da circulação, olhando ao longo do rasgo (um ponto de fuga)."""
    F = FORRO_ALA
    W = 1.21
    D0 = 1.6
    vp = (ox + 0.62 * sc, oy + (F - 1.55) * sc)
    def P(x, z, d):
        n = (ox + x * sc, oy + (F - z) * sc)
        k = D0 / (D0 + d)
        return (vp[0] + (n[0] - vp[0]) * k, vp[1] + (n[1] - vp[1]) * k)
    L = 8.4
    q = lambda pts, **kw: v.poly([P(*p) for p in pts], **kw)
    q([(0, F, 0), (W, F, 0), (W, F, L), (0, F, L)], fill='#fbf8f1', stroke=C['ink'], sw=0.25)       # forro
    q([(0, 0, 0), (0, F, 0), (0, F, L), (0, 0, L)], fill='#efeadc', stroke=C['ink'], sw=0.25)        # parede esq.
    q([(W, 0, 0), (W, F, 0), (W, F, L), (W, 0, L)], fill='#f3efe4', stroke=C['ink'], sw=0.25)        # parede dir.
    q([(0, 0, 0), (W, 0, 0), (W, 0, L), (0, 0, L)], fill='#e6e0d0', stroke=C['ink'], sw=0.25)        # piso
    q([(0, 0, L), (W, 0, L), (W, F, L), (0, F, L)], fill='#e9e4d6', stroke=C['ink'], sw=0.2)         # fundo
    # portas (esquerda) e porta do estar ao fundo
    for d0 in (1.95, 6.9):
        q([(0, 0, d0), (0, 2.10, d0), (0, 2.10, d0 + 0.8), (0, 0, d0 + 0.8)], fill='#fff', stroke=C['grey'], sw=0.2)
    q([(0.14, 0, L), (0.14, 2.10, L), (1.0, 2.10, L), (1.0, 0, L)], fill='#fff', stroke=C['grey'], sw=0.2)
    # luz no piso
    q([(0.05, 0, 0.1), (0.75, 0, 0.1), (0.75, 0, L - 0.1), (0.05, 0, L - 0.1)], fill=C['luz2'], op=0.22)
    q([(0.0, 1.0, 0.1), (0.0, F, 0.1), (0.0, F, L - 0.1), (0.0, 1.0, L - 0.1)], fill='url(#gLuz)', op=0.35)
    # rasgo
    x0, x1 = AF, AF + LARG
    q([(x0, F, 0.1), (x1, F, 0.1), (x1, F, L - 0.1), (x0, F, L - 0.1)], fill='#fff3d6', stroke=C['cort_line'], sw=0.3)
    a, b = P((x0 + x1) / 2, F, 0.3), P((x0 + x1) / 2, F, L - 0.3)
    v.line(*a, *b, C['luz2'], 2.4, cap='round')
    v.line(*a, *b, '#fffaf0', 0.8, cap='round')
    # moldura de corte (primeiro plano)
    q([(0, 0, 0), (W, 0, 0), (W, F, 0), (0, F, 0)], stroke=C['ink'], sw=0.5)
    for (x, z, d), t, dx, dy in (((x0, F, 0.4), 'rasgo 12 cm · luz para baixo', 20, -9), ((0.9, F, 1.0), 'forro +2,85', 16, -2),
                                 ((0.0, 1.4, 0.5), 'parede esquerda', -8, 4), ((0.4, 0, 1.2), 'luz no piso', 14, 8)):
        pp = P(x, z, d)
        v.circle(*pp, 0.45, fill=C['ink'])
        v.line(*pp, pp[0] + dx, pp[1] + dy, C['ink'], 0.18)
        v.text(pp[0] + dx + (0.8 if dx > 0 else -0.8), pp[1] + dy + 1, t, size=5.6, weight=600, anchor='start' if dx > 0 else 'end')


def resumo(v, x, y):
    """Resumo visual das dimensões propostas."""
    dados = (('12 cm', 'largura do rasgo'), ('15 cm', 'da parede esquerda'), ('≈ 15 cm', 'altura até a laje'), ('8,20 m', 'comprimento'))
    for i, (n, t) in enumerate(dados):
        xx = x + (i % 2) * 44
        yy = y + (i // 2) * 20
        v.rect(xx, yy, 41, 17, fill=C['creme'], rx=2.4)
        v.text(xx + 4, yy + 9.2, n, size=15, weight=800, family='Outfit', anchor='start', cor=C['luz'])
        v.text(xx + 4, yy + 13.8, t, size=5.8, weight=500, anchor='start')
    v.tag(x, y - 5, 'PROPOSTA', 'prop', anchor='start')
    v.text(x + 22, y - 3.9, 'dimensões a ajustar ao Tuboled escolhido', size=5.6, weight=500, anchor='start', cor=C['muted'])


def prancha():
    v = SVG()
    planta(v, 20, 26)
    mini_titulo(v, 14, 228, 'RG1', 'Rasgo · planta', 'planta 1:50')
    corte_transversal(v, 150, 108)
    mini_titulo(v, 118, 170, 'R1', 'Corte transversal do rasgo', 'escala 1:5', 'luz para baixo')
    corte_extremidade(v, 150, 262)
    mini_titulo(v, 118, 330, 'R2', 'Extremidade do rasgo', 'escala 1:5', 'junto à porta do estar')
    perspectiva(v, 345, 22, sc=58)
    mini_titulo(v, 312, 204, '3D', 'Como se vê da circulação', 'perspectiva · sem escala')
    resumo(v, 14, 250)
    escala_grafica(v, 14, 400, 50, 2, [0, 0.5, 1, 2])
    v.text(14, 397, 'planta 1:50', size=5.8, weight=600, anchor='start', cor=C['muted'])
    escala_grafica(v, 120, 400, 5, 0.3, [0, 0.1, 0.2, 0.3])
    v.text(120, 397, 'cortes 1:5', size=5.8, weight=600, anchor='start', cor=C['muted'])

    itens = [
        (1, 'Laje pré-fabricada = fundo do rasgo', 'Regularizar e pintar em branco fosco (melhora o rendimento da luz).', 'prop'),
        (2, 'Parede esquerda acabada', 'Referência para a faixa de 15 cm.', 'doc'),
        (3, 'Faixa de forro de 15 cm junto à parede', 'Mantém a luz no piso da circulação, sem mancha forte na parede.', 'prop'),
        (4, 'Laterais do rasgo em chapa até a laje', 'Com perfil de fixação na laje e no forro, conforme fabricante.', 'prop'),
        (5, 'Tuboled (L10) no fundo do rasgo', 'Modelo, suporte e modulação a definir com a loja de iluminação.', 'pend'),
        (6, 'Suporte do tubo fixado na laje', 'Conforme o produto escolhido.', 'pend'),
        (7, 'Cantoneiras nas duas arestas', 'Aresta viva e reta; massa e pintura por cima.', 'prop'),
        (8, 'Forro em chapa de gesso ST', 'Espessura conforme fabricante.', 'doc'),
        (9, 'Estrutura e pendurais do forro', 'Conforme manual do fabricante; manter fora do vão do rasgo.', 'pend'),
    ]
    pill = {'doc': '<span class="pill doc">DOC</span>', 'prop': '<span class="pill prop">PROPOSTA</span>',
            'pend': '<span class="pill pend">A DEFINIR</span>'}
    lista = ''.join(f'<tr><td style="width:6mm"><b style="display:inline-flex;width:4.4mm;height:4.4mm;border-radius:50%;background:#22251a;color:#fff;align-items:center;justify-content:center;font-size:6.4pt;font-family:Outfit">{n}</b></td>'
                    f'<td><b style="font-weight:600">{t}</b><span class="s">{d}</span></td><td style="text-align:right">{pill[k]}</td></tr>'
                    for n, t, d, k in itens)
    seq = ['Concluir e testar elétrica (alimentação do Tuboled) no entreforro.',
           'Marcar na laje as duas linhas do rasgo (15 e 27 cm da parede esquerda).',
           'Fixar os suportes dos tubos na laje, conforme o produto escolhido.',
           'Montar laterais, fechamentos das pontas e forro; aplicar cantoneiras.',
           'Tratar juntas e pintar; pintar o fundo (laje) em branco fosco.',
           'Instalar e testar os tubos; conferir continuidade da luz.']
    q1 = box(438, 12, 146, 176, 'b-creme', 'Componentes', 'QUADRO 1', f'<table>{lista}</table>'
             '<div style="font-weight:700;font-size:7.4pt;letter-spacing:.8pt;margin-top:3.5mm">SEQUÊNCIA DE EXECUÇÃO <span class="pill prop">PROPOSTA</span></div>'
             '<ol style="margin:1.6mm 0 0 4.2mm;font-size:7.4pt;font-weight:300;line-height:1.3">' + ''.join(f'<li style="margin-bottom:.6mm">{t}</li>' for t in seq) + '</ol>')
    obs = [
        ('Intenção de iluminação', 'Rasgo contínuo, com a luz voltada para baixo, reforçando a iluminação geral da circulação. Mantido do lado esquerdo, como no caderno de iluminação (L10).'),
        ('Dimensões propostas', 'Largura 12 cm, a 15 cm da parede esquerda, 8,20 m de comprimento (10 cm livres em cada ponta). Altura até a laje: cerca de 15 cm, medir em obra.'),
        ('Produto', 'Antes de fechar o forro, confirmar com a loja o diâmetro do tubo, o suporte e o comprimento das peças. Ajustar largura e comprimento do rasgo ao produto.'),
        ('Manutenção', 'Tubos trocados por baixo, pelo próprio rasgo. Se o produto usar fonte externa, prever o alçapão AL1 (D7, prancha 05) perto da ponta junto ao estar.'),
        ('Portas', 'O rasgo passa acima das portas da circulação (topo a 2,10 m). Não há interferência.'),
    ]
    q3 = box(438, 192, 146, 131, 'b-bege', 'Observações', 'QUADRO 2',
             '<div class="obs small">' + ''.join(f'<div class="i"><span class="t">{t}</span><p>{p}</p></div>' for t, p in obs) + '</div>')
    extra = q1 + q3 + carimbo(438, 327, 146, 83, 'Rasgo de luz', '1:50 · 1:5', 3, TOTAL) + \
        titulo(150, 381, '03', 'Rasgo de luz · circulação', 'RG1 · luz para baixo · dimensões propostas, aguardando aprovação · cotas em metros (planta) e centímetros (cortes)')
    return pagina(str(v), extra)
