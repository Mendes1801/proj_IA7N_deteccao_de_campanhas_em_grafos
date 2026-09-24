# Integrantes: Gabriel de Santana Santos | 10420595 | 10420595@mackenzista.com.br
#              Gabriel Erick Mendes | 10420391 | 10420391@mackenzista.com.br
#              Matheus Teles Magalhães | 10427410 | 10427410@mackenzista.com.br
# Conteúdo: testes das características calculadas sobre estados parciais.
# Histórico de alterações:
# 21/09/2026 | Gabriel Erick Mendes | Criação dos testes de características.
# 24/09/2026 | Grupo | Revisão e preparação para a entrega da disciplina.

import networkx as nx
import pytest

from len_eda.features import extract_features
from len_eda.temporal import partial_graph


def test_extract_features_uses_only_partial_graph():
    graph = nx.DiGraph()
    graph.add_edge(1, 2, timestamp=100, Interaction_Count=2)
    graph.add_edge(2, 1, timestamp=110, Interaction_Count=1)
    graph.add_edge(2, 3, timestamp=200, Interaction_Count=5)

    partial = partial_graph(graph, 2 / 3, "events")
    features = extract_features(partial)

    assert features["nodes"] == 2
    assert features["edges"] == 2
    assert features["interaction_count_sum"] == 3
    assert features["reciprocity"] == 1.0
    assert features["largest_weak_component_fraction"] == 1.0
    assert features["observed_span_hours"] == pytest.approx(10 / 3600)
