# -*- coding: utf-8 -*-
"""Desenho da base (paredes/janelas vetorizadas), pontos, cotas e etiquetas em qualquer escala."""
import json, os, math
from svgkit import *
import dados_pontos as D

BASE_JS = json.load(open(os.path.join(AQUI, 'base.json')))
MM = 72 / 25.4

class Vista:
    """mapeia metros (base) -> pt da folha. escala = denominador (100, 25, 50)."""
    def __init__(self, ox, oy, escala, x0=0.0, y0=0.0, clip=None):
        self.k = 1000 / escala * MM     # pt por metro
        self.ox, self.oy, self.x0, self.y0 = ox, oy, x0, y0
        self.clip = clip                # (x0, y0, x1, y1) em metros
    def X(self, x): return self.ox + (x - self.x0) * self.k
    def Y(self, y): return self.oy + (y - self.y0) * self.k
    def P(self, x, y): return self.X(x), self.Y(y)

def desenhar_base(s, v, sw_janela=True, parede=PAREDE):
    cid = None
    if v.clip:
        cid = s.uid('clip'); x0, y0, x1, y1 = v.clip
        s.defs.append('<clipPath id="%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/></clipPath>'
                      % (cid, v.X(x0), v.Y(y0), (x1 - x0) * v.k, (y1 - y0) * v.k))
        s.group('clip-path="url(#%s)"' % cid)
    for p in BASE_JS['paredes']:
        d = ''
        for anel in [p['pts']] + p['furos']:
            d += 'M' + ' L'.join('%.2f %.2f' % v.P(x, y) for x, y in anel) + ' Z '
        s.path(d, fill=parede, extra='fill-rule="evenodd"')
    for x, y, w, h in BASE_JS['janelas']:
        s.rect(v.X(x), v.Y(y), w * v.k, h * v.k, fill=JANELA)
    for x, y, w, h in BASE_JS['vidros']:
        s.rect(v.X(x), v.Y(y), w * v.k, h * v.k, fill='#c3c6b8')
    for pts in BASE_JS['caixilhos']:
        s.path('M' + ' L'.join('%.2f %.2f' % v.P(x, y) for x, y in pts) + ' Z', stroke=PAREDE, sw=0.4)
    if cid: s.end()

# ------------------------------------------------------------------ marcadores
def marcador(s, x, y, tipo, r=4.2, tracejado=False):
    sig, nome, cor, ctxt = D.TIPOS[tipo]
    if tipo == 'SC':     # saida de chuveiro: metade azul / metade vermelha
        s.path('M%.2f %.2f A%.2f %.2f 0 0 1 %.2f %.2f Z' % (x, y - r, r, r, x, y + r), fill=D.TIPOS['AQ'][2])
        s.path('M%.2f %.2f A%.2f %.2f 0 0 0 %.2f %.2f Z' % (x, y - r, r, r, x, y + r), fill=D.TIPOS['AF'][2])
        s.circle(x, y, r, stroke='#ffffff', sw=0.5)
    else:
        s.circle(x, y, r, fill=cor, stroke='#ffffff' if not tracejado else TINTA, sw=0.5 if not tracejado else 0.6,
                 dash='1.2 0.8' if tracejado else None)
    s.text(x, y + r * 0.45, sig, r * 1.25, 700, ctxt, anc='middle')

NORMAL = {'sup': (0, 1), 'inf': (0, -1), 'esq': (1, 0), 'dir': (-1, 0), None: (0, 1)}

def ponto_ampliado(s, v, p, r=4.8, afast=7.6, passo=10.6, eixo=True):
    """desenha a pilha de marcadores de um ponto a partir da face da parede, para dentro do
    ambiente (todos os servicos no mesmo eixo). Retorna a extremidade da pilha (pt)."""
    x, y = v.P(p['x'], p['y']); nx, ny = NORMAL[p['parede']]
    tipos = []
    for t, h, f in p['serv']:
        if t not in tipos: tipos.append(t)
    if p['parede'] is None:          # ponto isolado (ilha): pilha centrada
        x -= nx * (afast + passo * (len(tipos) - 1) / 2); y -= ny * (afast + passo * (len(tipos) - 1) / 2)
    ult = afast + passo * (len(tipos) - 1)
    if eixo:
        s.line(x, y, x + nx * (ult + r + 2), y + ny * (ult + r + 2), stroke=TINTA, sw=0.35, dash='2 1.2')
    for i, t in enumerate(tipos):
        cx, cy = x + nx * (afast + passo * i), y + ny * (afast + passo * i)
        marcador(s, cx, cy, t, r, tracejado=p['esquematico'])
    if p['parede'] is None:
        s.line(v.X(p['x']) - 5, v.Y(p['y']), v.X(p['x']) + 5, v.Y(p['y']), stroke=TERRA, sw=0.5)
        s.line(v.X(p['x']), v.Y(p['y']) - 5, v.X(p['x']), v.Y(p['y']) + 5, stroke=TERRA, sw=0.5)
    return x + nx * (ult + r), y + ny * (ult + r)

def ponto_simples(s, v, p, r=2.3):
    """marcador neutro de eixo (planta geral 1:100), afastado da face para dentro do ambiente."""
    x, y = v.P(p['x'], p['y']); nx, ny = NORMAL[p['parede']]
    if p['parede'] is None: nx = ny = 0
    cx, cy = x + nx * (r + 0.6), y + ny * (r + 0.6)
    s.circle(cx, cy, r, fill='#ffffff', stroke=TINTA, sw=0.5, dash='0.8 0.6' if p['esquematico'] else None)
    s.line(cx - r - 1.2, cy, cx + r + 1.2, cy, stroke=TINTA, sw=0.35)
    s.line(cx, cy - r - 1.2, cx, cy + r + 1.2, stroke=TINTA, sw=0.35)
    return cx, cy

# ------------------------------------------------------------------ cotas
def cota(s, v, c, desloc, tam=7.5, cor_txt=COTA_TXT, lado_txt=1, ext_de=None, ext_ate=None):
    """c: dict(eixo='x'|'y', de, ate, txt). desloc: coordenada (m) da linha de cota no outro eixo.
    ext_de / ext_ate: coordenada (m) de inicio das linhas de chamada (face/ponto) no outro eixo."""
    if c['eixo'] == 'x':
        x1, x2, y = v.X(c['de']), v.X(c['ate']), v.Y(desloc)
        for xx, e in ((x1, ext_de), (x2, ext_ate)):
            if e is not None: s.line(xx, v.Y(e), xx, y + 3 * (1 if y > v.Y(e) else -1), stroke=COTA, sw=0.35)
        s.line(x1, y, x2, y, stroke=COTA, sw=0.35)
        for xx in (x1, x2): s.circle(xx, y, 1.15, fill=COTA)
        s.text((x1 + x2) / 2, y - 2.6 if lado_txt > 0 else y + tam + 1.2, c['txt'], tam, 600, cor_txt, anc='middle')
    else:
        y1, y2, x = v.Y(c['de']), v.Y(c['ate']), v.X(desloc)
        for yy, e in ((y1, ext_de), (y2, ext_ate)):
            if e is not None: s.line(v.X(e), yy, x + 3 * (1 if x > v.X(e) else -1), yy, stroke=COTA, sw=0.35)
        s.line(x, y1, x, y2, stroke=COTA, sw=0.35)
        for yy in (y1, y2): s.circle(x, yy, 1.15, fill=COTA)
        tx = x - 2.6 if lado_txt > 0 else x + tam + 1.2
        s.text(tx, (y1 + y2) / 2, c['txt'], tam, 600, cor_txt, anc='middle', rot=-90)

# ------------------------------------------------------------------ etiquetas
def pilula(s, x, y, cod, tam=7.2, fundo=TERRA, cor=CREME, anc='middle'):
    w = largura(cod, tam, 700) + 7
    x0 = x - w / 2 if anc == 'middle' else (x if anc == 'start' else x - w)
    s.rect(x0, y - tam * 0.95, w, tam * 1.35, fill=fundo, rx=tam * 0.67)
    s.text(x0 + w / 2, y, cod, tam, 700, cor, anc='middle')
    return x0, x0 + w

def etiqueta(s, ax, ay, tx, ty, p, linhas=True, anc='start', tam=7.2, alturas=True, cor_lider=TINTA):
    """lider do fim da pilha (ax, ay) ate (tx, ty); pilula com o codigo + nome da peca + alturas."""
    s.line(ax, ay, tx, ty, stroke=cor_lider, sw=0.35)
    s.circle(ax, ay, 0.9, fill=cor_lider)
    xa, xb = pilula(s, tx, ty + 2.6, p['cod'], tam, anc=anc)
    xt = xb + 3 if anc != 'end' else xa - 3
    an = 'start' if anc != 'end' else 'end'
    s.text(xt, ty + 2.6, p['peca'], tam, 600, TINTA, anc=an)
    if alturas:
        s.text(xt, ty + 2.6 + tam * 1.25, txt_alturas(p), tam * 0.95, 400, TINTA, anc=an)

def txt_alturas(p, fontes=False):
    out = []
    for t, h, f in p['serv']:
        nome = D.SIGLA_TXT[t]
        out.append('%s %s%s' % (nome, h, (' ' + f) if fontes else ''))
    return ' · '.join(out)

def selo(s, x, y, txt, r=9.5, fundo=TERRA, cor=CREME, tam=None):
    s.circle(x, y, r, fill=fundo, stroke='#ffffff', sw=0.8)
    s.text(x, y + r * 0.36, txt, tam or r * 1.0, 700, cor, anc='middle')
