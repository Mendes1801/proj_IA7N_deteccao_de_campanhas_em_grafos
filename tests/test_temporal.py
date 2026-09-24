# Integrantes: Gabriel de Santana Santos | 10420595 | 10420595@mackenzista.com.br
#              Gabriel Erick Mendes | 10420391 | 10420391@mackenzista.com.br
#              Matheus Teles Magalhães | 10427410 | 10427410@mackenzista.com.br
# Conteúdo: testes da reconstrução de grafos parciais por tempo e por arestas.
# Histórico de alterações:
# 21/09/2026 | Gabriel Erick Mendes | Criação dos testes temporais.
# 24/09/2026 | Grupo | Revisão e preparação para a entrega da disciplina.

import networkx as nx
import pytest

from len_eda.temporal import partial_graph


@pytest.fixture
def temporal_graph():
    graph = nx.DiGraph()
    graph.add_edge("a", "b", timestamp=100, Interaction_Count=2)
    graph.add_edge("b", "c", timestamp=120, Interaction_Count=1)
    graph.add_edge("c", "d", timestamp=200, Interaction_Count=4)
    graph.add_node("future-isolate")
    return graph


def test_partial_graph_by_time_uses_elapsed_duration(temporal_graph):
    partial = partial_graph(temporal_graph, 0.5, "time")
    assert set(partial.edges()) == {("a", "b"), ("b", "c")}
    assert "future-isolate" not in partial
    assert partial.graph["cutoff_timestamp"] == 150


def test_partial_graph_by_events_uses_earliest_observed_edges(temporal_graph):
    partial = partial_graph(temporal_graph, 1 / 3, "events")
    assert set(partial.edges()) == {("a", "b")}
    assert set(partial.nodes()) == {"a", "b"}


def test_partial_graph_rejects_invalid_fraction(temporal_graph):
    with pytest.raises(ValueError):
        partial_graph(temporal_graph, 0, "time")
