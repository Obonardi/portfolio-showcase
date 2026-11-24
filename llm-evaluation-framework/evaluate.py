"""Aggregate human-assigned LLM evaluation scores; no model API required."""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

DIMENSIONS = ('accuracy', 'reasoning', 'instruction_following')


def load_rows(path):
    path = Path(path)
    with path.open(encoding='utf-8', newline='') as file:
        rows = list(csv.DictReader(file)) if path.suffix.lower() == '.csv' else json.load(file)
    if not isinstance(rows, list) or not rows:
        raise ValueError('Expected a nonempty list of evaluations')
    return rows


def summarize(rows):
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Each evaluation must be an object')
        for key in ('case_id', 'model', 'response', 'notes'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f'Missing or empty {key}')
        pair = (row['case_id'], row['model'])
        if pair in seen:
            raise ValueError(f'Duplicate evaluation: {pair}')
        seen.add(pair)
        scores = {}
        for key in DIMENSIONS:
            value = row.get(key)
            if isinstance(value, str) and value in ('0', '1', '2'):
                value = int(value)
            if type(value) is not int or value not in (0, 1, 2):
                raise ValueError(f'{key} must be 0, 1 or 2')
            scores[key] = value
        groups[row['model']].append((row, scores))
    report = []
    for model, items in sorted(groups.items()):
        averages = {key: round(mean(s[key] for _, s in items), 3) for key in DIMENSIONS}
        report.append({'model': model, 'count': len(items), 'case_ids': sorted(r['case_id'] for r, _ in items), **averages,
                       'overall_percent': round(100 * mean(v for _, s in items for v in s.values()) / 2, 2),
                       'failures': [{'case_id': r['case_id'], 'dimensions': [k for k in DIMENSIONS if s[k] == 0], 'notes': r['notes']} for r, s in items if 0 in s.values()]})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('--output', default='report.json')
    args = parser.parse_args()
    try:
        report = summarize(load_rows(args.input))
        Path(args.output).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    except (ValueError, OSError) as error:
        parser.exit(2, f'Error: {error}\n')
    print(f'Wrote {args.output}')


if __name__ == '__main__':
    main()
