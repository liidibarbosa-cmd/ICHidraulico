# -*- coding: utf-8 -*-
"""Dados do Caderno de Forro de Gesso — Residência IC.

Sistema de coordenadas: metros, mesmo do caderno de iluminação (origem no canto
superior esquerdo da planta, x para a direita, y para baixo). Faces internas das
paredes conferidas com o DWG "PROJETO IVAN E ANA - R01" (Planta de forro de gesso):
local_DWG = (x + 3,111 ; 40,036 - y).

Status: 'doc'  = documentado (DWG / cadernos existentes / decisão do cliente em 30/09/2026)
        'prop' = proposta desta revisão, aguarda aprovação
        'pend' = pendente de informação
"""

REV = 'R01'
DATA = '30/09/2026'
TOTAL = 6

# ---------------------------------------------------------------- níveis (m, a partir do piso acabado)
FORRO_ALA = 2.85      # DWG planta de forro: PD 2,85 m
LAJE_ALA = 3.00       # DWG corte AA: 3,00 m do piso acabado ao fundo da laje pré-fabricada
FORRO_ESTAR = 3.40    # DWG planta de forro: PD 3,40 m
LAJE_ESTAR = 3.70     # DWG corte BB: 3,70 m
CORT_LARG = 0.20      # decisão do cliente (30/09/2026): 20 cm de profundidade livre p/ as cortinas

# ---------------------------------------------------------------- ambientes com forro de gesso
# placa: 'RU' | 'RUp' (RU proposta) | 'ST'
AMB = [
    dict(id='BSM', nome='BANHO SUÍTE MASTER', rect=(1.08, 0.15, 3.03, 3.65), h=FORRO_ALA, laje=LAJE_ALA, placa='RU', area=6.83, lab=(2.05, 2.55)),
    dict(id='CLO', nome='CLOSET', rect=(3.18, 0.15, 6.68, 3.65), h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=12.25, lab=(4.93, 2.12)),
    dict(id='SM', nome='SUÍTE MASTER', rect=(6.83, 0.15, 11.48, 3.65), h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=15.75, lab=(8.55, 2.75)),
    dict(id='S2', nome='SUÍTE 2', rect=(2.58, 3.80, 6.68, 6.81), h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=12.30, lab=(3.85, 5.30)),
    dict(id='BS2', nome='BANHO SUÍTE 2', rect=(3.18, 6.95, 5.99, 8.45), h=FORRO_ALA, laje=LAJE_ALA, placa='RU', area=4.20, lab=(4.95, 8.10)),
    dict(id='BS1', nome='BANHO SUÍTE 1', rect=(3.18, 8.60, 5.99, 10.10), h=FORRO_ALA, laje=LAJE_ALA, placa='RU', area=4.20, lab=(4.95, 8.95)),
    dict(id='S1', nome='SUÍTE 1', rect=(2.58, 10.25, 6.68, 13.25), h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=12.30, lab=(5.45, 11.75)),
    dict(id='CIR', nome='CIRCULAÇÃO', poly=[(6.83, 3.80), (8.04, 3.80), (8.04, 12.20), (6.83, 12.20), (6.83, 10.10), (6.13, 10.10), (6.13, 6.95), (6.83, 6.95)],
         h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=12.85, lab=(7.62, 9.35), vert=True),
    dict(id='HO', nome='HOME OFFICE', rect=(8.18, 3.80, 11.48, 6.00), h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=7.26, lab=(9.85, 5.45)),
    dict(id='B4', nome='BANHO 4', rect=(8.18, 6.16, 11.48, 7.55), h=FORRO_ALA, laje=LAJE_ALA, placa='RU', area=4.62, lab=(9.85, 7.30)),
    dict(id='COZ', nome='COZINHA', rect=(2.58, 13.40, 6.83, 17.60), h=FORRO_ALA, laje=LAJE_ALA, placa='RUp', area=17.85, lab=(4.95, 13.95)),
    dict(id='AS', nome='A.S.', rect=(2.58, 17.75, 5.34, 19.75), h=FORRO_ALA, laje=LAJE_ALA, placa='RUp', area=5.50, lab=(3.35, 19.25)),
    dict(id='DES', nome='DESPENSA', rect=(5.49, 17.75, 6.68, 19.75), h=FORRO_ALA, laje=LAJE_ALA, placa='ST', area=2.40, lab=(6.08, 19.30)),
    dict(id='EST', nome='ESTAR / JANTAR', poly=[(6.83, 12.35), (12.08, 12.35), (12.08, 20.35), (8.48, 20.35), (8.48, 19.75), (6.83, 19.75)],
         h=FORRO_ESTAR, laje=LAJE_ESTAR, placa='ST', area=41.0, lab=(9.20, 17.55)),
]

# Áreas externas — SEM forro de gesso (decisão do cliente, 30/09/2026): revestimento a detalhar
EXTERNAS = [
    dict(nome='ÁREA GOURMET (varanda)', pos=(10.2, 10.9)),
]

# ---------------------------------------------------------------- cortineiros (comprimentos gerais do DWG)
# faixa = retângulo (x0,y0,x1,y1) do vão de 20 cm; 'parede' = lado da parede/esquadria
CORTINEIROS = [
    dict(id='CT1', amb='Suíte master', luz='L08 · fita LED (modelo a definir)', faixas=[(11.48 - CORT_LARG, 0.15, 11.48, 3.65)],
         comp=3.50, forro=FORRO_ALA, laje=LAJE_ALA, esq='P10 · porta de correr veneziana 2,50 × 2,10'),
    dict(id='CT2', amb='Estar / jantar', luz='L09 · Tuboled (modelo a definir)',
         faixas=[(8.58, 12.35, 12.08, 12.35 + CORT_LARG), (12.08 - CORT_LARG, 12.35 + CORT_LARG, 12.08, 20.35)],
         comp=11.30, forro=FORRO_ESTAR, laje=LAJE_ESTAR, esq='P05 (2×) 3,00 × 2,10 · J01 2,50 × 2,50'),
]

# ---------------------------------------------------------------- rasgo de luz (proposta)
RASGO_LARG = 0.12       # proposta
RASGO_AFAST = 0.15      # proposta: faixa de forro entre a parede esquerda e o rasgo
RASGO_PONTA = 0.10      # proposta: recuo nas duas extremidades
RASGO = dict(id='RG1', x0=6.83 + RASGO_AFAST, x1=6.83 + RASGO_AFAST + RASGO_LARG,
             y0=3.80 + RASGO_PONTA, y1=12.20 - RASGO_PONTA)

# ---------------------------------------------------------------- alçapões (proposta)
ALCAPOES = [
    dict(id='AL1', x=7.62, y=11.55, lado=0.40, uso='driver/fonte do rasgo L10, se o produto exigir fonte externa'),
]
