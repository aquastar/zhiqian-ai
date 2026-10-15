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
PAGES = ROOT / 'src' / 'pages' / 'funding'
ARCHIVE = PAGES / 'archive'
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


def md_table(rows, headers, keys):
    out = ['| ' + ' | '.join(headers) + ' |',
           '|' + '|'.join(['---'] * len(headers)) + '|']
    for r in rows:
        cells = []
        for k in keys:
            v = (r.get(k) or '').replace('|', '\\|')
            cells.append(f'[链接]({v})' if k == 'url' and v else v)
        out.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)


def page(title, date, window, body):
    w = ''
    if window:
        w = (f"收录窗口: {window['new_since']} 以来新发布, "
             f"或 {window['deadline_before']} 前截止.\n\n")
    return (f'---\ntitle: "{title}"\ndate: {date}\n---\n\n'
            f'# {title}\n\n更新于 {date}. {CAVEAT}\n\n{w}{body}\n')


def main():
    brief_p, registry_p, watchlist_p = sys.argv[1:4]
    date, window, opps, signals = parse_brief(load(brief_p))
    registry = parse_registry(load(registry_p))
    watchlist = parse_watchlist(load(watchlist_p))

    for d in (PAGES, ARCHIVE, PUBLIC):
        d.mkdir(parents=True, exist_ok=True)

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
    (PUBLIC / 'data.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (PUBLIC / f'{date}.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    body = ['## 机会总表\n',
            md_table(opps,
                     ['机构', '项目名称与编号', '截止日期', '预算与年限', '资格要点', '竞争度估计', '来源层', '链接'],
                     ['sponsor', 'program', 'deadline', 'budget', 'eligibility',
                      'competition', 'source_tier', 'url'])]
    if signals:
        body.append('\n## 早期信号\n')
        body += [f"- {s['note']}" + (f": {s['url']}" if s['url'] else '')
                 for s in signals]
    body = '\n'.join(body)

    links = ('[往期](/funding/archive/) | [data.json](/funding/data.json) | '
             '[registry.csv](/funding/registry.csv) | '
             '[watchlist.csv](/funding/watchlist.csv)\n\n')
    title = f'AI Funding Brief {date}'
    (PAGES / 'index.md').write_text(page(title, date, window, links + body), encoding='utf-8')
    (ARCHIVE / f'{date}.md').write_text(page(title, date, window, body), encoding='utf-8')

    dates = sorted((p.stem for p in ARCHIVE.glob('????-??-??.md')), reverse=True)
    lst = '\n'.join(f'- [{x}](/funding/archive/{x}/)' for x in dates)
    (ARCHIVE / 'index.md').write_text(
        f'---\ntitle: "AI Funding Brief Archive"\n---\n\n'
        f'# AI Funding Brief Archive\n\n{lst}\n', encoding='utf-8')

    with open(PUBLIC / 'registry.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['first_seen_date', 'sponsor', 'program',
                                          'deadline', 'url'])
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
    served = list(PUBLIC.glob('*')) + list(PAGES.rglob('*.md'))
    for p in served:
        if p.is_dir():
            continue
        text = p.read_text(encoding='utf-8')
        hit = [b for b in banned if b in text]
        if hit:
            sys.exit(f'{p}: personal content leaked into a public file: {hit}')

    print(f'brief {date}: {len(opps)} opportunities, {len(signals)} signals, '
          f'{len(registry)} registry rows, {len(watchlist)} watchlist rows')


if __name__ == '__main__':
    main()
