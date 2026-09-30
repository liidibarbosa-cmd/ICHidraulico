# -*- coding: utf-8 -*-
"""Prancha 05 — Detalhes construtivos complementares D1 a D8."""
from base import *
from dados_forro import *
from secao import *

CW, CH = 103.0, 178.0         # célula
X0, Y0 = 12.0, 14.0


def celula(i):
    c, r = i % 4, i // 4
    return X0 + c * (CW + 1.5), Y0 + r * (CH + 2)


def base_corte(v, s, F, Lz, x0=-0.05, x1=0.40, parede_esq=True, ru=False, gap=None):
    if parede_esq:
        parede(v, s, -0.12, 0.0, F - 0.16, Lz)
    laje(v, s, -0.12 if parede_esq else x0, x1, Lz)
    xa = 0.0 if parede_esq else x0
    chapa(v, s, xa + (0.02 if parede_esq else 0), F, x1, F + T_CHAPA, ru=ru)
    quebra_v(v, s.P(x1, 0)[0], s.P(0, F + 0.03)[1], s.P(0, F - 0.02)[1])


def rodape(v, x, y, cod, nome, esc, status, linhas):
    mini_titulo(v, x + 2, y, cod, nome, esc)
    v.tag(x + CW - 3, y - 7.5, {'prop': 'PROPOSTA', 'doc': 'DOCUMENTADO', 'pend': 'A DEFINIR'}[status], status, anchor='end')
    for i, t in enumerate(linhas):
        v.text(x + 4, y + 10 + i * 3.2, t, size=6.0, weight=400 if i else 500, anchor='start', cor=C['ink'] if i == 0 else C['muted'])


def nota(v, x1, y1, x2, y2, t, anchor='start', cor=None):
    v.seta_nota(x1, y1, x2, y2, cor)
    v.text(x2 + (0.8 if anchor == 'start' else -0.8), y2 + 1.0, t, size=5.4, weight=600, anchor=anchor, cor=cor or C['ink'])


def D1(v, x, y):
    F, Lz = FORRO_ALA, LAJE_ALA
    s = Secao(5, x + 30, y + 40 + (Lz - F) * 200 + F * 200)
    base_corte(v, s, F, Lz)
    # tabica
    a = s.P(0.0, F)
    v.poly([s.P(0.0, F + 0.035), s.P(0.03, F + 0.035), s.P(0.03, F + 0.01), s.P(0.012, F + 0.01), s.P(0.012, F)], stroke=C['rust'], sw=0.5, close=False)
    v.rect(*s.R(0.022, F, 0.30, F + T_CHAPA), fill='url(#hGesso)', stroke=C['ink'], sw=0.3)
    for xp in (0.12, 0.30):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.05, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.025, F + T_CHAPA + 0.022, Lz)
    nota(v, *s.P(0.02, F + 0.03), *s.P(0.10, F + 0.11), 'tabica metálica fixada na parede')
    nota(v, *s.P(0.011, F - 0.002), *s.P(0.10, F - 0.07), 'negativo: largura conforme modelo')
    nota(v, *s.P(0.20, F + 0.006), *s.P(0.26, F - 0.04), 'forro')
    rodape(v, x, y + 138, 'D1', 'Encontro com parede', 'escala 1:5', 'prop',
           ['Tabica perimetral em todos os ambientes.', 'Junta aberta evita trinca no encontro', 'forro × parede. Modelo a aprovar.'])


def D2(v, x, y):
    k = 80.0
    s = Secao(12.5, x + 50, y + 16 + (3.84 * k))
    parede(v, s, -0.075, 0.075, 2.62, LAJE_ESTAR)
    for (x0, x1, Lz) in ((-0.55, -0.075, LAJE_ALA), (0.075, 0.55, LAJE_ESTAR)):
        xx, yy, ww, hh = s.R(x0, Lz, x1, Lz + T_LAJE)
        v.rect(xx, yy, ww, hh, fill='url(#hLaje)', stroke=C['ink'], sw=0.35)
    chapa(v, s, -0.55, FORRO_ALA, -0.09, FORRO_ALA + T_CHAPA)
    chapa(v, s, 0.09, FORRO_ESTAR, 0.55, FORRO_ESTAR + T_CHAPA)
    for xx, F, Lz in ((-0.33, FORRO_ALA, LAJE_ALA), (0.30, FORRO_ESTAR, LAJE_ESTAR)):
        perfil_u(v, s, xx, F + T_CHAPA, xx + 0.05, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xx + 0.025, F + T_CHAPA + 0.022, Lz)
    for x0, x1, F in ((-0.09, -0.075, FORRO_ALA), (0.075, 0.09, FORRO_ESTAR)):
        v.rect(*s.R(x0, F, x1, F + 0.03), fill=C['rust'])
    marca_nivel(v, s.P(-0.50, 0)[0], s.P(0, FORRO_ALA)[1], '+2,85')
    marca_nivel(v, s.P(0.50, 0)[0], s.P(0, FORRO_ESTAR)[1], '+3,40', lado='esq')
    v.text(*s.P(-0.32, 2.70), 'cozinha / circulação', size=5.6, weight=600)
    v.text(*s.P(0.32, 3.25), 'estar / jantar', size=5.6, weight=600)
    nota(v, *s.P(0.078, 3.05), *s.P(0.16, 2.80), 'parede acabada até +3,40')
    rodape(v, x, y + 138, 'D2', 'Mudança de nível', 'escala 1:12,5', 'doc',
           ['Níveis 2,85 / 3,40 do DWG; a troca', 'acontece sempre sobre parede (verga).', 'Tabica dos dois lados, como em D1.'])


def D3(v, x, y):
    F, Lz = FORRO_ALA, LAJE_ALA
    s = Secao(5, x + 12, y + 40 + (Lz - F) * 200 + F * 200)
    base_corte(v, s, F, Lz, x0=-0.02, x1=0.44, parede_esq=False)
    xc = 0.21
    v.rect(*s.R(xc - 0.05, F, xc + 0.05, F + T_CHAPA), fill='#fff', stroke='none')
    v.rect(*s.R(xc - 0.045, F + T_CHAPA, xc + 0.045, F + 0.10), fill='#e3e0d6', stroke=C['ink'], sw=0.3)
    v.rect(*s.R(xc - 0.06, F - 0.004, xc + 0.06, F), fill='#bfbcb1', stroke=C['ink'], sw=0.2)
    for xp in (xc - 0.09, xc + 0.06):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.03, F + T_CHAPA + 0.022, 'cima')
    pendural(v, s, xc - 0.075, F + T_CHAPA + 0.022, Lz)
    pendural(v, s, xc + 0.075, F + T_CHAPA + 0.022, Lz)
    v.poly([s.P(xc - 0.03, F - 0.004), s.P(xc + 0.03, F - 0.004), s.P(xc + 0.10, F - 0.12), s.P(xc - 0.10, F - 0.12)], fill='url(#gLuz)')
    v.cota(*s.P(0.38, F), *s.P(0.38, Lz), off=0, txt='15', size=5.8, ext=False)
    nota(v, *s.P(xc, F + 0.09), *s.P(0.30, F + 0.20), 'altura da peça < entreforro')
    nota(v, *s.P(xc - 0.075, F + 0.02), *s.P(0.02, F - 0.06), 'perfis de reforço nos 2 lados')
    rodape(v, x, y + 138, 'D3', 'Recorte · luminária pontual', 'escala 1:5', 'prop',
           ['L01, L02, L04, L05. Recorte com gabarito', 'da peça; peças pesadas (L05) apoiadas', 'na estrutura, não só na placa.'])


def D4(v, x, y):
    F, Lz = FORRO_ALA, LAJE_ALA
    s = Secao(5, x + 12, y + 40 + (Lz - F) * 200 + F * 200)
    base_corte(v, s, F, Lz, x0=-0.02, x1=0.44, parede_esq=False)
    xc = 0.21
    v.rect(*s.R(xc - 0.03, F, xc + 0.03, F + T_CHAPA), fill='#fff')
    v.rect(*s.R(xc - 0.025, F + T_CHAPA, xc + 0.025, F + 0.075), fill='#dcd8cc', stroke=C['ink'], sw=0.3)
    v.rect(*s.R(xc - 0.035, F - 0.003, xc + 0.035, F), fill='#bfbcb1', stroke=C['ink'], sw=0.2)
    for xp in (xc - 0.07, xc + 0.04):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.03, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.015, F + T_CHAPA + 0.022, Lz)
    v.poly([s.P(xc - 0.02, F - 0.003), s.P(xc + 0.02, F - 0.003), s.P(xc + 0.08, F - 0.12), s.P(xc - 0.08, F - 0.12)], fill='url(#gLuz)')
    nota(v, *s.P(xc, F + 0.07), *s.P(0.28, F + 0.20), 'perfil L07 (corpo)')
    nota(v, *s.P(xc - 0.055, F + 0.02), *s.P(0.02, F - 0.06), 'requadro contínuo nas bordas')
    rodape(v, x, y + 138, 'D4', 'Recorte linear · perfil L07', 'escala 1:5', 'prop',
           ['Closet (2), home office (2) e cozinha (L).', 'Rasgo reto e contínuo, largura do perfil;', 'bordas reforçadas em todo o comprimento.'])


def D5(v, x, y):
    F, Lz = FORRO_ESTAR, LAJE_ESTAR
    s = Secao(10, x + 8, y + 40 + (Lz - F) * 100 + F * 100)
    laje(v, s, -0.02, 0.92, Lz)
    chapa(v, s, -0.02, F, 0.18, F + T_CHAPA)
    chapa(v, s, 0.72, F, 0.92, F + T_CHAPA)
    for xp in (0.15, 0.72):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.05, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.025, F + T_CHAPA + 0.022, Lz)
    v.rect(*s.R(0.20, F + 0.02, 0.70, Lz - 0.05), fill='#e9ecee', stroke=C['ink'], sw=0.35)
    v.rect(*s.R(0.16, F - 0.03, 0.74, F), fill='#f7f8f8', stroke=C['ink'], sw=0.3)
    for xp in (0.24, 0.66):
        a, b = s.P(xp, Lz), s.P(xp, Lz - 0.05)
        v.line(*a, *b, C['rust'], 0.6)
    v.text(*s.P(0.45, (F + Lz) / 2 - 0.02), 'E1 cassete', size=6.0, weight=700)
    v.cota(*s.P(0.84, F), *s.P(0.84, Lz), off=0, txt='30', size=6.0, ext=False)
    nota(v, *s.P(0.24, Lz - 0.03), *s.P(0.34, Lz + 0.20), 'suspensão própria na laje (manual Gree)', cor=C['rust'])
    nota(v, *s.P(0.17, F + 0.01), *s.P(0.0, F - 0.12), 'requadro em perfis na abertura')
    rodape(v, x, y + 138, 'D5', 'Cassete de ar-condicionado', 'escala 1:10', 'doc',
           ['Posição: tomadas R05 (1,80 × 3,95 m).', 'Abertura conforme gabarito Gree; o forro', 'não sustenta o aparelho. Conferir 30 cm.'])


def D6(v, x, y):
    F, Lz = FORRO_ESTAR, LAJE_ESTAR
    s = Secao(5, x + 12, y + 24 + (Lz - F) * 200 + F * 200)
    base_corte(v, s, F, Lz, x0=-0.02, x1=0.44, parede_esq=False)
    xc = 0.21
    a, b = s.P(xc, Lz), s.P(xc, F - 0.02)
    v.line(*a, *b, C['rust'], 0.7)
    v.rect(*s.R(xc - 0.04, F - 0.02, xc + 0.04, F), fill='#bfbcb1', stroke=C['ink'], sw=0.25)
    v.line(*s.P(xc, F - 0.02), *s.P(xc, F - 0.10), C['ink'], 0.3)
    v.poly([s.P(xc - 0.05, F - 0.155), s.P(xc + 0.05, F - 0.155), s.P(xc + 0.025, F - 0.10), s.P(xc - 0.025, F - 0.10)], fill='#6f6c60')
    v.text(*s.P(xc + 0.08, F - 0.14), 'pendente', size=5.4, weight=600, anchor='start')
    for xp in (xc - 0.08, xc + 0.05):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.03, F + T_CHAPA + 0.022, 'cima')
    nota(v, *s.P(xc, Lz - 0.08), *s.P(0.30, Lz - 0.02), 'fixação direta na laje', cor=C['rust'])
    nota(v, *s.P(xc + 0.04, F - 0.01), *s.P(0.30, F - 0.08), 'canopla')
    rodape(v, x, y + 138, 'D6', 'Pendentes L15 · jantar', 'escala 1:5', 'prop',
           ['Peso do pendente vai para a laje,', 'não para a placa. Posição final após', 'definir o modelo (caderno de iluminação).'])


def D7(v, x, y):
    F, Lz = FORRO_ALA, LAJE_ALA
    s = Secao(5, x + 12, y + 40 + (Lz - F) * 200 + F * 200)
    base_corte(v, s, F, Lz, x0=-0.02, x1=0.44, parede_esq=False)
    v.rect(*s.R(0.08, F - 0.001, 0.34, F + T_CHAPA), fill='url(#hGesso)', stroke=C['rust'], sw=0.45)
    for xp in (0.05, 0.34):
        perfil_u(v, s, xp, F + T_CHAPA, xp + 0.03, F + T_CHAPA + 0.022, 'cima')
        pendural(v, s, xp + 0.015, F + T_CHAPA + 0.022, Lz)
    v.cota(*s.P(0.08, F - 0.05), *s.P(0.34, F - 0.05), off=0, txt='tampa (medida do modelo)', size=5.2, ext=False)
    nota(v, *s.P(0.065, F + 0.02), *s.P(0.0, F - 0.10), 'requadro em perfis')
    rodape(v, x, y + 138, 'D7', 'Alçapão de inspeção', 'escala 1:5', 'prop',
           ['AL1 na circulação, só se a fonte do rasgo', 'for externa. Alçapão pronto para drywall,', 'tampa em placa, fecho por pressão.'])


def D8(v, x, y):
    F, Lz = FORRO_ESTAR, LAJE_ESTAR
    s = Secao(5, x + 12, y + 30 + (Lz - F) * 200 + F * 200)
    laje(v, s, -0.02, 0.44, Lz)
    for xp in (0.145, 0.275):
        pendural(v, s, xp, F + T_CHAPA + 0.022, Lz)
    chapa(v, s, -0.02, F, 0.19, F + T_CHAPA)
    chapa(v, s, 0.23, F, 0.44, F + T_CHAPA)
    perfil_u(v, s, 0.12, F + T_CHAPA, 0.17, F + T_CHAPA + 0.022, 'cima')
    perfil_u(v, s, 0.25, F + T_CHAPA, 0.30, F + T_CHAPA + 0.022, 'cima')
    v.poly([s.P(0.17, F + 0.03), s.P(0.19, F + 0.03), s.P(0.19, F), s.P(0.23, F), s.P(0.23, F + 0.03), s.P(0.25, F + 0.03)], stroke=C['rust'], sw=0.5, close=False)
    nota(v, *s.P(0.21, F + 0.01), *s.P(0.30, F + 0.12), 'perfil de junta de controle', cor=C['rust'])
    rodape(v, x, y + 138, 'D8', 'Junta de controle', 'escala 1:5', 'pend',
           ['Estar/jantar (41 m²): aplicar se o manual', 'do fabricante exigir para essa área ou', 'comprimento. Posição a definir.'])


def prancha():
    v = SVG()
    for i, f in enumerate((D1, D2, D3, D4, D5, D6, D7, D8)):
        x, y = celula(i)
        v.rect(x, y, CW, CH, fill='none', stroke=C['grey2'], sw=0.2, rx=2.5)
        f(v, x, y)
    obs = [
        ('Como ler', 'Cada detalhe traz o selo DOCUMENTADO (dado dos arquivos), PROPOSTA (aguarda sua aprovação) ou A DEFINIR (depende de fornecedor ou fabricante).'),
        ('Estrutura', 'Os perfis e pendurais desenhados são simbólicos. Tipo, espessura, espaçamento e fixação seguem o manual do fabricante escolhido.'),
        ('Carga no forro', 'Nada pesado apoiado só na placa: cassete, pendentes e luminárias grandes fixados na laje ou na estrutura. Limites conforme fabricante.'),
        ('Luminárias', 'Recortes marcados em obra com a peça ou o gabarito na mão. Fichas técnicas a receber da loja de iluminação.'),
        ('Ordem', 'Instalações do entreforro testadas antes de fechar o forro.'),
    ]
    q = box(438, 12, 146, 311, 'b-bege', 'Observações', 'QUADRO 1',
            '<div class="obs">' + ''.join(f'<div class="i"><span class="t">{t}</span><p>{p}</p></div>' for t, p in obs) + '</div>')
    extra = q + carimbo(438, 327, 146, 83, 'Detalhes', '1:5 · 1:10', 5, TOTAL) + \
        titulo(14, 381, '05', 'Detalhes complementares', 'Encontros, níveis, recortes, equipamentos e acessos · cotas em centímetros')
    return pagina(str(v), extra)
