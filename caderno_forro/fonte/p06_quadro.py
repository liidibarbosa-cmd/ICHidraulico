# -*- coding: utf-8 -*-
"""Prancha 06 — Quadro de materiais, quantitativos, notas de execução, normas e pendências."""
from base import *
from dados_forro import *

PILL = {'doc': '<span class="pill doc">DOC</span>', 'prop': '<span class="pill prop">PROPOSTA</span>',
        'pend': '<span class="pill pend">A DEFINIR</span>'}


def perimetro(a):
    if 'rect' in a:
        x0, y0, x1, y1 = a['rect']
        return 2 * ((x1 - x0) + (y1 - y0))
    p = a['poly']
    return sum(((p[i][0] - p[i - 1][0]) ** 2 + (p[i][1] - p[i - 1][1]) ** 2) ** 0.5 for i in range(len(p)))


def prancha():
    v = SVG()
    mats = [
        ('M1', 'Placa de gesso ST (standard)', 'Closet, suítes, home office, circulação, despensa, estar/jantar; testeiras e laterais do rasgo',
         'Placa para ambiente seco', 'Espessura e tipo de borda: manual do fabricante', 'prop'),
        ('M2', 'Placa de gesso RU (verde)', 'Banho Suíte Master, Banho Suíte 1, Banho Suíte 2, Banho 4',
         'Resistente à umidade · não impermeável', 'Espessura e espaçamentos para RU: manual do fabricante', 'doc'),
        ('M3', 'Placa de gesso RU (verde)', 'Cozinha e A.S.', 'Vapor de cocção e lavagem', 'Idem M2', 'prop'),
        ('M4', 'Estrutura de aço galvanizado', 'Todos os forros, testeiras e laterais', 'Perfis para forro (ABNT NBR 15217)',
         'Tipo, espaçamento e emendas: manual do fabricante', 'pend'),
        ('M5', 'Pendurais e fixação na laje', 'Todos os forros', 'Ancoragem adequada à laje pré-fabricada',
         'Tipo, espaçamento e carga: fabricante + projeto estrutural', 'pend'),
        ('M6', 'Tabica perimetral', 'Todos os encontros forro × parede (D1, D2)', 'Junta aberta (negativo), cor branca',
         'Modelo e largura a aprovar', 'prop'),
        ('M7', 'Cantoneira de proteção de aresta', 'Arestas das testeiras CT1/CT2 e do rasgo RG1', 'Aresta reta e protegida',
         'Modelo conforme fabricante', 'prop'),
        ('M8', 'Fita e massa para juntas', 'Todas as juntas; nos banhos, produtos para RU', 'Tratamento de juntas do sistema',
         'Produtos e demãos: manual do fabricante', 'pend'),
        ('M9', 'Parafusos e fixações', 'Placa × perfil, perfil × perfil', 'Aço com proteção à corrosão', 'Tipo e espaçamento: fabricante', 'pend'),
        ('M10', 'Pintura', 'ST: acrílica fosca branca · RU: tinta para áreas úmidas · fundo de cortineiros e rasgo: branco fosco',
         'Acabamento final', 'Preparação e produto: fabricantes do forro e da tinta', 'prop'),
        ('M11', 'Alçapão de inspeção', 'AL1 (circulação), só se o rasgo tiver fonte externa', 'Alçapão pronto para drywall', 'Medida do modelo', 'prop'),
        ('M12', 'Perfil de junta de controle', 'Estar/jantar, se exigido', 'Junta de movimentação', 'Critério: manual do fabricante', 'pend'),
    ]
    linhas = ''.join(f'<tr><td><b>{c}</b></td><td><b style="font-weight:600">{m}</b></td><td>{o}</td><td>{e}</td><td>{d}</td><td>{PILL[k]}</td></tr>'
                     for c, m, o, e, d, k in mats)
    qA = box(12, 12, 418, 190, 'b-creme big', 'Quadro de materiais', 'QUADRO 1',
             f'''<table><tr><th style="width:9mm">CÓD.</th><th style="width:48mm">MATERIAL</th><th>ONDE</th><th style="width:60mm">ESPECIFICAÇÃO DE PROJETO</th>
             <th style="width:70mm">DADO TÉCNICO · FONTE</th><th style="width:20mm">STATUS</th></tr>{linhas}</table>
             <div style="font-size:8.4pt;font-weight:300;margin-top:2.4mm">Nenhum valor de espessura, espaçamento ou fixação foi adotado sem fonte:
             esses dados virão do manual do fabricante escolhido (a definir) e da ABNT NBR 15758-2.</div>''')

    st = sum(a['area'] for a in AMB if a['placa'] == 'ST')
    ru = sum(a['area'] for a in AMB if a['placa'] == 'RU')
    rup = sum(a['area'] for a in AMB if a['placa'] == 'RUp')
    per = sum(perimetro(a) for a in AMB)
    rows = ''.join(f'<tr><td>{a["nome"].title().replace("A.s.", "A.S.")}</td><td>{ {"RU":"RU","RUp":"RU · prop.","ST":"ST"}[a["placa"]] }</td>'
                   f'<td class="n">{br(a["area"])}</td><td class="n">{br(perimetro(a), 1)}</td></tr>' for a in AMB)
    qB = box(12, 206, 170, 204, 'b-bege big', 'Quantitativos', 'QUADRO 2',
             f'''<table><tr><th>AMBIENTE</th><th>PLACA</th><th style="text-align:right">ÁREA m²</th><th style="text-align:right">PERÍM. m</th></tr>{rows}
             <tr><td><b>Total ST</b></td><td></td><td class="n"><b>{br(st)}</b></td><td></td></tr>
             <tr><td><b>Total RU (banhos)</b></td><td></td><td class="n"><b>{br(ru)}</b></td><td></td></tr>
             <tr><td><b>Total RU proposta</b> (coz. + A.S.)</td><td></td><td class="n"><b>{br(rup)}</b></td><td></td></tr>
             <tr><td><b>Tabica (perímetros)</b></td><td></td><td></td><td class="n"><b>≈ {br(per, 1)}</b></td></tr>
             <tr><td><b>Cortineiros</b> CT1 + CT2</td><td>20 cm</td><td></td><td class="n"><b>15,00</b></td></tr>
             <tr><td><b>Rasgo</b> RG1</td><td>12 cm</td><td></td><td class="n"><b>8,20</b></td></tr></table>
             <div style="font-size:8pt;font-weight:300;margin-top:2mm;line-height:1.3">Áreas do DWG (planta de forro). Perímetros pelas faces internas.
             Referência para orçamento: sem perdas, testeiras e recortes. Conferir em obra.</div>''')

    notas = [
        ('Antes de começar', ['Conferir todas as medidas e níveis no local; marcar o nível do forro nas paredes.',
                              'Concluir e testar elétrica, ar-condicionado (linhas e dreno), hidráulica e coifa no entreforro.',
                              'Marcar na laje as linhas dos cortineiros (20 cm da parede acabada) e do rasgo.']),
        ('Montagem', ['Estrutura, pendurais, fixações e espaçamentos conforme manual do fabricante e NBR 15758-2.',
                      'Nenhuma carga pendurada só na placa: cassete, pendentes e peças pesadas na laje ou na estrutura (D3, D5, D6).',
                      'Recortes de luminárias com a peça ou o gabarito na mão; conferir a altura de embutimento (entreforro de 15 cm).']),
        ('Cortineiros e rasgo', ['Vão livre de 20 cm contínuo, sem pendural ou perfil dentro do vão.',
                                 'Fixar trilho e suportes de luz antes de fechar; driver acessível pelo vão.',
                                 'Arestas com cantoneira, retas e contínuas; fundo pintado de branco fosco.']),
        ('Banhos', ['Placa RU, massa e fita para áreas úmidas; pintura própria para áreas úmidas.',
                    'RU não é impermeável: sem contato direto com água; ambiente ventilado.']),
        ('Acabamento', ['Tabica em todo o perímetro; juntas tratadas, lixadas e pintadas sem marcas sob luz rasante (cortineiros).']),
    ]
    corpo = '<div class="obs">' + ''.join(
        f'<div class="i"><span class="t" style="color:{C["creme"]}">{t}</span><p>' + '<br>'.join(f'· {x}' for x in itens) + '</p></div>'
        for t, itens in notas) + '</div>'
    qC = box(186, 206, 244, 204, 'b-rust big', 'Notas de execução', 'QUADRO 3', corpo)

    pend = [
        ('Decidido em 30/09/2026', ['Cortineiros com vão livre de 20 cm; comprimentos gerais do DWG.',
                                    'Rasgo com luz para baixo, reforçando a iluminação geral.',
                                    'Garagem, varanda e beirais sem forro (revestimento a detalhar).',
                                    'Luminárias sem locação na planta de forro.',
                                    'Fita LED, Tuboled e cortina definidos depois, com os fornecedores.']),
        ('Aguardando aprovação', ['RU na cozinha e na A.S.; ST nos secos.', 'Tabica perimetral (D1).',
                                  'Dimensões e posição do rasgo (12 cm, a 15 cm da parede, 8,20 m).',
                                  'Testeira, fonte na testeira e driver no vão (prancha 02).',
                                  'Fundos pintados, cantoneiras, alçapão AL1, fixações D3–D6.']),
        ('A definir', ['Fabricante de referência e seu manual técnico.', 'Box até o teto? Exaustão nos banhos?',
                       'Modelos de luminárias (fichas técnicas) e do cassete E1.',
                       'CAU da Isadora Ferrari: A263982-8 (iluminação) × A269382-8 (esquadrias).',
                       'Altura da J01: 2,50 m (esquadrias) × 2,00 m (DWG).']),
    ]
    corpoP = '<div class="obs">' + ''.join(
        f'<div class="i"><span class="t">{t}</span><p>' + '<br>'.join(f'· {x}' for x in itens) + '</p></div>' for t, itens in pend) + \
        '</div><div style="font-weight:700;font-size:7.4pt;letter-spacing:.8pt;margin-top:1mm">NORMAS E REFERÊNCIAS</div>' \
        '<p style="font-size:8.6pt;font-weight:300;line-height:1.35;margin-top:.8mm">ABNT NBR 15758-2 (forros em chapas de gesso para drywall) · ' \
        'ABNT NBR 14715-1 (chapas de gesso) · ABNT NBR 15217 (perfis de aço) · manual técnico do fabricante escolhido · ' \
        'cadernos de iluminação 02/04, tomadas 01/04, ar-condicionado 02/02, esquadrias e hidráulica · DWG “Projeto Ivan e Ana R01”.</p>'
    qD = box(438, 12, 146, 311, 'b-bege big', 'Decisões e pendências', 'QUADRO 4', corpoP)
    extra = qA + qB + qC + qD + carimbo(438, 327, 146, 83, 'Materiais e notas', 'sem escala', 6, TOTAL)
    return pagina(str(v), extra)
