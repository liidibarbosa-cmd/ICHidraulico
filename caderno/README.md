# Caderno de Detalhamento Hidráulico — Pontos em Planta — R02
Residência Ivan e Carol · Nova Odessa, SP · 28/09/2026

## Entregáveis
| Arquivo | Conteúdo |
|---|---|
| `CADERNO DE DETALHAMENTO HIDRAULICO - PONTOS EM PLANTA - R02.pdf` | 11 folhas A3 retrato (297 × 420 mm). Imprimir sem ajuste de escala. |
| `fonte/` | Arquivos-fonte editáveis que geram o PDF. |
| `fonte/previa_v2/v2_XX.png` | Renderização de cada folha do PDF (revisão visual). |

Folhas:
- 01/11 — planta geral de pontos hidráulicos (visão de conjunto, sobre a planta de layout real)
- 02/11 — Cozinha
- 03/11 — Gourmet
- 04/11 — Lavanderia
- 05/11 — WC 01
- 06/11 — WC 02
- 07/11 — WC Suíte Master
- 08/11 — WC Externo
- 09/11 — Quadro de pontos hidráulicos, tabela (1/2)
- 10/11 — Quadro de pontos hidráulicos, tabela (2/2)
- 11/11 — Status, pendências e normas de referência

## Referências visuais desta revisão (R02)
A pedido do cliente (28/09/2026), esta revisão foi refeita para seguir duas referências à risca:
- **Layout do caderno**: réplica da estrutura do *Caderno Detalhamento Residência IC — Portas e Janelas* (Rev. 01, 30/08/2026) — folha A3 retrato, bloco de legenda simples à direita, bloco de escala com barra gráfica e nota "imprimir sem ajuste de escala", caixa de referência remetendo ao quadro final, carimbo DUAS (verde-oliva, com barra "CONFERIR AS MEDIDAS NO LOCAL") e página final em formato de quadro/tabela com notas numeradas por categoria.
- **Representação dos pontos em planta**: réplica do estilo de referência do Portal Criativo — pontos coloridos por tipo (A.F./A.Q./ESG/V.D./R.G.), cotas em vermelho com linha e tiques de chamada, rótulo textual "SIGLA H=altura" ao lado de cada ponto, nome do ambiente e escala sob o desenho.
- **Planta-base**: `DETALHAMENTO A2 - LAYOUT - RESIDENCIA IC.pdf` (LayOut do SketchUp, Rev. 01, 01/05/2026) — usada como imagem de fundo da planta geral (folha 01/11).

## Status dos dados
Cada ponto hidráulico tem um status de **altura** e um status de **eixo (posição em planta)**, mostrados no rótulo de cada ponto e consolidados nas folhas 09–10/11:

- **Confirmado**: dado do Caderno Detalhamento Residência IC — Hidráulica Detalhe (Revisão 02, 24/09/2026), ou decisão explícita do cliente em 28/09/2026. Pode ser executado.
- **Proposta** (marcada com \*, ponto com preenchimento translúcido): valor usual de mercado, adotado na ausência de cota no caderno original, a pedido do cliente (28/09/2026). Precisa de validação do responsável pelo projeto hidrossanitário antes da execução.
- **Pendente** (ponto tracejado + "?"): posição em planta sem cota no caderno original e sem base segura para propor — afeta o eixo/posição do ponto, não apenas a altura.

## Pendências em aberto (dependem de arquivo/decisão ainda não recebidos)
1. **Posição da ilha da cozinha** em relação à parede — necessária para converter o eixo do lava-louças (hoje referenciado à borda da ilha, por decisão do cliente). Precisa de medida direta ou do detalhamento de marcenaria da ilha.
2. **Afastamento da parede esquerda** da cuba/torneira de bancada do Gourmet — não consta no caderno original.
3. **Prancha 01/02 do Caderno de Ar Condicionado** — só foi recebida a 02/02; a 01/02 pode conter informação relevante de forro/dreno de condensado que intercepte shafts hidráulicos.
4. Eixo dos registros gerais (dentro dos armários) em todos os banheiros — posição de projeto, não um dado padronizável.
5. Cota de fechamento da cuba/torneira de bancada do WC Suíte Master contra a parede lateral oposta.

## Base utilizada
- **Caderno Detalhamento Residência IC — Hidráulica Detalhe**, Revisão 02, 24/09/2026 (`referencias/pdfs_originais/`) — fonte de todos os pontos, eixos e alturas confirmados.
- **Caderno Detalhamento Residência IC — Ar Condicionados**, Revisão 01, 23/09/2026 (`referencias/pdfs_originais/`) — cruzado para nomenclatura de ambientes e possíveis interferências (dreno de condensado).
- **Caderno Detalhamento Residência IC — Portas e Janelas**, Revisão 01, 30/08/2026 (`referencias/pdfs_originais/`) — modelo de layout/identidade visual do caderno (replicado nesta revisão).
- **DETALHAMENTO A2 - LAYOUT - RESIDENCIA IC.pdf**, Revisão 01, 01/05/2026 (`referencias/pdfs_originais/`) — LayOut do SketchUp com o mobiliário real; usado como imagem de fundo da planta geral (folha 01/11).
- **PROJETO IVAN E ANA - R01.dwg** (`referencias/`) — mesmo arquivo usado no Caderno de Detalhamento de Piso da sessão anterior; usado para os polígonos dos ambientes (`fonte/zonas_dwg.json`), camada "PLANTA DE PISO". O DWG **não contém** pontos hidráulicos internos.
- Modelo SketchUp 3D (arquivo `.skp`): **não recebido** nesta sessão — necessário para resolver a pendência 1 acima com mais precisão do que a planta de layout em PDF permite.

## Divergência de nomes observada (não resolvida)
O carimbo do `DETALHAMENTO A2 - LAYOUT` identifica os clientes como "Ivan Neris / Ana Carolina Neris" e o endereço como "Santa Odessa SP". Mantido "Ivan e Carol" / "Nova Odessa, SP" nesta revisão, por já ser a forma usada em todos os demais documentos e ter sido confirmada pelo cliente em 28/09/2026 — mas fica registrado aqui caso queiram atualizar o carimbo do LayOut também.

## Decisões do cliente incorporadas (28/09/2026)
- Nome do projeto/clientes: "Ivan e Carol".
- Nome do ambiente: "WC Suíte Master" (original chamava "WC Casal").
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
python3 pranchas_v2.py                     # gera caderno_hidraulica_v2.html
node imprimir_v2.mjs                       # PDF A3 retrato + prévias PNG (Chromium)
```
- **Dados:** pontos, eixos, alturas e status de cada ambiente são editados em `fonte/dados_hidraulica.py` (reaproveitado da revisão anterior, sem mudança de conteúdo).
- **Desenho:** estilo, layout, ícones de peças e regras de posicionamento dos pontos/cotas são editados em `fonte/pranchas_v2.py`.
- **Imagem de fundo da planta geral:** `fonte/imagens/planta_geral_bg.jpg`, recortada e rotacionada a partir do LayOut do SketchUp; os selos numerados são posicionados por coordenadas aproximadas (fração da imagem) definidas em `CENTRO_BG`, dentro de `pranchas_v2.py`.
- **Base geométrica das plantas por ambiente:** `fonte/zonas_dwg.json` (polígonos dos ambientes extraídos do DWG, mesma convenção de coordenadas do Caderno de Piso: coordenadas locais = coordenadas do espaço do modelo do DWG − (3895, 760), em metros) — usado apenas para conferência de proporções; os retângulos desenhados em cada prancha usam as dimensões dos próprios eixos cotados no caderno original.
