# Factory Health Index (FHI)

## Definition
The **Factory Health Index (FHI)** is a unified metric designed to summarize the overall health of each asset by combining:
- **OEE (Overall Equipment Effectiveness):** Measures availability, performance, and quality.
- **Normalized RUL (Remaining Useful Life):** Indicates how much useful life remains for each asset, normalized across all assets.

The FHI is calculated as:

$$
FHI = w_1 \cdot OEE + w_2 \cdot RUL_{normalized}
$$

Where:
- $OEE$ is the asset's OEE score (from the gold layer)
- $RUL_{normalized}$ is the normalized predicted RUL (higher = healthier)
- $w_1$ and $w_2$ are weights (default: 0.5 each)

## Calculation Steps
1. **Compute OEE** for each asset using the gold layer model (`oee_final`).
2. **Predict RUL** for each asset using the best ML model (`nasa_rul_regressor`).
3. **Normalize RUL** across all assets: $RUL_{normalized} = \frac{RUL_i - RUL_{min}}{RUL_{max} - RUL_{min}}$
4. **Calculate FHI**: $FHI = 0.5 \times OEE + 0.5 \times RUL_{normalized}$

## Usage
- FHI provides a single, interpretable score for asset health.
- Can be used for ranking, alerting, and executive dashboards.

---

*See also: `dbt/models/gold/factory_health_index.sql` for implementation.*
