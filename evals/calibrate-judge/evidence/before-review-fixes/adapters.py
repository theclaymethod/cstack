"""Strict project-local response normalization; no SDK or network calls."""
import json
import math


def probability(value):
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('Expected finite probability in [0,1]')
    return float(value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON field')
        result[key] = value
    return result


def normalize(raw, config, exit_code=0):
    result = {'verdict': 'ERROR', 'failure_probability': None, 'rationale': None, 'error': None}
    if exit_code != 0:
        result['error'] = 'judge process did not exit successfully'; return result
    try:
        if config['backend'] == 'llm':
            answer = json.loads(raw['text'], object_pairs_hook=unique_object)
            if not isinstance(answer, dict) or not {'verdict'} <= set(answer) <= {'verdict', 'reason'}:
                raise ValueError('Malformed declared LLM verdict schema')
            verdict = answer['verdict']
            if verdict not in ('PASS', 'FAIL', 'UNKNOWN'):
                raise ValueError('Unsupported LLM verdict')
            reason = answer.get('reason')
            if reason is not None and not isinstance(reason, str):
                raise ValueError('Rationale must be a string or absent')
            result.update(verdict=verdict, rationale=reason)
        elif config['backend'] == 'jev':
            answer = raw['answers']['criterion']
            low, high = probability(config['pass_below']), probability(config['fail_at_or_above'])
            if low > high:
                raise ValueError('Abstention band is inverted')
            if answer['type'] == 'noul':
                p = probability(answer['noul'])
                if type(config['question_means_failure']) is not bool:
                    raise ValueError('Explicit yes/failure polarity is required')
                if not config['question_means_failure']: p = 1 - p
            elif answer['type'] == 'choice':
                probs = answer['probabilities']
                if set(probs) != {'PASS', 'FAIL'} or abs(sum(probability(v) for v in probs.values()) - 1) > 1e-8:
                    raise ValueError('Fixture Choice needs a complete PASS/FAIL distribution')
                if answer['choice'] not in probs or probs[answer['choice']] < max(probs.values()) - 1e-8:
                    raise ValueError('Choice disagrees with its native distribution')
                p = probability(probs['FAIL'])
            else:
                raise ValueError('This local adapter supports Noul/binary Choice, not native ordinal Score')
            result.update(failure_probability=p,
                          verdict='FAIL' if p >= high else 'PASS' if p < low else 'UNKNOWN')
            # Deliberately do not turn concentration confidence into P(failure) or invent a rationale.
        else:
            raise ValueError('Unsupported backend')
    except (ValueError, TypeError, KeyError) as error:
        result.update(verdict='ERROR', failure_probability=None, rationale=None, error=str(error))
    return result
