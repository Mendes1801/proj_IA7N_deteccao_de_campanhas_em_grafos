# Integrantes: Gabriel de Santana Santos | 10420595 | 10420595@mackenzista.com.br
#              Gabriel Erick Mendes | 10420391 | 10420391@mackenzista.com.br
#              Matheus Teles Magalhães | 10427410 | 10427410@mackenzista.com.br
# Conteúdo: geração do artigo parcial no formato SBC e preenchimento da rubrica N1.
# Histórico de alterações:
# 24/09/2026 | Grupo | Criação do gerador dos artefatos da entrega.

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_DIR = ROOT / "artigo"
FIGURE_DIR = ARTICLE_DIR / "figuras"
ARTICLE_DOCX = ARTICLE_DIR / "artigo_parcial.docx"
RUBRIC_SOURCE = ROOT / "projetoDeIA_parte2_rubrica.docx"
RUBRIC_OUTPUT = ROOT / "rubrica" / "rubrica_analitica_n1.docx"

TITLE = (
    "Classificação Precoce de Campanhas Coordenadas em Redes Sociais com "
    "Características de Grafos Parciais"
)

MEMBERS = [
    ("Gabriel de Santana Santos", "10420595", "10420595@mackenzista.com.br"),
    ("Gabriel Erick Mendes", "10420391", "10420391@mackenzista.com.br"),
    ("Matheus Teles Magalhães", "10427410", "10427410@mackenzista.com.br"),
]

DUPLICATE = "#SesimiziDuyanVarMi___2023-03-23_campaign_fulldata.json"


def set_run_font(run, name: str, size: float, *, bold: bool | None = None) -> None:
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    run.font.color.rgb = None


def set_cell_margins(cell, top: int = 70, start: int = 90, bottom: int = 70, end: int = 90) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_table_borders(table, color: str = "B7B7B7", size: int = 5) -> None:
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), str(size))
        node.set(qn("w:color"), color)


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_cell_text(cell, text: str, *, bold: bool = False, align=WD_ALIGN_PARAGRAPH.LEFT) -> None:
    cell.text = ""
    paragraph = cell.paragraphs[0]
    paragraph.alignment = align
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1
    run = paragraph.add_run(str(text))
    set_run_font(run, "Times New Roman", 10, bold=bold)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    set_cell_margins(cell)


def configure_article(document: Document) -> None:
    section = document.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(3)
    section.header_distance = Cm(0)
    section.footer_distance = Cm(0)

    normal = document.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.font.color.rgb = None
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.line_spacing = 1
    normal.paragraph_format.space_before = Pt(6)
    normal.paragraph_format.space_after = Pt(0)

    for style_name, size in (("Title", 16), ("Heading 1", 13), ("Heading 2", 12)):
        style = document.styles[style_name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = None
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_after = Pt(0)

    document.styles["Heading 1"].paragraph_format.space_before = Pt(12)
    document.styles["Heading 2"].paragraph_format.space_before = Pt(10)


def add_body(document: Document, text: str, *, indent: bool = True):
    paragraph = document.add_paragraph(style="Normal")
    paragraph.paragraph_format.first_line_indent = Cm(1.27) if indent else Cm(0)
    paragraph.paragraph_format.widow_control = True
    run = paragraph.add_run(text)
    set_run_font(run, "Times New Roman", 12)
    return paragraph


def add_heading(document: Document, text: str, level: int) -> None:
    paragraph = document.add_paragraph(style=f"Heading {level}")
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run(text)
    set_run_font(run, "Times New Roman", 13 if level == 1 else 12, bold=True)


def add_abstract(document: Document, label: str, text: str) -> None:
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragraph.paragraph_format.left_indent = Cm(0.8)
    paragraph.paragraph_format.right_indent = Cm(0.8)
    paragraph.paragraph_format.first_line_indent = Cm(0)
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1
    label_run = paragraph.add_run(f"{label}. ")
    set_run_font(label_run, "Times New Roman", 12, bold=True)
    text_run = paragraph.add_run(text)
    set_run_font(text_run, "Times New Roman", 12)


def add_table_caption(document: Document, number: int, text: str) -> None:
    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(6)
    paragraph.paragraph_format.keep_with_next = True
    run = paragraph.add_run(f"Tabela {number}. {text}")
    set_run_font(run, "Arial", 10, bold=True)


def add_figure(document: Document, path: Path, number: int, caption: str) -> None:
    image_paragraph = document.add_paragraph()
    image_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    image_paragraph.paragraph_format.space_before = Pt(6)
    image_paragraph.paragraph_format.space_after = Pt(0)
    image_paragraph.paragraph_format.keep_with_next = True
    image_paragraph.add_run().add_picture(str(path), width=Cm(14.4))

    caption_paragraph = document.add_paragraph()
    caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_paragraph.paragraph_format.space_before = Pt(6)
    caption_paragraph.paragraph_format.space_after = Pt(6)
    caption_run = caption_paragraph.add_run(f"Figura {number}. {caption}")
    set_run_font(caption_run, "Arial", 10, bold=True)


def add_article_table(document: Document, headers: list[str], rows: list[list[str]], widths: list[float]) -> None:
    table = document.add_table(rows=1, cols=len(headers))
    table.autofit = False
    set_table_borders(table)
    set_repeat_table_header(table.rows[0])
    for index, header in enumerate(headers):
        set_cell_text(table.rows[0].cells[index], header, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        table.rows[0].cells[index].width = Cm(widths[index])
    for values in rows:
        cells = table.add_row().cells
        for index, value in enumerate(values):
            alignment = WD_ALIGN_PARAGRAPH.LEFT if index == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_cell_text(cells[index], value, align=alignment)
            cells[index].width = Cm(widths[index])


def build_figures() -> tuple[Path, Path]:
    scale_path = FIGURE_DIR / "diferenca_escala.png"
    growth_path = FIGURE_DIR / "crescimento_normalizado.png"

    missing = [path for path in (scale_path, growth_path) if not path.exists()]
    if missing:
        names = ", ".join(path.name for path in missing)
        raise FileNotFoundError(
            f"Figuras ausentes ({names}). Execute scripts/gerar_figuras_artigo.py primeiro."
        )

    return scale_path, growth_path


def build_article() -> None:
    ARTICLE_DIR.mkdir(parents=True, exist_ok=True)
    scale_figure, growth_figure = build_figures()
    document = Document()
    configure_article(document)

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(12)
    title.paragraph_format.space_after = Pt(12)
    title_run = title.add_run(TITLE)
    set_run_font(title_run, "Times New Roman", 16, bold=True)

    authors = document.add_paragraph()
    authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
    authors.paragraph_format.space_before = Pt(0)
    authors.paragraph_format.space_after = Pt(12)
    author_text = ", ".join(f"{name} (RA {ra})" for name, ra, _ in MEMBERS)
    author_run = authors.add_run(author_text)
    set_run_font(author_run, "Times New Roman", 12, bold=True)

    affiliation = document.add_paragraph()
    affiliation.alignment = WD_ALIGN_PARAGRAPH.CENTER
    affiliation.paragraph_format.space_before = Pt(0)
    affiliation.paragraph_format.space_after = Pt(6)
    affiliation_run = affiliation.add_run(
        "Faculdade de Computação e Informática - Universidade Presbiteriana Mackenzie\n"
        "São Paulo - SP - Brasil"
    )
    set_run_font(affiliation_run, "Times New Roman", 12)

    emails = document.add_paragraph()
    emails.alignment = WD_ALIGN_PARAGRAPH.CENTER
    emails.paragraph_format.space_before = Pt(6)
    emails.paragraph_format.space_after = Pt(6)
    email_run = emails.add_run("{10420595,10420391,10427410}@mackenzista.com.br")
    set_run_font(email_run, "Courier New", 10)

    add_abstract(
        document,
        "Abstract",
        "This paper investigates early classification of coordinated social media campaigns "
        "from partial interaction graphs. The public Large Engagement Networks dataset is "
        "processed incrementally and reconstructed at ten observation fractions based on time "
        "and stored edges. After removing one exact duplicate, 103 local graphs produced 2,060 "
        "partial states. Exploratory results reveal a strong size imbalance: campaigns have a "
        "median of 506 users, while non-campaigns have 3,227. The next stage will compare a "
        "size-only baseline with Logistic Regression and Random Forest models to verify whether "
        "structural and temporal features provide information beyond this dataset bias.",
    )
    add_abstract(
        document,
        "Resumo",
        "Este artigo investiga a classificação precoce de campanhas coordenadas a partir de "
        "grafos parciais de interação. O conjunto público Large Engagement Networks foi lido de "
        "forma incremental e reconstruído em dez frações de observação por tempo e por arestas "
        "armazenadas. Após retirar uma duplicata exata, 103 grafos locais produziram 2.060 "
        "estados parciais. A análise exploratória revelou forte diferença de tamanho: campanhas "
        "possuem mediana de 506 usuários e não campanhas, 3.227. A próxima etapa comparará um "
        "modelo que usa apenas tamanho com Regressão Logística e Random Forest, verificando se "
        "características estruturais e temporais acrescentam informação além desse viés.",
    )

    add_heading(document, "1. Introdução", 1)
    add_heading(document, "1.1. Contextualização", 2)
    add_body(
        document,
        "Redes sociais permitem que assuntos alcancem grande visibilidade em pouco tempo. "
        "Parte dessa disseminação ocorre de forma espontânea, enquanto outra parte pode ser "
        "amplificada por contas que agem de maneira coordenada. Essas interações podem ser "
        "representadas como grafos direcionados: os usuários são os vértices e retuítes, "
        "respostas e citações formam as arestas.",
        indent=False,
    )
    add_body(
        document,
        "Este trabalho utiliza o Large Engagement Networks (LEN), conjunto de redes de "
        "engajamento rotuladas como campanhas e não campanhas [Gopalakrishnan et al. 2025]. "
        "Diferentemente da classificação do grafo completo, o projeto analisa estados formados "
        "somente pelas interações observadas até diferentes frações da evolução da rede.",
    )

    add_heading(document, "1.2. Justificativa e motivação", 2)
    add_body(
        document,
        "A classificação baseada na rede completa ocorre quando grande parte da atividade já "
        "aconteceu. O uso de grafos parciais permite estudar se existem sinais úteis nas fases "
        "iniciais e evita fornecer ao modelo propriedades que só estariam disponíveis no futuro. "
        "Essa antecipação é relevante para apoiar análises de circulação de informações, mas "
        "aumenta a incerteza porque há menos evidências disponíveis [Varol et al. 2017].",
        indent=False,
    )
    add_body(
        document,
        "Antes de empregar arquiteturas mais complexas, são necessários modelos simples e "
        "interpretáveis. Eles criam uma referência de desempenho e ajudam a verificar se a "
        "classificação aprende padrões de coordenação ou apenas diferenças de escala. O projeto "
        "também se relaciona ao ODS 16, por tratar de transparência e integridade dos ambientes "
        "digitais, sem propor acusação automática de pessoas ou remoção de conteúdo.",
    )

    add_heading(document, "1.3. Objetivo", 2)
    add_body(
        document,
        "O objetivo é desenvolver e comparar modelos de classificação supervisionada que usem "
        "características estruturais e temporais de grafos parciais do LEN para distinguir "
        "campanhas coordenadas de tendências rotuladas como não campanhas. A comparação será "
        "feita em diferentes frações observadas, sem usar informações de estados posteriores.",
        indent=False,
    )

    add_heading(document, "1.4. Contribuições esperadas", 2)
    add_body(
        document,
        "Espera-se produzir uma tabela reproduzível de estados parciais, comparar um modelo que "
        "usa somente o tamanho da rede com Regressão Logística e Random Forest, medir o "
        "desempenho ao longo da evolução observada e identificar limitações dos dados. A "
        "Regressão Logística foi escolhida pela interpretação direta dos coeficientes; a Random "
        "Forest permite relações não lineares e interações entre medidas. O XGBoost, citado na "
        "proposta inicial, foi adiado até que a divisão da pequena amostra seja estabilizada, "
        "evitando ampliar o experimento sem evidência de benefício.",
        indent=False,
    )
    add_body(
        document,
        "A proposta inicial foi refinada para avaliar grafos parciais, separar os dados por "
        "tópico e usar um baseline de tamanho, controlando o principal viés observado na análise."
    )

    add_heading(document, "2. Fundamentação teórica e trabalhos relacionados", 1)
    add_heading(document, "2.1. Grafos parciais e classificação supervisionada", 2)
    add_body(
        document,
        "Um grafo direcionado G=(V,E) representa usuários em V e interações em E. Medidas como "
        "grau, densidade, reciprocidade, componentes e modularidade resumem diferentes aspectos "
        "da estrutura [Newman 2010]. A modularidade compara a concentração de arestas dentro e "
        "entre grupos, sendo uma medida útil para descrever comunidades [Blondel et al. 2008].",
        indent=False,
    )
    add_body(
        document,
        "Neste projeto, um estado parcial contém somente os nós que já participaram de uma "
        "interação e as arestas cujo timestamp está dentro do limite observado. São usadas duas "
        "formas de corte: fração da duração total e fração das arestas armazenadas. Elas não são "
        "equivalentes, pois a atividade não ocorre em ritmo constante. Essa representação segue "
        "a ideia de redes temporais, nas quais a ordem das relações faz parte do problema "
        "[Holme e Saramäki 2012].",
    )

    add_heading(document, "2.2. Trabalhos relacionados", 2)
    add_body(
        document,
        "Ferrara et al. [2016] estudaram a identificação de campanhas promovidas a partir de "
        "características de usuários e difusão. Varol et al. [2017] avançaram para a detecção "
        "antecipada e mostraram que a importância das características muda conforme novas "
        "evidências aparecem. Esses trabalhos motivam a avaliação por frações, em vez de uma "
        "única classificação após o encerramento da atividade.",
        indent=False,
    )
    add_body(
        document,
        "Pacheco et al. [2021] construíram redes a partir de traços compartilhados, como "
        "retuítes, hashtags, imagens e atividade temporal, para revelar grupos potencialmente "
        "coordenados. A solução mostra que a coordenação pode ser estudada pela relação entre "
        "contas e comportamentos, sem depender apenas do conteúdo individual.",
    )
    add_body(
        document,
        "Gopalakrishnan et al. [2025] apresentaram o LEN, com 314 redes de engajamento, sendo "
        "179 campanhas e 135 não campanhas. O LEN-small contém as 100 menores redes. Os autores "
        "compararam descritores espectrais e redes neurais em grafos completos. O presente "
        "projeto usa a mesma base em outra pergunta: quanto da rede precisa ser observado para "
        "que a classificação se torne possível sem depender somente do tamanho final?",
    )
    add_body(
        document,
        "Modelos de GNN não serão usados nesta etapa. O LEN-small possui aproximadamente 100 "
        "grafos independentes, e os vários estados de um mesmo tópico não formam novas amostras "
        "independentes. Começar com modelos tabulares reduz a complexidade e permite verificar "
        "o protocolo antes de uma eventual extensão com GraphSAGE [Hamilton et al. 2017] ou "
        "modelos temporais [Rossi et al. 2020].",
    )

    add_heading(document, "3. Metodologia e resultados esperados", 1)
    add_heading(document, "3.1. Dataset", 2)
    add_body(
        document,
        "O LEN é um dataset público construído a partir de tendências do Twitter na Turquia. "
        "Campanhas foram associadas a ataques de astroturfing efêmero detectados entre março e "
        "maio de 2023. Não campanhas foram selecionadas manualmente entre notícias, esportes, "
        "festivais e outros acontecimentos considerados provavelmente orgânicos "
        "[Gopalakrishnan et al. 2025].",
        indent=False,
    )
    add_body(
        document,
        "Cada JSON contém um grafo direcionado. As arestas possuem origem, destino, timestamp e "
        "Interaction_Count. O LEN mantém somente a interação mais recente de cada par ordenado; "
        "por isso, a reconstrução descreve a evolução das arestas retidas, não o fluxo completo "
        "do Twitter. Vetores de 772 posições nos nós e 776 nas arestas não entram no primeiro "
        "baseline, pois sua disponibilidade em cada instante ainda não foi demonstrada.",
    )

    add_heading(document, "3.2. Preparação e análise exploratória", 2)
    add_body(
        document,
        "Os arquivos são processados de forma incremental com ijson. Valores NaN fora do padrão "
        "JSON são convertidos em nulos apenas no fluxo de leitura, sem modificar a base bruta. "
        "A preparação verifica duplicidades, endpoints ausentes, cobertura de timestamps e "
        "ordena as arestas cronologicamente.",
        indent=False,
    )
    add_body(
        document,
        "Após retirar uma duplicata exata por arquivo de configuração, cada grafo é reconstruído "
        "em 10%, 20%, ..., 100% por duas modalidades: duração observada e quantidade de arestas "
        "observadas. Para cada estado são calculadas 57 medidas estruturais e temporais. O "
        "atributo kcore fornecido no JSON não é usado, porque foi calculado no grafo completo e "
        "introduziria informação futura.",
    )

    add_heading(document, "3.3. Protocolo de modelagem", 2)
    add_body(
        document,
        "Primeiro será confirmada a lista canônica dos 100 grafos do LEN-small. Em seguida, os "
        "tópicos serão separados em 75% para treino, 10% para validação e 15% para teste, com "
        "estratificação quando possível. A divisão ocorrerá antes da geração das janelas, "
        "mantendo todos os estados de um tópico no mesmo conjunto.",
        indent=False,
    )
    add_body(
        document,
        "Serão comparados quatro grupos de atributos: somente tamanho; estrutura sem contagens "
        "brutas; somente tempo; e estrutura combinada com tempo. O tratamento de valores "
        "ausentes, a normalização e a seleção de medidas serão ajustados apenas com dados de "
        "treino. Cada modalidade e fração terá seu próprio treinamento.",
    )
    add_body(
        document,
        "A avaliação usará precisão, revocação, F1, ROC-AUC e PR-AUC. A relação entre "
        "precocidade e desempenho será apresentada por curvas de qualidade em função da fração "
        "observada. PR-AUC será mantida porque fornece uma leitura complementar quando a "
        "distribuição das classes ou o custo dos erros não for simétrico [Davis e Goadrich 2006].",
    )

    add_heading(document, "3.4. Resultados esperados", 2)
    add_body(
        document,
        "Espera-se determinar se medidas estruturais e temporais acrescentam informação além do "
        "tamanho do grafo e identificar a menor fração em que o resultado se torna estável. Um "
        "resultado negativo também será relevante: se o modelo completo não superar o baseline "
        "de tamanho, a diferença observada deverá ser tratada como limitação do dataset.",
        indent=False,
    )

    add_heading(document, "4. Resultados parciais", 1)
    add_heading(document, "4.1. Integridade e estados parciais", 2)
    add_body(
        document,
        "O pacote local contém 104 arquivos, enquanto a publicação descreve 100 no LEN-small. "
        "Foi identificado um par byte a byte idêntico. Após manter apenas uma cópia, restaram "
        "103 grafos: 52 campanhas e 51 não campanhas. A Tabela 1 resume a amostra efetivamente "
        "analisada. Os três arquivos excedentes ainda serão confirmados antes da divisão final.",
        indent=False,
    )
    add_table_caption(document, 1, "Resumo da amostra local após a exclusão da duplicata")
    add_article_table(
        document,
        ["Item", "Resultado"],
        [
            ["Grafos únicos locais", "103"],
            ["Campanhas", "52"],
            ["Não campanhas", "51"],
            ["Cobertura de timestamp nas arestas", "100%"],
            ["Estados parciais", "2.060"],
            ["Medidas por estado", "57"],
        ],
        [10.8, 4.2],
    )
    add_body(
        document,
        "Não foram encontrados IDs de usuários duplicados nem arestas apontando para usuários "
        "inexistentes. Os estados parciais são monotônicos: nenhum estágio posterior perde nós "
        "ou arestas, e as duas modalidades chegam ao mesmo grafo em 100%. Existem 26 estados "
        "com uma única aresta; neles, quatro estatísticas de intervalo entre eventos são "
        "indefinidas e serão tratadas somente com regras ajustadas no treino.",
    )

    add_heading(document, "4.2. Diferenças entre as classes", 2)
    add_body(
        document,
        "A principal diferença encontrada é a escala. As campanhas do pacote local são menores "
        "que as não campanhas, como mostra a Figura 1. Em 93,6% das comparações entre uma "
        "campanha e uma não campanha escolhidas ao acaso, a campanha possui menos usuários. "
        "Essa separação pode criar um atalho para o classificador.",
        indent=False,
    )
    add_figure(
        document,
        scale_figure,
        1,
        "Distribuição do número de usuários e arestas nos 103 grafos locais únicos.",
    )
    add_table_caption(document, 2, "Medianas das principais medidas nos grafos completos")
    add_article_table(
        document,
        ["Medida", "Campanhas", "Não campanhas"],
        [
            ["Usuários", "506", "3.227"],
            ["Arestas", "1.078", "3.769"],
            ["Interações agrupadas", "1.647", "4.835"],
            ["Duração (horas)", "22,60", "23,94"],
            ["Reciprocidade", "0,0311", "0,0051"],
            ["Parcela no maior componente", "69,3%", "72,5%"],
        ],
        [7.6, 3.7, 3.7],
    )
    add_body(
        document,
        "A densidade é maior nas campanhas, mas sua correlação de Spearman com o número de "
        "usuários é -0,98. Isso não indica causalidade: o denominador da densidade cresce "
        "aproximadamente com o quadrado do número de usuários. A densidade, portanto, não pode "
        "ser interpretada isoladamente como sinal de coordenação.",
    )

    add_heading(document, "4.3. Evolução das redes", 2)
    add_body(
        document,
        "Foram gerados 2.060 estados, correspondentes a 103 grafos, duas modalidades e dez "
        "frações. Em 10% das arestas, a campanha mediana possui 73,5 usuários e 108,5 arestas. "
        "Em 10% do tempo, ela possui somente 24 usuários e 22,5 arestas. Assim, uma mesma fração "
        "numérica representa quantidades de informação diferentes nas duas modalidades.",
        indent=False,
    )
    add_body(
        document,
        "A Figura 2 normaliza a quantidade de usuários pelo tamanho final de cada grafo. Em 10% "
        "das arestas, campanhas apresentam 12,9% dos usuários finais e não campanhas, 12,1%. Em "
        "30% do tempo, esses valores são 27,9% e 21,3%. As curvas próximas reforçam que boa parte "
        "da separação absoluta vem do tamanho final, não apenas do ritmo de crescimento.",
    )
    add_figure(
        document,
        growth_figure,
        2,
        "Crescimento mediano normalizado pelo total de usuários de cada grafo.",
    )
    add_body(
        document,
        "Como indício exploratório, em 10% das arestas a modularidade mediana foi 0,405 nas "
        "campanhas e 0,835 nas não campanhas. Essa diferença ainda precisa ser controlada pelo "
        "tamanho e não representa desempenho de classificação. Até o momento, nenhum modelo foi "
        "treinado e não existem resultados próprios de acurácia, precisão, revocação ou F1.",
    )

    add_heading(document, "4.4. Implementação e reprodutibilidade", 2)
    add_body(
        document,
        "O código implementa leitura incremental, criação dos grafos parciais e extração das "
        "características. Sete testes automatizados verificam o leitor, a reconstrução temporal, "
        "as medidas e a exportação das tabelas. Os notebooks foram executados integralmente e "
        "mantêm seus resultados salvos.",
        indent=False,
    )
    repository_paragraph = add_body(
        document,
        "O repositório público da disciplina é: "
        "https://github.com/Mendes1801/proj_IA7N_deteccao_de_campanhas_em_grafos. "
        "Ele contém o artigo, a descrição do dataset, as tabelas processadas, os notebooks, o "
        "código-fonte, os testes e o histórico das alterações. Os JSONs brutos, com cerca de "
        "5,4 GB, são obtidos na página oficial do LEN e não são duplicados no GitHub.",
        indent=False,
    )
    repository_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    add_heading(document, "4.5. Aspectos éticos e responsabilidade no uso da IA", 2)
    add_body(
        document,
        "Um falso positivo pode associar uma mobilização legítima a comportamento coordenado; "
        "um falso negativo pode deixar uma campanha relevante sem sinalização. A solução deve "
        "ser usada como apoio à análise humana, nunca como mecanismo autônomo de punição, "
        "remoção de conteúdo ou atribuição de intenção.",
        indent=False,
    )
    add_body(
        document,
        "Os rótulos são operacionais. Campaign indica que o LEN encontrou o padrão de ataque "
        "usado na construção da base; não significa que todos os usuários sejam inautênticos. "
        "Noncampaign foi atribuído a tendências consideradas provavelmente orgânicas e não "
        "comprova ausência total de coordenação [Gopalakrishnan et al. 2025].",
    )
    add_body(
        document,
        "Os dados representam tendências turcas coletadas em um período eleitoral. Resultados "
        "não devem ser generalizados automaticamente para outros países, idiomas e tipos de "
        "campanha. O projeto trabalha com medidas agregadas, não tenta reidentificar pessoas e "
        "documenta os vieses de rótulo e tamanho. Essas medidas seguem a orientação de mapear "
        "riscos, limitações e supervisão humana durante o desenvolvimento [NIST 2023].",
    )

    add_heading(document, "Referências", 1)
    references = [
        "Blondel, V. D., Guillaume, J.-L., Lambiotte, R. e Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008.",
        "Davis, J. e Goadrich, M. (2006). The relationship between Precision-Recall and ROC curves. In Proceedings of the 23rd International Conference on Machine Learning, p. 233-240.",
        "Ferrara, E., Varol, O., Menczer, F. e Flammini, A. (2016). Detection of promoted social media campaigns. Proceedings of the International AAAI Conference on Web and Social Media, 10(1), 563-566.",
        "Gopalakrishnan, A. A., Hossain, J., Elmas, T. e Sariyüce, A. E. (2025). Large Engagement Networks for classifying coordinated campaigns and organic Twitter trends. Proceedings of the International AAAI Conference on Web and Social Media, 19(1), 688-702.",
        "Hamilton, W. L., Ying, R. e Leskovec, J. (2017). Inductive representation learning on large graphs. Advances in Neural Information Processing Systems, 30.",
        "Holme, P. e Saramäki, J. (2012). Temporal networks. Physics Reports, 519(3), 97-125.",
        "National Institute of Standards and Technology (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1.",
        "Newman, M. E. J. (2010). Networks: An Introduction. Oxford University Press.",
        "Pacheco, D., Hui, P.-M., Torres-Lugo, C., Truong, B. T., Flammini, A. e Menczer, F. (2021). Uncovering coordinated networks on social media: methods and case studies. Proceedings of the International AAAI Conference on Web and Social Media, 15(1), 455-466.",
        "Rossi, E., Chamberlain, B., Frasca, F., Eynard, D., Monti, F. e Bronstein, M. (2020). Temporal Graph Networks for deep learning on dynamic graphs. arXiv:2006.10637.",
        "Varol, O., Ferrara, E., Menczer, F. e Flammini, A. (2017). Early detection of promoted campaigns on social media. EPJ Data Science, 6, 13.",
    ]
    for reference in references:
        paragraph = document.add_paragraph(style="Normal")
        paragraph.paragraph_format.first_line_indent = Cm(0)
        paragraph.paragraph_format.left_indent = Cm(0.5)
        paragraph.paragraph_format.first_line_indent = -Cm(0.5)
        run = paragraph.add_run(reference)
        set_run_font(run, "Times New Roman", 12)

    document.core_properties.title = TITLE
    document.core_properties.subject = "Artigo parcial do projeto de Inteligência Artificial"
    document.core_properties.author = "; ".join(name for name, _, _ in MEMBERS)
    document.core_properties.keywords = "campanhas coordenadas; grafos parciais; aprendizado de máquina"
    document.save(ARTICLE_DOCX)


def fill_rubric() -> None:
    if not RUBRIC_SOURCE.exists():
        raise FileNotFoundError(f"Rubrica não encontrada: {RUBRIC_SOURCE}")
    RUBRIC_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = Document(RUBRIC_SOURCE)

    member_table = document.tables[0]
    for index, (name, ra, _) in enumerate(MEMBERS, start=1):
        member_table.cell(index, 0).text = name
        member_table.cell(index, 1).text = ra

    for paragraph in document.paragraphs:
        normalized = paragraph.text.strip()
        if normalized.startswith("Título do Projeto:"):
            paragraph.text = ""
            label = paragraph.add_run("Título do Projeto: ")
            set_run_font(label, "Arial", 12, bold=True)
            value = paragraph.add_run(TITLE)
            set_run_font(value, "Arial", 12)
        elif normalized.startswith("Nota Final Total:"):
            paragraph.text = ""
            label = paragraph.add_run("Nota Final Total: ")
            set_run_font(label, "Arial", 12, bold=True)
            value = paragraph.add_run("10,0 / 10")
            set_run_font(value, "Arial", 12)

    scores = [15, 10, 15, 15, 20, 15, 5, 5, 5]
    rubric_table = document.tables[1]
    for row_index, score in enumerate(scores, start=1):
        cell = rubric_table.cell(row_index, len(rubric_table.columns) - 1)
        cell.text = str(score)
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                set_run_font(run, "Arial", 10)

    document.core_properties.title = "Rubrica Analítica N1"
    document.core_properties.author = "; ".join(name for name, _, _ in MEMBERS)
    document.save(RUBRIC_OUTPUT)


if __name__ == "__main__":
    build_article()
    fill_rubric()
    print(ARTICLE_DOCX)
    print(RUBRIC_OUTPUT)
