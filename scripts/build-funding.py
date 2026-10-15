#!/usr/bin/env python3
"""Turn the three Drive sources into public funding data.

Everything written here is served at zhiqian.ai/funding, so the one rule this
script enforces is that nothing personal survives the trip. The Drive brief is
written for one reader: it names him, it scores every opportunity against his
own research lines, and its headline section is strategy advice. None of that
belongs on a public page, and none of it is in the output.

Dropped on purpose, listed so the omission stays deliberate:

  - the "对象: <name>, <institution>" line
  - the 匹配度 column, a 1 to 10 personal fit score
  - the 本周头条 section, which is personal strategy end to end
  - the pointer to the private full report and its 低匹配项 count
  - the watchlist research_lines column, which keys rows to personal interests

What survives is the part that is true for anybody: who funds it, what it is
called, when it closes, how much, who may apply, how crowded it looks, and
where to read the call.

Usage: build-funding.py <brief.txt> <registry.txt> <watchlist.csv>
"""

import csv
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'src' / 'data'
PUBLIC = ROOT / 'public' / 'funding'

# The brief's table, left to right. 'skip' is the personal fit score.
COLUMNS = ['sponsor', 'program', 'deadline', 'budget', 'eligibility',
           'skip', 'competition', 'source_tier', 'url']

CAVEAT = ('未核实 = 未在一手页面确认. 以资助方官网为准, 本页仅为汇总.')


def load(path):
    text = pathlib.Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    if text.lstrip().lower().startswith(('<!doctype', '<html')):
        sys.exit(f"{path}: got an HTML page, the Drive file is probably not "
                 f"shared as 'Anyone with the link'")
    return text


def parse_brief(text):
    """Pull the date, the window and the opportunity table out of the brief."""
    m = re.search(r'AI Funding Brief (\d{4}-\d{2}-\d{2})', text)
    if not m:
        sys.exit("brief heading 'AI Funding Brief YYYY-MM-DD' not found")
    date = m.group(1)

    # The window is a fact about the search, not about the person, so it is
    # lifted out of the 对象 line before that line is discarded.
    window = {}
    w = re.search(r'窗口:\s*(\d{4}-\d{2}-\d{2})\s*以来新发布,\s*或\s*(\d{4}-\d{2}-\d{2})\s*前截止', text)
    if w:
        window = {'new_since': w.group(1), 'deadline_before': w.group(2)}

    rows = []
    for line in text.split('\n'):
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != len(COLUMNS):
            continue
        if cells[0] in ('机构', '') or set(cells[0]) <= set('-: '):
            continue        # header and the --- separator
        row = {k: v for k, v in zip(COLUMNS, cells) if k != 'skip'}
        rows.append(row)

    signals = []
    tail = text.split('## 3. 早期信号', 1)
    if len(tail) == 2:
        for line in tail[1].split('\n'):
            line = line.strip()
            if not line.startswith('- '):
                continue
            body = line[2:].strip()
            u = re.search(r'(https?://\S+)$', body)
            signals.append({
                'note': body[:u.start()].rstrip(' :') if u else body,
                'url': u.group(1) if u else '',
            })

    return date, window, rows, signals


def parse_registry(text):
    rows = []
    for line in text.split('\n'):
        if not re.match(r'^\s*\d{4}-\d{2}-\d{2}\s*\|', line):
            continue
        parts = [x.strip() for x in line.split('|')]
        # Anything past the fifth field is part of the url, which can itself
        # contain a pipe. Rejoin rather than truncate.
        parts = parts[:4] + ['|'.join(parts[4:]).strip()]
        rows.append(dict(zip(
            ['first_seen_date', 'sponsor', 'program', 'deadline', 'url'], parts)))
    return rows


def parse_watchlist(text):
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for r in reader:
        r.pop('research_lines', None)       # keys rows to personal interests
        rows.append({k: (v or '').strip() for k, v in r.items() if k})
    return rows


def main():
    brief_p, registry_p, watchlist_p = sys.argv[1:4]
    date, window, opps, signals = parse_brief(load(brief_p))
    registry = parse_registry(load(registry_p))
    watchlist = parse_watchlist(load(watchlist_p))

    for d in (DATA, PUBLIC):
        d.mkdir(parents=True, exist_ok=True)

    # Every opportunity in the weekly table is also a registry row, so the page
    # can show one list instead of two and the brief's extra columns ride along
    # on the row they belong to. The url alone is not enough of a key: three
    # sponsors list two separate programs behind a single landing page, and
    # matching on url would copy one programme's budget onto the other. Where a
    # url is shared, the programme names have to agree as well.
    def norm(x):
        return [t for t in re.split(r'[^a-z0-9]+', (x or '').lower()) if t]

    by_url = {}
    for r in registry:
        by_url.setdefault(r.get('url', ''), []).append(r)

    for o in opps:
        rows = by_url.get(o.get('url', ''), [])
        if not rows:
            continue
        if len(rows) > 1:
            want = set(norm(o.get('program')))
            scored = sorted(rows, key=lambda r: len(want & set(norm(r.get('program')))),
                            reverse=True)
            best = len(want & set(norm(scored[0].get('program'))))
            if best == 0:
                continue                      # same page, different programme
            rows = [scored[0]]
        target = rows[0]
        target['pick'] = True
        for k in ('budget', 'eligibility', 'competition', 'source_tier'):
            if o.get(k):
                target[k] = o[k]

    data = {
        'date': date,
        'window': window,
        'caveat': CAVEAT,
        'counts': {'opportunities': len(opps), 'early_signals': len(signals),
                   'registry': len(registry), 'watchlist': len(watchlist)},
        'opportunities': opps,
        'early_signals': signals,
        'registry': registry,
        'watchlist': watchlist,
    }
    blob = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    (PUBLIC / 'data.json').write_text(blob, encoding='utf-8')
    (PUBLIC / f'{date}.json').write_text(blob, encoding='utf-8')
    # The page imports this one. Keeping it in src means a missing or malformed
    # brief breaks the build loudly instead of rendering an empty table.
    (DATA / 'funding.json').write_text(blob, encoding='utf-8')

    with open(PUBLIC / 'registry.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['first_seen_date', 'sponsor', 'program',
                                          'deadline', 'url'], extrasaction='ignore')
        w.writeheader()
        w.writerows(registry)

    if watchlist:
        with open(PUBLIC / 'watchlist.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(watchlist[0].keys()))
            w.writeheader()
            w.writerows(watchlist)

    # A last sweep over everything that will be served. The personal lines are
    # removed structurally above; this is the check that says so out loud, and
    # fails the run rather than publishing a name by accident.
    banned = ['Zhiqian', 'RIT CS', '对象:', '匹配度', '本周头条', 'research_lines']
    for p in list(PUBLIC.glob('*')) + [DATA / 'funding.json']:
        if p.is_dir():
            continue
        hit = [b for b in banned if b in p.read_text(encoding='utf-8')]
        if hit:
            sys.exit(f'{p}: personal content leaked into a public file: {hit}')

    picks = sum(1 for r in registry if r.get('pick'))
    print(f'brief {date}: {len(opps)} opportunities ({picks} matched into the '
          f'registry), {len(signals)} signals, {len(registry)} registry rows, '
          f'{len(watchlist)} watchlist rows')


if __name__ == '__main__':
    main()
