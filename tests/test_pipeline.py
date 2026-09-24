# Integrantes: Gabriel de Santana Santos | 10420595 | 10420595@mackenzista.com.br
#              Gabriel Erick Mendes | 10420391 | 10420391@mackenzista.com.br
#              Matheus Teles Magalhães | 10427410 | 10427410@mackenzista.com.br
# Conteúdo: testes da lista de exclusões e da exportação da tabela de estados.
# Histórico de alterações:
# 21/09/2026 | Gabriel Erick Mendes | Criação dos testes do pipeline.
# 23/09/2026 | Gabriel Erick Mendes | Teste da exportação de tópicos com hashtag.
# 24/09/2026 | Grupo | Revisão e preparação para a entrega da disciplina.

import csv

from len_eda.pipeline import load_exclusions, write_feature_table


def test_load_exclusions_reads_only_marked_rows(tmp_path):
    path = tmp_path / "exclusions.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["file", "exclude", "reason"])
        writer.writeheader()
        writer.writerow({"file": "a.json", "exclude": "true", "reason": "duplicate"})
        writer.writerow({"file": "b.json", "exclude": "false", "reason": "keep"})
    assert load_exclusions(path) == {"a.json"}


def test_write_feature_table_quotes_hashtag_topics(tmp_path):
    output = tmp_path / "features.csv"
    write_feature_table(
        [{"file": "#topic.json", "topic": "#topic", "fraction": 0.1}],
        output,
    )

    lines = output.read_text(encoding="utf-8").splitlines()
    assert lines[1].startswith('"#topic.json","#topic",')
