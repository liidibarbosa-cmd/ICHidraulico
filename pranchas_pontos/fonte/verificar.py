# -*- coding: utf-8 -*-
"""Conferencia das pranchas contra os arquivos de referencia.
1. Cada cota fecha com a geometria (distancia entre face de referencia e ponto = valor cotado).
2. Posicao de cada ponto x planta de pontos (29/09): distancia ao ponto de cota correspondente
   no PDF da planta (transformado para metros pelo registro ECC).
3. Alturas com fonte 'C' x texto do caderno Hidraulica Detalhe Rev. 02.
4. Textos das cotas e codigos presentes no PDF gerado.
"""
import sys, os, re, numpy as np, pymupdf as fitz
import dados_pontos as D, geom
REF = os.path.join(geom.AQUI, '..', '..', 'referencias', 'pdfs_originais')
PDF = sys.argv[1]
erros = 0

# 1. fechamento das cotas
for k in D.ORDEM:
    for p in D.AMB[k]['pontos']:
        for c in p['cotas']:
            v = float(c['txt'].replace(',', '.'))
            real = abs(c['ate'] - c['de'])
            pos = p['x'] if c['eixo'] == 'x' else p['y']
            if abs(real - v) > 0.0005 or abs(pos - c['ate']) > 0.0005:
                print('ERRO cota', p['cod'], c['txt'], real); erros += 1
print('1. cotas fecham com a geometria: ok' if not erros else '1. ERROS: %d' % erros)

# 2. posicao x planta de pontos (pontos de cota vermelhos do PDF da planta)
pl = fitz.open(os.path.join(REF, 'CADERNO DETALHAMENTO RESIDENCIA IC - PONTOS HIDRAULICOS.pdf'))[0]
dots = []
for dr in pl.get_drawings():
    if dr.get('fill') == (1.0, 0.0, 0.0):
        r = dr['rect']; dots.append(geom.pt2m((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
dots = np.array(dots)
print('2. posição ao longo da cota x planta de pontos (cm):')
maxd = 0
for k in D.ORDEM:
    for p in D.AMB[k]['pontos']:
        for c in p['cotas']:
            ax = 0 if c['eixo'] == 'x' else 1
            alvo = c['ate']
            # ponto de cota da planta mais proximo no eixo da cota, na linha de chamada do ponto
            dd = np.abs(dots[:, ax] - alvo)
            j = int(np.argmin(dd)); dif = (dots[j, ax] - alvo) * 100
            maxd = max(maxd, abs(dif))
            flag = '' if abs(dif) <= 3.0 else '  <-- verificar'
            print('   %-5s %-32s %s %5s  planta-prancha = %+5.1f%s' % (p['cod'], p['peca'][:32], c['eixo'], c['txt'], dif, flag))
print('   maior diferença: %.1f cm' % maxd)

# 3. alturas do caderno
cad = fitz.open(os.path.join(REF, 'CADERNO DETALHAMENTO RESIDENCIA IC - HIDRAULICA DETALHE.pdf'))
txt = ' '.join(p.get_text() for p in cad)
esperado = {  # (codigo -> [(tipo, altura)]) conforme quadro de pontos do caderno
    'C1': [('AF', '1,00')], 'C2': [('AQ', '0,50'), ('ESG', '0,35')], 'C3': [('AF', '1,25')], 'C4': [('AF', '0,60')],
    'G1': [('AQ', '0,50')], 'L4': [('AF', '0,70')], 'L5': [('AF', '0,70')],
}
for pref in ('B1.', 'B2.', 'BM.', 'B4.'):
    esperado[pref + '1'] = [('SC', '2,10'), ('AF', '1,10'), ('AQ', '1,10')]
    if pref != 'B4.': esperado[pref + '4'] = [('AF', '0,60')]
esperado['B4.5'] = [('RG', '0,55')]
e3 = 0
for cod, lst in esperado.items():
    p = next(q for k in D.ORDEM for q in D.AMB[k]['pontos'] if q['cod'] == cod)
    serv = {(t, h): f for t, h, f in p['serv']}
    for t, h in lst:
        if serv.get((t, h)) != 'C': print('   ERRO altura', cod, t, h, serv); e3 += 1
for pal in ('A.F. 1,00', 'A.Q. 0,50', 'ESG 0,35', 'A.F. 1,25', 'A.F. 0,60', 'A.F. 0,70', 'A.F. 2,10', 'A.Q. 1,10', 'R.G. 0,55'):
    if pal not in txt: print('   ERRO: "%s" não encontrado no caderno' % pal); e3 += 1
# nenhum ponto marcado 'C' com valor que nao exista no caderno
for k in D.ORDEM:
    for p in D.AMB[k]['pontos']:
        for t, h, f in p['serv']:
            if f == 'C' and h != 'piso' and h not in txt: print('   ERRO: %s %s %s não está no caderno' % (p['cod'], t, h)); e3 += 1
print('3. alturas com fonte C conferem com o caderno: ok' if not e3 else '3. ERROS: %d' % e3)
erros += e3

# 4. textos no PDF gerado
doc = fitz.open(PDF)
pag = [p.get_text() for p in doc]
e4 = 0
onde = {'COZ': 1, 'GOU': 1, 'LAV': 1, 'W01': 2, 'W02': 2, 'WSM': 2, 'WEX': 2, 'EXT': 0}
for k in D.ORDEM:
    for p in D.AMB[k]['pontos']:
        t = pag[onde[k]]
        if p['cod'] not in t: print('   ERRO: código %s ausente na prancha %d' % (p['cod'], onde[k] + 1)); e4 += 1
        for c in p['cotas']:
            if c['txt'] not in t: print('   ERRO: cota %s de %s ausente' % (c['txt'], p['cod'])); e4 += 1
for i, t in enumerate(pag):
    for obrig in ('Residência Ivan e Ana Neris', 'A263982-8', 'A290220-6', '%02d/04' % (i + 1), D.REV, '02/10/2026'):
        if obrig.replace(' ', '') not in t.replace(' ', '').replace('\xa0', ''):
            print('   ERRO: "%s" ausente no carimbo da prancha %d' % (obrig, i + 1)); e4 += 1
print('4. códigos, cotas e carimbos presentes no PDF: ok' if not e4 else '4. ERROS: %d' % e4)
erros += e4
print('TOTAL DE ERROS:', erros)
sys.exit(1 if erros else 0)
