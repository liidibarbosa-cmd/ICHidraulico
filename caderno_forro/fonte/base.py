# -*- coding: utf-8 -*-
"""Base grafica do Caderno de Detalhamento de Forro de Gesso (Residencia IC).

Replica o padrao do Caderno de Detalhamento - Iluminacao (prancha 02/04 R01):
folha A2 paisagem, desenho a esquerda, quadros arredondados a direita
(creme / terracota / bege) e carimbo DUAS verde-oliva.
Unidades: milimetros de papel (viewBox 594 x 420).
"""
import html, json, math, os

AQUI = os.path.dirname(os.path.abspath(__file__))
GEO = json.load(open(os.path.join(AQUI, 'geometria_base.json')))
LUM = json.load(open(os.path.join(AQUI, 'luminarias_ref.json')))

PAGE_W, PAGE_H = 594.0, 420.0
PT = 0.3528  # 1 pt em mm

# ------------------------------------------------------------- paleta (medida no PDF de iluminacao)
C = dict(
    ink='#22251a', muted='#595447', grey='#999b87', grey2='#c9c6b6', faint='#b9b5a5',
    creme='#f5e7c4', rust='#903f2a', rust2='#b8331a', bege='#f7f2e8', olive='#3f422f',
    papel='#ffffff', st='#fbf8f1',
    ru='#cfe3c4', ru_line='#5f8f4e', ru_txt='#3f6e31',
    cort_fill='#fae5b6', cort_line='#eda80d', luz='#cc7300', luz2='#f4b940',
    laje='#d9d6cb', alv='#e9e4d6', gesso='#fdfbf5', aco='#7d8088', madeira='#c7a27a',
    prop='#903f2a', doc='#3f422f',
)

esc = lambda s: html.escape(str(s))
br = lambda v, n=2: (f'{v:.{n}f}').replace('.', ',')


# ======================================================================= SVG
class SVG:
    """Acumulador de elementos SVG em mm de papel."""
    def __init__(self):
        self.e = []

    def add(self, s):
        self.e.append(s)
        return self

    def __str__(self):
        return ''.join(self.e)

    # --- primitivas
    def line(self, x1, y1, x2, y2, cor=None, w=0.25, dash=None, cap='butt', op=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{cor or C["ink"]}" '
                 f'stroke-width="{w}" stroke-linecap="{cap}"{da}{o}/>')

    def rect(self, x, y, w, h, fill='none', stroke='none', sw=0.25, rx=0, dash=None, op=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{da}{o}/>')

    def poly(self, pts, fill='none', stroke='none', sw=0.25, close=True, dash=None, op=None, join='miter'):
        d = 'M' + ' L'.join(f'{x:.3f},{y:.3f}' for x, y in pts) + (' Z' if close else '')
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}"{da}{o}/>')

    def path(self, d, fill='none', stroke='none', sw=0.25, dash=None, op=None, cap='butt'):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{da}{o}/>')

    def circle(self, x, y, r, fill='none', stroke='none', sw=0.25, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}/>')

    def text(self, x, y, s, size=7, weight=500, cor=None, anchor='middle', family='Manrope', rot=0,
             ls=0, italic=False, op=None):
        fs = size * PT
        tr = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot else ''
        lsa = f' letter-spacing="{ls}"' if ls else ''
        it = ' font-style="italic"' if italic else ''
        o = f' opacity="{op}"' if op else ''
        self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-family="{family}" font-size="{fs:.3f}" font-weight="{weight}" '
                 f'fill="{cor or C["ink"]}" text-anchor="{anchor}"{tr}{lsa}{it}{o}>{esc(s)}</text>')

    def lines_text(self, x, y, linhas, size=7, lh=1.25, **kw):
        for i, s in enumerate(linhas):
            self.text(x, y + i * size * PT * lh, s, size=size, **kw)

    # --- elementos de representacao
    def cota(self, x1, y1, x2, y2, off=4.0, txt=None, size=6.2, cor=None, tcor=None, ext=True, lado=1,
             weight=600):
        """Cota alinhada (estilo do caderno de tomadas: linha cinza, pontos nas extremidades)."""
        cor = cor or C['grey']
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy * lado, ux * lado
        a1 = (x1 + nx * off, y1 + ny * off)
        a2 = (x2 + nx * off, y2 + ny * off)
        if ext and off:
            g = 0.8 if off > 0 else -0.8
            self.line(x1 + nx * g, y1 + ny * g, a1[0] + nx * 1.0, a1[1] + ny * 1.0, cor, 0.13)
            self.line(x2 + nx * g, y2 + ny * g, a2[0] + nx * 1.0, a2[1] + ny * 1.0, cor, 0.13)
        self.line(*a1, *a2, cor, 0.18)
        self.circle(*a1, 0.45, fill=cor)
        self.circle(*a2, 0.45, fill=cor)
        if txt is None:
            txt = br(L)
        mx, my = (a1[0] + a2[0]) / 2, (a1[1] + a2[1]) / 2
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90.1 or ang < -89.9:
            ang += 180
        tx, ty = mx + nx * 1.0, my + ny * 1.0
        # texto sempre "acima" da linha de cota no sentido de leitura
        ox, oy = math.sin(math.radians(ang)) * 0.9, -math.cos(math.radians(ang)) * 0.9
        self.text(mx + ox, my + oy, txt, size=size, weight=weight, cor=tcor or C['ink'], rot=ang if abs(ang) > 0.1 else 0)

    def tag(self, x, y, txt, kind='prop', size=5.2, anchor='middle'):
        """Selo de status: prop = PROPOSTA (terracota) | doc = DOCUMENTADO (oliva) | pend = PENDENTE."""
        fs = size * PT
        w = len(txt) * fs * 0.66 + 2.4
        h = fs + 1.6
        if anchor == 'start':
            x0 = x
        elif anchor == 'end':
            x0 = x - w
        else:
            x0 = x - w / 2
        if kind == 'prop':
            self.rect(x0, y - h / 2, w, h, fill='#fff', stroke=C['prop'], sw=0.3, rx=h / 2)
            self.text(x0 + w / 2, y + fs * 0.36, txt, size=size, weight=700, cor=C['prop'], ls=0.15)
        elif kind == 'pend':
            self.rect(x0, y - h / 2, w, h, fill='#fff', stroke=C['rust2'], sw=0.3, rx=h / 2, dash='0.8 0.5')
            self.text(x0 + w / 2, y + fs * 0.36, txt, size=size, weight=700, cor=C['rust2'], ls=0.15)
        else:
            self.rect(x0, y - h / 2, w, h, fill=C['doc'], stroke='none', rx=h / 2)
            self.text(x0 + w / 2, y + fs * 0.36, txt, size=size, weight=700, cor=C['creme'], ls=0.15)
        return w

    def chamada(self, x, y, det, prancha, r=3.6, cor=None):
        """Selo de chamada de detalhe: circulo dividido (detalhe / prancha)."""
        cor = cor or C['rust']
        self.circle(x, y, r, fill='#fff', stroke=cor, sw=0.35)
        self.line(x - r + 0.4, y, x + r - 0.4, y, cor, 0.25)
        self.text(x, y - 0.75, det, size=6.2, weight=800, cor=cor, family='Outfit')
        self.text(x, y + 2.35, prancha, size=5.0, weight=600, cor=cor)

    def corte_marca(self, x1, y1, x2, y2, det, prancha, lado=1, cor=None):
        """Linha de corte com setas de visada e selos nas extremidades."""
        cor = cor or C['rust']
        self.line(x1, y1, x2, y2, cor, 0.35, dash='3 1 0.6 1')
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy * lado, ux * lado
        for (px, py), s in (((x1, y1), -1), ((x2, y2), 1)):
            # seta de visada
            ax, ay = px + nx * 3.2, py + ny * 3.2
            self.line(px, py, ax, ay, cor, 0.35)
            self.poly([(ax + nx * 1.4, ay + ny * 1.4), (ax + ux * 0.9, ay + uy * 0.9), (ax - ux * 0.9, ay - uy * 0.9)],
                      fill=cor)
            self.chamada(px + ux * s * 4.6, py + uy * s * 4.6, det, prancha, r=3.2, cor=cor)

    def seta_nota(self, x1, y1, x2, y2, cor=None, w=0.2):
        """Linha de chamada com ponto na origem (x1,y1) e cotovelo ate o texto (x2,y2)."""
        cor = cor or C['ink']
        self.circle(x1, y1, 0.55, fill=cor)
        self.line(x1, y1, x2, y2, cor, w)


def hatch_defs():
    """Padroes de hachura usados em todas as pranchas."""
    return f'''
<defs>
 <pattern id="hRU" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)">
   <rect width="1.6" height="1.6" fill="{C['ru']}"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="{C['ru_line']}" stroke-width="0.16"/></pattern>
 <pattern id="hRUp" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)">
   <rect width="1.6" height="1.6" fill="#e6f0df"/><line x1="0" y1="0" x2="0" y2="1.6" stroke="{C['ru_line']}" stroke-width="0.12" stroke-dasharray="0.5 0.35"/></pattern>
 <pattern id="hLaje" patternUnits="userSpaceOnUse" width="3" height="3">
   <rect width="3" height="3" fill="{C['laje']}"/><circle cx="0.8" cy="0.9" r="0.22" fill="#8d8a7e"/>
   <circle cx="2.2" cy="2.1" r="0.16" fill="#8d8a7e"/><path d="M1.9 0.5 l0.5 0.8 h-1z" fill="none" stroke="#8d8a7e" stroke-width="0.12"/></pattern>
 <pattern id="hAlv" patternUnits="userSpaceOnUse" width="2" height="2" patternTransform="rotate(45)">
   <rect width="2" height="2" fill="{C['alv']}"/><line x1="0" y1="0" x2="0" y2="2" stroke="#a09a86" stroke-width="0.18"/></pattern>
 <pattern id="hGesso" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
   <rect width="1.2" height="1.2" fill="{C['gesso']}"/><circle cx="0.6" cy="0.6" r="0.12" fill="#c9c3ae"/></pattern>
 <pattern id="hGessoRU" patternUnits="userSpaceOnUse" width="1.2" height="1.2">
   <rect width="1.2" height="1.2" fill="{C['ru']}"/><circle cx="0.6" cy="0.6" r="0.12" fill="{C['ru_line']}"/></pattern>
 <pattern id="hExt" patternUnits="userSpaceOnUse" width="2.4" height="2.4" patternTransform="rotate(-45)">
   <rect width="2.4" height="2.4" fill="#fff"/><line x1="0" y1="0" x2="0" y2="2.4" stroke="#dcd8ca" stroke-width="0.2"/></pattern>
 <pattern id="hCer" patternUnits="userSpaceOnUse" width="1" height="4">
   <rect width="1" height="4" fill="#e7eef0"/><line x1="0" y1="0" x2="1" y2="0" stroke="#8aa0a8" stroke-width="0.2"/></pattern>
 <linearGradient id="gLuz" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0" stop-color="{C['luz2']}" stop-opacity="0.55"/><stop offset="1" stop-color="{C['luz2']}" stop-opacity="0"/></linearGradient>
 <linearGradient id="gLuzH" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0" stop-color="{C['luz2']}" stop-opacity="0.55"/><stop offset="1" stop-color="{C['luz2']}" stop-opacity="0"/></linearGradient>
</defs>'''


# ====================================================== mapeamentos de coordenadas
class Planta:
    """Mapeia metros (sistema do caderno de iluminacao, y para baixo) em mm de papel."""
    def __init__(self, escala, ox, oy, x0=0.0, y0=0.0):
        self.k = 1000.0 / escala
        self.ox, self.oy, self.x0, self.y0 = ox, oy, x0, y0

    def P(self, x, y):
        return (self.ox + (x - self.x0) * self.k, self.oy + (y - self.y0) * self.k)

    def mm(self, m):
        return m * self.k


class Secao:
    """Mapeia metros (x para a direita, z para cima) em mm de papel. (ox, oy) = ponto x=0, z=0."""
    def __init__(self, escala, ox, oy):
        self.k = 1000.0 / escala
        self.ox, self.oy = ox, oy

    def P(self, x, z):
        return (self.ox + x * self.k, self.oy - z * self.k)

    def mm(self, m):
        return m * self.k

    def R(self, x0, z0, x1, z1):
        """Retangulo (mm) a partir de dois cantos em metros."""
        a = self.P(x0, z1)
        b = self.P(x1, z0)
        return a[0], a[1], b[0] - a[0], b[1] - a[1]


# ================================================================ desenho da planta-base
def paredes(v, pl, clip=None, cor=None):
    """Paredes (preenchidas) e linhas de esquadria/portas do caderno de iluminacao."""
    def dentro(x0, y0, x1, y1):
        if not clip:
            return True
        cx0, cy0, cx1, cy1 = clip
        return not (x1 < cx0 or x0 > cx1 or y1 < cy0 or y0 > cy1)
    for l in GEO['lines']:
        xs = []
        ys = []
        for s in l['segs']:
            for p in s[1:]:
                xs.append(p[0]); ys.append(p[1])
        bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
        if (by1 - by0) > 9 or (bx1 - bx0) > 9:
            continue  # muros e divisas do lote
        if (by0 > 19.95 and bx1 < 6.9) or by1 > 20.6:
            continue  # garagem (area externa)
        if bx0 > 12.1 or (bx0 < 1.0 and bx1 < 1.2):
            continue
        if not dentro(bx0, by0, bx1, by1):
            continue
        d = ''
        for s in l['segs']:
            if s[0] == 'l':
                a, b = pl.P(*s[1]), pl.P(*s[2])
                d += f'M{a[0]:.3f},{a[1]:.3f} L{b[0]:.3f},{b[1]:.3f} '
            elif s[0] == 'c':
                a, b, c2, e = (pl.P(*p) for p in s[1:])
                d += f'M{a[0]:.3f},{a[1]:.3f} C{b[0]:.3f},{b[1]:.3f} {c2[0]:.3f},{c2[1]:.3f} {e[0]:.3f},{e[1]:.3f} '
            elif s[0] == 're':
                a, b = pl.P(*s[1]), pl.P(*s[2])
                d += f'M{a[0]:.3f},{a[1]:.3f} H{b[0]:.3f} V{b[1]:.3f} H{a[0]:.3f} Z '
            elif s[0] == 'qu':
                pts = [pl.P(*p) for p in s[1:]]
                d += 'M' + ' L'.join(f'{x:.3f},{y:.3f}' for x, y in pts) + ' Z '
        w = 0.12 if (l['w'] or 0) < 0.5 else 0.16
        v.path(d, stroke=cor or '#8f8c7e', sw=w)
    for w in GEO['walls']:
        if w[3] > 20.6 or (w[1] > 19.95 and w[2] < 6.7 and w[3] > 20.2):
            continue
        if (w[2] - w[0]) > 0.3 and (w[3] - w[1]) > 0.3:
            continue  # halos de simbolos (nao sao paredes)
        if w[0] > 12.3:
            continue
        if not dentro(*w):
            continue
        a, b = pl.P(w[0], w[1]), pl.P(w[2], w[3])
        v.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=C['ink'])


# ---------------------------------------------------------------- simbolos de luminarias (indicativos)
def lum_simbolo(v, x, y, code, s=1.0, cor=None, rotulo=True):
    cor = cor or '#9b9788'
    r = 1.35 * s
    if code in ('L01', 'L02', 'L04'):
        v.circle(x, y, r, fill='#f1efe8', stroke=cor, sw=0.15)
        if code == 'L01':
            v.rect(x - 0.45 * s, y - 0.45 * s, 0.9 * s, 0.9 * s, fill=cor)
        elif code == 'L02':
            v.rect(x - 0.95 * s, y - 0.4 * s, 1.9 * s, 0.8 * s, fill=cor)
        else:
            v.rect(x - 0.55 * s, y - 0.55 * s, 1.1 * s, 1.1 * s, fill=cor)
    elif code == 'L05':
        v.rect(x - 1.5 * s, y - 1.5 * s, 3.0 * s, 3.0 * s, fill='#f1efe8', stroke=cor, sw=0.18)
        v.rect(x - 0.9 * s, y - 0.9 * s, 1.8 * s, 1.8 * s, stroke=cor, sw=0.15)
    elif code == 'L06':
        v.circle(x, y, r, fill='#f1efe8', stroke=cor, sw=0.15)
        v.line(x - r * 0.7, y, x + r * 0.7, y, cor, 0.15)
        v.line(x, y - r * 0.7, x, y + r * 0.7, cor, 0.15)
    elif code == 'L15':
        v.circle(x, y, r, fill='#fff', stroke=cor, sw=0.2)
        v.circle(x, y, r * 0.45, fill=cor)
    if rotulo:
        v.text(x + r + 0.5, y - r * 0.4, code, size=4.2, weight=700, cor=cor, anchor='start')


# ======================================================================= HTML
FONT_CSS = '''
@font-face{font-family:Manrope;font-weight:300;src:url(fonts/manrope-latin-300-normal.woff2)}
@font-face{font-family:Manrope;font-weight:400;src:url(fonts/manrope-latin-400-normal.woff2)}
@font-face{font-family:Manrope;font-weight:500;src:url(fonts/manrope-latin-500-normal.woff2)}
@font-face{font-family:Manrope;font-weight:600;src:url(fonts/manrope-latin-600-normal.woff2)}
@font-face{font-family:Manrope;font-weight:700;src:url(fonts/manrope-latin-700-normal.woff2)}
@font-face{font-family:Manrope;font-weight:800;src:url(fonts/manrope-latin-700-normal.woff2)}
@font-face{font-family:Outfit;font-weight:600;src:url(fonts/outfit-latin-600-normal.woff2)}
@font-face{font-family:Outfit;font-weight:700;src:url(fonts/outfit-latin-700-normal.woff2)}
@font-face{font-family:Outfit;font-weight:800;src:url(fonts/outfit-latin-800-normal.woff2)}
'''

CSS = FONT_CSS + f'''
@page{{size:594mm 420mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#e9e7e1}}
body{{font-family:Manrope,sans-serif;color:{C['ink']};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.sheet{{position:relative;width:594mm;height:420mm;background:#fff;overflow:hidden;page-break-after:always;margin:0 auto 10mm}}
@media print{{html,body{{background:#fff}}.sheet{{margin:0}}}}
.sheet>svg.dw{{position:absolute;left:0;top:0;width:594mm;height:420mm}}
.box{{position:absolute;border-radius:4.2mm;padding:5mm 5.4mm 4mm;overflow:hidden}}
.box h2{{font-family:Outfit;font-weight:800;font-size:17pt;letter-spacing:-0.2pt;line-height:1}}
.box .qn{{position:absolute;right:5.4mm;top:6mm;font-weight:700;font-size:8.5pt;letter-spacing:2.6pt}}
.b-creme{{background:{C['creme']}}}
.b-rust{{background:{C['rust']};color:{C['creme']}}}
.b-bege{{background:{C['bege']}}}
.b-olive{{background:{C['olive']};color:{C['creme']}}}
.box table{{width:100%;border-collapse:collapse;margin-top:4mm}}
.box th{{font-size:6.8pt;font-weight:700;text-align:left;letter-spacing:.2pt;padding:0 1.2mm 1.6mm 0;border-bottom:.25mm solid rgba(34,37,26,.18);vertical-align:bottom}}
.b-rust th{{border-bottom-color:rgba(245,231,196,.3)}}
.box td{{font-size:7.8pt;padding:1.45mm 1.2mm 1.45mm 0;border-bottom:.2mm solid rgba(34,37,26,.13);vertical-align:top;line-height:1.28}}
.b-rust td{{border-bottom-color:rgba(245,231,196,.18)}}
.box td.n{{text-align:right;white-space:nowrap}}
.box td .s{{display:block;color:{C['muted']};font-weight:300;font-size:7pt}}
.b-rust td .s{{color:rgba(245,231,196,.72)}}
.obs{{margin-top:4mm}}
.obs .i{{margin-bottom:2.3mm}}
.obs .t{{color:{C['rust']};font-weight:600;font-size:9.4pt;display:block;margin-bottom:.4mm}}
.obs p{{font-weight:300;font-size:8.6pt;line-height:1.3}}
.obs.small .t{{font-size:8.6pt}} .obs.small p{{font-size:7.9pt}}
.pill{{display:inline-block;border-radius:9mm;padding:.15mm 1.6mm;font-size:5.8pt;font-weight:700;letter-spacing:.3pt;vertical-align:1px;white-space:nowrap}}
.pill.prop{{border:.3mm solid {C['prop']};color:{C['prop']};background:#fff}}
.pill.doc{{background:{C['doc']};color:{C['creme']}}}
.pill.pend{{border:.3mm dashed {C['rust2']};color:{C['rust2']};background:#fff}}
.b-rust .pill.prop{{border-color:{C['creme']};color:{C['creme']};background:transparent}}
.b-rust .pill.doc{{background:{C['creme']};color:{C['rust']}}}
.leg{{display:grid;grid-template-columns:15mm 1fr;column-gap:2.4mm;row-gap:1.7mm;margin-top:4mm;align-items:center}}
.leg svg{{width:15mm;height:6.2mm;background:#fff;border-radius:1.4mm}}
.leg div{{font-size:7.7pt;line-height:1.2}}
.leg div .s{{display:block;font-size:6.8pt;font-weight:300;opacity:.85}}
.carimbo{{position:absolute;border-radius:4.2mm;background:{C['olive']};color:{C['creme']};padding:5.2mm 6mm}}
.carimbo .lg{{height:9.2mm}}
.carimbo .ct{{position:absolute;right:6mm;top:7mm;font-weight:700;font-size:8.5pt;letter-spacing:2.8pt}}
.carimbo .k{{font-weight:700;font-size:7.4pt;letter-spacing:.9pt;margin-top:2.3mm}}
.carimbo .v{{font-weight:300;font-size:9.6pt;line-height:1.3}}
.carimbo .pj{{font-family:Outfit;font-weight:800;font-size:14.5pt;line-height:1.15}}
.carimbo .g{{display:grid;grid-template-columns:1.25fr 0.6fr 0.55fr;column-gap:3mm}}
.carimbo .big{{font-weight:600;font-size:19pt;letter-spacing:.3pt;line-height:1.05}}
.carimbo .vv{{font-weight:600;font-size:10.4pt}}
.titulo{{position:absolute;display:flex;gap:3mm;align-items:flex-start}}
.titulo .num{{width:9.6mm;height:9.6mm;border-radius:50%;background:{C['rust']};color:{C['creme']};font-weight:700;font-size:10pt;display:flex;align-items:center;justify-content:center;flex:none;margin-top:.4mm}}
.titulo h1{{font-family:Outfit;font-weight:800;font-size:21pt;letter-spacing:-0.3pt;line-height:1.05}}
.titulo .sub{{font-weight:300;font-size:8.6pt;margin-top:1.2mm}}
.big td{{font-size:9.2pt;padding:2.1mm 1.4mm 2.1mm 0}} .big th{{font-size:7.6pt}} .big td .s{{font-size:8pt}}
.big .obs p{{font-size:9.4pt;line-height:1.38}} .big .obs .t{{font-size:10.4pt;margin-bottom:.8mm}} .big .obs .i{{margin-bottom:3.4mm}}
.aviso{{position:absolute;font-size:7pt;font-weight:600;letter-spacing:1.4pt;color:{C['rust']}}}
'''


def box(x, y, w, h, cls, titulo, qn, corpo):
    return (f'<div class="box {cls}" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm">'
            f'<h2>{titulo}</h2><div class="qn">{qn}</div>{corpo}</div>')


def carimbo(x, y, w, h, planta, escala, prancha, total, data='30/09/2026', rev='R01'):
    barra = ''.join(f'<rect x="{i*8}" y="0" width="8" height="1.8" fill="{C["creme"] if i%2==0 else "none"}" '
                    f'stroke="{C["creme"]}" stroke-width=".25"/>' for i in range(5))
    return f'''<div class="carimbo" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm">
 <img class="lg" src="imagens/logo_duas_creme.png"><div class="ct">CARIMBO</div>
 <div class="k">PROJETO</div><div class="pj">Residência Ivan e Ana Neris</div><div class="v">Nova Odessa – SP</div>
 <div class="k">RESPONSÁVEIS TÉCNICAS</div>
 <div class="v">Lidiane Barbosa · CAU A290220-6<br>Isadora Ferrari · CAU A263982-8</div>
 <div class="g" style="margin-top:.6mm">
  <div><div class="k">PLANTA</div><div class="vv">{planta}</div><div class="k">ESCALA</div><div class="vv">{escala}</div>
   <svg viewBox="0 0 40.5 2.2" style="width:40.5mm;height:2.2mm;margin-top:1.2mm">{barra}</svg>
   <div class="v" style="font-size:7pt;margin-top:.4mm">Imprimir em A2 sem ajuste de escala</div></div>
  <div><div class="k">DATA</div><div class="vv">{data}</div><div class="k">PRANCHA</div><div class="big">{prancha:02d}/{total:02d}</div></div>
  <div><div class="k">&nbsp;</div><div class="vv">&nbsp;</div><div class="k">REVISÃO</div><div class="big">{rev}</div></div>
 </div></div>'''


def titulo(x, y, num, nome, sub):
    return (f'<div class="titulo" style="left:{x}mm;top:{y}mm"><div class="num">{num}</div>'
            f'<div><h1>{nome}</h1><div class="sub">{sub}</div></div></div>')


def escala_grafica(v, x, y, escala, metros, marcas=None, h=1.5):
    """Barra de escala alternada (mesmo desenho do caderno de iluminacao)."""
    k = 1000.0 / escala
    marcas = marcas or list(range(0, int(metros) + 1))
    n = len(marcas) - 1
    for i in range(n):
        a, b = marcas[i], marcas[i + 1]
        v.rect(x + a * k, y, (b - a) * k, h, fill=C['ink'] if i % 2 == 0 else '#fff', stroke=C['ink'], sw=0.2)
    for m in marcas:
        s = (f'{m:g}'.replace('.', ',')) + (' m' if m == marcas[-1] else '')
        v.text(x + m * k, y + h + 3.0, s, size=6.2, weight=500)


def mini_titulo(v, x, y, cod, nome, escala, sub=None, prancha=None):
    """Titulo de desenho secundario: selo + nome + escala (sublinhado)."""
    v.circle(x + 3.4, y - 1.4, 3.4, fill=C['rust'])
    v.text(x + 3.4, y - 0.1, cod, size=7.2, weight=800, cor=C['creme'], family='Outfit')
    v.text(x + 8.6, y, nome, size=11.5, weight=800, family='Outfit', anchor='start')
    v.text(x + 8.6, y + 4.3, escala + (f'  ·  {sub}' if sub else ''), size=6.8, weight=400, anchor='start', cor=C['muted'])


def pagina(conteudo_svg, html_extra, W=PAGE_W, H=PAGE_H):
    moldura = f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="3" fill="none" stroke="{C["ink"]}" stroke-width="0.3"/>'
    return (f'<section class="sheet"><svg class="dw" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'{hatch_defs()}{moldura}{conteudo_svg}</svg>{html_extra}</section>')


def documento(secoes):
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>Caderno de Forro de Gesso</title><style>{CSS}</style></head><body>{"".join(secoes)}</body></html>')


def leg_svg(inner, w=15, h=6.2):
    return f'<svg viewBox="0 0 {w} {h}">{hatch_defs()}{inner}</svg>'
