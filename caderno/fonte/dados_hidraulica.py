# -*- coding: utf-8 -*-
"""
Dados dos pontos hidraulicos - Residencia Ivan e Carol - Nova Odessa, SP.

Fontes:
- CADERNO DETALHAMENTO RESIDENCIA IC - HIDRAULICA DETALHE.pdf (Revisao 02, 24/09/2026) -> "cad"
- PROJETO IVAN E ANA - R01.dwg, camada "PLANTA DE PISO" (mesma base da sessao de pisos) -> "dwg"
- Decisoes tomadas em conversa com o cliente em 28/09/2026 -> "cliente"
- Alturas/afastamentos ausentes no caderno original: propostas de mercado (NBR 5626, 5628,
  7198 e 8160 como referencia normativa geral; NAO sao valores normativos fixos, sao praticas
  usuais de instalacao) -> "proposta"

status possiveis por valor: "confirmado" (vem do caderno original), "proposta" (adotado por nos,
falta validacao do responsavel hidrossanitario), "pendente" (nem confirmado nem proponivel com
segurenca - posicao de projeto que so o cliente/escritorio define).
"""

REV = "R01"
DATA = "28/09/2026"
CLIENTES = "Ivan e Carol"
ENDERECO = "Nova Odessa, SP"
RESP = [("Arq. Lidiane Barbosa", "CAU A290220-6"), ("Arq. Isadora Ferrari", "CAU A269382-8")]
ORIGEM = "Caderno Detalhamento Residencia IC - Hidraulica Detalhe, Rev. 02, 24/09/2026 + PROJETO IVAN E ANA - R01.dwg"

TIPOS = {
    "AF": dict(nome="Agua fria", cor="#2f5f8a", sigla="A.F."),
    "AQ": dict(nome="Agua quente", cor="#a3402f", sigla="A.Q."),
    "ESG": dict(nome="Esgoto", cor="#c98a2e", sigla="ESG"),
    "VD": dict(nome="Valvula de descarga", cor="#4f7a3f", sigla="V.D."),
    "RG": dict(nome="Registro geral", cor="#c9a92e", sigla="R.G."),
}

# cada ponto: id, nome, x, y (m, coordenadas locais do desenho esquematico do ambiente,
# origem no canto inferior-esquerdo do retangulo do ambiente), pontos_agua: lista de
# {tipo, altura, status, origem}
# eixo_status: "confirmado" (x,y vem do caderno) | "pendente" (posicao nao cotada, sem invencao)
# nota: quando eixo_status="pendente", x/y sao apenas um posicionamento esquematico para
# desenhar o simbolo (marcado com contorno tracejado), NAO uma cota valida.

AMBIENTES = {

"COZ": dict(
    prancha="01", nome="Cozinha", W=4.25, H=4.20,
    parede_ref="Eixos verticais a partir da parede inferior (filtro). Geladeira a partir das paredes esquerda e direita. Lava-loucas a partir da borda da ilha (posicao da ilha ainda nao determinada - ver observacao).",
    porta=(0.0, 0.0, "H"),
    pontos=[
        dict(id="1", nome="Filtro", x=0.0, y=1.00, eixo_status="confirmado",
             eixo_txt="1,00 da parede inferior",
             agua=[dict(tipo="AF", altura=1.00, status="confirmado")]),
        dict(id="2", nome="Cuba pia · torneira de bancada", x=0.0, y=2.15, eixo_status="confirmado",
             eixo_txt="1,15 a partir do eixo do filtro · 2,05 ate a parede superior",
             agua=[dict(tipo="AQ", altura=0.50, status="confirmado"),
                   dict(tipo="AF", altura=0.50, status="proposta", origem="mesma linha do A.Q. confirmado"),
                   dict(tipo="ESG", altura=0.35, status="confirmado")]),
        dict(id="3", nome="Geladeira", x=3.60, y=4.20, eixo_status="confirmado",
             eixo_txt="3,60 da parede esquerda · 0,50 ate a parede direita (confere aprox. com o DWG, tolerancia 0,15 m)",
             agua=[dict(tipo="AF", altura=1.25, status="confirmado")]),
        dict(id="4", nome="Lava-louças (ilha)", x=1.90, y=0.60, eixo_status="pendente",
             eixo_txt="0,40 da borda esquerda da ilha — posicao da ilha em relacao a parede AINDA NAO DEFINIDA (decisao do cliente: manter por ora referenciado a ilha)",
             agua=[dict(tipo="AF", altura=0.60, status="confirmado"),
                   dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao sob a cuba, pratica usual")]),
    ],
    obs=[
        "Cotas em planta reproduzidas do caderno original (Revisao 02), sem alteracao.",
        "Eixo do lava-loucas cotado a partir da borda da ilha, nao da parede — referencia nao inequivoca. Decisao do cliente (28/09/2026): manter a referencia da ilha por enquanto; converter para a parede assim que a posicao da ilha for confirmada (medida direta ou modelo SketchUp).",
        "Altura de A.F. na cuba/torneira de bancada e de E.S.G. no lava-loucas: PROPOSTA nossa (mercado), nao constam no caderno original. Validar com o responsavel hidrossanitario antes da execucao.",
        "Normas de referencia: NBR 5626 (agua fria), NBR 7198 (agua quente) e NBR 8160 (esgoto sanitario).",
    ],
),

"GOU": dict(
    prancha="02", nome="Gourmet", W=4.55, H=2.20,
    parede_ref="Parede superior (2,80) e parede inferior (1,75). Afastamento da parede esquerda NAO COTADO no caderno original.",
    porta=(4.55, 0.0, "H"),
    pontos=[
        dict(id="1", nome="Cuba · torneira de bancada", x=2.30, y=1.10, eixo_status="pendente",
             eixo_txt="2,80 da parede superior · 1,75 ate a parede inferior (fecha com a profundidade do ambiente) — afastamento da parede esquerda NAO COTADO: posicao horizontal aproximada, NAO cotar em obra sem confirmar",
             agua=[dict(tipo="AQ", altura=0.50, status="confirmado"),
                   dict(tipo="AF", altura=0.50, status="proposta", origem="mesma linha do A.Q. confirmado"),
                   dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao sob a cuba, pratica usual")]),
    ],
    obs=[
        "Cliente confirmou (28/09/2026): este ambiente nao tera nenhum equipamento adicional de agua (sem geladeira/adega/maquina de gelo).",
        "Falta o afastamento da parede esquerda da cuba/torneira de bancada — nao e uma altura de instalacao padronizavel, e uma posicao de projeto. Precisamos dessa medida (planta cotada complementar, SketchUp ou medicao em campo) antes de fixar o eixo definitivo.",
        "Altura de A.F. e de E.S.G.: PROPOSTA nossa (mercado), a validar com o responsavel hidrossanitario.",
    ],
),

"LAV": dict(
    prancha="03", nome="Lavanderia", W=2.55, H=2.00,
    parede_ref="Parede esquerda, com cotas encadeadas (0,40 · 0,60 · 0,80 · 0,75).",
    porta=(2.55, 0.0, "H"),
    pontos=[
        dict(id="1", nome="Torneira de parede · tanque", x=0.40, y=1.60, eixo_status="confirmado",
             eixo_txt="0,40 da parede esquerda",
             agua=[dict(tipo="AF", altura=1.00, status="proposta", origem="altura usual de torneira de parede alta para tanque")]),
        dict(id="2", nome="Torneira de parede · tanque", x=1.00, y=1.60, eixo_status="confirmado",
             eixo_txt="0,60 a partir do eixo 1",
             agua=[dict(tipo="AF", altura=1.00, status="proposta", origem="altura usual de torneira de parede alta para tanque")]),
        dict(id="3", nome="Maquina de lavar roupas", x=1.80, y=1.60, eixo_status="confirmado",
             eixo_txt="0,80 a partir do eixo 2",
             agua=[dict(tipo="AF", altura=0.70, status="confirmado"),
                   dict(tipo="ESG", altura=0.60, status="proposta", origem="altura usual de saida da maquina de lavar")]),
        dict(id="4", nome="Tanquinho", x=2.55, y=1.60, eixo_status="confirmado",
             eixo_txt="0,75 a partir do eixo 3",
             agua=[dict(tipo="AF", altura=0.70, status="confirmado"),
                   dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao do tanquinho, pratica usual")]),
        dict(id="5", nome="A.F. + ESG da bancada do tanque", x=1.20, y=0.30, eixo_status="pendente",
             eixo_txt="EIXO NAO COTADO no caderno original — posicao esquematica, NAO cotar em obra",
             agua=[dict(tipo="AF", altura=1.00, status="confirmado"),
                   dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao, pratica usual")]),
    ],
    obs=[
        "PENDENCIA DE PROJETO (mantida por decisao do cliente, 28/09/2026): sao DOIS eixos de torneira de parede independentes (pontos 1 e 2), reproduzindo o caderno original tal como esta. A vista do caderno original mostrava um unico ponto de A.F. entre as duas torneiras — nao reproduzimos essa vista; os dois eixos em planta valem como projetados.",
        "Secadora: cliente confirmou (28/09/2026) que sera ELETRICA — nao ha ponto de agua ou esgoto dedicado a ela nesta prancha.",
        "Alturas de A.F. nas torneiras de parede e de E.S.G. na maquina de lavar e no tanquinho: PROPOSTA nossa (mercado), a validar com o responsavel hidrossanitario.",
        "Eixo do ponto 5 nao consta no caderno original e nao e um dado padronizavel — posicao em planta pendente de definicao.",
    ],
),

}

# WCs: mesma estrutura de pontos (chuveiro tipo ducha com A.Q. externa, registros, ducha
# higienica, bacia, valvula de descarga, cuba/torneira de bancada, registro geral).
def wc(prancha, nome, W, H, chain_txt, chuveiro_x, registros_afast_status,
       ducha_x, bacia_x, vd_x_status, cuba_x, rg_status, ag_extra=None, obs_extra=None):
    pontos = [
        dict(id="1", nome="Chuveiro (tipo ducha)", x=chuveiro_x, y=0.0, eixo_status="confirmado",
             eixo_txt=f"{chuveiro_x:.2f} da parede de referencia",
             agua=[dict(tipo="AF", altura=2.10, status="confirmado")]),
        dict(id="2", nome="Registros do chuveiro", x=chuveiro_x, y=0.0, eixo_status="confirmado",
             eixo_txt="mesmo eixo do chuveiro — afastamento lateral entre A.Q. e A.F. " + registros_afast_status,
             agua=[dict(tipo="AQ", altura=1.10, status="confirmado"),
                   dict(tipo="AF", altura=1.10, status="confirmado")]),
        dict(id="3", nome="Ducha higienica", x=ducha_x, y=0.0, eixo_status="confirmado",
             eixo_txt=f"{ducha_x:.2f} da parede de referencia",
             agua=[dict(tipo="AF", altura=0.50, status="proposta", origem="altura usual de ducha higienica")]),
        dict(id="4", nome="Bacia sanitaria", x=bacia_x, y=0.0, eixo_status="confirmado",
             eixo_txt=f"{bacia_x:.2f} da parede de referencia",
             agua=[dict(tipo="AF", altura=0.30, status="proposta", origem="altura usual de alimentacao de caixa acoplada"),
                   dict(tipo="ESG", altura=0.0, status="confirmado", origem="ESG no piso, conforme caderno original")]),
        dict(id="5", nome="Valvula de descarga", x=bacia_x, y=0.0, eixo_status=vd_x_status,
             eixo_txt="mesmo eixo da bacia sanitaria (posicao usual — valvula fica sobre a saida da bacia)",
             agua=[dict(tipo="VD", altura=1.10, status="proposta", origem="altura usual de acionamento de valvula de descarga")]),
        dict(id="6", nome="Cuba pia · torneira de bancada", x=cuba_x, y=0.0, eixo_status="confirmado",
             eixo_txt=f"{cuba_x:.2f} da parede de referencia",
             agua=(ag_extra or [dict(tipo="AF", altura=0.60, status="confirmado"),
                   dict(tipo="AQ", altura=0.60, status="proposta", origem="mesma linha do A.F. confirmado"),
                   dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao, pratica usual")])),
        dict(id="7", nome="Registro geral (dentro do armario)", x=cuba_x, y=H*0.5, eixo_status="pendente",
             eixo_txt="EIXO NAO COTADO no caderno original — posicao esquematica dentro do armario, NAO cotar em obra",
             agua=[dict(tipo="RG", altura=0.55, status=rg_status,
                        origem="valor confirmado no caderno original para o WC Externo (unico R.G. cotado na casa) — adotado aqui por analogia" if rg_status=="proposta" else "confirmado no caderno original")]),
    ]
    obs = [
        "Chuveiro mantido como tipo ducha (misturador), alimentado por agua quente de origem externa (nao eletrico) — decisao do cliente, 28/09/2026.",
        "Cotas de eixo em planta reproduzidas do caderno original (Revisao 02), " + chain_txt,
        "Alturas marcadas como PROPOSTA sao valores usuais de mercado (nao constam no caderno original) — decisao do cliente (28/09/2026): adotar e sinalizar, aguardando validacao do responsavel hidrossanitario antes da execucao.",
        "Eixo do registro geral nao consta no caderno original: e uma posicao de projeto (local dentro do armario), nao um dado padronizavel — mantido pendente.",
        "Normas de referencia: NBR 5626 (agua fria), NBR 7198 (agua quente) e NBR 8160 (esgoto sanitario).",
    ]
    if obs_extra:
        obs = obs_extra + obs
    return dict(prancha=prancha, nome=nome, W=W, H=H, parede_ref="Parede de referencia, cotas encadeadas: " + chain_txt,
                porta=(0.0, 0.0, "H"), pontos=pontos, obs=obs)

AMBIENTES["WC1"] = wc("04", "WC 01", 2.90, 1.50,
    "0,45 · 0,75 · 0,20 · 0,95 · 0,55 (chuveiro / ducha / bacia / cuba / parede direita).",
    0.45, "NAO COTADO no caderno original (PROPOSTA: 0,06 m, afastamento usual entre registros)",
    1.20, 1.40, "pendente", 2.35, "proposta")

AMBIENTES["WC2"] = wc("05", "WC 02", 2.90, 1.50,
    "0,45 · 0,75 · 0,20 · 0,95 · 0,55 (chuveiro / ducha / bacia / cuba / parede direita) — disposicao espelhada em relacao ao WC 01.",
    0.45, "NAO COTADO no caderno original (PROPOSTA: 0,06 m, afastamento usual entre registros)",
    1.20, 1.40, "pendente", 2.35, "proposta")

AMBIENTES["WCE"] = wc("07", "WC Externo", 3.10, 1.40,
    "0,55 · 0,60 · 0,20 · 0,60 · 1,15 (chuveiro / ducha / bacia / cuba / parede direita).",
    0.55, "NAO COTADO no caderno original (PROPOSTA: 0,06 m, afastamento usual entre registros)",
    1.15, 1.35, "pendente", 1.95, "confirmado",
    ag_extra=[dict(tipo="AF", altura=0.60, status="confirmado", origem="decisao do cliente 28/09/2026: usar 0,60 m, mesma referencia dos demais WCs, em vez do valor de 0,55 m que no caderno original estava sobreposto ao do registro geral"),
              dict(tipo="AQ", altura=0.60, status="proposta", origem="mesma linha do A.F."),
              dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao, pratica usual")],
    obs_extra=["Divergencia resolvida (decisao do cliente, 28/09/2026): a altura do A.F. da cuba/torneira de bancada passa a ser 0,60 m, igual aos demais WCs — no caderno original ela aparecia na vista sobreposta a linha do registro geral (0,55 m), sem cota propria. O registro geral deste ambiente mantem seus 0,55 m, que sao o UNICO valor de R.G. confirmado em todo o caderno original — por isso foi adotado por analogia nos demais banheiros."])

# WC Suite Master: layout proprio (chuveiro numa parede, ducha/bacia/cuba noutra).
AMBIENTES["WCS"] = dict(
    prancha="06", nome="WC Suíte Master", W=1.95, H=3.50,
    parede_ref="Parede superior, cotas encadeadas: 0,25 (ducha) · 0,20 (bacia) · 1,15 (cuba). Chuveiro em parede propria: 1,25 a partir do eixo da cuba · 0,55 ate a parede inferior (fecha com tolerancia de 0,10 m em relacao a cadeia acumulada).",
    porta=(0.0, 3.50, "H"),
    pontos=[
        dict(id="3", nome="Ducha higienica", x=0.0, y=3.25, eixo_status="confirmado",
             eixo_txt="0,25 da parede superior",
             agua=[dict(tipo="AF", altura=0.50, status="proposta", origem="altura usual de ducha higienica")]),
        dict(id="4", nome="Bacia sanitaria", x=0.0, y=3.05, eixo_status="confirmado",
             eixo_txt="0,20 a partir do eixo da ducha",
             agua=[dict(tipo="AF", altura=0.30, status="proposta", origem="altura usual de alimentacao de caixa acoplada"),
                   dict(tipo="ESG", altura=0.0, status="confirmado", origem="ESG no piso, conforme caderno original")]),
        dict(id="5", nome="Valvula de descarga", x=0.0, y=3.05, eixo_status="pendente",
             eixo_txt="mesmo eixo da bacia sanitaria (posicao usual)",
             agua=[dict(tipo="VD", altura=1.10, status="proposta", origem="altura usual de acionamento de valvula de descarga")]),
        dict(id="6", nome="Cuba pia · torneira de bancada", x=0.0, y=1.90, eixo_status="confirmado",
             eixo_txt="1,15 a partir do eixo da bacia — falta a cota de fechamento ate a parede lateral oposta",
             agua=[dict(tipo="AF", altura=0.60, status="confirmado"),
                   dict(tipo="AQ", altura=0.60, status="proposta", origem="mesma linha do A.F. confirmado"),
                   dict(tipo="ESG", altura=0.50, status="proposta", origem="saida de sifao, pratica usual")]),
        dict(id="1", nome="Chuveiro (tipo ducha)", x=0.0, y=0.55, eixo_status="confirmado",
             eixo_txt="1,25 a partir do eixo da cuba · 0,55 ate a parede inferior",
             agua=[dict(tipo="AF", altura=2.10, status="confirmado")]),
        dict(id="2", nome="Registros do chuveiro", x=0.0, y=0.55, eixo_status="confirmado",
             eixo_txt="mesmo eixo do chuveiro — afastamento lateral entre A.Q. e A.F. NAO COTADO (PROPOSTA: 0,06 m)",
             agua=[dict(tipo="AQ", altura=1.10, status="confirmado"),
                   dict(tipo="AF", altura=1.10, status="confirmado")]),
        dict(id="7", nome="Registro geral (dentro do armario)", x=0.0, y=1.90, eixo_status="pendente",
             eixo_txt="EIXO NAO COTADO no caderno original — posicao esquematica dentro do armario, NAO cotar em obra",
             agua=[dict(tipo="RG", altura=0.55, status="proposta",
                        origem="valor confirmado no caderno original para o WC Externo (unico R.G. cotado na casa) — adotado aqui por analogia")]),
    ],
    obs=[
        "Nome do ambiente mantido como 'WC Suite Master' (decisao do cliente, 28/09/2026) — no caderno original ele aparece como 'WC Casal' e no DWG de referencia como 'Banheiro Casal'.",
        "Chuveiro mantido como tipo ducha (misturador), alimentado por agua quente de origem externa (nao eletrico) — decisao do cliente, 28/09/2026.",
        "O chuveiro fica em parede propria, distinta da parede onde estao ducha/bacia/cuba — a cadeia de cotas do caderno original fecha com 0,10 m de tolerancia; nao e uma cota exata, e sim a soma dos trechos publicados.",
        "Falta a cota que fecha a cuba/torneira de bancada contra a parede lateral oposta — nao e uma altura padronizavel, precisamos dessa medida.",
        "Alturas marcadas como PROPOSTA sao valores usuais de mercado (nao constam no caderno original) — decisao do cliente (28/09/2026): adotar e sinalizar, aguardando validacao do responsavel hidrossanitario.",
        "Normas de referencia: NBR 5626 (agua fria), NBR 7198 (agua quente) e NBR 8160 (esgoto sanitario).",
    ],
)

ORDEM = ["COZ", "GOU", "LAV", "WC1", "WC2", "WCS", "WCE"]
