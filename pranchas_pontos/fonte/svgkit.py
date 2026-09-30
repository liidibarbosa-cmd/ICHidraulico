# -*- coding: utf-8 -*-
"""Primitivas SVG no padrao grafico das pranchas de eletrica (Tomadas R05):
folha A2 paisagem em pt (1683,78 x 1190,55), paineis arredondados, quadros numerados,
carimbo oliva, tipografia Manrope + Aloevera Display (titulos)."""
import os, math
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1683.78, 1190.55

# cores (extraidas da prancha de Tomadas R05)
OLIVA = '#3f422f'      # paineis escuros / moldura
TINTA = '#22251a'      # texto escuro
TERRA = '#903f2a'      # terracota
CREME = '#f5e7c4'      # painel legenda / texto claro
CLARO = '#f7f2e8'      # painel observacoes
COTA = '#999c87'       # linhas de cota
COTA_TXT = '#4f5240'   # texto de cota
PAREDE = '#111111'
JANELA = '#a9ad9c'

# ------------------------------------------------------------------ medicao de texto
_FONTS = {}
def _font(peso):
    if peso not in _FONTS:
        if peso == 'aloe':
            f = TTFont(os.path.join(AQUI, 'fonts', 'aloevera-bold-dup.ttf'))
        else:
            f = TTFont(os.path.join(AQUI, 'fonts', 'manrope-latin-%d-normal.woff2' % peso))
        _FONTS[peso] = (f.getBestCmap(), f['hmtx'].metrics, f['head'].unitsPerEm)
    return _FONTS[peso]

def largura(txt, tam, peso=400, ls=0.0):
    cmap, hm, upm = _font(peso)
    w = 0
    for ch in txt:
        g = cmap.get(ord(ch)) or cmap.get(ord(' '))
        w += hm[g][0] if g in hm else upm * 0.5
    return w * tam / upm + ls * max(len(txt) - 1, 0)

def quebrar(txt, larg, tam, peso=400):
    linhas, atual = [], ''
    for pal in txt.split(' '):
        t = (atual + ' ' + pal).strip()
        if largura(t, tam, peso) <= larg or not atual:
            atual = t
        else:
            linhas.append(atual); atual = pal
    if atual: linhas.append(atual)
    return linhas

# ------------------------------------------------------------------ primitivas
def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def f2(v): return ('%.2f' % v).rstrip('0').rstrip('.') if isinstance(v, float) else str(v)

class Svg:
    _cont = 0                      # contador global: ids unicos no documento HTML inteiro
    def __init__(self):
        self.p = []
        self.defs = []
    def uid(self, pref='i'):
        Svg._cont += 1; return '%s%d' % (pref, Svg._cont)
    def add(self, s): self.p.append(s)
    def rect(self, x, y, w, h, fill='none', stroke='none', sw=0, rx=0, extra=''):
        self.add('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s" stroke="%s" stroke-width="%.2f" %s/>'
                 % (x, y, w, h, rx, fill, stroke, sw, extra))
    def line(self, x1, y1, x2, y2, stroke=TINTA, sw=0.5, dash=None, extra=''):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.add('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"%s %s/>'
                 % (x1, y1, x2, y2, stroke, sw, d, extra))
    def circle(self, x, y, r, fill='none', stroke='none', sw=0, dash=None, extra=''):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.add('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="%s" stroke-width="%.2f"%s %s/>'
                 % (x, y, r, fill, stroke, sw, d, extra))
    def path(self, d, fill='none', stroke='none', sw=0, extra=''):
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f" %s/>' % (d, fill, stroke, sw, extra))
    def text(self, x, y, s, tam=10, peso=400, cor=TINTA, anc='start', ls=0, rot=None, extra=''):
        fam = "Aloevera" if peso == 'aloe' else "Manrope"
        w = 700 if peso == 'aloe' else peso
        tr = ' transform="rotate(%.1f %.2f %.2f)"' % (rot, x, y) if rot else ''
        lsp = ' letter-spacing="%.2f"' % ls if ls else ''
        self.add('<text x="%.2f" y="%.2f" font-family="%s" font-weight="%d" font-size="%.2f" fill="%s" text-anchor="%s"%s%s %s>%s</text>'
                 % (x, y, fam, w, tam, cor, anc, lsp, tr, extra, esc(s)))
    def rich(self, x, y, partes, tam=10, anc='start'):
        """partes: lista de (texto, peso, cor)."""
        spans = ''.join('<tspan font-family="%s" font-weight="%d" fill="%s">%s</tspan>'
                        % ('Aloevera' if p == 'aloe' else 'Manrope', 700 if p == 'aloe' else p, c, esc(t))
                        for t, p, c in partes)
        self.add('<text x="%.2f" y="%.2f" font-size="%.2f" text-anchor="%s" xml:space="preserve">%s</text>' % (x, y, tam, anc, spans))
    def image(self, x, y, w, h, href):
        self.add('<image x="%.2f" y="%.2f" width="%.2f" height="%.2f" href="%s" preserveAspectRatio="xMidYMid meet"/>' % (x, y, w, h, href))
    def group(self, extra=''):
        self.add('<g %s>' % extra)
    def end(self): self.add('</g>')
    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                'width="594mm" height="420mm" viewBox="0 0 %.2f %.2f"><defs>%s</defs>%s</svg>'
                % (W, H, ''.join(self.defs), '\n'.join(self.p)))

# ------------------------------------------------------------------ elementos de prancha
COL2 = (822.0, 1224.8)
COL3 = (1247.2, 1655.2)
TOPO, BASE = 33.8, 1162.5

def moldura(s):
    s.rect(0, 0, W, H, fill='#ffffff')
    s.rect(18, 18, W - 36, H - 36, stroke=OLIVA, sw=1.5, rx=14)

def painel(s, x0, y0, x1, y1, fundo, titulo=None, quadro=None, cor_txt=None):
    cor_txt = cor_txt or (CREME if fundo in (TERRA, OLIVA) else TINTA)
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=fundo, rx=16)
    if titulo:
        s.text(x0 + 16, y0 + 24.5, titulo, 17, 'aloe', cor_txt)
    if quadro:
        s.text(x1 - 17.8, y0 + 25.5, 'QUADRO ' + quadro, 10, 700, cor_txt, anc='end', ls=2.6)
    return cor_txt

def paragrafo(s, x, y, txt, larg, tam=11, peso=400, cor=TINTA, entre=None):
    entre = entre or tam * 1.33
    for i, l in enumerate(quebrar(txt, larg, tam, peso)):
        s.text(x, y + i * entre, l, tam, peso, cor)
    return y + len(quebrar(txt, larg, tam, peso)) * entre

def carimbo(s, logo_href, planta, escala_txt, prancha, rev, data, escala_barra=None, projeto=None, endereco=None, resp=None):
    x0, y0, x1, y1 = COL3[0], 927.0, COL3[1], BASE
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=OLIVA, rx=16)
    s.image(1263.0, 941.2, 119.2, 23.3, logo_href)
    s.text(1637.9, 954.0, 'CARIMBO', 9.5, 700, CREME, anc='end', ls=2.6)
    s.text(1262.8, 979.5, 'PROJETO', 8.5, 700, CREME, ls=0.8)
    s.text(1262.8, 995.0, projeto, 15, 'aloe', CREME)
    s.text(1262.8, 1010.0, endereco, 10.5, 300, CREME)
    s.text(1262.8, 1028.3, 'RESPONSÁVEIS TÉCNICAS', 8.5, 700, CREME, ls=0.8)
    for i, r in enumerate(resp):
        s.text(1262.8, 1041.5 + i * 15, r, 11, 300, CREME)
    s.text(1262.8, 1074.7, 'PLANTA', 8.5, 700, CREME, ls=0.8)
    s.text(1262.8, 1089.2, planta, 11, 600, CREME)
    s.text(1457.0, 1074.7, 'DATA', 8.5, 700, CREME, ls=0.8)
    s.text(1457.0, 1089.2, data, 11, 600, CREME)
    s.text(1262.8, 1106.3, 'ESCALA', 8.5, 700, CREME, ls=0.8)
    s.text(1262.8, 1121.5, escala_txt, 11, 600, CREME)
    s.text(1457.0, 1106.3, 'PRANCHA', 8.5, 700, CREME, ls=0.8)
    s.text(1457.0, 1125.2, prancha, 20, 'aloe', CREME)
    s.text(1528.1, 1106.3, 'REVISÃO', 8.5, 700, CREME, ls=0.8)
    s.text(1528.1, 1125.0, rev, 19, 700, CREME)
    s.text(1262.8, 1156.0, 'Conferir as medidas no local', 8.5, 500, CREME)
    if escala_barra:   # (pt por metro, metros totais, rotulo)
        k, m, rot = escala_barra
        L = k * m; xb, yb = 1263.8, 1129.5
        s.rect(xb - 0.4, yb - 0.4, L + 0.8, 6.1, stroke=CREME, sw=0.75)
        n = 5
        for i in range(n):
            if i % 2 == 0: s.rect(xb + i * L / n, yb, L / n, 5.3, fill=CREME)
        s.text(xb + L + 6, yb + 5.3, rot, 8.5, 300, CREME)

def titulo_desenho(s, x, y, num, titulo, sub, cor=TERRA):
    s.circle(x + 15, y - 7, 15, fill=cor)
    s.text(x + 15, y - 1.2, num, 14, 'aloe', CREME, anc='middle')
    s.text(x + 38, y, titulo, 22, 'aloe', TINTA)
    if sub: s.text(x + 38, y + 17, sub, 11.5, 600, TINTA)

def barra_escala(s, x, y, k, marcas, unidade='m'):
    """barra alternada preto/branco no estilo da prancha de tomadas."""
    L = k * marcas[-1]
    s.rect(x, y, L, 8.2, stroke=PAREDE, sw=0.75)
    for i in range(len(marcas) - 1):
        if i % 2 == 0:
            s.rect(x + k * marcas[i], y, k * (marcas[i + 1] - marcas[i]), 8.2, fill=PAREDE)
    for i, mk in enumerate(marcas):
        lab = ('%g' % mk).replace('.', ',') + (' ' + unidade if i == len(marcas) - 1 else '')
        s.text(x + k * mk, y + 21, lab, 9.5, 700, TINTA, anc='middle' if i else 'start')
