"""
Utilitários de exportação: CSV, PNG (Plotly) e relatório simples.
"""
import pandas as pd
from io import BytesIO


def counts_to_csv(counts: dict) -> bytes:
    """Converte dicionário de contagens em CSV (estado, contagem, probabilidade)."""
    total = sum(counts.values()) or 1
    rows = [
        {"estado": k, "contagem": v, "probabilidade": round(v / total, 4)}
        for k, v in sorted(counts.items())
    ]
    df = pd.DataFrame(rows)
    return df.to_csv(index=False).encode("utf-8")


def plotly_to_png(fig) -> bytes:
    """Exporta figura Plotly para PNG usando kaleido."""
    return fig.to_image(format="png")


def build_report(
    module: str,
    circuit_info: dict,
    counts: dict,
    extra: dict | None = None,
) -> str:
    """Gera relatório textual simples do experimento."""
    total = sum(counts.values()) or 1
    lines = [
        "RELATÓRIO — QUANTUM LAB",
        "=" * 40,
        f"Módulo: {module}",
        f"Profundidade do circuito: {circuit_info.get('depth', '—')}",
        f"Portas: {circuit_info.get('size', '—')}",
        f"Total de medições: {total}",
        "",
        "Distribuição dos resultados:",
    ]
    for state, count in sorted(counts.items()):
        prob = 100 * count / total
        lines.append(f"  {state}: {count} ({prob:.1f}%)")

    if extra:
        lines.append("")
        lines.append("Informações adicionais:")
        for k, v in extra.items():
            lines.append(f"  {k}: {v}")

    lines.append("")
    lines.append("Nota: resultados obtidos por simulação real com Qiskit Aer.")
    return "\n".join(lines)