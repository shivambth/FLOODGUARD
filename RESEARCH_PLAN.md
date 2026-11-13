# Research plan: moving from demo to genuine flood-risk research

## Research question
Can rainfall, river-gauge, terrain, soil-moisture and drainage indicators help identify flood events at a defined location and forecast horizon?

## Required dataset table

| Field | Required definition |
|---|---|
| Event label | Documented flood/no-flood outcome |
| Event timestamp | Start time and reporting convention |
| Location | Gauge, catchment, district or grid identifier |
| Rainfall | Source, accumulation period, units |
| River level | Gauge ID, datum, units, timestamp |
| Terrain | Elevation source and resolution |
| Soil moisture | Source, units, time |
| Drainage | Measured or defensibly derived variable |

## Research safeguards
- Do not mix measurements from different times without a documented alignment rule.
- Avoid leakage: no information recorded after the prediction cut-off may enter the features.
- Split by time and, where possible, by catchment/location.
- Compare against simple baselines.
- Report precision, recall, F1, PR-AUC, false alarms and missed events.
- Document class imbalance and missing observations.
- Never equate a model score with a calibrated probability without calibration tests.
- Do not issue public safety warnings from a student prototype.

## Candidate data sources to investigate
- Central Water Commission / India-WRIS official river and flood information.
- IMD rainfall observations or official gridded products.
- NASA GPM precipitation products.
- USGS flood-event and hydrology datasets.
- Copernicus / relevant national elevation and land-cover products.

Check availability, licence, spatial coverage, resolution, timestamps and permitted use before downloading. Cite the exact version used.
