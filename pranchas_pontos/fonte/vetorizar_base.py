# -*- coding: utf-8 -*-
"""Vetoriza a planta-base da prancha de TOMADAS (R05, 30/09/2026): remove os simbolos
eletricos (abertura morfologica 9x9 px: tracos e triangulos < 9 px somem, paredes >= 12 px
ficam), extrai paredes (poligonos), janelas/vidros (cinza) e grava base.json em metros.
Sistema de coordenadas: origem no canto superior esquerdo do raster da prancha de tomadas,
x para a direita, y para baixo, 1 m = 127,56 px (raster 2952 px em 656 pt, escala 1:100).
Tambem grava a transformacao planta de pontos (pt, PDF 1:200) -> base (m)."""
import cv2, numpy as np, json, sys, pymupdf as fitz
TOM = sys.argv[1]
PX_M = 2952 / 656.0 * 72 / 25.4 * 10   # px por metro (1 m = 10 mm em 1:100)
d = fitz.open(TOM); pix = fitz.Pixmap(d, 36)
im = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3][:, :, ::-1].copy()
g = im.mean(axis=2)
dark = (g < 110).astype(np.uint8)
walls = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
grey = ((g > 120) & (g < 215)).astype(np.uint8) & (1 - cv2.dilate(walls, np.ones((5, 5), np.uint8)))
def m(v): return round(float(v) / PX_M, 4)
out = dict(px_m=PX_M, paredes=[], janelas=[], vidros=[], caixilhos=[])
cs, hier = cv2.findContours(walls, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
def simplificar(c):
    ap = cv2.approxPolyDP(c, 1.2, True).reshape(-1, 2).astype(float)
    # contornos com trechos diagonais longos (linha inclinada do lote): tolerancia maior, sem degraus
    diag = any(min(abs(b[0] - a[0]), abs(b[1] - a[1])) > 6 for a, b in zip(ap, np.roll(ap, -1, axis=0)))
    if diag and cv2.arcLength(c, True) > 2000:
        ap = cv2.approxPolyDP(c, 4.0, True).reshape(-1, 2).astype(float)
    n = len(ap)
    for k in range(n):
        a, b = ap[k], ap[(k + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) > 4 * abs(dy): y = (a[1] + b[1]) / 2; a[1] = b[1] = y
        elif abs(dy) > 4 * abs(dx): x = (a[0] + b[0]) / 2; a[0] = b[0] = x
    return ap
for i, c in enumerate(cs):
    if hier[0][i][3] >= 0 or cv2.contourArea(c) < 40: continue      # so contornos externos aqui
    ap = simplificar(c)
    (cx, cy), (w, h), _ = cv2.minAreaRect(ap.astype(np.float32))
    if min(w, h) < 0.08 * PX_M:          # tracos finos pretos = caixilhos de janela (nao sao paredes)
        if max(w, h) > 0.2 * PX_M: out['caixilhos'].append([[m(x), m(y)] for x, y in ap])
        continue
    furos = []
    j = hier[0][i][2]                 # primeiro filho (furo = interior de ambiente cercado)
    while j >= 0:
        if cv2.contourArea(cs[j]) >= 40:
            furos.append([[m(x), m(y)] for x, y in simplificar(cs[j])])
        j = hier[0][j][0]
    out['paredes'].append(dict(pts=[[m(x), m(y)] for x, y in ap], furos=furos))
n, lab, st, cen = cv2.connectedComponentsWithStats(grey, 8)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if max(w, h) < 70 or a < 150: continue
    r = [m(x), m(y), m(w), m(h)]
    (out['janelas'] if min(w, h) >= 0.08 * PX_M else out['vidros']).append(r)   # vidro = box / porta de vidro
A = np.load('A_pt2base.npy')   # pt (PDF planta de pontos) -> px base (registro ECC afim)
out['pt2m'] = (A / PX_M).tolist()
json.dump(out, open('base.json', 'w'), indent=0)
print(len(out['paredes']), 'paredes', len(out['janelas']), 'janelas', len(out['vidros']), 'vidros', len(out['caixilhos']), 'caixilhos')
