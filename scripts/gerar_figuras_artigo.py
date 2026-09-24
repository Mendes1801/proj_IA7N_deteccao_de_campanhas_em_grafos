# Integrantes: Gabriel de Santana Santos | 10420595 | 10420595@mackenzista.com.br
#              Gabriel Erick Mendes | 10420391 | 10420391@mackenzista.com.br
#              Matheus Teles Magalhães | 10427410 | 10427410@mackenzista.com.br
# Conteúdo: geração das figuras usadas no artigo parcial da entrega N1.
# Histórico de alterações:
# 24/09/2026 | Grupo | Criação do gerador de figuras do artigo.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "artigo" / "figuras"
DUPLICATE = "#SesimiziDuyanVarMi___2023-03-23_campaign_fulldata.json"


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    summary = pd.read_csv(ROOT / "dados" / "processados" / "len_small_summary.csv")
    summary = summary.loc[summary["file"] != DUPLICATE].copy()
    partial = pd.read_csv(ROOT / "dados" / "processados" / "partial_graph_features.csv")

    names = {"campaign": "Campanhas", "noncampaign": "Não campanhas"}
    order = ["campaign", "noncampaign"]
    colors = ["#4D4D4D", "#BDBDBD"]

    scale_path = FIGURE_DIR / "diferenca_escala.png"
    figure, axes = plt.subplots(1, 2, figsize=(8.2, 3.5))
    for axis, column, label in zip(
        axes,
        ("nodes", "edges"),
        ("Usuários", "Arestas"),
        strict=True,
    ):
        values = [summary.loc[summary["label"] == item, column] for item in order]
        box = axis.boxplot(
            values,
            patch_artist=True,
            tick_labels=[names[item] for item in order],
        )
        for patch, color in zip(box["boxes"], colors, strict=True):
            patch.set_facecolor(color)
        axis.set_yscale("log")
        axis.set_ylabel(f"{label} (escala logarítmica)")
        axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(scale_path, dpi=260, bbox_inches="tight")
    plt.close(figure)

    growth = partial.merge(
        summary[["file", "nodes", "edges"]].rename(
            columns={"nodes": "full_nodes", "edges": "full_edges"}
        ),
        on="file",
        how="left",
    )
    growth["node_share"] = growth["nodes"] / growth["full_nodes"]

    growth_path = FIGURE_DIR / "crescimento_normalizado.png"
    figure, axes = plt.subplots(1, 2, figsize=(8.4, 3.5), sharey=True)
    styles = {"campaign": ("-", "o"), "noncampaign": ("--", "s")}
    for axis, mode, title in zip(
        axes,
        ("time", "events"),
        ("Fração da duração", "Fração das arestas"),
        strict=True,
    ):
        selected = growth.loc[growth["partiality_mode"] == mode]
        for label in order:
            medians = (
                selected.loc[selected["label"] == label]
                .groupby("fraction", as_index=False)["node_share"]
                .median()
            )
            line, marker = styles[label]
            axis.plot(
                medians["fraction"] * 100,
                medians["node_share"] * 100,
                linestyle=line,
                marker=marker,
                color="#222222" if label == "campaign" else "#777777",
                label=names[label],
                linewidth=1.7,
                markersize=3.5,
            )
        axis.set_title(title)
        axis.set_xlabel("Fração observada (%)")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("Usuários observados em relação ao total (%)")
    axes[1].legend(frameon=False, loc="lower right")
    figure.tight_layout()
    figure.savefig(growth_path, dpi=260, bbox_inches="tight")
    plt.close(figure)

    print(scale_path)
    print(growth_path)


if __name__ == "__main__":
    main()
