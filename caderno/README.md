# Caderno de Detalhamento Hidráulico — Pontos em Planta — R01
Residência Ivan e Carol · Nova Odessa, SP · 28/09/2026

## Entregáveis
| Arquivo | Conteúdo |
|---|---|
| `CADERNO DE DETALHAMENTO HIDRAULICO - PONTOS EM PLANTA - R01.pdf` | 9 folhas A2 (594 × 420 mm). Imprimir sem ajuste de escala. |
| `fonte/` | Arquivos-fonte editáveis que geram o PDF. |
| `fonte/previa/folha_XX.png` | Renderização de cada folha do PDF (revisão visual). |

Folhas:
- 00/08 — planta geral de pontos hidráulicos (visão de conjunto, base do DWG)
- 01/08 — Cozinha
- 02/08 — Gourmet
- 03/08 — Lavanderia
- 04/08 — WC 01
- 05/08 — WC 02
- 06/08 — WC Suíte Master
- 07/08 — WC Externo
- 08/08 — Quadro consolidado e pendências (todos os pontos da casa)

## Status dos dados
Cada ponto hidráulico tem um status de **altura** e um status de **eixo (posição em planta)**, mostrados no quadro de pontos de cada prancha e consolidados na prancha 08/08:

- **Confirmado**: dado do Caderno Detalhamento Residência IC — Hidráulica Detalhe (Revisão 02, 24/09/2026), ou decisão explícita do cliente em 28/09/2026. Pode ser executado.
- **Proposta** (marcada com \*): valor usual de mercado, adotado na ausência de cota no caderno original, a pedido do cliente (28/09/2026). Precisa de validação do responsável pelo projeto hidrossanitário antes da execução.
- **Pendente**: posição em planta sem cota no caderno original e sem base segura para propor — afeta o eixo/posição do ponto, não apenas a altura.

## Pendências em aberto (dependem de arquivo/decisão ainda não recebidos)
1. **Posição da ilha da cozinha** em relação à parede — necessária para converter o eixo do lava-louças (hoje referenciado à borda da ilha, por decisão do cliente). Precisa do modelo SketchUp ou de medida direta.
2. **Afastamento da parede esquerda** da cuba/torneira de bancada do Gourmet — não consta no caderno original.
3. **Prancha 01/02 do Caderno de Ar Condicionado** — só foi recebida a 02/02; a 01/02 pode conter informação relevante de forro/dreno de condensado que intercepte shafts hidráulicos.
4. Eixo dos registros gerais (dentro dos armários) em todos os banheiros — posição de projeto, não um dado padronizável.
5. Cota de fechamento da cuba/torneira de bancada do WC Suíte Master contra a parede lateral oposta.

## Base utilizada
- **Caderno Detalhamento Residência IC — Hidráulica Detalhe**, Revisão 02, 24/09/2026 (`referencias/pdfs_originais/`) — fonte de todos os pontos, eixos e alturas confirmados.
- **Caderno Detalhamento Residência IC — Ar Condicionados**, Revisão 01, 23/09/2026 (`referencias/pdfs_originais/`) — cruzado para nomenclatura de ambientes e identificar possíveis interferências (dreno de condensado).
- **PROJETO IVAN E ANA - R01.dwg** (`referencias/`) — mesmo arquivo usado no Caderno de Detalhamento de Piso da sessão anterior. Confirmado pelo cliente (28/09/2026) como planta-base. Usado apenas para a planta geral (prancha 00/08): paredes e ambientes, camada "PLANTA DE PISO". O DWG **não contém** pontos hidráulicos internos — as camadas "Esgoto" e "AGUAS PLUVIAIS" existem apenas na planta de implantação (ligação à rede pública).
- Modelo SketchUp: **não recebido** nesta sessão — necessário para resolver a pendência 1 acima.

## Decisões do cliente incorporadas (28/09/2026)
- Nome do projeto/clientes: "Ivan e Carol" (mantido, apesar de o DWG e o caderno de AC usarem "Ivan e Ana").
- Nome do ambiente: "WC Suíte Master" (mantido; original chamava "WC Casal").
- Chuveiros: tipo ducha (misturador), alimentados por água quente de origem externa — não elétricos.
- Lava-louças: cota mantida a partir da borda da ilha (não da parede) até a posição da ilha ser confirmada.
- WC Externo: altura do A.F. da bancada corrigida para 0,60 m (igual aos demais WCs).
- Lavanderia: mantidos os dois eixos de torneira de parede independentes.
- Gourmet: sem equipamento adicional de água.
- Secadora: elétrica — sem ponto de água/esgoto dedicado.
- Alturas/afastamentos ausentes no caderno original: adotar valores usuais de mercado, sinalizados como proposta.

## Como regenerar
```bash
cd caderno/fonte
npm i playwright                          # uma vez (Chromium já vem pré-instalado no ambiente)
python3 pranchas_hidraulica.py             # gera caderno_hidraulica.html
node imprimir.mjs                          # PDF A2 + prévias PNG (Chromium)
```
- **Dados:** pontos, eixos, alturas e status de cada ambiente são editados em `fonte/dados_hidraulica.py`.
- **Desenho:** estilo, layout e regras de posicionamento dos selos/pontos são editados em `fonte/pranchas_hidraulica.py`.
- **Base geométrica da planta geral:** `fonte/zonas_dwg.json` (polígonos dos ambientes extraídos do DWG, mesma convenção de coordenadas do Caderno de Piso: coordenadas locais = coordenadas do espaço do modelo do DWG − (3895, 760), em metros).
