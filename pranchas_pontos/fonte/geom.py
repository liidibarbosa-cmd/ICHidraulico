# -*- coding: utf-8 -*-
"""Utilitarios de geometria sobre base.json: varredura de faces de parede (m)."""
import json, numpy as np, cv2, os
AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(os.path.join(AQUI, 'base.json')))
_R = 1000
_img = None
def _raster():
    global _img
    if _img is None:
        _img = np.zeros((int(31 * _R), int(24 * _R)), np.uint8)
        for p in BASE['paredes']:
            cv2.fillPoly(_img, [(np.array(p['pts']) * _R).astype(np.int32)], 255)
            for f in p['furos']:
                cv2.fillPoly(_img, [(np.array(f) * _R).astype(np.int32)], 0)
        for x, y, w, h in BASE['janelas']:
            cv2.rectangle(_img, (int(x * _R), int(y * _R)), (int((x + w) * _R), int((y + h) * _R)), 255, -1)
    return _img
def face(x, y, direcao):
    """Coordenada (m) da primeira face de parede/janela a partir de (x, y) na direcao
    'esq' | 'dir' | 'sup' | 'inf'."""
    img = _raster(); dx, dy = dict(esq=(-1, 0), dir=(1, 0), sup=(0, -1), inf=(0, 1))[direcao]
    px, py = int(round(x * _R)), int(round(y * _R)); k = 0
    while img[py + dy * k, px + dx * k] == 0:
        k += 1
        if k > 8 * _R: raise ValueError('sem parede %s a partir de (%.2f, %.2f)' % (direcao, x, y))
    return round((px + dx * k) / _R if dx else (py + dy * k) / _R, 3)
def pt2m(x, y):
    A = np.array(BASE['pt2m']); return tuple(A @ np.array([x, y, 1.0]))
