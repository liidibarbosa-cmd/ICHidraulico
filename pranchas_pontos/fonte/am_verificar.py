# -*- coding: utf-8 -*-
"""Conferencia do caderno de areas molhadas (A3):
1. Vaos dos boxes x vidros da base (a face do box coincide com o vidro desenhado na planta).
2. Elevacoes planificadas: cada cota de ponto parte de uma quina da parede das pecas (referencia certa)
   e a distancia na elevacao = valor cotado; janela J04 dentro do fundo; ralo no fundo.
3. Pontos e alturas do caderno = pranchas hidraulicas (mesmos dados) e codigos presentes em cada folha.
4. Carimbos: CAU, data, revisao, numeracao das folhas."""
import sys, json, pymupdf as fitz
import dados_pontos as D, am_banhos as BH, geom
PDF = sys.argv[1]; erros = 0
def erro(*a):
    global erros; erros += 1; print('   ERRO', *a)
# 1
for k, b in BH.BANHOS.items():
    eixo, c, a0, a1 = b['vidro']
    def ok(r):
        if eixo == 'x': return abs(r[0] + r[2] / 2 - c) < 0.02 and r[1] < a1 and r[1] + r[3] > a0
        return abs(r[1] + r[3] / 2 - c) < 0.02 and r[0] < a1 and r[0] + r[2] > a0
    vid = [r for r in geom.BASE['vidros'] if ok(r)]
    if not vid: erro(k, 'vidro do box nao encontrado na base')
    x0, y0, x1, y1 = b['box']
    face = x1 if eixo == 'x' else y0
    r = vid[0]; fv = r[0] if eixo == 'x' else r[1] + r[3]
    if abs(face - fv) > 0.01: erro(k, 'face do box %.3f x vidro %.3f' % (face, fv))
    print('1. %-20s vão %s × %s · vidro ok' % (b['nome'], BH.fmt(BH.dims(b)[0]), BH.fmt(BH.dims(b)[1])))
# 2
for k, b in BH.BANHOS.items():
    ip = b['ip']; L = BH.comp(b['segs'][ip]); s0 = sum(BH.comp(sg) for sg in b['segs'][:ip])
    for p in D.AMB[k]['pontos']:
        for c in p['cotas']:
            ref = (c['de'], p['y']) if c['eixo'] == 'x' else (p['x'], c['de'])
            sr = BH.s_de(b, ip, *ref); sp = BH.s_de(b, ip, p['x'], p['y'])
            if min(abs(sr - s0), abs(sr - s0 - L)) > 0.001: erro(k, p['cod'], 'referência fora da quina')
            if abs(abs(sp - sr) - float(c['txt'].replace(',', '.'))) > 0.0005: erro(k, p['cod'], 'distância na elevação')
        if p.get('ralo'):
            ifun = [i for i, sg in enumerate(b['segs']) if sg[2] == 'fundo do box'][0]
            sf0 = sum(BH.comp(sg) for sg in b['segs'][:ifun]); sr = BH.s_de(b, ifun, p['x'], p['y'])
            if not sf0 < sr < sf0 + BH.comp(b['segs'][ifun]): erro(k, 'ralo fora do fundo')
    if b['janela']:
        ifun = [i for i, sg in enumerate(b['segs']) if sg[2] == 'fundo do box'][0]
        sf0 = sum(BH.comp(sg) for sg in b['segs'][:ifun])
        for pt in b['janela']:
            if not sf0 - 1e-6 <= BH.s_de(b, ifun, *pt) <= sf0 + BH.comp(b['segs'][ifun]) + 1e-6: erro(k, 'J04 fora do fundo')
print('2. elevações planificadas: referências nas quinas e distâncias = cotas' + ('' if not erros else ' (ver erros)'))
# 3 e 4
doc = fitz.open(PDF); pag = [p.get_text().replace('\xa0', ' ') for p in doc]
onde = {'W01': 1, 'W02': 2, 'WSM': 3, 'WEX': 4, 'COZ': 5, 'GOU': 6, 'LAV': 6}
for k, i in onde.items():
    for p in D.AMB[k]['pontos']:
        if p['cod'] not in pag[i]: erro('código %s ausente na folha %02d' % (p['cod'], i + 1))
        for c in p['cotas']:
            if c['txt'] not in pag[i]: erro('cota %s de %s ausente na folha %02d' % (c['txt'], p['cod'], i + 1))
        for t, h, f in p['serv']:
            if h not in pag[i]: erro('altura %s de %s ausente' % (h, p['cod']))
if 'PG1' not in pag[5]: erro('PG1 ausente na cozinha')
for i, t in enumerate(pag):
    for ob in ('A263982-8', 'A290220-6', '02/10/2026', 'Nº 00', '%02d/09' % (i + 1), 'Ivan e Ana Neris'):
        if ob not in t: erro('"%s" ausente na folha %02d' % (ob, i + 1))
    if t.count('A269382-8') > (1 if i == 0 else 0): erro('CAU errado na folha %02d' % (i + 1))   # folha 01: so na pendencia
print('3/4. códigos, cotas, alturas e carimbos no PDF' + (': ok' if not erros else ''))
print('TOTAL DE ERROS:', erros); sys.exit(1 if erros else 0)
