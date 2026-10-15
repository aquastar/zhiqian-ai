#!/usr/bin/env python3
"""Compare the deadlines we publish against each venue's own site.

ccfddl is a hand-maintained catalogue and it lags. Where it has no announced
date it rolls last year's forward and marks the result an estimate, and those
estimates can be far out: ICDAR was showing November when its own site said
the following February. This finds those cases.

It reports rather than rewrites. Site prose is not reliable enough to publish
from directly, as the dates it surfaces include conference dates, notification
dates and the leftovers of previous years. A human reads this list and adds
the confirmed ones to DEADLINE_FIX in build-conferences.py, where each entry
carries the date, the source url and the sentence it came from.

    python3 scripts/check-deadlines.py            # venues whose date we estimate
    python3 scripts/check-deadlines.py --all      # every ranked venue
"""

import datetime
import html
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
TODAY = datetime.date.today()

MONTHS = {m.lower(): i for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July',
     'August', 'September', 'October', 'November', 'December'], 1)}
for _m, _i in list(MONTHS.items()):
    MONTHS[_m[:3]] = _i

DATE_RE = re.compile(
    r'\b(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d\d)\b'
    r'|\b(\d{1,2})\s+(' + '|'.join(sorted(MONTHS, key=len, reverse=True)) + r')\.?,?\s+(20\d\d)\b'
    r'|\b(20\d\d)-(\d{2})-(\d{2})\b', re.I)

# A line has to be about submitting, not about the meeting or the outcome.
WANT = re.compile(r'\b(submission|submit|paper|abstract|deadline|due)\b', re.I)
SKIP = re.compile(r'\b(notification|accept|camera|rebuttal|review|registration|'
                  r'workshop|tutorial|poster|demo|doctoral|author response|'
                  r'travel|visa|early bird)\b', re.I)
CFP_RE = re.compile(
    r'href=["\']([^"\']*(?:call[-_]?for[-_]?paper|cfp|important[-_]?date|submission|dates)[^"\']*)["\']', re.I)


def iso(m):
    g = m.groups()
    try:
        if g[0]:
            return f'{int(g[2]):04d}-{MONTHS[g[0].lower()]:02d}-{int(g[1]):02d}'
        if g[3]:
            return f'{int(g[5]):04d}-{MONTHS[g[4].lower()]:02d}-{int(g[3]):02d}'
        return f'{g[6]}-{g[7]}-{g[8]}'
    except (KeyError, ValueError):
        return None


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read(700_000).decode('utf-8', 'replace')
    except Exception:
        return ''


def plain(body):
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', body, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body)))


def candidates(link):
    """Submission-looking dates in the future, with the sentence each came from."""
    body = fetch(link)
    if not body:
        return None, []
    text = plain(body)
    for sub in [urllib.parse.urljoin(link, m.group(1)) for m in CFP_RE.finditer(body)][:2]:
        more = fetch(sub)
        if more:
            text += ' ' + plain(more)

    # Important-dates blocks are routinely one unpunctuated run:
    # "Workshop proposal deadline September 4, 2026 Main submission deadline
    # (ARR) October 12, 2026 Notification ...". Splitting on sentences finds
    # nothing there, so each date is classified by the words immediately
    # before it instead, which is where its label sits.
    out = []
    for m in DATE_RE.finditer(text):
        d = iso(m)
        if not d or d < TODAY.isoformat():
            continue
        label = text[max(0, m.start() - 75):m.start()]
        # Only the last label wins: in a run, the words nearest the date are
        # the ones describing it.
        label = re.split(r'(?<=20\d\d)\s', label)[-1]
        if not WANT.search(label) or SKIP.search(label):
            continue
        line = re.sub(r'\s+', ' ', label + m.group(0)).strip()
        if (d, line) not in out:
            out.append((d, line[-120:]))
    return text, out[:4]


def load(name):
    src = (ROOT / 'src' / 'data' / 'conferences.js').read_text(encoding='utf-8')
    i = src.index(f'export const {name} = [') + len(f'export const {name} = ')
    depth = 0
    for j, ch in enumerate(src[i:], i):
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                return json.loads(src[i:j + 1])
    raise SystemExit(f'could not read {name}')


def main():
    every = '--all' in sys.argv
    venues = [c for c in load('ranked')
              if c.get('link') and (every or c.get('estimated'))]
    print(f'checking {len(venues)} venues against their own sites\n')

    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda c: candidates(c['link']), venues))

    disagree = unreachable = silent = agree = 0
    for c, (text, hits) in zip(venues, results):
        ours = c['nextDeadline']
        mark = 'est' if c.get('estimated') else '   '
        if text is None:
            unreachable += 1
            print(f'{c["title"]:<12} {mark} ours {ours}   SITE UNREACHABLE  {c["link"]}')
            continue
        if not hits:
            silent += 1
            continue
        dates = [d for d, _ in hits]
        if ours in dates:
            agree += 1
            continue
        disagree += 1
        print(f'{c["title"]:<12} {mark} ours {ours}   site says {", ".join(sorted(set(dates)))}')
        for d, line in hits[:2]:
            print(f'{"":<17}   {d}  "{line}"')
        print(f'{"":<17}   {c["link"]}')

    print(f'\nagree {agree}, disagree {disagree}, site said nothing usable {silent}, '
          f'unreachable {unreachable}')


if __name__ == '__main__':
    main()
