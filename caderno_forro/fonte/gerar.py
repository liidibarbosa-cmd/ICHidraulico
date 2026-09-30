# -*- coding: utf-8 -*-
"""Gera caderno_forro.html (todas as pranchas). Uso: python3 gerar.py [n1 n2 ...]"""
import sys, importlib
from base import documento
MODS = ['p01_planta', 'p02_cortineiros', 'p03_rasgo', 'p04_banheiros', 'p05_detalhes', 'p06_quadro']
sel = [int(a) for a in sys.argv[1:]] or list(range(1, len(MODS) + 1))
secs = []
for i in sel:
    m = importlib.import_module(MODS[i - 1])
    secs.append(m.prancha())
open('caderno_forro.html', 'w', encoding='utf-8').write(documento(secs))
print('ok', sel)
