# Validation checklist (reference)

Must pass before sharing any metric. Same content is enforced via `.cursor/rules/validation-checklist.mdc` when installed.

---

## Data & scope
- [ ] Source identified (db/table OR file path)
- [ ] Time window stated
- [ ] Filters stated (region/product/segment)
- [ ] Definition stated (numerator/denominator)

## Reproducibility
- [ ] SQL saved in `/sql/queries` OR code saved in `/notebooks` or `/src`
- [ ] Output saved to `/sql/outputs` or `/data/processed`
- [ ] Output has timestamp/version in filename
- [ ] Metric in report includes proof tag

## Sanity checks
- [ ] Compare vs prior period / expected range
- [ ] Check duplicates / missing values
- [ ] Check join keys (1:1 vs 1:m)
- [ ] Spot-check sample rows

## Approval
- [ ] Peer review (even if it's "you yesterday")
- [ ] Final sign-off comment in PR / commit message
