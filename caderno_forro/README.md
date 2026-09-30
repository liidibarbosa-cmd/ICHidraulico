# Caderno de Detalhamento — Forro de Gesso — R01
Residência Ivan e Ana Neris · Nova Odessa, SP · 30/09/2026 · emissão para validação

## Entregáveis
| Arquivo | Conteúdo |
|---|---|
| `CADERNO DE DETALHAMENTO - FORRO DE GESSO - R01.pdf` | 6 folhas A2 paisagem (594 × 420 mm), mesmo padrão gráfico do caderno de iluminação 02/04. Imprimir sem ajuste de escala. |
| `fonte/previa/folha_XX.png` | Prévia de cada folha. |
| `fonte/` | Arquivos-fonte que geram o PDF. |

Folhas:
- 01/06 — Planta de forro 1:75: ambientes, placa ST/RU, alturas (forro e laje), cortineiros e rasgo cotados, luminárias indicativas, chamadas e esquema de níveis
- 02/06 — Cortineiros CT1 (suíte master) e CT2 (estar/jantar): plantas 1:50, cortes C1/C2 1:5, perspectiva, canto em L (C3) e cabeceira (C4) 1:10
- 03/06 — Rasgo de luz RG1 (circulação): planta 1:50, cortes R1/R2 1:5, perspectiva
- 04/06 — Banheiros em placa RU: plantas 1:25, corte típico B1 1:10, adequação por banho, “RU não é impermeável”
- 05/06 — Detalhes D1 a D8: tabica, mudança de nível, recortes pontual e linear, cassete E1, pendentes, alçapão, junta de controle
- 06/06 — Quadro de materiais, quantitativos, notas de execução, decisões/pendências e normas

## Status dos dados
Cada item traz um selo: **DOCUMENTADO** (dado dos arquivos ou decisão do cliente), **PROPOSTA** (aguarda aprovação) ou **A DEFINIR** (depende de fabricante/fornecedor).

## Base
- DWG `referencias/PROJETO IVAN E ANA - R01.dwg`: *Planta de forro de gesso* (PD por ambiente, placa RU nos banhos, cortineiros, entreforro de 30 cm no estar) e cortes AA/BB (fundo da laje a 3,00 m e 3,70 m). Lido com LibreDWG.
- Caderno de iluminação 02/04 R01 (luminárias, L08/L09/L10) — geometria das paredes extraída deste PDF (`fonte/geometria_base.json`).
- Caderno de tomadas 01/04 R05 (posição do cassete E1), ar-condicionado 02/02, esquadrias R01 e hidráulica R02.

## Decisões do cliente (30/09/2026)
- Luminárias sem locação na planta de forro; só cortineiros e rasgo são posicionados.
- Cortineiros com 20 cm de vão livre; comprimentos gerais do DWG.
- Rasgo com luz para baixo, reforçando a iluminação geral da circulação.
- Garagem, varanda e beirais sem forro de gesso (revestimento a detalhar depois).
- Alturas das janelas dos banhos serão revistas; desconsideradas no forro.
- Fita LED, Tuboled e cortina definidos depois com os fornecedores.

## Pendências
Fabricante de referência (espessuras, perfis, pendurais e espaçamentos só entram com o manual técnico — os sites dos fabricantes estão bloqueados neste ambiente); box dos banhos até o teto e exaustão; fichas técnicas das luminárias e do cassete; CAU da Isadora Ferrari (A263982-8 × A269382-8); altura da J01 (2,50 × 2,00 m); aprovação das propostas.

Tipografia: títulos em Outfit (substituta da Aloevera Display, cujo arquivo completo não estava disponível) e texto em Manrope.

## Como regenerar
```bash
cd caderno_forro/fonte
npm i                      # playwright (usa o Chromium pré-instalado em /opt/pw-browsers)
python3 gerar.py           # gera caderno_forro.html (ou: python3 gerar.py 1 3 para folhas específicas)
node imprimir.mjs          # PDF A2 + prévias PNG
```
Dados editáveis em `fonte/dados_forro.py`; desenho em `p01_planta.py` … `p06_quadro.py`; estilo e carimbo em `base.py`.
