# Measure agreement and uncertainty

Match the statistic to the label unit and population. Report per-criterion agreement for per-criterion gold; do not silently turn it into whole-case truth. Always preserve case/family counts, prevalence, attempted membership and missing outcomes.

## Kappa and operational errors

For nominal paired labels, Cohen's kappa is `(observed agreement - expected agreement) / (1 - expected agreement)`. Expected agreement uses both marginal label distributions. Use ordinary kappa for binary or unordered classes. For genuinely ordered ratings, predeclare the order and disagreement weights before computing weighted kappa. Numeric class IDs alone do not establish order.

No pairs or expected agreement of one makes kappa undefined. Preserve that status and its reason. An always-PASS judge against 95 passes and five failures has 95 percent agreement and kappa zero. Two always-PASS labelings have undefined kappa. Neither case justifies silently reporting perfect chance-corrected agreement.

Kappa is symmetric and prevalence-sensitive. Use it alongside the full confusion table, not a universal acceptance band. With failure as positive:

| Gold | Judge FAIL | Judge PASS |
| --- | --- | --- |
| FAIL | TP, caught failure | FN, false pass |
| PASS | FP, false rejection | TN, accepted pass |

Name denominators: failure catch is `TP/(TP+FN)`; false passes among gold failures are `FN/(TP+FN)`; false rejection among gold passes is `FP/(FP+TN)`. False outcomes among judge passes are `FN/(TN+FN)`, a different quantity. Leave empty-denominator rates undefined. Retain all classes for multiclass tasks.

UNKNOWN, abstention, refusal, malformed output, timeout and transport error stay visible. Report coverage and these outcomes by gold class. Kappa/confusion on decided pairs are conditional statistics; report all-selected outcomes and any fallback behavior alongside them. Dropping difficult examples cannot earn an undisclosed agreement gain. Never assume fallback decisions are correct without measuring them.

Sources: [Cohen kappa API](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html), [prevalence analysis](https://pubmed.ncbi.nlm.nih.gov/2348207/), [selective classification](https://jmlr.csail.mit.edu/papers/v11/el-yaniv10a.html).

## Uncertainty and repeated trials

Report the interval method, confidence level, sampling unit, source-family count and assumptions. For related examples, keep paired labels and resample independent families as whole clusters when that matches the population claim. Row-weighted traffic and equal-weight families differ. Too few families, rare classes or undefined bootstrap replicates limit inference; do not discard problematic replicates silently or imply that a narrow interval certifies trust.

Repeated calls to one frozen example estimate within-example variability. Measure that separately from correctness against gold and probability reliability across examples. A stable judge can be consistently wrong. Paired candidate comparisons should use comparable cases/trials and retain model versions, sampling/cache settings and costs.

Sources: [clustered bootstrap](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.1467-9868.2007.00593.x), [kappa variance](https://www.statsmodels.org/stable/generated/statsmodels.stats.inter_rater.cohens_kappa.html).

## Probabilities and decisions

When actual event probabilities are available, report reliability bins/curves, Brier score and log loss with their supported coverage. Brier/log loss also reflect discrimination and uncertainty; an improvement alone does not isolate probability calibration. Preserve impossible-event/infinite-loss observations rather than clipping them without a declared policy.

Fit a supported probability mapping on independent or out-of-fold predictions. Select thresholds/review bands against the owner's error costs on development evidence. Threshold tuning, probability calibration and label-agreement optimization are different operations. Do not reuse final labels for any of them. Record unsupported probability fields as unavailable.

Sources: [probability calibration](https://scikit-learn.org/stable/modules/calibration.html), [decision thresholds](https://scikit-learn.org/stable/modules/classification_threshold.html). Required rates, acceptable costs and evidence volume belong to the owner; a small kappa or accuracy target is not a universal production policy.
