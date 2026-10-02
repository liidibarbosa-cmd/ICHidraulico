# -*- coding: utf-8 -*-
"""Caderno de areas molhadas (A3 retrato) - elementos de folha no padrao dos cadernos A3 do
escritorio (Revestimentos de parede/piso R00): fundo claro, cabecalho espacado em terracota,
titulo Aloevera, painel de notas creme e carimbo oliva no rodape."""
import os
from svgkit import *
from svgkit import _font
from planta import *
import dados_pontos as D
import pranchas as PR
import gas as G                       # registra o tipo GAS e o ponto do fogao (PG1)

W3, H3 = 841.89, 1190.55
FUNDO = '#f7f2e8'
PAPEL = '#fbf8f1'
REV = 'R00'
DATA = '02/10/2026'
TOTAL = 9
CAB = 'ÁREAS MOLHADAS · CADERNO DE DETALHAMENTO · REVISÃO 00'
ML, MR = 28.3, 813.6                  # margens
NOTAS = (28.5, 941.2, 479.2, 1162.5)
CARIMBO = (495.8, 941.2, 813.8, 1162.5)
K25, K50, K100 = 1000 / 25 * MM, 1000 / 50 * MM, 1000 / 100 * MM

# revestimentos (Caderno de revestimentos de parede 02/02 R00, legenda)
RP = {
    'RP02': ('#a78a5c', 'Porcelanato Santorini OFW NAT', 'Portinari'),
    'RP03': ('#8f8779', 'Porcelanato Confete WH NAT', 'Ceusa · cód. 5041209A'),
    'RP04': ('#b46f61', 'Porcelanato Confete PK NAT (Pink)', 'Ceusa · cód. 5041210A'),
    'RP05': ('#6a6f41', 'Revestimento Fatto Oliva AC', 'Decortiles · SC 8068139'),
    'RP06': ('#8b6d4a', 'Travertino Rock Face', 'Pedreira (compra à parte)'),
    'RP07': ('#5e6a6f', 'Cerâmica simples (fundo da marcenaria)', 'Eliane · SC 8039383'),
}
def tint(cor, f=0.32):
    r, g, b = int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16)
    m = lambda c: int(round(255 - (255 - c) * f))
    return '#%02x%02x%02x' % (m(r), m(g), m(b))

# status (mesma ideia dos marcadores do caderno de forro)
ST = {
    'D': ('DOCUMENTADO', '#dfe3cf', OLIVA, None),
    'P': ('PROPOSTA', '#ffffff', TERRA, TERRA),
    'A': ('A DEFINIR', TERRA, CREME, None),
    'C': ('A CONFIRMAR', '#ecc9bb', '#6b2e1f', None),
}

class Svg3(Svg):
    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                'width="297mm" height="420mm" viewBox="0 0 %.2f %.2f"><defs>%s</defs>%s</svg>'
                % (W3, H3, ''.join(self.defs), '\n'.join(self.p)))

_ALOE = None
def aloe_ok(txt):
    global _ALOE
    if _ALOE is None: _ALOE = _font('aloe')[0]
    return all(ord(c) in _ALOE or c == ' ' for c in txt)

def taloe(s, x, y, txt, tam, cor=TINTA, anc='start'):
    """titulo em Aloevera; se faltar glifo na fonte reconstruida, Manrope 700."""
    if aloe_ok(txt): s.text(x, y, txt, tam, 'aloe', cor, anc=anc)
    else: s.text(x, y, txt, tam * 0.92, 700, cor, anc=anc)

def caps(s, x, y, txt, tam=6.5, cor=TERRA, anc='start', ls=2.0, peso=600):
    s.text(x, y, txt.upper(), tam, peso, cor, anc=anc, ls=ls)

def folha(titulo):
    s = Svg3()
    s.rect(0, 0, W3, H3, fill=FUNDO)
    caps(s, ML, 35.5, CAB, 6.5, TERRA, ls=2.2)
    taloe(s, ML, 66, titulo, 25.5)
    return s

def chip(s, x, y, st, tam=4.9, anc='start'):
    txt, fundo, cor, borda = ST[st]
    w = largura(txt, tam, 700, 0.5) + 7
    x0 = x if anc == 'start' else (x - w if anc == 'end' else x - w / 2)
    s.rect(x0, y - tam - 1.6, w, tam + 4.2, fill=fundo, stroke=borda or 'none', sw=0.6 if borda else 0, rx=(tam + 4.2) / 2)
    s.text(x0 + w / 2, y, txt, tam, 700, cor, anc='middle', ls=0.5)
    return x0 + w

def titulo(s, x, y, cod, tit, sub=None):
    w = max(largura(cod, 5.8, 700) + 8, 18)
    s.rect(x, y - 9.4, w, 12.4, fill=OLIVA, rx=3)
    s.text(x + w / 2, y - 0.9, cod, 5.8, 700, CREME, anc='middle')
    taloe(s, x + w + 6, y + 1.2, tit, 11.5)
    if sub: s.text(x + w + 6, y + 11.6, sub, 6.4, 400, COTA_TXT)

def carimbo3(s, n, tipo, escala):
    x0, y0, x1, y1 = CARIMBO
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=OLIVA, rx=16)
    s.image(510.2, 950.5, 92, 17.5, PR.LOGO)
    caps(s, 799.4, 961, 'Folha', 5.7, CREME, anc='end', ls=1.6)
    s.text(799.4, 991, '%02d/%02d' % (n, TOTAL), 24, 600, CREME, anc='end')
    caps(s, 510.2, 1001.5, 'Tipo', 5.7, CREME, ls=1.6)
    taloe(s, 510.2, 1021.5, tipo, 15.3, CREME)
    def campo(x, y, rot, *vals):
        caps(s, x, y, rot, 5.7, CREME, ls=0.8)
        for i, v in enumerate(vals): s.text(x, y + 8.6 + i * 9.7, v, 7.1, 400, CREME)
    campo(510.2, 1039.6, 'Obra', 'Residência Ivan e Ana Neris · casa unifamiliar térrea')
    campo(510.2, 1062.6, 'Clientes', 'Ivan e Ana Neris')
    campo(660.5, 1062.6, 'Endereço', 'Nova Odessa, SP')
    campo(510.2, 1085.0, 'Arq. responsável', 'Lidiane Barbosa', 'CAU A290220-6')
    campo(660.5, 1085.0, 'Arq. corresponsável', 'Isadora Ferrari', 'CAU A263982-8')
    campo(510.2, 1117.3, 'Data', DATA)
    campo(660.5, 1117.3, 'Revisão', 'Nº 00')
    campo(696.8, 1117.3, 'Escala', escala)
    s.rect(510.7, 1137.8, 288.8, 19.4, fill=TERRA, rx=9.7)
    caps(s, 655.1, 1150.0, 'Conferir as medidas no local', 6.5, CREME, anc='middle', ls=1.0)

def notas(s, itens, titulo='Notas', escala=None, colw=None, status_leg=True):
    """itens: lista de (tag, texto, status|None). Duas colunas, a 2a comeca quando a 1a enche."""
    x0, y0, x1, y1 = NOTAS
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=CREME, rx=16)
    caps(s, 50.9, 962.5, titulo, 6.5, TERRA, ls=2.0, peso=700)
    cols = [(49.6, 92.0, 150), (266.0, 308.5, 152)]
    ylim = 1112 if (escala or status_leg) else 1150
    ci, y = 0, 980.0
    for tag, txt, st in itens:
        cx, tx, tw = cols[ci]
        linhas = quebrar(txt, tw, 6.4, 400)
        h = max(len(linhas) * 8.8, 18 if st else 9) + 5
        if y + h > ylim and ci == 0:
            ci, y = 1, 980.0; cx, tx, tw = cols[ci]
            linhas = quebrar(txt, tw, 6.4, 400); h = max(len(linhas) * 8.8, 18 if st else 9) + 5
        s.text(cx, y, tag, 6.4, 700, '#7a3423')
        if st: chip(s, cx - 0.5, y + 10, st, 4.3)
        for i, l in enumerate(linhas): s.text(tx, y + i * 8.8, l, 6.4, 400, TINTA)
        y += h
    if escala:
        k, marcas, rot = escala
        caps(s, 50.9, 1128.0, 'Escala ' + rot, 5.7, TERRA, ls=1.8)
        xb, yb = 50.9, 1133.2
        for i in range(len(marcas) - 1):
            s.rect(xb + marcas[i] * k, yb, (marcas[i + 1] - marcas[i]) * k, 4.2,
                   fill=TINTA if i % 2 == 0 else FUNDO, stroke=TINTA, sw=0.7)
        for i, m in enumerate(marcas):
            s.text(xb + m * k, yb + 12.5, ('%g' % m).replace('.', ',') + (' m' if i == len(marcas) - 1 else ''),
                   5.7, 400, TINTA, anc='start' if i == 0 else 'middle')
    if status_leg:
        x = 300.0 if escala else 50.9
        caps(s, x, 1128.0, 'Status', 5.7, TERRA, ls=1.8)
        xx = x
        for k_ in 'DPAC':
            xx = chip(s, xx, 1141.5, k_, 4.6) + 4

# ------------------------------------------------------------------ elevacao planificada
def elevacao(s, ox, oy, k, segs, alt, pontos=(), clad=(), elems=(), cotas_extra=(), niveis_extra=(),
             rot_pil=True, mostrar_niveis=True, tam_m=4.2, dims=None):
    """Elevacao planificada (paredes vistas de dentro, desdobradas da esquerda para a direita).
    segs: [(comp_m, rotulo)]; clad: [(s0, s1, h0, h1, codigo)]; elems: [(tipo, s0, s1, h0, h1, rotulo)]
    tipo em 'janela' | 'nicho' | 'ralo' | 'vidro' | 'volume' | 'texto'. pontos: [(s_m, ponto)]. oy = piso (pt)."""
    X = lambda sm: ox + sm * k
    Y = lambda h: oy - h * k
    comp = sum(c for c, _ in segs)
    s.rect(X(0), Y(alt), comp * k, alt * k, fill=PAPEL)
    for s0, s1, h0, h1, cod in clad:
        s.rect(X(s0), Y(h1), (s1 - s0) * k, (h1 - h0) * k, fill=tint(RP[cod][0], 0.30))
        # juntas indicativas (paginacao nao definida aqui): textura leve
        cid = s.uid('cl')
        s.defs.append('<clipPath id="%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/></clipPath>'
                      % (cid, X(s0), Y(h1), (s1 - s0) * k, (h1 - h0) * k))
        s.group('clip-path="url(#%s)" opacity="0.35"' % cid)
        yy = Y(h0)
        while yy > Y(h1):
            for xx in range(int(X(s0)) + (3 if int((Y(h0) - yy) / 7) % 2 else 0), int(X(s1)) + 1, 6):
                s.circle(xx, yy - 3.5, 0.35, fill=RP[cod][0])
            yy -= 7
        s.end()
    pils_cl = []
    for s0, s1, h0, h1, cod in clad:
        pils_cl.append(((X(s0) + X(s1)) / 2, Y(h1) + 9, cod))
    # elementos
    for tipo, s0, s1, h0, h1, rot in elems:
        if tipo == 'janela':
            s.rect(X(s0), Y(h1), (s1 - s0) * k, (h1 - h0) * k, fill='#ffffff', stroke=TINTA, sw=0.6)
            s.line(X(s0), Y(h1), X(s1), Y(h0), stroke=TINTA, sw=0.25); s.line(X(s0), Y(h0), X(s1), Y(h1), stroke=TINTA, sw=0.25)
            if rot:
                for i, l in enumerate(rot.split('\n')):
                    w = largura(l, 5.6, 600) + 5
                    yy = (Y(h0) + Y(h1)) / 2 - 3 + i * 7.6
                    s.rect((X(s0) + X(s1)) / 2 - w / 2, yy - 5.2, w, 7.2, fill='#ffffff')
                    s.text((X(s0) + X(s1)) / 2, yy, l, 5.6, 600 if i == 0 else 400, TINTA, anc='middle')
        elif tipo == 'nicho':
            s.rect(X(s0), Y(h1), (s1 - s0) * k, (h1 - h0) * k, fill='#d9cfbd', stroke=TINTA, sw=0.6)
            if rot: s.text((X(s0) + X(s1)) / 2, (Y(h0) + Y(h1)) / 2 + 2, rot, 5.6, 600, TINTA, anc='middle')
        elif tipo == 'ralo':
            s.rect(X(s0), Y(0) - 2.4, (s1 - s0) * k, 2.4, fill=TINTA)
            if rot: s.text((X(s0) + X(s1)) / 2, Y(0) - 4.4, rot, 5.2, 600, TINTA, anc='middle')
        elif tipo == 'vidro':
            s.line(X(s0), Y(0), X(s0), Y(h1), stroke='#5b8fa8', sw=1.4)
            if rot: s.text(X(s0) + (3 if s1 >= 0 else -3), Y(h1) - 2.5, rot, 5.2, 600, '#3d6b80', anc='start' if s1 >= 0 else 'end')
        elif tipo == 'volume':
            s.rect(X(s0), Y(h1), (s1 - s0) * k, (h1 - h0) * k, fill='none', stroke=TINTA, sw=0.7, extra='stroke-dasharray="3 1.6"')
            if rot:
                for i, l in enumerate(rot.split('\n')):
                    s.text((X(s0) + X(s1)) / 2, (Y(h0) + Y(h1)) / 2 + i * 7.6, l, 5.6, 600 if i == 0 else 400, TINTA, anc='middle')
        elif tipo == 'texto':
            s.text((X(s0) + X(s1)) / 2, Y(h0), rot, 5.8, 500, COTA_TXT, anc='middle')
    # quinas e contorno
    acc = 0
    for c, _ in segs[:-1]:
        acc += c; s.line(X(acc), Y(0), X(acc), Y(alt), stroke=TINTA, sw=0.5)
    s.rect(X(0), Y(alt), comp * k, alt * k, stroke=TINTA, sw=0.9)
    s.line(X(-0.18), oy, X(comp + 0.18), oy, stroke=PAREDE, sw=1.4)
    for x, y, cod in pils_cl:
        pilula(s, x, y, cod, 5.6, fundo=tint(RP[cod][0], 0.75), cor=TINTA if cod in ('RP02', 'RP03') else CREME)
    # pontos
    alturas = set(niveis_extra) | {alt}
    marcas, rot_pts = [], []
    for sm, p in pontos:
        grupos = {}
        for t, h, f in p['serv']:
            hv = 0.0 if h == 'piso' else float(h.replace(',', '.'))
            grupos.setdefault(hv, []).append(t)
        for hv, lst in grupos.items():
            if hv > 0: alturas.add(hv)
            n = len(lst)
            for i, t in enumerate(lst):
                marcas.append((X(sm) + (i - (n - 1) / 2) * (tam_m * 2.15), Y(hv) if hv > 0 else oy - tam_m - 0.6, t, p['esquematico']))
        rot_pts.append((X(sm), p['cod'], max(grupos)))
    # niveis a esquerda
    if mostrar_niveis:
        xo = X(0) - 13
        niv = sorted(h for h in alturas if h > 0)
        s.line(xo, oy, xo, Y(max(niv)), stroke=COTA, sw=0.35)
        lab = []
        for hv in niv:
            yy = Y(hv); lab.append(min(yy, lab[-1] - 7.4) if lab else min(yy, oy - 6.5))
        for hv, ly in zip(niv, lab):
            yy = Y(hv)
            s.circle(xo, yy, 1.05, fill=COTA)
            s.line(xo, yy, X(0), yy, stroke=COTA, sw=0.3)
            s.line(xo - 1.5, yy, xo - 6, ly, stroke=COTA, sw=0.3)
            s.text(xo - 7, ly + 2.2, ('%.2f' % hv).replace('.', ','), 6.2, 600, COTA_TXT, anc='end')
        s.circle(xo, oy, 1.05, fill=COTA)
        s.text(xo - 7, oy + 2.2, '0,00', 6.2, 600, COTA_TXT, anc='end')
    # eixos e pilulas dos pontos (faixa alta, alternando quando proximos)
    nivel_ant, x_ant = 1, -999
    hpil = max(h for _, _, h in rot_pts) + 0.42 if rot_pts else 0
    for xx, cod, hmax in sorted(rot_pts):
        nivel = 1 - nivel_ant if xx - x_ant < 24 else 0
        hy = hpil + nivel * 0.13
        s.line(xx, oy, xx, Y(hy) + 4, stroke=TINTA, sw=0.3, dash='2 1.3')
        if rot_pil: pilula(s, xx, Y(hy) + 2.0, cod, 5.6)
        nivel_ant, x_ant = nivel, xx
    for cx, cy, t, esq in marcas:
        marcador(s, cx, cy, t, tam_m, tracejado=esq)
    # cotas horizontais: segmentos (linha 1) e total (linha 2)
    def cota_h(a, b, y, txt, sub=None):
        s.line(X(a), y, X(b), y, stroke=TERRA, sw=0.35)
        for xx in (X(a), X(b)): s.line(xx, y - 2.5, xx, y + 2.5, stroke=TERRA, sw=0.35)
        s.text((X(a) + X(b)) / 2, y - 2.2, txt, 6.2, 700, '#7a3423', anc='middle')
        if sub: s.text((X(a) + X(b)) / 2, y + 7.2, sub, 5.4, 400, COTA_TXT, anc='middle')
    if dims is None:
        acc = 0
        for c, rot in segs:
            cota_h(acc, acc + c, oy + 11, fmt(c), rot); acc += c
    else:
        for a, b, rot in dims: cota_h(a, b, oy + 11, fmt(b - a), rot)
    for a, b, txt, sub, lin in cotas_extra:
        cota_h(a, b, oy + 11 + lin * 19, txt, sub)
    return X, Y

def fmt(v): return ('%.2f' % v).replace('.', ',')

# ------------------------------------------------------------------ quadros
def quadro_pts(s, x0, y0, x1, cods, titulo='Pontos e alturas', extra=None):
    """quadro compacto dos pontos (fundo terracota)."""
    pts = [PR.PT[c] if c in PR.PT else extra[c] for c in cods]
    h = 30 + sum(30 if p['serv'] else 22 for p in pts) + 18
    s.rect(x0, y0, x1 - x0, h, fill=TERRA, rx=12)
    taloe(s, x0 + 12, y0 + 19, titulo, 11.5, CREME)
    caps(s, x1 - 12, y0 + 18, 'Altura (m) · fonte', 5.4, CREME, anc='end', ls=1.0)
    y = y0 + 36
    for p in pts:
        s.text(x0 + 12, y, p['cod'], 7.4, 700, CREME)
        s.text(x0 + 42, y, p['peca'], 7.3, 600, CREME)
        s.text(x0 + 42, y + 9, p['eixo_txt'], 6.0, 300, CREME)
        xx = x0 + 42
        for t, hh, f in p['serv']:
            marcador(s, xx + 3.6, y + 16.6, t, 3.6, tracejado=p['esquematico'])
            s.text(xx + 9.6, y + 19.2, hh, 6.8, 600, CREME)
            w = largura(hh, 6.8, 600)
            s.text(xx + 10.4 + w, y + 16.8, f, 4.8, 700, CREME)
            xx += 10.4 + w + 13
        y += 30
    s.text(x0 + 12, y + 2, 'Fontes: C caderno Hidráulica Rev. 02 · D definição do cliente · P padrão do escritório.', 5.6, 400, CREME)
    return y0 + h

def quadro_itens(s, x0, y0, x1, titulo, itens, fundo='#ffffff', larg_txt=None):
    """itens: (rotulo, texto, status). Retorna y final."""
    tw = larg_txt or (x1 - x0 - 128)
    alt = 0
    lin = [(r, quebrar(t, tw, 6.3, 400), st) for r, t, st in itens]
    alt = 30 + sum(max(len(l), 1) * 8.4 + 4.6 for _, l, _ in lin)
    s.rect(x0, y0, x1 - x0, alt, fill=fundo, rx=12, stroke='#e2d8c3', sw=0.6)
    taloe(s, x0 + 12, y0 + 19, titulo, 11.5)
    y = y0 + 36
    for r, l, st in lin:
        s.text(x0 + 12, y, r, 6.4, 700, '#7a3423')
        for i, t in enumerate(l): s.text(x0 + 72, y + i * 8.4, t, 6.3, 400, TINTA)
        if st: chip(s, x1 - 10, y + 0.6, st, 4.3, anc='end')
        y += max(len(l), 1) * 8.4 + 4.6
    return y0 + alt

def html3(folhas):
    ff = ''
    for w in (300, 400, 500, 600, 700):
        ff += "@font-face{font-family:'Manrope';font-weight:%d;src:url('fonts/manrope-latin-%d-normal.woff2') format('woff2');}\n" % (w, w)
    ff += "@font-face{font-family:'Aloevera';font-weight:700;src:url('fonts/aloevera-bold-dup.ttf') format('truetype');}\n"
    corpo = '\n'.join('<section class="folha">%s</section>' % f for f in folhas)
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Áreas molhadas · Residência IC</title><style>%s'
            '@page{size:297mm 420mm;margin:0}html,body{margin:0;padding:0;background:#fff}'
            'section.folha{width:297mm;height:420mm;overflow:hidden;page-break-after:always;break-after:page}'
            'section.folha svg{display:block}text{font-kerning:normal}</style></head><body>%s</body></html>' % (ff, corpo))
