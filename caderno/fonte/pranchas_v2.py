# -*- coding: utf-8 -*-
"""Gera caderno_hidraulica_v2.html (9 folhas A3 retrato) a partir de dados_hidraulica.py.
Layout e identidade visual replicam o Caderno de Detalhamento de Portas e Janelas
(mesma estrutura de carimbo, legenda, bloco de escala e Quadro final).
A representacao dos pontos em planta (pontos coloridos + cotas em vermelho com
linhas de chamada) segue a referencia do Portal Criativo.
Imprimir o PDF em A3 retrato sem ajuste de escala (ver imprimir_v2.mjs).
"""
import json, math, os, html
from dados_hidraulica import AMBIENTES, ORDEM, TIPOS, REV, DATA, CLIENTES, ENDERECO, RESP, ORIGEM

AQUI = os.path.dirname(os.path.abspath(__file__))
ZONAS = json.load(open(os.path.join(AQUI, 'zonas_dwg.json')))

# ---------------------------------------------------------------- paleta DUAS
C = dict(
    bg='#f5f0e2', ink='#22251a', rust='#9a3f2b', rust_t='#7a3423', olive='#3a3d2c',
    olive2='#4a4e37', cream='#f2ead0', line='#d9cfba', wall='#3a3d2c', porta='#fdfbf6',
    pend='#a83b2e',
)
# tipos de ponto hidraulico: cor de referencia (uso Brasil: azul=fria, vermelho=quente)
TCOR = dict(AF='#2f6fa1', AQ='#b23327', ESG='#a3672a', VD='#3f7a4f', RG='#2a2a24')

esc = lambda s: html.escape(str(s))
br = lambda v, n=2: (f'{v:.{n}f}').replace('.', ',')

PAGE_W, PAGE_H = 297.0, 420.0  # mm, A3 retrato


# ======================================================================= SVG
class Plano:
    """Desenho esquematico em mm de papel. Origem do ambiente = canto inferior-esquerdo."""
    def __init__(self, x0, y0, wmm, hmm, W, H, escala):
        self.x0, self.y0, self.wmm, self.hmm = x0, y0, wmm, hmm
        self.W, self.H, self.s = W, H, escala
        self.el = []

    def mm(self, m):
        return m * 1000 / self.s

    def P(self, x, y):
        return (self.x0 + self.mm(x), self.y0 + self.hmm - self.mm(y))

    def add(self, s):
        self.el.append(s)

    # ---- desenho basico
    def parede(self, pts, fechado=True):
        d = 'M' + ' L'.join(f'{self.P(*p)[0]:.2f},{self.P(*p)[1]:.2f}' for p in pts) + (' Z' if fechado else '')
        self.add(f'<path d="{d}" fill="{C["porta"]}" stroke="{C["wall"]}" stroke-width="2.4"/>')

    def linha(self, p1, p2, cor, w=0.5, dash=None):
        x1, y1 = self.P(*p1); x2, y2 = self.P(*p2)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{cor}" stroke-width="{w}"{da}/>')

    PT = 0.3528  # 1 pt em mm, para tratar `size` como pontos tipograficos

    def texto(self, x, y, s, size=8, weight=500, cor=None, anchor='middle', family='Manrope', rot=0):
        px, py = self.P(x, y)
        cor = cor or C['ink']
        tr = f' transform="rotate({rot} {px:.2f} {py:.2f})"' if rot else ''
        self.add(f'<text x="{px:.2f}" y="{py:.2f}" font-family="{family}" font-size="{size*self.PT:.2f}" font-weight="{weight}" '
                 f'fill="{cor}" text-anchor="{anchor}" dominant-baseline="middle"{tr}>{esc(s)}</text>')

    # ---- cota estilo Portal Criativo: linha vermelha fina + tiques + numero
    def cota_chain(self, p1, p2, valor, perp, offset, tick=2.6):
        x1, y1 = self.P(*p1); x2, y2 = self.P(*p2)
        ox, oy = perp[0] * offset, perp[1] * offset
        x1, y1, x2, y2 = x1 + ox, y1 + oy, x2 + ox, y2 + oy
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{C["rust"]}" stroke-width="0.45"/>')
        tx, ty = perp[1] * tick, -perp[0] * tick
        for xx, yy in ((x1, y1), (x2, y2)):
            self.add(f'<line x1="{xx-tx:.2f}" y1="{yy-ty:.2f}" x2="{xx+tx:.2f}" y2="{yy+ty:.2f}" stroke="{C["rust"]}" stroke-width="0.45"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        rot = -90 if abs(perp[0]) > abs(perp[1]) else 0
        bw = 2.6 + 1.15 * len(valor)
        bh = 3.4
        if rot:
            self.add(f'<rect x="{mx-bh/2:.2f}" y="{my-bw/2:.2f}" width="{bh:.2f}" height="{bw:.2f}" fill="{C["bg"]}"/>')
        else:
            self.add(f'<rect x="{mx-bw/2:.2f}" y="{my-bh/2:.2f}" width="{bw:.2f}" height="{bh:.2f}" fill="{C["bg"]}"/>')
        self.add(f'<text x="{mx:.2f}" y="{my+0.15:.2f}" font-family="Manrope" font-size="{7.6*self.PT:.2f}" font-weight="700" '
                 f'fill="{C["rust"]}" text-anchor="middle" dominant-baseline="middle"'
                 + (f' transform="rotate({rot} {mx:.2f} {my:.2f})"' if rot else '') + f'>{esc(valor)}</text>')

    def ponto(self, x, y, tipo, status, r=3.6):
        px, py = self.P(x, y)
        cor = TCOR[tipo]
        if status == 'confirmado':
            self.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" fill="{cor}" stroke="{C["bg"]}" stroke-width="0.7"/>')
        elif status == 'proposta':
            self.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" fill="{cor}" fill-opacity="0.35" stroke="{cor}" stroke-width="0.9"/>')
        else:
            self.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" fill="none" stroke="{C["pend"]}" stroke-width="0.9" stroke-dasharray="1.6 1.3"/>')
        return px, py

    def svg(self, wmm=None, hmm=None):
        w = wmm if wmm else self.wmm
        h = hmm if hmm else self.hmm
        return ''.join(self.el)


# ============================================================== icones fixos
def icone_bacia(pl, x, y, rot=0):
    """Bacia sanitaria simples: tanque + bacia oval, ponto de referencia = saida traseira."""
    g0 = len(pl.el)
    pl.add(f'<g>')
    px, py = pl.P(x, y)
    def R(dx, dy):
        a = math.radians(rot)
        return (dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a))
    tw, th = pl.mm(0.38), pl.mm(0.12)
    dx, dy = R(0, -th * 0.7)
    pl.add(f'<rect x="{px-tw/2+dx:.2f}" y="{py-th/2+dy:.2f}" width="{tw:.2f}" height="{th:.2f}" rx="1.2" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.6" transform="rotate({rot} {px:.2f} {py:.2f})"/>')
    bw, bh = pl.mm(0.36), pl.mm(0.40)
    dx2, dy2 = R(0, th * 0.55 + bh * 0.42)
    pl.add(f'<ellipse cx="{px+dx2:.2f}" cy="{py+dy2:.2f}" rx="{bw/2:.2f}" ry="{bh/2:.2f}" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.6" transform="rotate({rot} {px+dx2:.2f} {py+dy2:.2f})"/>')
    pl.add('</g>')


def icone_cuba(pl, x, y, w_m, rot=0):
    """Bancada + cuba (oval) + torneira (tracinho)."""
    px, py = pl.P(x, y)
    a = math.radians(rot)
    def R(dx, dy):
        return (dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a))
    cw, cd = pl.mm(w_m), pl.mm(0.55)
    dx, dy = R(0, cd * 0.05)
    pl.add(f'<rect x="{px-cw/2:.2f}" y="{py-cd/2:.2f}" width="{cw:.2f}" height="{cd:.2f}" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.6" transform="rotate({rot} {px:.2f} {py:.2f})"/>')
    ow, oh = cw * 0.42, cd * 0.5
    pl.add(f'<ellipse cx="{px:.2f}" cy="{py:.2f}" rx="{ow/2:.2f}" ry="{oh/2:.2f}" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.5" transform="rotate({rot} {px:.2f} {py:.2f})"/>')


def icone_chuveiro(pl, x, y, rot=0):
    px, py = pl.P(x, y)
    r = pl.mm(0.22)
    pl.add(f'<rect x="{px-r:.2f}" y="{py-r:.2f}" width="{2*r:.2f}" height="{2*r:.2f}" fill="none" '
           f'stroke="{C["ink"]}" stroke-width="0.55" stroke-dasharray="1.4 1" transform="rotate({rot} {px:.2f} {py:.2f})"/>')


def icone_tanque(pl, x, y, w_m, rot=0):
    px, py = pl.P(x, y)
    cw, cd = pl.mm(w_m), pl.mm(0.58)
    pl.add(f'<rect x="{px-cw/2:.2f}" y="{py-cd/2:.2f}" width="{cw:.2f}" height="{cd:.2f}" rx="2" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.6" transform="rotate({rot} {px:.2f} {py:.2f})"/>')


def icone_maquina(pl, x, y, rot=0):
    px, py = pl.P(x, y)
    s = pl.mm(0.60)
    pl.add(f'<rect x="{px-s/2:.2f}" y="{py-s/2:.2f}" width="{s:.2f}" height="{s:.2f}" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.6" transform="rotate({rot} {px:.2f} {py:.2f})"/>')
    pl.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{s*0.32:.2f}" fill="none" stroke="{C["ink"]}" stroke-width="0.5"/>')


def icone_geladeira(pl, x, y, rot=0):
    px, py = pl.P(x, y)
    w, d = pl.mm(0.65), pl.mm(0.65)
    pl.add(f'<rect x="{px-w/2:.2f}" y="{py-d/2:.2f}" width="{w:.2f}" height="{d:.2f}" '
           f'fill="none" stroke="{C["ink"]}" stroke-width="0.6" transform="rotate({rot} {px:.2f} {py:.2f})"/>')


ICONES = {
    'Chuveiro': (icone_chuveiro, {}),
    'Bacia sanitaria': (icone_bacia, {}),
    'Geladeira': (icone_geladeira, {}),
}


def desenha_icone(pl, nome, x, y, rot, w_hint=0.85):
    n = nome.lower()
    if 'chuveiro' in n:
        icone_chuveiro(pl, x, y, rot)
    elif 'bacia' in n:
        icone_bacia(pl, x, y, rot)
    elif 'cuba' in n or 'torneira de bancada' in n:
        icone_cuba(pl, x, y, w_hint, rot)
    elif 'maquina de lavar' in n or 'máquina de lavar' in n:
        icone_maquina(pl, x, y, rot)
    elif 'geladeira' in n:
        icone_geladeira(pl, x, y, rot)


# ==================================================================== paginas
def cabecalho_dados(titulo):
    return (f'<div class="hdr"><div class="hdr-tag">HIDRÁULICA · REVISÃO {REV}</div>'
            f'<div class="hdr-title">{esc(titulo)}</div></div>')


def carimbo(prancha_num, total, tipo_planta, escala_txt):
    resp_html = (f'<div><div class="cb-lbl">ARQ. RESPONSÁVEL</div><div class="cb-val">{esc(RESP[0][0])}<br>{esc(RESP[0][1])}</div></div>'
                 f'<div><div class="cb-lbl">ARQ. CORRESPONSÁVEL</div><div class="cb-val">{esc(RESP[1][0])}<br>{esc(RESP[1][1])}</div></div>')
    return f'''
<div class="carimbo">
  <div class="carimbo-top">
    <div class="carimbo-logo">DUAS<br><span>design &amp; arq</span></div>
    <div class="carimbo-pr"><div class="cb-lbl" style="color:{C['cream']};opacity:.75">FOLHA</div>
      <div class="carimbo-pr-num">{prancha_num}<span>/{total}</span></div></div>
  </div>
  <div class="carimbo-body">
    <div class="cb-lbl">TIPO</div>
    <div class="cb-val strong">{esc(tipo_planta)}</div>
    <div class="cb-lbl">OBRA</div>
    <div class="cb-val">Design de interiores de casa unifamiliar térrea</div>
    <div class="cb-row2">
      <div><div class="cb-lbl">CLIENTES</div><div class="cb-val">{esc(CLIENTES)}</div></div>
      <div><div class="cb-lbl">ENDEREÇO</div><div class="cb-val">{esc(ENDERECO)}</div></div>
    </div>
    <div class="cb-row2">{resp_html}</div>
    <div class="cb-row2">
      <div><div class="cb-lbl">DATA</div><div class="cb-val">{DATA}</div></div>
      <div><div class="cb-lbl">REVISÃO Nº</div><div class="cb-val">{REV} &nbsp; <span class="cb-lbl" style="display:inline">ESCALA</span> {esc(escala_txt)}</div></div>
    </div>
  </div>
  <div class="carimbo-bottom">CONFERIR AS MEDIDAS NO LOCAL</div>
</div>'''


def bloco_escala(escala_num, nota_extra=''):
    largura_barra = 60
    return f'''
<div class="side-block">
  <div class="side-title">ESCALA</div>
  <div class="escala-num">1/{escala_num}</div>
  <svg width="{largura_barra}mm" height="7mm" viewBox="0 0 {largura_barra} 7">
    <rect x="0" y="1" width="{largura_barra/3:.1f}" height="4" fill="{C['wall']}"/>
    <rect x="{largura_barra/3:.1f}" y="1" width="{largura_barra/3:.1f}" height="4" fill="#ffffff" stroke="{C['wall']}" stroke-width="0.3"/>
    <rect x="{2*largura_barra/3:.1f}" y="1" width="{largura_barra/3:.1f}" height="4" fill="{C['wall']}"/>
  </svg>
  <div class="escala-nota">Imprimir em A3 sem ajuste de escala.{(' ' + nota_extra) if nota_extra else ''}</div>
</div>'''


def bloco_legenda(itens_extra=None):
    itens = ''
    for k in ('AF', 'AQ', 'ESG', 'VD', 'RG'):
        t = TIPOS[k]
        itens += (f'<div class="leg-it"><span class="leg-sw" style="background:{TCOR[k]}"></span>'
                  f'<b>{esc(t["sigla"])}</b> {esc(t["nome"])}</div>')
    extra = itens_extra or ''
    return f'''
<div class="side-block">
  <div class="side-title">LEGENDA</div>
  {itens}
  <div class="leg-it"><span class="leg-sw" style="background:{TCOR['AF']}"></span>ponto confirmado</div>
  <div class="leg-it"><span class="leg-sw" style="background:{TCOR['AF']};opacity:.35;border:0.9px solid {TCOR['AF']}"></span>altura proposta (mercado) *</div>
  <div class="leg-it"><span class="leg-sw" style="background:transparent;border:1px dashed {C['pend']}"></span>eixo pendente de definição</div>
  {extra}
</div>'''


def bloco_referencia(texto):
    return f'''
<div class="side-block">
  <div class="side-title">REFERÊNCIA</div>
  <div class="ref-txt">{texto}</div>
</div>'''


def agrupar_pontos(pontos):
    grupos = {}
    ordem = []
    for p in pontos:
        chave = (round(p['x'], 2), round(p['y'], 2))
        if chave not in grupos:
            grupos[chave] = []
            ordem.append(chave)
        grupos[chave].append(p)
    return [(k, grupos[k]) for k in ordem]


def parede_mais_proxima(x, y, W, H):
    dl, dr, db, dt = x, W - x, y, H - y
    m = min(dl, dr, db, dt)
    if m == db:
        return 'baixo'
    if m == dt:
        return 'cima'
    if m == dl:
        return 'esquerda'
    return 'direita'


def desenha_cotas(pl, grupos, W, H):
    """Cadeia de cotas estilo Portal Criativo ao longo da parede com mais pontos confirmados."""
    baldes = {'baixo': [], 'cima': [], 'esquerda': [], 'direita': []}
    for (gx, gy), pts in grupos:
        if all(p['eixo_status'] != 'confirmado' for p in pts):
            continue
        lado = parede_mais_proxima(gx, gy, W, H)
        baldes[lado].append((gx, gy))
    lado_principal = max(baldes, key=lambda k: len(baldes[k]))
    pts = baldes[lado_principal]
    if not pts:
        return
    horizontal = lado_principal in ('baixo', 'cima')
    pts = sorted(set(pts), key=lambda p: p[0] if horizontal else p[1])
    coords = [p[0] if horizontal else p[1] for p in pts]
    total = W if horizontal else H
    seq = [0.0] + coords + [total]
    seq = sorted(set(round(v, 3) for v in seq))
    if horizontal:
        y0 = 0.0 if lado_principal == 'baixo' else H
        perp = (0, 1) if lado_principal == 'baixo' else (0, -1)
        offset = 11
        for a, b in zip(seq, seq[1:]):
            if b - a < 0.03:
                continue
            pl.cota_chain((a, y0), (b, y0), br(b - a), perp, offset)
    else:
        x0 = 0.0 if lado_principal == 'esquerda' else W
        perp = (-1, 0) if lado_principal == 'esquerda' else (1, 0)
        offset = 11
        for a, b in zip(seq, seq[1:]):
            if b - a < 0.03:
                continue
            pl.cota_chain((x0, a), (x0, b), br(b - a), perp, offset)


def folha_ambiente_v2(cod, amb, prancha_num, total):
    W, H = amb['W'], amb['H']
    plano_w, plano_h = 178, 320
    escala = max(W * 1000 / (plano_w - 30), H * 1000 / (plano_h - 30)) * 1.0
    wmm, hmm = W * 1000 / escala, H * 1000 / escala
    x0 = 20 + (plano_w - 30 - wmm) / 2
    y0 = 20 + (plano_h - 30 - hmm) / 2
    pl = Plano(x0, y0, wmm, hmm, W, H, escala)
    pl.parede([(0, 0), (W, 0), (W, H), (0, H)])

    grupos = agrupar_pontos(amb['pontos'])
    desenha_cotas(pl, grupos, W, H)

    for (gx, gy), pts in grupos:
        lado = parede_mais_proxima(gx, gy, W, H)
        rot = {'baixo': 0, 'cima': 180, 'esquerda': 90, 'direita': 270}[lado]
        nomes = [p['nome'] for p in pts]
        ux, uy = {'baixo': (0, 1), 'cima': (0, -1), 'esquerda': (1, 0), 'direita': (-1, 0)}[lado]
        perp = (-uy, ux)
        primeiro_com_icone = next((p for p in pts if any(k in p['nome'].lower() for k in
                                    ('chuveiro', 'bacia', 'cuba', 'torneira de bancada', 'tanquinho',
                                     'maquina de lavar', 'máquina de lavar', 'geladeira'))), None)
        eixo_pendente_grupo = any(p['eixo_status'] == 'pendente' for p in pts)
        if primeiro_com_icone and not eixo_pendente_grupo:
            desenha_icone(pl, primeiro_com_icone['nome'], gx + ux * 0.32, gy + uy * 0.32, rot)
        aguas = [(p, a) for p in pts for a in p['agua']]
        n = len(aguas)
        push = 0.18 if eixo_pendente_grupo else 0.30
        for i, (p, a) in enumerate(aguas):
            f = i - (n - 1) / 2
            dxm = ux * push + perp[0] * f * 0.20
            dym = uy * push + perp[1] * f * 0.20
            px, py = pl.ponto(gx + dxm, gy + dym, a['tipo'], a['status'])
        # rotulo textual: sigla(s) + altura(s), estilo Portal Criativo ("CA H=0,60")
        label_push = 0.34 if eixo_pendente_grupo else 0.60
        lx = gx + ux * label_push
        ly = gy + uy * label_push
        linhas = []
        for p2, a in aguas:
            marca = '*' if a['status'] == 'proposta' else ('?' if a['status'] == 'pendente' else '')
            hv = f"{br(a['altura'])}" if a.get('altura') is not None else '?'
            linhas.append(f"{TIPOS[a['tipo']]['sigla']} H={hv}{marca}")
        line_h_m = 4.4 * escala / 1000
        anchor = 'start' if ux >= 0 else 'end'
        if ux == 0:
            anchor = 'middle'
        for k, txt in enumerate(linhas):
            pl.texto(lx, ly - k * line_h_m, txt, size=6.4, weight=700, cor=C['rust_t'], anchor=anchor)
        if any(p['eixo_status'] == 'pendente' for p in pts):
            pl.texto(gx - ux * 0.55, gy - uy * 0.55, '?', size=9, weight=800, cor=C['pend'], anchor='middle')

    svg = (f'<svg width="{plano_w}mm" height="{plano_h}mm" viewBox="0 0 {plano_w} {plano_h}">'
           f'{pl.svg()}</svg>')

    ref_txt = 'Peça, altura, status e observações completas de cada ponto no Quadro de Pontos Hidráulicos, folha 09/09.'
    return f'''
<section class="sheet">
  <div class="plano-col">
    <div class="plano-wrap">{svg}</div>
    <div class="legenda-inline">
      <b>{esc(amb['nome'])}</b> · planta de pontos hidráulicos
    </div>
    <div class="escala-caption">ESCALA 1/{round(escala)}</div>
  </div>
  <div class="side-col">
    {bloco_legenda()}
    {bloco_referencia(ref_txt)}
    {bloco_escala(round(escala))}
  </div>
  {carimbo(prancha_num, total, f"Planta de pontos hidráulicos · {amb['nome']}", f"1/{round(escala)}")}
</section>'''


# fracoes (x,y) aproximadas do centro de cada ambiente na imagem de fundo (0-1)
CENTRO_BG = {
    'COZ': (0.17, 0.51), 'LAV': (0.17, 0.62), 'GOU': (0.46, 0.35),
    'WCE': (0.43, 0.28), 'WCS': (0.06, 0.14), 'WC1': (0.15, 0.25), 'WC2': (0.15, 0.35),
}


def folha_geral_v2(prancha_num, total):
    img_w_mm, img_h_mm = 190, 297
    x0, y0 = 14, 16
    itens = ''
    for cod in ORDEM:
        amb = AMBIENTES[cod]
        fx, fy = CENTRO_BG[cod]
        px, py = x0 + fx * img_w_mm, y0 + fy * img_h_mm
        itens += (f'<circle cx="{px:.2f}" cy="{py:.2f}" r="6.4" fill="{C["rust"]}" stroke="{C["bg"]}" stroke-width="0.8"/>'
                  f'<text x="{px:.2f}" y="{py+0.4:.2f}" font-family="Manrope" font-size="6.2" font-weight="700" '
                  f'fill="{C["cream"]}" text-anchor="middle" dominant-baseline="middle">{esc(amb["prancha"])}</text>')
    svg = (f'<svg width="{img_w_mm}mm" height="{img_h_mm}mm" viewBox="0 0 {img_w_mm} {img_h_mm}">'
           f'<image href="imagens/planta_geral_bg.jpg" x="0" y="0" width="{img_w_mm}" height="{img_h_mm}" '
           f'preserveAspectRatio="xMidYMid slice"/>{itens}</svg>')

    itens_idx = ''.join(
        f'<div class="idx-it"><span class="idx-badge">{AMBIENTES[c]["prancha"]}</span>{esc(AMBIENTES[c]["nome"])}'
        f'<span class="idx-n">{len(AMBIENTES[c]["pontos"])} pontos</span></div>' for c in ORDEM)

    return f'''
<section class="sheet">
  <div class="plano-col" style="width:{img_w_mm+6}mm">
    <div class="plano-wrap" style="left:{x0}mm;top:{y0}mm;position:absolute">{svg}</div>
    <div class="legenda-inline" style="position:absolute;left:{x0}mm;top:{y0+img_h_mm+4}mm">
      <b>Planta geral</b> · pontos hidráulicos por ambiente
    </div>
  </div>
  <div class="side-col">
    <div class="side-block">
      <div class="side-title">ÍNDICE DE PRANCHAS</div>
      {itens_idx}
    </div>
    {bloco_referencia('Posição dos selos nesta planta é esquemática, apenas para localizar o ambiente. Eixos, alturas e cotas de execução estão nas pranchas 02 a 08 (uma por ambiente) e no Quadro de Pontos Hidráulicos, folha 09/09.')}
    {bloco_escala(100, 'Planta-base: PROJETO IVAN E ANA - R01, LayOut SketchUp (maio/2026).')}
  </div>
  {carimbo(prancha_num, total, 'Planta geral de pontos hidráulicos', '1/100 aprox.')}
</section>'''


def folha_quadro_v2(prancha_num, total, codigos, titulo='Quadro de pontos hidráulicos'):
    linhas = ''
    for cod in codigos:
        amb = AMBIENTES[cod]
        linhas += f'<tr class="sub"><td colspan="7">{esc(amb["prancha"])} · {esc(amb["nome"]).upper()}</td></tr>'
        for p in amb['pontos']:
            for i, a in enumerate(p['agua']):
                t = TIPOS[a['tipo']]
                status_lbl = {'confirmado': 'Confirmado', 'proposta': 'Proposta *', 'pendente': 'Pendente'}[a['status']]
                status_cls = {'confirmado': 'st-ok', 'proposta': 'st-prop', 'pendente': 'st-pend'}[a['status']]
                altura_txt = f"{br(a['altura'])} m" if a.get('altura') is not None else '—'
                nome_cell = esc(p['nome']) if i == 0 else ''
                linhas += (f'<tr><td>{esc(p["id"]) if i==0 else ""}</td><td>{nome_cell}</td>'
                           f'<td><span class="dot" style="background:{TCOR[a["tipo"]]}"></span>{esc(t["sigla"])}</td>'
                           f'<td>{esc(altura_txt)}</td>'
                           f'<td><span class="st {status_cls}">{status_lbl}</span></td>'
                           f'<td>{esc("Confirmado" if p["eixo_status"]=="confirmado" else "Pendente")}</td>'
                           f'<td class="obs-cell">{esc(a.get("origem","") if a["status"]!="confirmado" else "")}</td></tr>')
    tabela = f'''<table class="quadro-final">
      <thead><tr><th>Pt.</th><th>Peça</th><th>Tipo</th><th>Altura</th><th>Status altura</th><th>Status eixo</th><th>Observação</th></tr></thead>
      <tbody>{linhas}</tbody></table>'''
    return f'''
<section class="sheet">
  {cabecalho_dados(titulo)}
  <div class="quadro-area quadro-area-full">{tabela}</div>
  {carimbo(prancha_num, total, 'Quadro de pontos hidráulicos · tabela', 'Sem escala')}
</section>'''


def folha_notas_v2(prancha_num, total):
    return f'''
<section class="sheet">
  {cabecalho_dados('Status, pendências e normas')}
  <div class="footnotes footnotes-full">
    <div class="fn-col">
      <div class="fn-title">STATUS</div>
      <div class="fn-it"><b>Confirmado</b> — dado do Caderno Detalhamento Hidráulico original (Revisão 02, 24/09/2026) ou decisão explícita do cliente em 28/09/2026. Pode ser executado.</div>
      <div class="fn-it"><b>Proposta *</b> — valor usual de mercado, adotado na ausência de cota no caderno original, a pedido do cliente (28/09/2026). Precisa de validação do responsável pelo projeto hidrossanitário antes da execução.</div>
      <div class="fn-it"><b>Pendente</b> — posição em planta sem cota no caderno original e sem base segura para propor. Afeta o eixo do ponto, não apenas a altura.</div>
    </div>
    <div class="fn-col">
      <div class="fn-title">PENDÊNCIAS EM ABERTO</div>
      <div class="fn-it">1. Posição da ilha da cozinha em relação à parede — necessária para converter o eixo do lava-louças. Falta medida direta ou modelo SketchUp detalhado da marcenaria.</div>
      <div class="fn-it">2. Afastamento da parede esquerda da cuba/torneira de bancada do Gourmet — não consta no caderno original.</div>
      <div class="fn-it">3. Prancha 01/02 do Caderno de Ar Condicionado — só foi recebida a 02/02; pode conter dreno de condensado que intercepte shafts hidráulicos.</div>
      <div class="fn-it">4. Eixo dos registros gerais (dentro dos armários) em todos os banheiros — posição de projeto, não um dado padronizável.</div>
      <div class="fn-it">5. WC Suíte Master: falta a cota de fechamento da cuba/torneira de bancada contra a parede lateral oposta.</div>
    </div>
  </div>
  <div class="normas-box normas-box-notas">
    <div class="normas-title">NORMAS DE REFERÊNCIA</div>
    <div class="normas-it"><b>NBR 5626</b> Instalações prediais de água fria.</div>
    <div class="normas-it"><b>NBR 7198</b> Instalações prediais de água quente.</div>
    <div class="normas-it"><b>NBR 8160</b> Sistemas prediais de esgoto sanitário.</div>
  </div>
  {carimbo(prancha_num, total, 'Quadro de pontos hidráulicos · status e pendências', 'Sem escala')}
</section>'''


def gerar():
    total = '11'
    folhas = [folha_geral_v2('01', total)]
    for i, cod in enumerate(ORDEM):
        folhas.append(folha_ambiente_v2(cod, AMBIENTES[cod], f'{i+2:02d}', total))
    folhas.append(folha_quadro_v2('09', total, ORDEM[:4], 'Quadro de pontos hidráulicos (1/2)'))
    folhas.append(folha_quadro_v2('10', total, ORDEM[4:], 'Quadro de pontos hidráulicos (2/2)'))
    folhas.append(folha_notas_v2('11', total))

    css = '''
@font-face{font-family:'Manrope';font-weight:400;src:url('fonts/manrope-latin-400-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-weight:500;src:url('fonts/manrope-latin-500-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-weight:600;src:url('fonts/manrope-latin-600-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-weight:700;src:url('fonts/manrope-latin-700-normal.woff2') format('woff2');}
@font-face{font-family:'Outfit';font-weight:600;src:url('fonts/outfit-latin-400-normal.woff2') format('woff2');}
@page{ size: 297mm 420mm; margin:0; }
*{box-sizing:border-box;}
body{margin:0;font-family:'Manrope',sans-serif;color:%(ink)s;}
.sheet{width:297mm;height:420mm;position:relative;overflow:hidden;background:%(bg)s;page-break-after:always;break-after:page;}
.sheet:last-child{page-break-after:auto;break-after:auto;}

.hdr{position:absolute;left:14mm;top:12mm;width:260mm;}
.hdr-tag{font-size:9pt;font-weight:700;letter-spacing:1.4pt;color:%(rust)s;}
.hdr-title{font-family:'Outfit',sans-serif;font-size:24pt;font-weight:600;color:%(ink)s;margin-top:1.5mm;}

.plano-col{position:absolute;left:12mm;top:12mm;width:184mm;height:404mm;}
.plano-wrap{border:0.3mm solid %(line)s;background:#fdfbf6;}
.legenda-inline{font-size:9pt;margin-top:2.5mm;color:%(ink)s;}
.escala-caption{font-size:8pt;color:%(olive)s;margin-top:0.8mm;letter-spacing:0.3pt;}

.side-col{position:absolute;right:12mm;top:12mm;width:80mm;}
.side-block{margin-bottom:6mm;}
.side-title{font-size:8.4pt;font-weight:700;letter-spacing:1pt;color:%(rust)s;margin-bottom:2.2mm;}
.leg-it{display:flex;align-items:center;gap:2.4mm;font-size:7.6pt;line-height:1.3;margin-top:1.7mm;}
.leg-sw{width:4.6mm;height:4.6mm;border-radius:50%%;flex:none;}
.ref-txt{font-size:7.6pt;line-height:1.42;color:%(olive)s;}
.escala-num{font-family:'Outfit',sans-serif;font-size:19pt;font-weight:600;color:%(ink)s;margin:1mm 0;}
.escala-nota{font-size:6.6pt;color:%(olive)s;margin-top:1.4mm;line-height:1.3;}

.idx-it{display:flex;align-items:center;gap:2.6mm;font-size:8.6pt;padding:1.6mm 0;border-bottom:0.25mm solid %(line)s;}
.idx-badge{width:6mm;height:6mm;border-radius:50%%;background:%(rust)s;color:%(cream)s;font-size:7pt;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;}
.idx-n{margin-left:auto;font-size:6.8pt;color:%(olive)s;}

.carimbo{position:absolute;right:12mm;bottom:10mm;width:80mm;border-radius:1.5mm;overflow:hidden;background:%(olive)s;color:%(cream)s;}
.carimbo-top{display:flex;justify-content:space-between;align-items:flex-start;padding:3mm 3.5mm 1.5mm;}
.carimbo-logo{font-family:'Outfit',sans-serif;font-size:11pt;font-weight:600;line-height:1;}
.carimbo-logo span{font-family:'Manrope';font-size:5.6pt;font-weight:500;display:block;letter-spacing:0.4pt;opacity:.8;}
.carimbo-pr{text-align:right;}
.carimbo-pr-num{font-family:'Outfit',sans-serif;font-size:15pt;font-weight:600;line-height:1;}
.carimbo-pr-num span{font-size:8pt;font-weight:500;opacity:.8;}
.carimbo-body{padding:0 3.5mm 2.5mm;}
.cb-lbl{font-size:5.6pt;font-weight:700;letter-spacing:0.4pt;opacity:.72;margin-top:2mm;}
.cb-val{font-size:7.4pt;font-weight:500;line-height:1.35;}
.cb-val.strong{font-weight:700;font-size:8.6pt;}
.cb-row2{display:flex;gap:3mm;}
.cb-row2>div{flex:1;}
.carimbo-bottom{background:%(rust)s;color:%(cream)s;font-size:6.2pt;font-weight:700;letter-spacing:0.4pt;text-align:center;padding:2mm;margin-top:1mm;}

.quadro-area{position:absolute;left:14mm;top:38mm;width:269mm;height:290mm;overflow:hidden;}
.quadro-area-full{height:362mm;width:269mm;}
table.quadro-final{border-collapse:collapse;width:100%%;font-size:7pt;}
table.quadro-final th{background:%(olive)s;color:%(cream)s;text-align:left;padding:1.3mm 2.2mm;font-size:6.6pt;}
table.quadro-final td{padding:1mm 2.2mm;border-bottom:0.2mm solid %(line)s;line-height:1.25;}
table.quadro-final tr.sub td{background:%(cream)s;color:%(rust_t)s;font-weight:700;font-size:7.2pt;padding-top:2mm;}
td.obs-cell{font-size:6.2pt;font-style:italic;color:#8a8266;}
.dot{display:inline-block;width:2.4mm;height:2.4mm;border-radius:50%%;margin-right:1.1mm;vertical-align:middle;}
.st{font-size:6.2pt;font-weight:700;padding:0.4mm 1.4mm;border-radius:2.6mm;white-space:nowrap;}
.st-ok{background:#dfe8d2;color:#3f5c2f;}
.st-prop{background:%(cream)s;color:%(rust_t)s;}
.st-pend{background:#f3d6d0;color:%(pend)s;}

.footnotes{position:absolute;left:14mm;top:322mm;width:185mm;display:flex;gap:8mm;}
.footnotes-full{top:42mm;width:269mm;gap:14mm;}
.fn-col{flex:1;}
.fn-title{font-size:9pt;font-weight:700;letter-spacing:0.8pt;color:%(rust)s;margin-bottom:3mm;}
.fn-it{font-size:8.4pt;line-height:1.55;margin-top:3.4mm;color:%(ink)s;}

.normas-box{position:absolute;left:14mm;bottom:10mm;width:170mm;background:%(cream)s;border-radius:2mm;padding:3mm 4mm;}
.normas-box-notas{width:199mm;bottom:auto;top:230mm;padding:4mm 5mm;}
.normas-title{font-size:7.4pt;font-weight:700;letter-spacing:0.6pt;color:%(rust_t)s;margin-bottom:1.6mm;}
.normas-it{font-size:7.2pt;line-height:1.4;margin-top:1mm;}
''' % C

    html_out = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
                f'<title>Caderno de Detalhamento Hidráulico — Pontos em Planta — {REV}</title>'
                f'<style>{css}</style></head><body>{"".join(folhas)}</body></html>')
    open(os.path.join(AQUI, 'caderno_hidraulica_v2.html'), 'w', encoding='utf-8').write(html_out)
    print('ok', len(folhas), 'folhas')


if __name__ == '__main__':
    gerar()
