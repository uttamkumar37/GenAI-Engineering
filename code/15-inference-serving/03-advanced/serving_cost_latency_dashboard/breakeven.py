from __future__ import annotations

from data import ServingOption


def monthly_cost(option: ServingOption, monthly_tokens: float) -> float:
    variable_cost = (monthly_tokens / 1000.0) * option.cost_per_1k_tokens_usd
    return option.fixed_monthly_cost_usd + variable_cost


def breakeven_tokens(managed: ServingOption, self_hosted: ServingOption) -> float | None:
    # Solve for monthly_tokens where monthly_cost(managed) == monthly_cost(self_hosted):
    # managed_var * T = self_hosted_fixed + self_hosted_var * T
    # T = self_hosted_fixed / (managed_var_per_token - self_hosted_var_per_token)
    managed_per_token = managed.cost_per_1k_tokens_usd / 1000.0
    self_hosted_per_token = self_hosted.cost_per_1k_tokens_usd / 1000.0
    denom = managed_per_token - self_hosted_per_token
    if denom <= 0:
        return None  # self-hosting never wins on pure per-token cost at this configuration
    return self_hosted.fixed_monthly_cost_usd / denom


UNACCOUNTED_FACTORS = [
    "GPU idle cost during low-traffic periods (you pay for the instance whether or not it's serving)",
    "Ops/on-call burden of running your own serving stack (upgrades, scaling, incident response)",
    "Reliability/SLA differences: managed APIs often have stronger uptime guarantees out of the box",
    "Engineering time spent building and maintaining the self-hosted pipeline",
    "Cold-start/scale-up latency when self-hosted capacity needs to grow with demand spikes",
]


if __name__ == "__main__":
    from data import SERVING_OPTIONS

    managed = next(o for o in SERVING_OPTIONS if o.name == "managed_api")
    for option in SERVING_OPTIONS:
        if option is managed:
            continue
        tokens = breakeven_tokens(managed, option)
        if tokens is None:
            print(f"{option.name}: never cheaper than managed API on per-token cost alone")
        else:
            print(f"{option.name}: breakeven at {tokens:,.0f} tokens/month (~{tokens / 1000:,.0f}k tokens)")

    print("\nWhat per-token cost comparisons don't account for:")
    for factor in UNACCOUNTED_FACTORS:
        print(f"  - {factor}")
