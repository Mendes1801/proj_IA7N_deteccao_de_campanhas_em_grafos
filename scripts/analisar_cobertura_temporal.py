# Integrantes: Gabriel de Santana Santos | 10420595 | 10420595@mackenzista.com.br
#              Gabriel Erick Mendes | 10420391 | 10420391@mackenzista.com.br
#              Matheus Teles Magalhães | 10427410 | 10427410@mackenzista.com.br
# Conteúdo: análise da disponibilidade de timestamps individuais no LEN-Small.
# Histórico de alterações:
# 24/09/2026 | Grupo | Criação e análise da relação entre tamanho e perda temporal.

"""Quantifica a perda de timestamps individuais no LEN-Small local.

Cada aresta retida pelo LEN possui um timestamp, mas ``Interaction_Count`` pode
indicar que várias interações foram agrupadas nessa aresta. Nesses casos,
somente o horário da interação mais recente está disponível.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter


LABELS = {"campaign": "Campanhas", "noncampaign": "Não campanhas"}
ORDER = ["campaign", "noncampaign"]


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "sim"}


def analyze_temporal_coverage(
    summary: pd.DataFrame,
    exclusions: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Calcula a parcela de interações que possui timestamp individual."""

    required = {
        "file",
        "topic",
        "label",
        "nodes",
        "edges",
        "interaction_count_sum",
    }
    missing = sorted(required.difference(summary.columns))
    if missing:
        raise ValueError(f"colunas ausentes: {', '.join(missing)}")

    frame = summary.copy()
    if exclusions is not None and not exclusions.empty:
        if not {"file", "exclude"}.issubset(exclusions.columns):
            raise ValueError("o arquivo de exclusões deve conter file e exclude")
        excluded = set(
            exclusions.loc[exclusions["exclude"].map(_truthy), "file"].astype(str)
        )
        frame = frame.loc[~frame["file"].astype(str).isin(excluded)].copy()

    frame["interactions_with_individual_timestamp"] = frame["edges"]
    frame["interactions_without_individual_timestamp"] = (
        frame["interaction_count_sum"] - frame["edges"]
    )
    if (frame["interactions_without_individual_timestamp"] < 0).any():
        raise ValueError("interaction_count_sum menor que edges")

    frame["individual_timestamp_share"] = (
        frame["edges"] / frame["interaction_count_sum"]
    )
    frame["missing_individual_timestamp_share"] = (
        1 - frame["individual_timestamp_share"]
    )
    columns = [
        "file",
        "topic",
        "label",
        "nodes",
        "edges",
        "interaction_count_sum",
        "interactions_with_individual_timestamp",
        "interactions_without_individual_timestamp",
        "individual_timestamp_share",
        "missing_individual_timestamp_share",
    ]
    return frame[columns].sort_values(["label", "file"]).reset_index(drop=True)


def print_summary(coverage: pd.DataFrame) -> None:
    interactions = coverage["interaction_count_sum"].sum()
    timestamps = coverage["interactions_with_individual_timestamp"].sum()
    print(f"Grafos analisados: {len(coverage)}")
    print(f"Interações indicadas por Interaction_Count: {interactions:,.0f}")
    print(f"Interações com timestamp individual: {timestamps:,.0f}")
    print(f"Cobertura temporal agregada: {timestamps / interactions:.1%}")
    print(f"Interações sem horário individual: {interactions - timestamps:,.0f}")
    for label in ORDER:
        selected = coverage.loc[coverage["label"] == label]
        class_interactions = selected["interaction_count_sum"].sum()
        class_timestamps = selected["interactions_with_individual_timestamp"].sum()
        print(
            f"{LABELS[label]}: {class_timestamps / class_interactions:.1%} "
            "das interações com timestamp individual"
        )
    print("Correlação de Spearman entre tamanho e perda temporal:")
    for label, selected in [("Todos", coverage), *coverage.groupby("label")]:
        name = LABELS.get(label, label)
        edge_share = selected[["edges", "missing_individual_timestamp_share"]].corr(
            method="spearman"
        ).iloc[0, 1]
        edge_count = selected[
            ["edges", "interactions_without_individual_timestamp"]
        ].corr(method="spearman").iloc[0, 1]
        node_share = selected[["nodes", "missing_individual_timestamp_share"]].corr(
            method="spearman"
        ).iloc[0, 1]
        print(
            f"  {name}: arestas × proporção perdida={edge_share:.3f}; "
            f"arestas × quantidade perdida={edge_count:.3f}; "
            f"nós × proporção perdida={node_share:.3f}"
        )


def plot_coverage(coverage: pd.DataFrame, output: Path) -> None:
    """Gera uma figura com a distribuição e o total agregado por classe."""

    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(1, 2, figsize=(8.6, 3.5))

    values = [
        coverage.loc[coverage["label"] == label, "individual_timestamp_share"]
        for label in ORDER
    ]
    boxes = axes[0].boxplot(
        values,
        patch_artist=True,
        tick_labels=[LABELS[label] for label in ORDER],
    )
    for patch, color in zip(boxes["boxes"], ["#666666", "#C5C5C5"], strict=True):
        patch.set_facecolor(color)
    axes[0].set_ylabel("Interações com timestamp individual")
    axes[0].set_title("Distribuição por grafo")
    axes[0].yaxis.set_major_formatter(PercentFormatter(1))
    axes[0].set_ylim(0, 1.04)
    axes[0].grid(axis="y", alpha=0.25)

    retained = []
    missing = []
    for label in ORDER:
        selected = coverage.loc[coverage["label"] == label]
        total = selected["interaction_count_sum"].sum()
        kept = selected["interactions_with_individual_timestamp"].sum() / total
        retained.append(kept)
        missing.append(1 - kept)
    positions = range(len(ORDER))
    axes[1].bar(positions, retained, color="#666666")
    axes[1].bar(
        positions,
        missing,
        bottom=retained,
        color="#D9D9D9",
    )
    for position, kept, lost in zip(positions, retained, missing, strict=True):
        axes[1].text(
            position,
            kept / 2,
            f"{kept:.1%}\ncom horário",
            ha="center",
            va="center",
            color="white",
        )
        axes[1].text(
            position,
            kept + lost / 2,
            f"{lost:.1%}\nsem horário",
            ha="center",
            va="center",
        )
    axes[1].set_xticks(list(positions), [LABELS[label] for label in ORDER])
    axes[1].set_ylim(0, 1)
    axes[1].yaxis.set_major_formatter(PercentFormatter(1))
    axes[1].set_ylabel("Parcela agregada das interações")
    axes[1].set_title("Totais por classe")
    axes[1].grid(axis="y", alpha=0.2)

    figure.tight_layout()
    figure.savefig(output, dpi=260, bbox_inches="tight")
    plt.close(figure)


def plot_size_relation(coverage: pd.DataFrame, output: Path) -> None:
    """Relaciona o tamanho dos grafos à perda absoluta e proporcional de tempo."""

    output.parent.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(1, 2, figsize=(8.8, 3.6))
    styles = {
        "campaign": ("o", "#555555"),
        "noncampaign": ("^", "#B5B5B5"),
    }
    for label in ORDER:
        selected = coverage.loc[coverage["label"] == label]
        marker, color = styles[label]
        axes[0].scatter(
            selected["edges"],
            selected["missing_individual_timestamp_share"],
            marker=marker,
            color=color,
            edgecolor="#222222",
            linewidth=0.4,
            alpha=0.8,
            label=LABELS[label],
        )
        axes[1].scatter(
            selected["edges"],
            selected["interactions_without_individual_timestamp"] + 1,
            marker=marker,
            color=color,
            edgecolor="#222222",
            linewidth=0.4,
            alpha=0.8,
            label=LABELS[label],
        )

    for axis in axes:
        axis.set_xscale("log")
        axis.set_xlabel("Arestas armazenadas (escala logarítmica)")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("Proporção de interações sem horário")
    axes[0].yaxis.set_major_formatter(PercentFormatter(1))
    axes[0].set_ylim(-0.02, 0.91)
    axes[0].set_title("Perda proporcional")
    axes[1].set_yscale("log")
    axes[1].set_ylabel("Interações sem horário individual + 1")
    axes[1].set_title("Perda absoluta")
    axes[1].legend(frameon=False, fontsize=8, loc="lower right")

    proportional = []
    absolute = []
    for label in ORDER:
        selected = coverage.loc[coverage["label"] == label]
        proportional.append(
            selected[["edges", "missing_individual_timestamp_share"]]
            .corr(method="spearman")
            .iloc[0, 1]
        )
        absolute.append(
            selected[["edges", "interactions_without_individual_timestamp"]]
            .corr(method="spearman")
            .iloc[0, 1]
        )
    axes[0].text(
        0.03,
        0.05,
        f"Spearman por classe\nC: {proportional[0]:.2f} | NC: {proportional[1]:.2f}",
        transform=axes[0].transAxes,
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#BBBBBB", "alpha": 0.9},
    )
    axes[1].text(
        0.03,
        0.84,
        f"Spearman por classe\nC: {absolute[0]:.2f} | NC: {absolute[1]:.2f}",
        transform=axes[1].transAxes,
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#BBBBBB", "alpha": 0.9},
    )
    figure.tight_layout()
    figure.savefig(output, dpi=260, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analisa a disponibilidade de timestamps individuais no LEN-Small."
    )
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--exclusions", type=Path)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-figure", type=Path, required=True)
    parser.add_argument("--output-size-figure", type=Path, required=True)
    args = parser.parse_args()

    summary = pd.read_csv(args.summary)
    exclusions = pd.read_csv(args.exclusions) if args.exclusions else None
    coverage = analyze_temporal_coverage(summary, exclusions)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    coverage.to_csv(args.output_csv, index=False)
    plot_coverage(coverage, args.output_figure)
    plot_size_relation(coverage, args.output_size_figure)
    print_summary(coverage)
    print(args.output_csv)
    print(args.output_figure)
    print(args.output_size_figure)


if __name__ == "__main__":
    main()
