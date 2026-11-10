"""Agreement, uncertainty and probability diagnostics, with explicit denominators."""
from collections import Counter, defaultdict
import math
import random


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def agreement(rows, labels=('PASS', 'FAIL'), weighting=None):
    labels = tuple(labels)
    if not labels or len(labels) != len(set(labels)) or weighting not in (None, 'linear', 'quadratic'):
        raise ValueError('Declare unique labels and supported ordinal weighting')
    table = {gold: {pred: 0 for pred in labels} for gold in labels}
    other = {gold: {'UNKNOWN': 0, 'ERROR': 0} for gold in labels}
    for row in rows:
        if row['gold'] not in labels or row['verdict'] not in (*labels, 'UNKNOWN', 'ERROR'):
            raise ValueError('Unsupported gold or prediction label')
        if row['verdict'] in labels:
            table[row['gold']][row['verdict']] += 1
        else:
            other[row['gold']][row['verdict']] += 1
    n = sum(sum(v.values()) for v in table.values())
    observed = ratio(sum(table[label][label] for label in labels), n)
    if n:
        marginal_gold = {label: sum(table[label].values()) / n for label in labels}
        marginal_pred = {label: sum(table[g][label] for g in labels) / n for label in labels}
        expected_agreement = sum(marginal_gold[label] * marginal_pred[label] for label in labels)
        observed_disagreement = expected_disagreement = 0.0
        for i, gold in enumerate(labels):
            for j, pred in enumerate(labels):
                penalty = float(i != j) if weighting is None else abs(i - j) / max(1, len(labels) - 1)
                if weighting == 'quadratic': penalty **= 2
                observed_disagreement += penalty * table[gold][pred] / n
                expected_disagreement += penalty * marginal_gold[gold] * marginal_pred[pred]
        kappa = 1 - observed_disagreement / expected_disagreement if expected_disagreement else None
        reason = None if expected_disagreement else 'expected_disagreement_is_zero'
    else:
        marginal_gold = marginal_pred = {}; expected_agreement = None; kappa = None; reason = 'no_decided_pairs'
        observed_disagreement = expected_disagreement = None
    rates = {}
    if set(labels) == {'PASS', 'FAIL'}:
        tp, fn = table['FAIL']['FAIL'], table['FAIL']['PASS']
        fp, tn = table['PASS']['FAIL'], table['PASS']['PASS']
        rates = {'TP': tp, 'FN': fn, 'FP': fp, 'TN': tn,
                 'failure_catch': ratio(tp, tp + fn), 'false_pass_among_gold_failures': ratio(fn, tp + fn),
                 'false_rejection_among_gold_passes': ratio(fp, fp + tn),
                 'false_outcomes_among_judge_passes': ratio(fn, tn + fn)}
    return {'attempted': len(rows), 'decided': n, 'coverage': ratio(n, len(rows)),
            'confusion': table, 'other_by_gold': other,
            'gold_prevalence_all_attempted': {label: ratio(sum(r['gold'] == label for r in rows), len(rows)) for label in labels},
            'labels': list(labels), 'observed_agreement_decided': observed,
            'nominal_expected_agreement_decided': expected_agreement,
            'kappa_observed_disagreement': observed_disagreement, 'kappa_expected_disagreement': expected_disagreement,
            'kappa_decided': kappa, 'kappa_undefined_reason': reason, 'weighting': weighting,
            'marginal_gold_decided': marginal_gold, 'marginal_prediction_decided': marginal_pred,
            'failure_positive_rates_decided': rates}


def percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    low = int(position); high = min(low + 1, len(ordered) - 1)
    return ordered[low] * (high - position) + ordered[high] * (position - low) if high != low else ordered[low]


def uncertainty(rows, draws=200, seed=17):
    """Paired whole-family bootstrap; undefined replicates stay visible."""
    if type(draws) is not int or draws < 2:
        raise ValueError('Need at least two bootstrap replicates')
    groups = defaultdict(list)
    for row in rows:
        if not isinstance(row.get('family'), str) or not row['family']:
            raise ValueError('An independent resampling-family declaration is required')
        groups[row['family']].append(row)
    keys = sorted(groups)
    if len(keys) < 2:
        return {'method': 'paired family bootstrap', 'families': len(keys), 'draws': draws,
                'intervals': {}, 'reason': 'insufficient_independent_families'}
    rng = random.Random(seed)
    values = {'kappa_decided': [], 'failure_catch': [], 'false_pass_among_gold_failures': [],
              'false_rejection_among_gold_passes': [], 'coverage': []}
    for _ in range(draws):
        sample = [row for _ in keys for row in groups[rng.choice(keys)]]
        result = agreement(sample)
        for name in values:
            values[name].append(result.get(name, result['failure_positive_rates_decided'].get(name)))
    intervals = {}
    for name, series in values.items():
        undefined = sum(value is None for value in series)
        intervals[name] = {'bounds': None if undefined else [percentile(series, .025), percentile(series, .975)],
                           'undefined_replicates': undefined}
    return {'method': 'paired whole-family percentile bootstrap, row-weighted within sampled families',
            'confidence_level': .95, 'seed': seed, 'families': len(keys), 'draws': draws, 'intervals': intervals,
            'limits': 'Assumes independent declared families and an appropriate sampling model; few families/rare classes limit inference. Undefined replicates suppress that interval rather than being discarded.'}


def probability_diagnostics(rows, bins=5):
    if type(bins) is not int or bins < 1:
        raise ValueError('Need a positive bin count')
    known = []
    for row in rows:
        p = row.get('failure_probability')
        if p is None: continue
        if row['gold'] not in ('PASS', 'FAIL') or type(p) not in (float, int) or not 0 <= p <= 1 or not math.isfinite(p):
            raise ValueError('Need finite native P(failure), not confidence or an ordinal score')
        known.append((float(p), int(row['gold'] == 'FAIL')))
    reliability = []
    for index in range(bins):
        selected = [(p, y) for p, y in known if min(int(p * bins), bins - 1) == index]
        reliability.append({'lower': index / bins, 'upper': (index + 1) / bins, 'count': len(selected),
            'mean_probability': ratio(sum(p for p, _ in selected), len(selected)),
            'empirical_failure_rate': ratio(sum(y for _, y in selected), len(selected))})
    losses = []
    for p, y in known:
        event_probability = p if y else 1 - p
        losses.append(-math.log(event_probability) if event_probability else None)
    return {'probability_pairs': len(known), 'attempted': len(rows),
            'brier': ratio(sum((p - y) ** 2 for p, y in known), len(known)),
            'log_loss': None if None in losses else ratio(sum(losses), len(losses)),
            'log_loss_infinite': None in losses, 'reliability_bins': reliability,
            'limits': 'Brier/log loss include discrimination and uncertainty; these do not alone isolate calibration.'}
