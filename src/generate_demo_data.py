"""Generate clearly labelled synthetic data for software demonstration only.

This dataset is NOT historical flood observations and must never be used for
real-world warnings, scientific claims, or emergency decisions.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "demo_synthetic_flood_data.csv"

def make_data(n=5000, seed=42):
    rng = np.random.default_rng(seed)
    rainfall_24h = rng.gamma(shape=2.2, scale=22, size=n).clip(0, 250)
    rainfall_72h = (rainfall_24h * rng.uniform(1.2, 3.2, n) +
                    rng.normal(0, 20, n)).clip(0, 500)
    river_level = rng.uniform(0.2, 8.0, n)
    river_capacity = rng.uniform(2.5, 7.0, n)
    soil_saturation = rng.uniform(10, 100, n)
    elevation = rng.uniform(0, 80, n)
    drainage = rng.uniform(0, 100, n)  # higher = better drainage

    # Synthetic teaching rule, not a hydrological model.
    score = (
        0.020 * rainfall_24h +
        0.008 * rainfall_72h +
        0.52 * river_level -
        0.35 * river_capacity +
        0.018 * soil_saturation -
        0.018 * elevation -
        0.012 * drainage +
        rng.normal(0, 0.65, n)
    )
    flood_within_24h = (score > 1.55).astype(int)

    df = pd.DataFrame({
        "rainfall_24h_mm": rainfall_24h.round(1),
        "rainfall_72h_mm": rainfall_72h.round(1),
        "river_level_m": river_level.round(2),
        "river_capacity_m": river_capacity.round(2),
        "soil_saturation_pct": soil_saturation.round(1),
        "elevation_m": elevation.round(1),
        "drainage_score": drainage.round(1),
        "flood_within_24h": flood_within_24h,
    })
    return df

if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    df = make_data()
    df.to_csv(OUT, index=False)
    print(f"Created {OUT} with {len(df)} synthetic rows.")
    print("WARNING: synthetic demonstration data, not real flood records.")
