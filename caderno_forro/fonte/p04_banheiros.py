# -*- coding: utf-8 -*-
"""Prancha 04 — Banheiros: forro em placa RU."""
from base import *
from dados_forro import *
from secao import *
import p01_planta as P1

BANHOS = [a for a in AMB if a['placa'] == 'RU']


def planta_banho(v, a, ox, oy, esc=25):
    x0, y0, x1, y1 = a['rect']
    m = 0.22
    pl = Planta(esc, ox, oy, x0 - m, y0 - m)
    W, H = pl.mm(x1 - x0 + 2 * m), pl.mm(y1 - y0 + 2 * m)
    cid = 'cp' + a['id']
    v.add(f'<clipPath id="{cid}"><rect x="{ox}" y="{oy}" width="{W}" height="{H}"/></clipPath><g clip-path="url(#{cid})">')
    p0, p1 = pl.P(x0 - m, y0 - m), pl.P(x1 + m, y1 + m)
    v.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], fill='#f4f2ec')
    q0, q1 = pl.P(x0, y0), pl.P(x1, y1)
    v.rect(q0[0], q0[1], q1[0] - q0[0], q1[1] - q0[1], fill='url(#hRU)')
    # junta perimetral (tabica) — traço interno
    g = pl.mm(0.03)
    v.rect(q0[0] + g, q0[1] + g, q1[0] - q0[0] - 2 * g, q1[1] - q0[1] - 2 * g, stroke=C['ru_txt'], sw=0.3, dash='1.6 0.8')
    paredes(v, pl, cor='#6f6c60')
    for o in LUM['pontuais']:
        if x0 <= o['x'] <= x1 and y0 <= o['y'] <= y1:
            x, y = pl.P(o['x'], o['y'])
            lum_simbolo(v, x, y, o['code'], s=1.5, cor='#6f6c60')
            if o['code'] == 'L01':
                v.circle(x, y, 7.5, stroke=C['ru_txt'], sw=0.25, dash='1 0.7')
                v.text(x, y + 10.2, 'área do box', size=5.0, weight=600, cor=C['ru_txt'])
    v.add('</g>')
    v.rect(ox, oy, W, H, stroke=C['grey2'], sw=0.2)
    P = pl.P
    v.cota(*P(x0, y1 + 0.13), *P(x1, y1 + 0.13), off=0, txt=br(round((x1 - x0) / 0.05) * 0.05), size=6.0, ext=False)
    v.cota(*P(x0 - 0.13, y0), *P(x0 - 0.13, y1), off=0, txt=br(round((y1 - y0) / 0.05) * 0.05), size=6.0, ext=False)
    return pl


def corte_banho(v, ox, y_forro):
    """B1 — corte típico no encontro forro RU × parede revestida (1:10)."""
    F, Lz = FORRO_ALA, LAJE_ALA
    k = 100.0
    s = Secao(10, ox, y_forro + F * k)
    zb = 1.85
    parede(v, s, -0.17, -0.012, zb, Lz)
    x, y, w, h = s.R(-0.012, zb, 0.0, F)
    v.rect(x, y, w, h, fill='url(#hCer)', stroke=C['ink'], sw=0.2)
    laje(v, s, -0.17, 1.05, Lz)
    chapa(v, s, 0.008, F, 1.05, F + T_CHAPA, ru=True)
    quebra_v(v, s.P(1.05, 0)[0], s.P(0, F + 0.03)[1], s.P(0, F - 0.02)[1])
    # tabica / perfil perimetral
    perfil_u(v, s, 0.0, F, 0.02, F + 0.03, 'dir')
    for xp in (0.30, 0.75):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.05, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.025, F + T_CHAPA + 0.022, Lz)
    # luminária embutida L01 (recorte)
    lx = 0.52
    x, y, w, h = s.R(lx - 0.045, F, lx + 0.045, F + 0.07)
    v.rect(x, y, w, h, fill='#e3e0d6', stroke=C['ink'], sw=0.25)
    v.poly([s.P(lx - 0.03, F), s.P(lx + 0.03, F), s.P(lx + 0.16, F - 0.45), s.P(lx - 0.16, F - 0.45)], fill='url(#gLuz)')
    # chuveiro (A.F. 2,10 — caderno hidráulico)
    c0 = s.P(-0.012, 2.10)
    v.line(*c0, *s.P(0.30, 2.10), '#6f6c60', 0.8)
    v.rect(*s.P(0.26, 2.10), 7, 1.4, fill='#6f6c60')
    for i in range(6):
        v.line(*s.P(0.27 + i * 0.012, 2.08), *s.P(0.24 + i * 0.02, 1.9), '#8aa0a8', 0.2, dash='0.6 0.6')
    # vapor
    for i, xx in enumerate((0.25, 0.42, 0.62)):
        p = s.P(xx, 2.25 + (i % 2) * 0.1)
        v.path(f'M{p[0]:.2f},{p[1]+10:.2f} q-2,-3 0,-6 q2,-3 0,-6', stroke='#9fb3ba', sw=0.4)
    # cotas e níveis
    v.cota(*s.P(0.92, F), *s.P(0.92, Lz), off=0, txt='15 cm', size=6.0, ext=False)
    xm = s.P(1.09, 0)[0]
    marca_nivel(v, xm, s.P(0, F)[1], f'+{br(F)} forro RU')
    marca_nivel(v, xm, s.P(0, Lz)[1], f'+{br(Lz)} laje')
    marca_nivel(v, xm, s.P(0, 2.10)[1], '+2,10 chuveiro (A.F.)', cor='#6f6c60')
    Rr = lambda x, z: s.P(x, z)
    L = s.P(-0.17, 0)[0]
    top = Rr(0, Lz + 0.20)[1]
    call(v, *Rr(-0.09, 2.6), L - 8, Rr(0, 2.6)[1], 1)
    call(v, *Rr(-0.006, 2.3), L - 8, Rr(0, 2.3)[1], 2)
    call(v, *Rr(0.01, F + 0.02), Rr(0.08, 0)[0], top, 3)
    call(v, *Rr(0.20, F + 0.006), Rr(0.18, 0)[0], Rr(0, F - 0.2)[1], 4)
    call(v, *Rr(0.325, F + 0.03), Rr(0.30, 0)[0], top, 5)
    call(v, *Rr(lx, F + 0.04), Rr(0.52, 0)[0], top, 6)
    call(v, *Rr(0.62, 2.35), Rr(0.72, 0)[0], Rr(0, 2.0)[1], 7)


def prancha():
    v = SVG()
    pos = {'BSM': (16, 22), 'BS2': (128, 22), 'BS1': (128, 122), 'B4': (274, 22)}
    for a in BANHOS:
        ox, oy = pos[a['id']]
        pl = planta_banho(v, a, ox, oy)
        x0, y0, x1, y1 = a['rect']
        H = pl.mm(y1 - y0 + 0.44)
        mini_titulo(v, ox, oy + H + 8, 'B', a['nome'].title().replace('Suíte', 'Suíte'), 'planta 1:25',
                    f'{br(a["area"])} m² · forro +2,85 · placa RU')
    # planta-chave
    kp = Planta(250, 352, 134)
    P1.fill_ambientes(v, kp, [a for a in AMB if a['placa'] != 'RU'])
    P1.fill_ambientes(v, kp, BANHOS)
    paredes(v, kp)
    for a in BANHOS:
        x0, y0, x1, y1 = a['rect']
        c = kp.P((x0 + x1) / 2, (y0 + y1) / 2)
        v.circle(*c, 2.4, fill='#fff', stroke=C['ru_txt'], sw=0.3)
        v.text(c[0], c[1] + 0.9, 'B', size=5.4, weight=800, cor=C['ru_txt'], family='Outfit')
    v.text(300, 150, 'LOCALIZAÇÃO', size=6.6, weight=800, ls=1.1, anchor='start')
    v.text(300, 154, 'planta-chave · sem escala', size=5.6, weight=400, anchor='start', cor=C['muted'])
    v.text(300, 160, 'B = banhos com forro RU', size=5.6, weight=600, anchor='start', cor=C['ru_txt'])
    corte_banho(v, 40, 268)
    mini_titulo(v, 14, 222, 'B1', 'Corte típico · forro RU no banho', 'escala 1:10', 'vale para os 4 banhos')
    escala_grafica(v, 274, 122, 25, 1, [0, 0.25, 0.5, 1])
    v.text(274, 119, 'plantas 1:25', size=5.8, weight=600, anchor='start', cor=C['muted'])
    escala_grafica(v, 14, 400, 10, 0.5, [0, 0.1, 0.2, 0.3, 0.5])
    v.text(14, 397, 'corte 1:10', size=5.8, weight=600, anchor='start', cor=C['muted'])

    # --- quadro de adequação (HTML, área de desenho)
    ban = [('Banho Suíte Master', '6,83', 'J04 · basculante'), ('Banho Suíte 2', '4,20', 'J04 · basculante'),
           ('Banho Suíte 1', '4,20', 'J04 · basculante'), ('Banho 4', '4,62', 'J06 · ventilação')]
    rows = ''.join(f'<tr><td><b style="font-weight:600">{n}</b></td><td class="n">{ar}</td><td>{j} <span class="pill doc">DOC</span></td>'
                   f'<td>sim <span class="pill doc">DOC</span></td><td><span class="pill pend">A CONFIRMAR</span></td>'
                   f'<td><span class="pill pend">A CONFIRMAR</span></td><td><b style="color:#3f6e31">Adequada</b>, se as condições ao lado forem atendidas</td></tr>'
                   for n, ar, j in ban)
    adequ = box(222, 240, 208, 96, 'b-bege', 'Adequação por banho', 'QUADRO 3',
                f'''<table><tr><th>BANHO</th><th style="text-align:right">m²</th><th>VENTILAÇÃO NATURAL</th><th>CHUVEIRO</th>
                <th>BOX ATÉ O TETO?</th><th>EXAUSTÃO</th><th>PLACA RU</th></tr>{rows}</table>
                <div style="font-size:7pt;font-weight:300;line-height:1.3;margin-top:2.4mm">Janelas e chuveiros: cadernos de esquadrias e hidráulica.
                As alturas das janelas serão revistas (mais baixas) e não interferem no forro. <b style="font-weight:600">Se o box for fechado até o teto</b>,
                o vapor fica confinado junto ao forro: consultar o fabricante antes de manter a placa RU sobre o box.</div>''')

    itens = [
        (1, 'Parede', 'Alvenaria existente/projeto.', 'doc'),
        (2, 'Revestimento cerâmico até o forro', 'B.I. total nos banhos, conforme corte AA do DWG.', 'doc'),
        (3, 'Tabica / perfil perimetral', 'Junta aberta (negativo) entre forro e revestimento, largura conforme modelo da tabica (ver D1).', 'prop'),
        (4, 'Forro em placa RU (verde)', 'Juntas e massa próprias para áreas úmidas, conforme fabricante.', 'doc'),
        (5, 'Estrutura e pendurais', 'Aço galvanizado; espaçamentos para placa RU conforme manual do fabricante.', 'pend'),
        (6, 'Luminária embutida L01/L02', 'Peça com grau de proteção adequado a área molhada (a confirmar na ficha técnica).', 'pend'),
        (7, 'Vapor do banho', 'Ventilar após o uso; forro RU tolera umidade eventual, não água.', 'doc'),
    ]
    pill = {'doc': '<span class="pill doc">DOC</span>', 'prop': '<span class="pill prop">PROPOSTA</span>',
            'pend': '<span class="pill pend">A DEFINIR</span>'}
    lista = ''.join(f'<tr><td style="width:6mm"><b style="display:inline-flex;width:4.4mm;height:4.4mm;border-radius:50%;background:#22251a;color:#fff;align-items:center;justify-content:center;font-size:6.4pt;font-family:Outfit">{n}</b></td>'
                    f'<td><b style="font-weight:600">{t}</b><span class="s">{d}</span></td><td style="text-align:right">{pill[k]}</td></tr>'
                    for n, t, d, k in itens)
    q1 = box(438, 12, 146, 122, 'b-creme', 'Componentes', 'QUADRO 1', f'<table>{lista}</table>')
    ru = f'''<div style="margin-top:3.5mm;font-family:Outfit;font-weight:800;font-size:15pt;line-height:1.1">
      Resistente à umidade<br><span style="opacity:.75">não é impermeável.</span></div>
      <div class="obs small" style="margin-top:2.6mm">
      <div class="i"><span class="t" style="color:{C['creme']}">O que a placa RU faz</span><p>Absorve menos água que a placa comum e suporta a umidade do ar
      do banho, de forma intermitente, em ambiente ventilado.</p></div>
      <div class="i"><span class="t" style="color:{C['creme']}">O que ela não faz</span><p>Não resiste a água corrente, jato, respingo direto nem vazamento.
      Não é barreira de água e não substitui impermeabilização.</p></div>
      <div class="i"><span class="t" style="color:{C['creme']}">Condições para usar</span><p>Uso interno · ventilação natural ou mecânica · sem contato direto
      com água · sem vapor contínuo (sauna, ofurô fechado) · pintura própria para áreas úmidas · tratamento de juntas com produtos
      para RU. Confirmar cada item no manual do fabricante escolhido.</p></div>
      <div class="i"><span class="t" style="color:{C['creme']}">Uso e manutenção</span><p>Manter a janela ou o exaustor em uso após o banho.
      Vazamento no entreforro (hidráulica ou dreno) deve ser corrigido e a placa atingida substituída.</p></div></div>'''
    q2 = box(438, 138, 146, 185, 'b-rust', 'Placa RU', 'QUADRO 2', ru)
    extra = adequ + q1 + q2 + carimbo(438, 327, 146, 83, 'Banheiros · RU', '1:25 · 1:10', 4, TOTAL) + \
        titulo(236, 381, '04', 'Banheiros · placa RU', 'Forro de gesso em placa resistente à umidade (verde) nos 4 banhos · decisão de projeto')
    return pagina(str(v), extra)
