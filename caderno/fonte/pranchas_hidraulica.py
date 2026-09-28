# -*- coding: utf-8 -*-
"""Gera caderno_hidraulica.html (9 folhas A2) a partir de dados_hidraulica.py.
Imprimir o PDF em A2 sem ajuste de escala (ver imprimir.mjs).
"""
import json, os, html
from dados_hidraulica import AMBIENTES, ORDEM, TIPOS, REV, DATA, CLIENTES, ENDERECO, RESP, ORIGEM

AQUI = os.path.dirname(os.path.abspath(__file__))
ZONAS = json.load(open(os.path.join(AQUI, 'zonas_dwg.json')))

C = dict(bg='#f7f2e8', ink='#22251a', rust='#903f2a', rust_t='#7a3423', olive='#3f422f',
         olive2='#4f5439', band='#ece4d4', cream='#f5e7c4', line='#d8cfbc', wall='#4a4638',
         pend='#b23b2e')

esc = lambda s: html.escape(str(s))
br = lambda v, n=2: (f'{v:.{n}f}').replace('.', ',')

PAGE_W, PAGE_H = 594.0, 420.0  # mm, A2 paisagem


class Plano:
    """Desenho esquematico simples (retangulo do ambiente + pontos), em mm de papel."""
    def __init__(self, x0mm, y0mm, wmm, hmm, W, H, escala):
        self.x0, self.y0, self.wmm, self.hmm = x0mm, y0mm, wmm, hmm
        self.W, self.H, self.s = W, H, escala
        self.el = []

    def mm(self, m):
        return m * 1000 / self.s

    def P(self, x, y):
        # origem do ambiente = canto inferior-esquerdo; y cresce para cima
        return (self.x0 + self.mm(x), self.y0 + self.hmm - self.mm(y))

    def add(self, s):
        self.el.append(s)

    def linha(self, p1, p2, cor, w=0.5, dash=None, cap='round'):
        x1, y1 = self.P(*p1); x2, y2 = self.P(*p2)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{cor}" stroke-width="{w}" stroke-linecap="{cap}"{da}/>')

    def rect_ambiente(self):
        x1, y1 = self.P(0, self.H); x2, y2 = self.P(self.W, 0)
        w = x2 - x1; h = y2 - y1
        self.add(f'<rect x="{x1:.2f}" y="{y1:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#fbf8f1" stroke="{C["wall"]}" stroke-width="2.6"/>')

    def texto(self, x, y, s, size=9.5, weight=500, cor=None, anchor='middle', rot=0, family='Manrope', dy=0):
        px, py = self.P(x, y); py += dy
        cor = cor or C['ink']
        tr = f' transform="rotate({rot} {px:.2f} {py:.2f})"' if rot else ''
        self.add(f'<text x="{px:.2f}" y="{py:.2f}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{cor}" text-anchor="{anchor}" dominant-baseline="middle"{tr}>{esc(s)}</text>')

    def badge(self, x, y, s, cor=C['rust'], tcor='#f5e7c4', d=15, tracejado=False):
        px, py = self.P(x, y)
        dash = ' stroke-dasharray="3 2.5"' if tracejado else ''
        stroke = f' stroke="{C["pend"]}" stroke-width="1.6"{dash}' if tracejado else ''
        if len(s) <= 1:
            r = d / 2
            self.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" fill="{cor}"{stroke}/>')
        else:
            w = d + 4.6 * (len(s) - 1)
            h = d
            self.add(f'<rect x="{px-w/2:.2f}" y="{py-h/2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{h/2:.2f}" fill="{cor}"{stroke}/>')
        self.add(f'<text x="{px:.2f}" y="{py+0.5:.2f}" font-family="Manrope" font-size="7.6" font-weight="700" '
                 f'fill="{tcor}" text-anchor="middle" dominant-baseline="middle">{esc(s)}</text>')

    def ponto_agua(self, x, y, tipo, dx, dy, r=5.2):
        px, py = self.P(x, y)
        px += dx; py += dy
        cor = TIPOS[tipo]['cor']
        self.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r}" fill="{cor}" stroke="{C["bg"]}" stroke-width="1.2"/>')

    def cota(self, p1, p2, valor, offset=18, lado='baixo'):
        x1, y1 = self.P(*p1); x2, y2 = self.P(*p2)
        if lado == 'baixo':
            y1 += offset; y2 += offset
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{C["rust"]}" stroke-width="0.6"/>')
        for xx, yy in ((x1, y1), (x2, y2)):
            self.add(f'<line x1="{xx:.2f}" y1="{yy-3:.2f}" x2="{xx:.2f}" y2="{yy+3:.2f}" stroke="{C["rust"]}" stroke-width="0.6"/>')
        mx = (x1 + x2) / 2
        self.add(f'<rect x="{mx-16:.1f}" y="{y1-7:.1f}" width="32" height="11" fill="{C["bg"]}"/>')
        self.add(f'<text x="{mx:.2f}" y="{y1:.2f}" font-family="Manrope" font-size="7.6" font-weight="600" '
                 f'fill="{C["rust_t"]}" text-anchor="middle" dominant-baseline="middle">{esc(valor)}</text>')

    def svg(self):
        return ''.join(self.el)


def cabecalho(prancha_num, total, disciplina, titulo, subtitulo):
    return f'''
<div class="hdr">
  <div class="hdr-tag">PRANCHA {prancha_num}/{total} · {esc(disciplina)}</div>
  <div class="hdr-title">{esc(titulo)}</div>
  <div class="hdr-sub">{esc(subtitulo)}</div>
</div>'''


def carimbo(prancha_num, total, tipo_planta, escala_txt):
    resp_html = ''.join(f'<div class="resp-row">{esc(n)} · {esc(c)}</div>' for n, c in RESP)
    return f'''
<div class="carimbo">
  <div class="carimbo-top">
    <div class="carimbo-logo">DUAS<br><span>design &amp; arq</span></div>
    <div class="carimbo-pr">
      <div class="carimbo-pr-num">{prancha_num}<span>/{total}</span></div>
      <div class="carimbo-pr-rev">REVISÃO {REV}</div>
    </div>
  </div>
  <div class="carimbo-body">
    <div class="cb-lbl">PROJETO</div>
    <div class="cb-val strong">Residência IC · Detalhamento de pontos hidráulicos</div>
    <div class="cb-row2">
      <div><div class="cb-lbl">CLIENTES</div><div class="cb-val">{esc(CLIENTES)}</div></div>
      <div><div class="cb-lbl">ENDEREÇO</div><div class="cb-val">{esc(ENDERECO)}</div></div>
    </div>
    <div class="cb-lbl">TIPO DE PLANTA</div>
    <div class="cb-val">{esc(tipo_planta)}</div>
    <div class="cb-lbl">RESPONSÁVEIS TÉCNICOS (projeto de interiores)</div>
    <div class="cb-val">{resp_html}</div>
    <div class="cb-row2">
      <div><div class="cb-lbl">DATA</div><div class="cb-val">{DATA}</div></div>
      <div><div class="cb-lbl">ESCALA</div><div class="cb-val">{esc(escala_txt)}</div></div>
    </div>
    <div class="cb-lbl">ORIGEM</div>
    <div class="cb-val small">{esc(ORIGEM)}</div>
  </div>
  <div class="carimbo-bottom">CONFERIR AS MEDIDAS SINALIZADAS COMO PROPOSTA/PENDÊNCIA ANTES DE EXECUTAR · VÁLIDO EM A2 A 100%</div>
</div>'''


def legenda():
    itens = ''
    for k in ('AF', 'AQ', 'ESG', 'VD', 'RG'):
        t = TIPOS[k]
        itens += (f'<div class="leg-it"><span class="leg-sw" style="background:{t["cor"]}"></span>'
                  f'<b>{esc(t["sigla"])}</b> {esc(t["nome"])}</div>')
    itens += ('<div class="leg-it"><span class="leg-badge">1</span>Selo numerado do ponto '
              '(remete ao quadro de pontos)</div>')
    itens += ('<div class="leg-it"><span class="leg-badge pend">1</span>Selo tracejado: posição '
              'em planta NÃO COTADA no caderno original — esquemática, não cotar em obra</div>')
    return f'''
<div class="panel">
  <div class="panel-title">Legenda</div>
  {itens}
  <div class="leg-note"><b>Confirmado</b> · dado do caderno original, Revisão 02.<br>
  <b>Proposta</b> · valor usual de mercado adotado por nós (não consta no original) — marcado com asterisco (*) no quadro de pontos, a validar com o responsável hidrossanitário.<br>
  <b>Pendênte</b> · posição de projeto sem informação suficiente para propor — aguarda definição.</div>
</div>'''


def quadro_pontos(amb):
    cards = ''
    for p in amb['pontos']:
        linhas = ''
        for a in p['agua']:
            t = TIPOS[a['tipo']]
            marca = '*' if a['status'] == 'proposta' else ('—' if a['status'] == 'pendente' else '')
            altura_txt = f"{br(a['altura'])} m" if a.get('altura') is not None else 'a definir'
            origem = a.get('origem', '')
            cls = 'v-proposta' if a['status'] == 'proposta' else ('v-pendente' if a['status'] == 'pendente' else '')
            linhas += (f'<div class="qp-agua {cls}"><span class="qp-dot" style="background:{t["cor"]}"></span>'
                       f'<b>{esc(t["sigla"])}</b> {esc(altura_txt)}{marca}'
                       + (f'<div class="qp-origem">{esc(origem)}</div>' if origem else '') + '</div>')
        eixo_cls = ' eixo-pendente' if p['eixo_status'] == 'pendente' else ''
        badge_num = ('<span class="qp-num pend">' + esc(p['id']) + '</span>') if p['eixo_status'] == 'pendente' else ('<span class="qp-num">' + esc(p['id']) + '</span>')
        cards += (f'<div class="qp-card">'
                  f'<div class="qp-head">{badge_num}<b>{esc(p["nome"])}</b></div>'
                  f'<div class="qp-eixo{eixo_cls}">EIXO {esc(p["eixo_txt"])}</div>'
                  f'<div class="qp-aguas">{linhas}</div></div>')
    return f'<div class="panel qp-panel"><div class="panel-title">Quadro de pontos</div>{cards}</div>'


def observacoes(amb):
    itens = ''.join(f'<div class="ob-it"><span class="ob-num">{i+1}</span>{esc(o)}</div>' for i, o in enumerate(amb['obs']))
    return f'<div class="panel"><div class="panel-title">Observações técnicas</div>{itens}</div>'


def escala_dims(W, H, disp_w_mm, disp_h_mm):
    return min(disp_w_mm / W, disp_h_mm / H) and (W * 1000 / disp_w_mm)


def folha_ambiente(codigo, amb, prancha_num, total):
    W, H = amb['W'], amb['H']
    # area de desenho: bloco esquerdo, ~230mm largura util, ~230mm altura util
    disp_w, disp_h = 225, 225
    escala = max(W * 1000 / disp_w, H * 1000 / disp_h) * 1.35
    wmm, hmm = W * 1000 / escala, H * 1000 / escala
    x0 = 30 + (disp_w - wmm) / 2
    y0 = 88 + (disp_h - hmm) / 2
    pl = Plano(x0, y0, wmm, hmm, W, H, escala)
    pl.rect_ambiente()
    # porta esquematica (arco simples) no canto informado
    pl.texto(W / 2, H + 0.32, 'PLANTA DE EIXOS HIDRÁULICOS · ESC 1/' + str(round(escala)), size=9, weight=700, cor=C['rust_t'], anchor='middle')
    grupos = {}
    for p in amb['pontos']:
        chave = (round(p['x'], 2), round(p['y'], 2))
        grupos.setdefault(chave, []).append(p)
    for (gx, gy), pts in grupos.items():
        ids = '·'.join(p['id'] for p in pts)
        trace = any(p['eixo_status'] == 'pendente' for p in pts)
        pl.badge(gx, gy, ids, tracejado=trace)
        aguas = [a for p in pts for a in p['agua']]
        # empurra os pontos de agua para longe da parede mais proxima (regra do menor afastamento)
        dl, dr, db, dt = gx, W - gx, gy, H - gy
        m = min(dl, dr, db, dt)
        if m == db:
            ux, uy = 0, 1
        elif m == dt:
            ux, uy = 0, -1
        elif m == dl:
            ux, uy = 1, 0
        else:
            ux, uy = -1, 0
        perp = (-uy, ux)
        n = len(aguas)
        for i, a in enumerate(aguas):
            f = (i - (n - 1) / 2)
            dx = ux * 19 + perp[0] * f * 11
            dy = -(uy * 19 + perp[1] * f * 11)  # tela: y cresce p/ baixo
            pl.ponto_agua(gx, gy, a['tipo'], dx, dy)
    # escala grafica
    bx0, by0 = x0, y0 + hmm + 14
    for i in range(3):
        cor = C['wall'] if i % 2 == 0 else '#ffffff'
        pl.add(f'<rect x="{bx0+i*(1000/escala):.2f}" y="{by0:.2f}" width="{1000/escala:.2f}" height="4" fill="{cor}" stroke="{C["wall"]}" stroke-width="0.4"/>')
    pl.texto(0, 0, '', size=1)  # no-op mantem metodo
    pl.add(f'<text x="{bx0:.2f}" y="{by0+13:.2f}" font-family="Manrope" font-size="7" fill="{C["ink"]}">0</text>')
    pl.add(f'<text x="{bx0+3*(1000/escala):.2f}" y="{by0+13:.2f}" font-family="Manrope" font-size="7" fill="{C["ink"]}">3 m</text>')

    svg = (f'<svg width="{disp_w+60}mm" height="{disp_h+50}mm" viewBox="0 0 {disp_w+60} {disp_h+50}" '
           f'style="position:absolute;left:0;top:0">{pl.svg()}</svg>')

    return f'''
<section class="sheet">
  {cabecalho(prancha_num, total, 'HIDRÁULICA', amb['nome'], 'Planta de eixos · pontos de água fria, água quente e esgoto')}
  <div class="ref-parede">{esc(amb['parede_ref'])}</div>
  <div class="plano-area">{svg}</div>
  <div class="col-esq">{quadro_pontos(amb)}</div>
  <div class="col-dir">{legenda()}{observacoes(amb)}</div>
  {carimbo(prancha_num, total, f"Planta de eixos hidráulicos · {amb['nome']}", f"1/{round(escala)} (esquemático, reduzido para A2)")}
</section>'''


def folha_geral(prancha_num, total):
    xs = [p[0] for z in ZONAS.values() for p in z['pts']]
    ys = [p[1] for z in ZONAS.values() for p in z['pts']]
    x0d, y0d, x1d, y1d = min(xs), min(ys), max(xs), max(ys)
    Wt, Ht = x1d - x0d, y1d - y0d
    disp_h = 290
    escala = (Ht * 1000 / disp_h) * 1.05
    wmm, hmm = Wt * 1000 / escala, Ht * 1000 / escala
    x0, y0 = 40, 88
    svg_w, svg_h = max(x0 + wmm + 40, 200), y0 + hmm + 34

    class PlanoGeral(Plano):
        def P(self, x, y):
            return (self.x0 + (x - x0d) * 1000 / self.s, self.y0 + self.hmm - (y - y0d) * 1000 / self.s)

    pl = PlanoGeral(x0, y0, wmm, hmm, Wt, Ht, escala)
    cod2zona = {'COZ': 'COZ', 'GOU': 'VAR', 'LAV': 'LAV', 'WC1': 'W01', 'WC2': 'W02', 'WCS': 'BCA', 'WCE': 'BEX'}
    zona2cod = {v: k for k, v in cod2zona.items()}
    for zid, z in ZONAS.items():
        pts = z['pts']
        d = 'M' + ' L'.join(f'{pl.P(*p)[0]:.2f},{pl.P(*p)[1]:.2f}' for p in pts) + ' Z'
        molhado = zid in cod2zona.values()
        fill = '#f4e6c9' if molhado else '#fbf8f1'
        pl.add(f'<path d="{d}" fill="{fill}" stroke="{C["wall"]}" stroke-width="1.4"/>')
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        px, py = pl.P(cx, cy)
        # bounding box em mm de papel, so rotula se houver espaco legivel
        xs_p = [pl.P(*p)[0] for p in pts]; ys_p = [pl.P(*p)[1] for p in pts]
        bw, bh = max(xs_p) - min(xs_p), max(ys_p) - min(ys_p)
        if molhado:
            continue  # nome do ambiente molhado fica só no selo + índice, evita sobreposição
        if bw > 26 and bh > 11:
            nome_curto = z['nome'].replace('Circulação Interna', 'Circulação').replace(' / Sala Jantar', '/Jantar')
            pl.add(f'<text x="{px:.2f}" y="{py:.2f}" font-family="Manrope" font-size="3.1" font-weight="600" '
                   f'fill="{C["olive"]}" text-anchor="middle" dominant-baseline="middle">{esc(nome_curto)}</text>')
    for cod in ORDEM:
        amb = AMBIENTES[cod]
        zid = cod2zona[cod]
        z = ZONAS[zid]
        pts = z['pts']
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        px, py = pl.P(cx, cy)
        pl.add(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="6.4" fill="{C["rust"]}" stroke="{C["bg"]}" stroke-width="0.8"/>'
               f'<text x="{px:.2f}" y="{py+0.4:.2f}" font-family="Manrope" font-size="6" font-weight="700" '
               f'fill="{C["cream"]}" text-anchor="middle" dominant-baseline="middle">{amb["prancha"]}</text>')

    bx0, by0 = x0, y0 + hmm + 16
    for i in range(3):
        cor = C['wall'] if i % 2 == 0 else '#ffffff'
        pl.add(f'<rect x="{bx0+i*(2000/escala):.2f}" y="{by0:.2f}" width="{2000/escala:.2f}" height="4" fill="{cor}" stroke="{C["wall"]}" stroke-width="0.4"/>')
    pl.add(f'<text x="{bx0:.2f}" y="{by0+13:.2f}" font-family="Manrope" font-size="7" fill="{C["ink"]}">0</text>')
    pl.add(f'<text x="{bx0+3*(2000/escala):.2f}" y="{by0+13:.2f}" font-family="Manrope" font-size="7" fill="{C["ink"]}">6 m</text>')
    pl.add(f'<text x="{x0:.2f}" y="{y0-8:.2f}" font-family="Manrope" font-size="9" font-weight="700" '
           f'fill="{C["rust_t"]}">PLANTA GERAL · ESC 1/{round(escala)}</text>')

    svg = f'<svg width="{svg_w:.1f}mm" height="{svg_h:.1f}mm" viewBox="0 0 {svg_w:.1f} {svg_h:.1f}" style="position:absolute;left:0;top:0">{pl.svg()}</svg>'

    itens_idx = ''.join(
        f'<div class="idx-it"><span class="idx-badge">{AMBIENTES[c]["prancha"]}</span>{esc(AMBIENTES[c]["nome"])}'
        f'<span class="idx-n">{len(AMBIENTES[c]["pontos"])} pontos</span></div>' for c in ORDEM)

    return f'''
<section class="sheet">
  {cabecalho(prancha_num, total, 'HIDRÁULICA', 'Planta geral de pontos hidráulicos', 'Visão de conjunto · base de paredes: PROJETO IVAN E ANA - R01.dwg, camada PLANTA DE PISO')}
  <div class="plano-area">{svg}</div>
  <div class="col-idx">
    <div class="panel">
      <div class="panel-title">Índice de pranchas</div>
      {itens_idx}
      <div class="leg-note">Esta planta geral tem finalidade de localização e coordenação entre ambientes (prumadas, shafts compartilhados). As cotas de execução de cada ponto estão nas pranchas 01 a 07, não nesta.</div>
    </div>
  </div>
  <div class="col-dir">
    <div class="panel">
      <div class="panel-title">Observações técnicas</div>
      <div class="ob-it"><span class="ob-num">1</span>Base de paredes e ambientes extraída do DWG "PROJETO IVAN E ANA - R01.dwg" (mesmo arquivo usado no Caderno de Detalhamento de Piso), camada geométrica "PLANTA DE PISO", em metros. Confirmado pelo cliente como planta-base (28/09/2026).</div>
      <div class="ob-it"><span class="ob-num">2</span>O DWG NÃO contém pontos hidráulicos internos: as únicas camadas de água/esgoto do arquivo ("Esgoto", "AGUAS PLUVIAIS") estão na planta de implantação (ligação à rede pública), não na planta de piso. Os pontos aqui representados vêm do caderno hidráulico original e das propostas sinalizadas nas pranchas 01 a 07.</div>
      <div class="ob-it"><span class="ob-num">3</span>Ambientes hachurados em tom mais escuro: os 7 ambientes com pontos hidráulicos detalhados neste caderno.</div>
      <div class="ob-it"><span class="ob-num">4</span>Nomenclatura do DWG difere em alguns casos da adotada nas pranchas de detalhe (ex.: "Banheiro Casal" no DWG = "WC Suíte Master" aqui; "Varanda Gourmet" no DWG = "Gourmet" aqui) — mantida a nomenclatura do caderno hidráulico original por decisão do cliente.</div>
    </div>
  </div>
  {carimbo(prancha_num, total, 'Planta geral de pontos hidráulicos', f'1/{round(escala)} (esquemático, reduzido para A2)')}
</section>'''


def folha_quadro_final(prancha_num, total):
    linhas = ''
    for cod in ORDEM:
        amb = AMBIENTES[cod]
        for p in amb['pontos']:
            for a in p['agua']:
                t = TIPOS[a['tipo']]
                status_lbl = {'confirmado': 'Confirmado', 'proposta': 'Proposta', 'pendente': 'Pendente'}[a['status']]
                status_cls = {'confirmado': 'st-ok', 'proposta': 'st-prop', 'pendente': 'st-pend'}[a['status']]
                eixo_lbl = 'Pendente' if p['eixo_status'] == 'pendente' else 'Confirmado'
                eixo_cls = 'st-pend' if p['eixo_status'] == 'pendente' else 'st-ok'
                altura_txt = f"{br(a['altura'])} m" if a.get('altura') is not None else '—'
                linhas += (f'<tr><td>{esc(amb["prancha"])}</td><td>{esc(amb["nome"])}</td>'
                           f'<td>{esc(p["id"])}</td><td>{esc(p["nome"])}</td>'
                           f'<td><span class="dot" style="background:{t["cor"]}"></span>{esc(t["sigla"])}</td>'
                           f'<td>{esc(altura_txt)}</td>'
                           f'<td><span class="st {status_cls}">{status_lbl}</span></td>'
                           f'<td><span class="st {eixo_cls}">{eixo_lbl}</span></td></tr>')
    tabela = f'''<table class="quadro-final">
      <thead><tr><th>Pr.</th><th>Ambiente</th><th>Pt.</th><th>Peça</th><th>Tipo</th><th>Altura</th><th>Status altura</th><th>Status eixo</th></tr></thead>
      <tbody>{linhas}</tbody></table>'''
    return f'''
<section class="sheet">
  {cabecalho(prancha_num, total, 'HIDRÁULICA', 'Quadro consolidado e pendências', 'Todos os pontos da casa · conferir status antes da execução')}
  <div class="quadro-final-area">{tabela}</div>
  <div class="col-dir-full">
    <div class="panel">
      <div class="panel-title">Como usar este quadro</div>
      <div class="ob-it"><span class="ob-num">1</span><b>Confirmado</b>: dado do caderno hidráulico original (Revisão 02) ou decisão explícita do cliente em 28/09/2026. Pode ser executado.</div>
      <div class="ob-it"><span class="ob-num">2</span><b>Proposta</b>: valor usual de mercado, adotado por nós na ausência de cota no caderno original, sinalizado a pedido do cliente. Precisa de validação do responsável pelo projeto hidrossanitário antes da execução.</div>
      <div class="ob-it"><span class="ob-num">3</span><b>Pendênte</b>: posição em planta sem cota no caderno original e sem base segura para propor (afeta o eixo/posição do ponto, não apenas a altura) — ver observações da prancha do ambiente.</div>
      <div class="ob-it"><span class="ob-num">4</span>Pendências em aberto que dependem de arquivo ainda não recebido: modelo SketchUp (posição da ilha da cozinha); prancha 01/02 do caderno de ar condicionado (possível interferência de dreno de condensado); afastamento da parede esquerda da bancada do Gourmet.</div>
    </div>
  </div>
  {carimbo(prancha_num, total, 'Quadro consolidado de pontos hidráulicos', 'sem escala (tabela)')}
</section>'''


def gerar():
    total = '08'
    folhas = [folha_geral('00', total)]
    for cod in ORDEM:
        amb = AMBIENTES[cod]
        folhas.append(folha_ambiente(cod, amb, amb['prancha'], total))
    folhas.append(folha_quadro_final('08', total))

    css = '''
@font-face{font-family:'Manrope';font-weight:400;src:url('fonts/manrope-latin-400-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-weight:500;src:url('fonts/manrope-latin-500-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-weight:600;src:url('fonts/manrope-latin-600-normal.woff2') format('woff2');}
@font-face{font-family:'Manrope';font-weight:700;src:url('fonts/manrope-latin-700-normal.woff2') format('woff2');}
@page{ size: 594mm 420mm; margin:0; }
*{box-sizing:border-box;}
body{margin:0;font-family:'Manrope',sans-serif;color:%(ink)s;}
.sheet{width:594mm;height:420mm;position:relative;overflow:hidden;background:%(bg)s;page-break-after:always;break-after:page;}
.sheet:last-child{page-break-after:auto;break-after:auto;}
.hdr{position:absolute;left:14mm;top:10mm;width:420mm;}
.hdr-tag{font-size:10.5pt;font-weight:700;letter-spacing:1.6pt;color:%(rust)s;}
.hdr-title{font-size:27pt;font-weight:700;color:%(ink)s;margin-top:1mm;}
.hdr-sub{font-size:10pt;font-weight:500;color:%(olive)s;margin-top:1mm;max-width:400mm;}
.ref-parede{position:absolute;left:14mm;top:34mm;width:300mm;font-size:8.6pt;color:%(olive)s;font-weight:500;line-height:1.35;background:%(band)s;border-radius:2mm;padding:2.5mm 4mm;}
.plano-area{position:absolute;left:0mm;top:0mm;}
.col-esq{position:absolute;left:14mm;top:318mm;width:270mm;}
.col-idx{position:absolute;left:200mm;top:88mm;width:220mm;}
.col-dir{position:absolute;right:14mm;top:10mm;width:150mm;}
.col-dir-full{position:absolute;right:14mm;top:60mm;width:150mm;}
.panel{background:#fdfbf6;border:0.4mm solid %(line)s;border-radius:3mm;padding:4mm 5mm;margin-bottom:4mm;}
.panel-title{font-size:11pt;font-weight:700;color:%(rust_t)s;margin-bottom:2.5mm;border-bottom:0.4mm solid %(line)s;padding-bottom:1.5mm;}
.leg-it{display:flex;align-items:center;gap:2.5mm;font-size:7.6pt;line-height:1.3;margin-top:1.6mm;}
.leg-sw{width:5mm;height:5mm;border-radius:50%%;flex:none;}
.leg-badge{width:5mm;height:5mm;border-radius:50%%;background:%(rust)s;color:%(cream)s;font-size:6pt;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;}
.leg-badge.pend{background:transparent;border:1px dashed %(pend)s;color:%(pend)s;}
.leg-note{font-size:7pt;color:%(olive)s;line-height:1.4;margin-top:2.5mm;}
.qp-panel{column-count:2;column-gap:6mm;}
.qp-card{break-inside:avoid;background:%(band)s;border-radius:2.5mm;padding:2.5mm 3.5mm;margin-bottom:2.5mm;}
.qp-head{display:flex;align-items:center;gap:2mm;font-size:8.6pt;font-weight:700;margin-bottom:1mm;}
.qp-num{width:5.5mm;height:5.5mm;border-radius:50%%;background:%(rust)s;color:%(cream)s;font-size:7pt;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;}
.qp-num.pend{background:transparent;border:1px dashed %(pend)s;color:%(pend)s;}
.qp-eixo{font-size:6.8pt;color:%(olive)s;line-height:1.3;margin-bottom:1.3mm;}
.qp-eixo.eixo-pendente{color:%(pend)s;font-weight:600;}
.qp-agua{font-size:7.4pt;display:flex;align-items:flex-start;gap:1.6mm;margin-top:0.8mm;}
.qp-dot{width:2.6mm;height:2.6mm;border-radius:50%%;margin-top:0.9mm;flex:none;}
.qp-agua.v-proposta{color:%(rust_t)s;}
.qp-agua.v-pendente{color:%(pend)s;}
.qp-origem{font-size:6.2pt;color:#8a8266;font-style:italic;margin-left:4.2mm;}
.ob-it{display:flex;gap:2mm;font-size:7.6pt;line-height:1.4;margin-top:2mm;}
.ob-num{width:4.6mm;height:4.6mm;border-radius:50%%;background:%(olive)s;color:%(cream)s;font-size:6.6pt;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;}
.carimbo{position:absolute;right:14mm;bottom:10mm;width:150mm;border:0.5mm solid %(olive)s;border-radius:2mm;overflow:hidden;background:#fdfbf6;}
.carimbo-top{background:%(olive)s;color:%(cream)s;display:flex;justify-content:space-between;align-items:center;padding:3mm 4mm;}
.carimbo-logo{font-size:12pt;font-weight:800;line-height:1;}
.carimbo-logo span{font-size:6pt;font-weight:500;display:block;letter-spacing:0.5pt;}
.carimbo-pr-num{font-size:16pt;font-weight:800;}
.carimbo-pr-num span{font-size:9pt;font-weight:500;}
.carimbo-pr-rev{font-size:6.6pt;font-weight:700;letter-spacing:0.6pt;text-align:right;}
.carimbo-body{padding:2.5mm 4mm;}
.cb-lbl{font-size:5.6pt;font-weight:700;letter-spacing:0.5pt;color:%(rust_t)s;margin-top:1.8mm;}
.cb-val{font-size:7.6pt;font-weight:500;}
.cb-val.strong{font-weight:700;}
.cb-val.small{font-size:6.4pt;line-height:1.3;}
.cb-row2{display:flex;gap:4mm;}
.cb-row2>div{flex:1;}
.resp-row{font-size:6.8pt;}
.carimbo-bottom{background:%(rust)s;color:%(cream)s;font-size:5.8pt;font-weight:700;letter-spacing:0.3pt;text-align:center;padding:1.6mm;}
.idx-it{display:flex;align-items:center;gap:2.5mm;font-size:8.6pt;padding:1.4mm 0;border-bottom:0.3mm solid %(line)s;}
.idx-badge{width:6mm;height:6mm;border-radius:50%%;background:%(rust)s;color:%(cream)s;font-size:7.5pt;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none;}
.idx-n{margin-left:auto;font-size:7pt;color:%(olive)s;}
.quadro-final-area{position:absolute;left:14mm;top:32mm;width:400mm;height:382mm;overflow:hidden;}
table.quadro-final{border-collapse:collapse;width:100%%;font-size:6.6pt;}
table.quadro-final th{background:%(olive)s;color:%(cream)s;text-align:left;padding:1.1mm 2.2mm;font-size:6.4pt;}
table.quadro-final td{padding:0.85mm 2.2mm;border-bottom:0.2mm solid %(line)s;line-height:1.25;}
table.quadro-final tr:nth-child(even){background:%(band)s;}
.dot{display:inline-block;width:2.6mm;height:2.6mm;border-radius:50%%;margin-right:1.2mm;vertical-align:middle;}
.st{font-size:6.6pt;font-weight:700;padding:0.5mm 1.6mm;border-radius:3mm;}
.st-ok{background:#dfe8d2;color:#3f5c2f;}
.st-prop{background:%(cream)s;color:%(rust_t)s;}
.st-pend{background:#f3d6d0;color:%(pend)s;}
''' % C

    html_out = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
                f'<title>Caderno de Detalhamento Hidráulico — Pontos em Planta — {REV}</title>'
                f'<style>{css}</style></head><body>{"".join(folhas)}</body></html>')
    open(os.path.join(AQUI, 'caderno_hidraulica.html'), 'w', encoding='utf-8').write(html_out)
    print('ok', len(folhas), 'folhas')


if __name__ == '__main__':
    gerar()
