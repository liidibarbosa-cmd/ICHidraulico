# -*- coding: utf-8 -*-
"""Elementos de corte reutilizados (laje, parede, forro, testeira, perfis, luz, cortina)."""
import math
from base import *

T_CHAPA = 0.0125   # espessura apenas GRÁFICA da chapa no desenho (a especificação vem do fabricante)
T_LAJE = 0.12      # espessura GRÁFICA da laje (não documentada; ver projeto estrutural)


def quebra_h(v, x0, x1, y, amp=1.2):
    """Linha de interrupção horizontal (zigue-zague)."""
    xm = (x0 + x1) / 2
    v.poly([(x0, y), (xm - 1.5, y), (xm - 0.6, y - amp), (xm + 0.6, y + amp), (xm + 1.5, y), (x1, y)], stroke=C['ink'],
           sw=0.2, close=False)


def quebra_v(v, x, y0, y1, amp=1.2):
    ym = (y0 + y1) / 2
    v.poly([(x, y0), (x, ym - 1.5), (x - amp, ym - 0.6), (x + amp, ym + 0.6), (x, ym + 1.5), (x, y1)], stroke=C['ink'],
           sw=0.2, close=False)


def laje(v, s, x0, x1, z, rot=True):
    x, y, w, h = s.R(x0, z, x1, z + T_LAJE)
    v.rect(x, y, w, h, fill='url(#hLaje)', stroke=C['ink'], sw=0.35)
    quebra_v(v, x + w, y - 1, y + h + 1)
    return (x, y, w, h)


def parede(v, s, x0, x1, z0, z1, reboco=0.02):
    x, y, w, h = s.R(x0, z0, x1, z1)
    v.rect(x, y, w, h, fill='url(#hAlv)', stroke=C['ink'], sw=0.35)
    xr, yr, wr, hr = s.R(x1 - reboco, z0, x1, z1)
    v.rect(xr, yr, wr, hr, fill='#f4f1e8', stroke=C['ink'], sw=0.15)
    quebra_h(v, x - 1, x + w + 1, y + h)


def chapa(v, s, x0, z0, x1, z1, ru=False):
    x, y, w, h = s.R(x0, z0, x1, z1)
    v.rect(x, y, w, h, fill='url(#hGessoRU)' if ru else 'url(#hGesso)', stroke=C['ink'], sw=0.3)
    return (x, y, w, h)


def perfil_u(v, s, x0, z0, x1, z1, aberto='baixo'):
    """Perfil metálico em U (desenho simbólico, dimensões gráficas)."""
    x, y, w, h = s.R(x0, z0, x1, z1)
    t = 0.35
    if aberto == 'baixo':
        v.poly([(x, y + h), (x, y), (x + w, y), (x + w, y + h)], stroke=C['aco'], sw=t, close=False)
    elif aberto == 'cima':
        v.poly([(x, y), (x, y + h), (x + w, y + h), (x + w, y)], stroke=C['aco'], sw=t, close=False)
    elif aberto == 'esq':
        v.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], stroke=C['aco'], sw=t, close=False)
    else:
        v.poly([(x + w, y), (x, y), (x, y + h), (x + w, y + h)], stroke=C['aco'], sw=t, close=False)


def pendural(v, s, x, z0, z1):
    a, b = s.P(x, z0), s.P(x, z1)
    v.line(*a, *b, C['aco'], 0.35)
    v.rect(b[0] - 0.9, b[1] - 0.2, 1.8, 0.8, fill=C['aco'])


def cantoneira(v, s, x, z, dx=1, dz=1, L=0.02):
    a = s.P(x, z)
    b = s.P(x + dx * L, z)
    c = s.P(x, z + dz * L)
    v.poly([b, a, c], stroke=C['rust'], sw=0.45, close=False)


def cortina(v, s, x, z_top, z_bot, amp=0.012, passo=0.05):
    pts = []
    n = max(2, int((z_top - z_bot) / passo))
    d = f'M{s.P(x, z_top)[0]:.2f},{s.P(x, z_top)[1]:.2f} '
    for i in range(n):
        za = z_top - i * passo
        zb = za - passo
        c = s.P(x + (amp if i % 2 else -amp), (za + zb) / 2)
        e = s.P(x, zb)
        d += f'Q{c[0]:.2f},{c[1]:.2f} {e[0]:.2f},{e[1]:.2f} '
    v.path(d, stroke='#7c7a70', sw=0.3, dash='1.6 0.7')


def zona(v, s, x0, z0, x1, z1, cor, rot=None, size=5.2):
    x, y, w, h = s.R(x0, z0, x1, z1)
    v.rect(x, y, w, h, fill=cor, stroke=cor, sw=0.25, dash='1 0.6', op=0.9)


def cone_luz(v, pts):
    v.poly(pts, fill='url(#gLuz)')


def marca_nivel(v, x, y, txt, lado='dir', cor=None, doc=True):
    cor = cor or C['rust']
    v.poly([(x - 1.4, y - 2.2), (x + 1.4, y - 2.2), (x, y)], fill=cor)
    v.line(x - 4, y, x + (15 if lado == 'dir' else -15), y, cor, 0.25)
    v.text(x + (2.2 if lado == 'dir' else -2.2), y - 1.0, txt, size=6.0, weight=700, cor=cor,
           anchor='start' if lado == 'dir' else 'end')


def num(v, x, y, n, cor=None, r=2.3):
    cor = cor or C['ink']
    v.circle(x, y, r, fill=cor)
    v.text(x, y + 0.95, str(n), size=6.2, weight=800, cor='#fff', family='Outfit')


def call(v, px, py, tx, ty, n, cor=None):
    """Chamada numerada: ponto no elemento (px,py) e selo em (tx,ty)."""
    cor = cor or C['ink']
    v.circle(px, py, 0.5, fill=cor)
    v.line(px, py, tx, ty, cor, 0.18)
    num(v, tx, ty, n, cor)


# ------------------------------------------------------------- perspectiva de corte (extrusão oblíqua)
class Persp:
    """Extrusão oblíqua de um corte (x,z em metros) ao longo de y. Projeção cavaleira a 30°."""
    def __init__(self, esc, ox, oy, ang=30, f=0.55):
        self.k = 1000 / esc
        self.ox, self.oy = ox, oy
        self.cx = math.cos(math.radians(ang)) * f
        self.cy = math.sin(math.radians(ang)) * f

    def P(self, x, y, z):
        return (self.ox + (x + y * self.cx) * self.k, self.oy - (z + y * self.cy) * self.k)

    def caixa(self, v, x0, z0, x1, z1, y0, y1, fill, top=None, side=None, sw=0.25, stroke=None, faces='fts'):
        st = stroke or C['ink']
        P = self.P
        if 't' in faces:  # face superior
            v.poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], fill=top or fill, stroke=st, sw=sw)
        if 's' in faces:  # face lateral direita
            v.poly([P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1)], fill=side or fill, stroke=st, sw=sw)
        if 'f' in faces:  # face frontal (plano do corte)
            v.poly([P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1)], fill=fill, stroke=st, sw=sw)
