# -*- coding: utf-8 -*-
"""Caderno de detalhamento das areas molhadas - Residencia Ivan e Ana Neris - R00 (02/10/2026).
9 folhas A3 retrato no padrao dos cadernos A3 do escritorio. Gera areas_molhadas.html.
  01 planta-chave, indice e legenda   02-05 banhos   06 cozinha   07 gourmet e A.S.   08 detalhes   09 loucas e metais"""
import os
from am_base import *
import am_banhos as BH
import am_outras as OU

if __name__ == '__main__':
    folhas = [OU.folha_chave()] + [BH.folha_banho(k) for k in ('W01', 'W02', 'WSM', 'WEX')] + \
             [OU.folha_cozinha(), OU.folha_gourmet_as(), OU.folha_detalhes(), OU.folha_loucas()]
    assert len(folhas) == TOTAL
    open(os.path.join(AQUI, 'areas_molhadas.html'), 'w').write(html3(folhas))
    print('folhas:', len(folhas))
