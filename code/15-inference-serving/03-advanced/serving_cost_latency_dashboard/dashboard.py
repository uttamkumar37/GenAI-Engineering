from __future__ import annotations

from breakeven import breakeven_tokens, monthly_cost
from data import SERVING_OPTIONS, ServingOption

# Fixed categorical color order (distinct hues, assigned by entity not by rank).
COLORS = {
    "managed_api": "#4C72B0",
    "self_hosted_vllm_fp16": "#DD8452",
    "self_hosted_vllm_int4": "#55A868",
}


def render_matplotlib(options: list[ServingOption], monthly_token_volumes: list[float]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping chart render (table output below still works).")
        return

    fig, (ax_cost, ax_latency) = plt.subplots(1, 2, figsize=(11, 4.5))

    for option in options:
        costs = [monthly_cost(option, v) for v in monthly_token_volumes]
        ax_cost.plot(
            monthly_token_volumes,
            costs,
            label=option.name,
            color=COLORS[option.name],
            linewidth=2,
        )
    ax_cost.set_xlabel("monthly tokens")
    ax_cost.set_ylabel("monthly cost (USD)")
    ax_cost.set_title("Cost vs. volume")
    ax_cost.grid(True, alpha=0.2)
    ax_cost.legend(frameon=False)

    names = [o.name for o in options]
    p50 = [o.p50_latency_ms for o in options]
    p95 = [o.p95_latency_ms for o in options]
    x = range(len(names))
    width = 0.35
    ax_latency.bar(
        [i - width / 2 for i in x], p50, width, label="p50", color="#4C72B0"
    )
    ax_latency.bar(
        [i + width / 2 for i in x], p95, width, label="p95", color="#B0B0B0"
    )
    ax_latency.set_xticks(list(x))
    ax_latency.set_xticklabels(names, rotation=15, ha="right")
    ax_latency.set_ylabel("latency (ms)")
    ax_latency.set_title("p50 / p95 latency")
    ax_latency.grid(True, axis="y", alpha=0.2)
    ax_latency.legend(frameon=False)

    fig.tight_layout()
    out_path = "serving_cost_latency_dashboard.png"
    fig.savefig(out_path, dpi=150)
    print(f"Saved chart to {out_path}")


def print_table(options: list[ServingOption], monthly_token_volumes: list[float]) -> None:
    header = "option".ljust(26) + "".join(f"{str(int(v/1000)) + 'k':>12}" for v in monthly_token_volumes)
    print(header)
    for option in options:
        row = option.name.ljust(26)
        for v in monthly_token_volumes:
            row += f"{'$' + format(monthly_cost(option, v), ',.0f'):>12}"
        print(row)


if __name__ == "__main__":
    volumes = [100_000, 1_000_000, 10_000_000, 50_000_000, 100_000_000]

    print("Monthly cost by volume:")
    print_table(SERVING_OPTIONS, volumes)

    print("\nBreakeven analysis vs managed API:")
    managed = next(o for o in SERVING_OPTIONS if o.name == "managed_api")
    for option in SERVING_OPTIONS:
        if option is managed:
            continue
        tokens = breakeven_tokens(managed, option)
        label = f"{tokens:,.0f} tokens/month" if tokens else "never (per-token cost alone)"
        print(f"  {option.name}: {label}")

    print()
    render_matplotlib(SERVING_OPTIONS, volumes)
