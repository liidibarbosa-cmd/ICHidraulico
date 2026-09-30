# -*- coding: utf-8 -*-
"""Prancha 01 — Planta de forro (1:75)."""
from base import *
from dados_forro import *

ESC = 75
PL = Planta(ESC, ox=43.6, oy=26.0)


def _poly_room(a):
    if 'rect' in a:
        x0, y0, x1, y1 = a['rect']
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return a['poly']


def fill_ambientes(v, pl, amb=AMB, sw=0.0):
    for a in amb:
        pts = [pl.P(*p) for p in _poly_room(a)]
        f = {'RU': 'url(#hRU)', 'RUp': 'url(#hRUp)', 'ST': C['st']}[a['placa']]
        v.poly(pts, fill=f)
        if a['placa'] == 'RUp':
            v.poly(pts, stroke=C['prop'], sw=0.3, dash='1.4 0.9')


def rotulo_amb(v, pl, a, s=1.0, cota_h=True):
    x, y = pl.P(*a['lab'])
    v.text(x, y, a['nome'], size=6.0 * s, weight=700, ls=0.2)
    y2 = y + 2.0 * s
    # etiqueta de nível
    w, h = 17.5 * s, 5.4 * s
    v.rect(x - w / 2, y2, w, h, fill='#fff', stroke=C['ink'], sw=0.22, rx=1.0)
    v.text(x, y2 + 2.45 * s, f'FORRO +{br(a["h"])}', size=5.6 * s, weight=800, family='Outfit')
    v.text(x, y2 + 4.55 * s, f'laje +{br(a["laje"])} · entref. {int(round((a["laje"]-a["h"])*100))} cm', size=3.9 * s, weight=500, cor=C['muted'])
    pl_txt = {'RU': 'placa RU', 'RUp': 'placa RU · proposta', 'ST': 'placa ST'}[a['placa']]
    cor = C['ru_txt'] if a['placa'] != 'ST' else C['muted']
    v.text(x, y2 + h + 2.3 * s, pl_txt, size=4.6 * s, weight=700 if a['placa'] != 'ST' else 500, cor=cor)


def cortineiros(v, pl, cts=CORTINEIROS, eixo=True):
    for ct in cts:
        for (x0, y0, x1, y1) in ct['faixas']:
            a, b = pl.P(x0, y0), pl.P(x1, y1)
            v.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=C['cort_fill'], stroke=C['cort_line'], sw=0.3)
            if eixo:
                if (x1 - x0) < (y1 - y0):
                    xm = (a[0] + b[0]) / 2
                    v.line(xm, a[1], xm, b[1], C['luz'], 0.45, dash='2.2 0.8')
                else:
                    ym = (a[1] + b[1]) / 2
                    v.line(a[0], ym, b[0], ym, C['luz'], 0.45, dash='2.2 0.8')


def rasgo(v, pl, r=RASGO):
    a, b = pl.P(r['x0'], r['y0']), pl.P(r['x1'], r['y1'])
    v.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=C['cort_fill'], stroke=C['cort_line'], sw=0.3)
    xm = (a[0] + b[0]) / 2
    v.line(xm, a[1], xm, b[1], C['luz'], 0.45)


def luminarias(v, pl, s=0.8, rot=True, clip=None):
    for o in LUM['pontuais']:
        if clip and not (clip[0] <= o['x'] <= clip[2] and clip[1] <= o['y'] <= clip[3]):
            continue
        x, y = pl.P(o['x'], o['y'])
        lum_simbolo(v, x, y, o['code'], s=s, rotulo=rot)
    for o in LUM['lineares']:
        pts = [pl.P(*p) for p in o['pts']]
        if clip and not all(clip[0] - 0.1 <= p[0] <= clip[2] + 0.1 and clip[1] - 0.1 <= p[1] <= clip[3] + 0.1 for p in o['pts']):
            continue
        v.poly(pts, stroke='#9b9788', sw=0.55, close=False)
        for p in (pts[0], pts[-1]):
            v.circle(*p, 0.35, fill='#9b9788')
        if rot:
            v.text(pts[0][0] + 1.0, pts[0][1] - 1.1, 'L07', size=4.2, weight=700, cor='#9b9788', anchor='start')


def cassete(v, pl, lado=0.70, rot=True):
    e = LUM['E1']
    a = pl.P(e['x'] - lado / 2, e['y'] - lado / 2)
    L = pl.mm(lado)
    v.rect(a[0], a[1], L, L, fill='#fff', stroke='#6f6c60', sw=0.25, dash='1.2 0.7')
    v.rect(a[0] + L * 0.3, a[1] + L * 0.3, L * 0.4, L * 0.4, stroke='#6f6c60', sw=0.18)
    if rot:
        v.text(a[0] + L / 2, a[1] + L + 2.6, 'E1 · cassete', size=4.4, weight=700, cor='#6f6c60')


def alcapoes(v, pl):
    for al in ALCAPOES:
        a = pl.P(al['x'] - al['lado'] / 2, al['y'] - al['lado'] / 2)
        L = pl.mm(al['lado'])
        v.rect(a[0], a[1], L, L, fill='#fff', stroke=C['prop'], sw=0.3)
        v.line(a[0], a[1], a[0] + L, a[1] + L, C['prop'], 0.2)
        v.line(a[0] + L, a[1], a[0], a[1] + L, C['prop'], 0.2)


def esquema_niveis(v, x, y_piso, esc=60):
    """Esquema de níveis (corte esquemático) — escala vertical 1:60, horizontal sem escala."""
    k = 1000 / esc
    Z = lambda z: y_piso - z * k
    # piso
    v.line(x, Z(0), x + 222, Z(0), C['ink'], 0.4)
    v.text(x + 223, Z(0) + 1.1, '±0,00 piso acabado', size=5.8, weight=600, anchor='start')
    # ala íntima / serviço
    xa0, xa1 = x + 6, x + 104
    xb0, xb1 = x + 116, x + 214
    for (x0, x1, fz, lz, nome) in ((xa0, xa1, FORRO_ALA, LAJE_ALA, 'Suítes · closet · home office · banhos · circulação · cozinha · A.S. · despensa'),
                                   (xb0, xb1, FORRO_ESTAR, LAJE_ESTAR, 'Estar / jantar')):
        v.rect(x0 - 3, Z(lz) - 0.16 * k, (x1 - x0) + 6, 0.16 * k, fill='url(#hLaje)', stroke=C['ink'], sw=0.25)
        v.rect(x0 - 3, Z(lz + 0.16), 3, Z(0) - Z(lz + 0.16), fill='url(#hAlv)', stroke=C['ink'], sw=0.2)
        v.rect(x1, Z(lz + 0.16), 3, Z(0) - Z(lz + 0.16), fill='url(#hAlv)', stroke=C['ink'], sw=0.2)
        # forro com cortineiro na parede direita
        cw = CORT_LARG * k * 1.0
        v.rect(x0, Z(fz), (x1 - x0) - cw - 0.5, 0.9, fill='url(#hGesso)', stroke=C['ink'], sw=0.2)
        # testeira do cortineiro
        tx = x1 - cw - 0.5
        v.rect(tx, Z(lz), 0.6, Z(fz) - Z(lz) + 0.9, fill=C['gesso'], stroke=C['ink'], sw=0.2)
        # cortina esquemática
        v.path(f'M{x1-cw*0.45:.2f},{Z(lz)+0.8:.2f} ' + ' '.join(f'Q{x1-cw*0.45+(0.7 if i%2 else -0.7):.2f},{Z(lz)+0.8+(i+0.5)*4:.2f} {x1-cw*0.45:.2f},{Z(lz)+0.8+(i+1)*4:.2f}' for i in range(int((Z(0)-Z(lz)-1.5)/4))),
               stroke=C['grey'], sw=0.25)
        # luz
        v.poly([(tx - 0.2, Z(lz) + 0.8), (x1 - cw * 0.2, Z(lz) + 0.8), (x1 - cw * 0.2, Z(fz) + 10)], fill='url(#gLuz)')
        v.circle(tx - 0.8, Z(lz) + 1.2, 0.7, fill=C['luz'])
        # cotas de nível
        for z, t, lado in ((fz, f'+{br(fz)} forro', 0), (lz, f'+{br(lz)} fundo da laje', 1)):
            yy = Z(z) + (0.9 if lado == 0 else 0)
            v.line(x0 + 8, yy, x0 + 8, yy + (2.0 if lado == 0 else -2.0), C['rust'], 0.25)
            v.poly([(x0 + 6.8, yy + (1.6 if lado == 0 else -1.6)), (x0 + 9.2, yy + (1.6 if lado == 0 else -1.6)), (x0 + 8, yy)], fill=C['rust'])
            v.text(x0 + 10.5, yy + (3.0 if lado == 0 else -1.0), t, size=5.8, weight=700, cor=C['rust'], anchor='start')
        v.text((x0 + x1) / 2 - 4, Z(0) - 4.0, nome, size=5.2, weight=600, cor=C['muted'])
        # entreforro
        v.cota(x0 + 44, Z(lz), x0 + 44, Z(fz), off=0, txt=f'{int(round((lz-fz)*100))} cm', size=5.4, ext=False)
        v.text(x0 + 48, (Z(lz) + Z(fz)) / 2 + 1, 'entreforro', size=5.2, weight=400, anchor='start', cor=C['muted'])
        v.text(x1 - cw / 2 - 0.3, Z(fz) + 7.5, 'cortineiro', size=4.6, weight=600, anchor='end', cor=C['luz'])
        v.text(x1 - cw / 2 - 0.3, Z(fz) + 9.6, '20 cm', size=4.6, weight=600, anchor='end', cor=C['luz'])


def prancha():
    v = SVG()
    pl = PL
    fill_ambientes(v, pl)
    # áreas externas (sem forro)
    for e in EXTERNAS:
        x, y = pl.P(*e['pos'])
        v.text(x, y, e['nome'], size=5.4, weight=600, cor='#a9a594')
        v.text(x, y + 2.3, 'área externa · sem forro de gesso', size=4.4, weight=400, cor='#a9a594')
        v.text(x, y + 4.3, 'revestimento a detalhar', size=4.4, weight=400, cor='#a9a594')
    paredes(v, pl)
    luminarias(v, pl, s=0.72)
    cassete(v, pl)
    cortineiros(v, pl)
    rasgo(v, pl)
    alcapoes(v, pl)
    for a in AMB:
        rotulo_amb(v, pl, a, s=0.78 if a['id'] == 'CIR' else 0.95)

    # ---------------- cotas gerais dos ambientes (faces internas)
    P = pl.P
    ct = lambda x1, y1, x2, y2, off, lado=1, t=None, **kw: v.cota(*P(x1, y1), *P(x2, y2), off=off, lado=lado, txt=t or br(round(((x2-x1)**2+(y2-y1)**2)**0.5/0.05)*0.05), size=5.4, **kw)
    # topo (externo, acima da planta)
    for (x0, x1) in ((1.08, 3.03), (3.18, 6.68), (6.83, 11.28)):
        ct(x0, 0.15, x1, 0.15, off=7.5, lado=1)
    ct(11.28, 0.15, 11.48, 0.15, off=7.5, lado=1, t='0,20', tcor=C['luz'])
    # lateral esquerda
    for (y0, y1) in ((0.15, 3.65), (3.80, 6.81), (6.95, 8.45), (8.60, 10.10), (10.25, 13.25), (13.40, 17.60), (17.75, 19.75)):
        xx = 1.08 if y1 <= 3.7 else (2.58 if (y0 < 6.9 or y0 > 10.2) else 3.18)
        ct(xx, y1, xx, y0, off=9.0 + (1.08 - xx) * 13.33 * 0 if xx == 1.08 else 9.0, lado=1)
    # larguras internas
    ct(2.58, 4.25, 6.68, 4.25, off=0, ext=False)
    ct(2.58, 10.70, 6.68, 10.70, off=0, ext=False)
    ct(3.18, 7.35, 5.99, 7.35, off=0, ext=False)
    ct(3.18, 9.70, 5.99, 9.70, off=0, ext=False)
    ct(2.58, 16.95, 6.83, 16.95, off=0, ext=False)
    ct(2.58, 18.15, 5.34, 18.15, off=0, ext=False)
    ct(5.49, 18.15, 6.68, 18.15, off=0, ext=False, t='1,20')
    ct(8.18, 4.25, 11.48, 4.25, off=0, ext=False)
    ct(8.63, 3.80, 8.63, 6.00, off=0, ext=False)
    ct(8.63, 6.16, 8.63, 7.55, off=0, ext=False, t='1,40')
    # suíte master: profundidade
    ct(7.30, 0.15, 7.30, 3.65, off=0, ext=False)
    # circulação
    ct(6.83, 12.02, 8.04, 12.02, off=0, ext=False, t='1,20')
    # estar: 1,75 + 3,50 (cortineiro) no topo; 8,00 à direita
    ct(6.83, 12.35, 8.58, 12.35, off=-5.2, lado=1)
    ct(8.58, 12.35, 12.08, 12.35, off=-5.2, lado=1, tcor=C['luz'])
    ct(12.08, 12.35, 12.08, 20.35, off=-9.0, lado=1)
    ct(11.88, 20.35, 12.08, 20.35, off=-4.5, lado=1, t='0,20', tcor=C['luz'])
    ct(6.83, 19.45, 12.08, 19.45, off=0, ext=False, t='5,25')
    ct(8.48, 20.35, 12.08, 20.35, off=-4.5, lado=1, t='3,60')
    # suíte master cortineiro 3,50 (externo à direita)
    ct(11.48, 0.15, 11.48, 3.65, off=-9.0, lado=1)

    # ---------------- rotulos de cortineiros / rasgo (à direita)
    def nota(xm, ym, xt, yt, linhas, cor=C['ink'], tag=None, tagk='doc'):
        v.seta_nota(xm, ym, xt - 1.2, yt - 1.0, cor)
        v.line(xt - 1.2, yt - 1.0, xt + 24, yt - 1.0, cor, 0.2)
        for i, (s, sz, wt, cc) in enumerate(linhas):
            v.text(xt, yt + 2.6 + i * 2.9, s, size=sz, weight=wt, cor=cc, anchor='start')
        if tag:
            v.tag(xt + 0.2, yt - 3.4, tag, tagk, anchor='start')

    xa, ya = P(11.38, 1.0)
    nota(xa, ya, 236, 36, [('CT1 · CORTINEIRO ILUMINADO', 6.2, 800, C['ink']),
                           ('vão livre 20 cm · 3,50 m (parede inteira)', 5.3, 500, C['ink']),
                           ('luz L08 · fita LED — modelo a definir', 5.3, 400, C['muted']),
                           ('ver cortes C1 · prancha 02', 5.3, 600, C['rust'])], tag='DOCUMENTADO', tagk='doc')
    xa, ya = P(11.98, 14.2)
    nota(xa, ya, 236, 196, [('CT2 · CORTINEIRO ILUMINADO', 6.2, 800, C['ink']),
                            ('vão livre 20 cm · em L: 3,50 + 8,00 m', 5.3, 500, C['ink']),
                            ('luz L09 · Tuboled — modelo a definir', 5.3, 400, C['muted']),
                            ('ver corte C2 · prancha 02', 5.3, 600, C['rust'])], tag='DOCUMENTADO', tagk='doc')
    xa, ya = P((RASGO['x0'] + RASGO['x1']) / 2, 5.6)
    nota(xa, ya, 236, 104, [('RG1 · RASGO DE LUZ (luz para baixo)', 6.2, 800, C['ink']),
                            ('12 cm × 8,20 m · a 15 cm da parede', 5.3, 500, C['ink']),
                            ('luz L10 · Tuboled — modelo a definir', 5.3, 400, C['muted']),
                            ('ver cortes R1 · R2 · prancha 03', 5.3, 600, C['rust'])], tag='PROPOSTA', tagk='prop')
    xa, ya = P(LUM['E1']['x'] + 0.35, LUM['E1']['y'])
    nota(xa, ya, 236, 248, [('E1 · CASSETE DE AR-CONDICIONADO', 6.2, 800, C['ink']),
                            ('1,80 m da parede lateral · 3,95 m da superior', 5.3, 500, C['ink']),
                            ('abertura e fixação: ver D5 · prancha 05', 5.3, 600, C['rust'])], tag='DOCUMENTADO', tagk='doc')
    xa, ya = P(ALCAPOES[0]['x'] + 0.2, ALCAPOES[0]['y'])
    nota(xa, ya, 236, 132, [('AL1 · ALÇAPÃO DE INSPEÇÃO', 6.2, 800, C['ink']),
                            ('para a fonte do rasgo, se houver', 5.3, 500, C['ink']),
                            ('ver D7 · prancha 05', 5.3, 600, C['rust'])], tag='PROPOSTA', tagk='prop')

    # ---------------- marcas de corte e chamadas
    v.corte_marca(*P(10.55, 1.25), *P(12.35, 1.25), 'C1', '02', lado=-1)
    v.corte_marca(*P(11.0, 17.9), *P(12.8, 17.9), 'C2', '02', lado=-1)
    v.corte_marca(*P(6.30, 5.0), *P(8.60, 5.0), 'R1', '03', lado=-1)
    v.chamada(*P(12.55, 12.0), 'C3', '02')
    v.chamada(*P(8.58, 11.85), 'C4', '02')
    v.chamada(*P(7.45, 12.55), 'R2', '03')
    v.chamada(*P(5.1, 15.2), 'D4', '05')
    v.chamada(*P(10.28, 15.25), 'D5', '05')
    v.chamada(*P(9.05, 13.85), 'D6', '05')
    v.chamada(*P(6.35, 13.80), 'D2', '05')
    v.chamada(*P(3.95, 1.0), 'D1', '05')
    v.chamada(*P(5.55, 4.60), 'D3', '05')
    v.chamada(*P(7.10, 11.25), 'D7', '05')
    for a in AMB:
        if a['placa'] == 'RU':
            x0, y0, x1, y1 = a['rect']
            pos = (x0 + 0.36, (y0 + y1) / 2) if a['id'] in ('BS1', 'BS2') else (x1 - 0.30, y0 + 0.32)
            v.chamada(*P(*pos), 'B', '04', cor=C['ru_txt'])

    # norte / orientação igual ao caderno de iluminação — sem norte no original: não indicar
    # ---------------- esquema de níveis
    v.text(14, 305.5, 'ESQUEMA DE NÍVEIS', size=7.0, weight=800, ls=1.2, anchor='start')
    v.text(14, 309.0, 'corte esquemático · alturas do piso acabado ao forro e ao fundo da laje (DWG) · vertical 1:60, horizontal sem escala',
           size=5.6, weight=400, cor=C['muted'], anchor='start')
    esquema_niveis(v, 14, 377)

    escala_grafica(v, 14, 404.5, ESC, 8, [0, 1, 2, 3, 4, 6, 8])

    # ---------------------------------------------------------------- quadros
    linhas = ''
    for a in AMB:
        pl_txt = {'RU': '<b style="color:#3f6e31">RU</b>', 'RUp': '<b style="color:#3f6e31">RU</b> <span class="pill prop">PROPOSTA</span>', 'ST': 'ST'}[a['placa']]
        linhas += (f'<tr><td>{a["nome"].title().replace("Suíte","Suíte").replace("A.s.","A.S.")}</td><td>{pl_txt}</td>'
                   f'<td class="n"><b>{br(a["h"])}</b></td><td class="n">{br(a["laje"])}</td>'
                   f'<td class="n">{int(round((a["laje"]-a["h"])*100))} cm</td><td class="n">{br(a["area"])}</td></tr>')
    q1 = box(290, 12, 140, 241, 'b-creme', 'Ambientes e níveis', 'QUADRO 1',
             f'''<table><tr><th>AMBIENTE</th><th>PLACA</th><th style="text-align:right">FORRO</th><th style="text-align:right">LAJE</th>
             <th style="text-align:right">ENTREF.</th><th style="text-align:right">ÁREA m²</th></tr>{linhas}</table>
             <div style="font-size:6.8pt;font-weight:300;margin-top:2mm;line-height:1.3">Alturas em metros a partir do piso acabado.
             Forro e área: planta de forro de gesso do DWG. Laje: cortes AA e BB do DWG. <b style="font-weight:600">Placa RU</b> nos banhos:
             DWG. <b style="font-weight:600">RU na cozinha e na A.S.</b>: proposta desta revisão. <b style="font-weight:600">ST</b> nos demais:
             placa padrão para ambientes secos, proposta.</div>
             <table style="margin-top:3.2mm"><tr><th>ELEMENTO</th><th>VÃO</th><th style="text-align:right">COMPR.</th><th>STATUS</th></tr>
             <tr><td><b>CT1</b> cortineiro · suíte master<span class="s">L08 fita LED · modelo a definir</span></td><td>20 cm</td><td class="n">3,50 m</td><td><span class="pill doc">DOC</span></td></tr>
             <tr><td><b>CT2</b> cortineiro · estar/jantar<span class="s">L09 Tuboled · modelo a definir</span></td><td>20 cm</td><td class="n">3,50 + 8,00 m</td><td><span class="pill doc">DOC</span></td></tr>
             <tr><td><b>RG1</b> rasgo · circulação<span class="s">L10 Tuboled · modelo a definir</span></td><td>12 cm</td><td class="n">8,20 m</td><td><span class="pill prop">PROPOSTA</span></td></tr>
             </table>''')

    def LS(inner):
        return leg_svg(inner)
    leg = f'''<div class="leg">
      {LS('<rect x="1" y="1" width="13" height="4.2" fill="#fbf8f1" stroke="#22251a" stroke-width=".2"/>')}<div>Forro de gesso · placa ST<span class="s">ambientes secos</span></div>
      {LS('<rect x="1" y="1" width="13" height="4.2" fill="url(#hRU)" stroke="#22251a" stroke-width=".2"/>')}<div>Forro de gesso · placa RU (verde)<span class="s">banhos · documentado</span></div>
      {LS('<rect x="1" y="1" width="13" height="4.2" fill="url(#hRUp)" stroke="#903f2a" stroke-width=".3" stroke-dasharray="1.4 .9"/>')}<div>Placa RU proposta<span class="s">cozinha e A.S. · aguarda aprovação</span></div>
      {LS('<rect x="1" y="2" width="13" height="2.2" fill="#fae5b6" stroke="#eda80d" stroke-width=".3"/><line x1="1" y1="3.1" x2="14" y2="3.1" stroke="#cc7300" stroke-width=".45" stroke-dasharray="2.2 .8"/>')}<div>Cortineiro iluminado · vão 20 cm<span class="s">faixa = vão no forro · traço = fonte de luz</span></div>
      {LS('<rect x="1" y="2.3" width="13" height="1.6" fill="#fae5b6" stroke="#eda80d" stroke-width=".3"/><line x1="1" y1="3.1" x2="14" y2="3.1" stroke="#cc7300" stroke-width=".45"/>')}<div>Rasgo de luz · luz para baixo<span class="s">faixa = rasgo · linha = fonte de luz</span></div>
      {LS('<rect x="1" y="0" width="13" height="6.2" fill="#fff"/><circle cx="4" cy="3.1" r="1.1" fill="#f1efe8" stroke="#9b9788" stroke-width=".15"/><rect x="3.3" y="2.8" width="1.4" height=".6" fill="#9b9788"/><rect x="8.3" y="1.9" width="2.4" height="2.4" fill="#f1efe8" stroke="#9b9788" stroke-width=".18"/><line x1="11.5" y1="3.1" x2="14" y2="3.1" stroke="#9b9788" stroke-width=".55"/>')}<div>Luminárias · posição indicativa<span class="s">códigos do caderno de iluminação · sem locação</span></div>
      {LS('<rect x="4.5" y=".8" width="4.6" height="4.6" fill="#fff" stroke="#6f6c60" stroke-width=".25" stroke-dasharray="1.2 .7"/>')}<div>Cassete de ar-condicionado E1<span class="s">posição do caderno de tomadas R05</span></div>
      {LS('<rect x="5" y="1" width="4.2" height="4.2" fill="#fff" stroke="#903f2a" stroke-width=".3"/><line x1="5" y1="1" x2="9.2" y2="5.2" stroke="#903f2a" stroke-width=".2"/><line x1="9.2" y1="1" x2="5" y2="5.2" stroke="#903f2a" stroke-width=".2"/>')}<div>Alçapão de inspeção<span class="s">proposta</span></div>
      {LS('<circle cx="7.5" cy="3.1" r="2.8" fill="#fff" stroke="#903f2a" stroke-width=".3"/><line x1="4.9" y1="3.1" x2="10.1" y2="3.1" stroke="#903f2a" stroke-width=".22"/><text x="7.5" y="2.6" font-size="1.8" font-family="Outfit" font-weight="800" fill="#903f2a" text-anchor="middle">D1</text><text x="7.5" y="5.1" font-size="1.5" font-family="Manrope" font-weight="600" fill="#903f2a" text-anchor="middle">05</text>')}<div>Chamada de detalhe<span class="s">código / prancha</span></div>
      {LS('<line x1="1" y1="3.1" x2="14" y2="3.1" stroke="#999b87" stroke-width=".18"/><circle cx="1.5" cy="3.1" r=".45" fill="#999b87"/><circle cx="13.5" cy="3.1" r=".45" fill="#999b87"/><text x="7.5" y="2.2" font-size="1.9" font-weight="600" text-anchor="middle" font-family="Manrope">3,50</text>')}<div>Cota em metros<span class="s">faces internas acabadas</span></div>
    </div>
    <div style="margin-top:3mm;display:flex;gap:1.6mm;align-items:center;font-size:7pt"><span class="pill doc">DOCUMENTADO</span> dado dos arquivos &nbsp; <span class="pill prop">PROPOSTA</span> aguarda aprovação</div>'''
    q2 = box(290, 258, 140, 152, 'b-rust', 'Legenda', 'QUADRO 2', leg)

    obs = [
        ('1. Base', 'Planta de forro de gesso e cortes AA/BB do DWG “Projeto Ivan e Ana R01”; caderno de iluminação 02/04 R01; tomadas 01/04 R05; esquadrias R01.'),
        ('2. Área do forro', 'Somente ambientes internos. Garagem, varanda gourmet e beirais recebem outro revestimento, a detalhar em caderno próprio.'),
        ('3. Cortineiros (CT1, CT2)', 'Vão livre de 20 cm (decisão de 30/09/2026), medido da parede acabada à face interna da testeira. Comprimentos gerais do DWG. Tipo de cortina, trilho e fonte de luz a definir com os fornecedores.'),
        ('4. Rasgo (RG1)', 'Luz voltada para baixo, reforçando a iluminação geral da circulação. Posição, largura e extremidades são proposta; ajustar ao Tuboled escolhido.'),
        ('5. Luminárias', 'Símbolos só indicam tipo e quantidade de recortes. Locação conforme caderno de iluminação e marcação em obra.'),
        ('6. Banhos', 'Placa RU (verde) resiste à umidade, mas não é impermeável. Ver prancha 04.'),
        ('7. Entreforro de 15 cm', 'Nas alas íntima e de serviço há só 15 cm entre forro e laje. Conferir a altura de embutimento de L05, L07 e das fontes antes de comprar.'),
        ('8. Compatibilizar', 'Cassete E1 (entreforro 30 cm × manual Gree); hi-walls E2 a E6 acima das portas; duto da coifa; linhas frigorígenas e dreno. Executar o forro após testes das instalações do entreforro.'),
        ('9. Especificação do sistema', 'Espessura das placas, perfis, pendurais, fixações e espaçamentos conforme manual do fabricante escolhido e ABNT NBR 15758-2. Ver prancha 06.'),
        ('10. Pendências', 'Fabricante de referência; modelos da fita LED e do Tuboled; tipo de cortina e trilho; box dos banhos (até o teto?); aprovação das propostas marcadas.'),
    ]
    q3 = box(438, 12, 146, 310, 'b-bege', 'Observações', 'QUADRO 3',
             '<div class="obs">' + ''.join(f'<div class="i"><span class="t">{t}</span><p>{p}</p></div>' for t, p in obs) + '</div>')
    extra = q1 + q2 + q3 + carimbo(438, 327, 146, 83, 'Forro de gesso', '1:75 · folha A2', 1, TOTAL) + \
        titulo(14, 381, '01', 'Planta de forro', 'Escala 1:75 · plotagem em A2 · cotas em metros · faces internas acabadas · conferir as medidas no local')
    return pagina(str(v), extra)
