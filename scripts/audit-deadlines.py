"""Weekly audit of the deadlines that nothing upstream maintains.

Run from the repo root:  python3 scripts/audit-deadlines.py
Prints Markdown. The weekly workflow puts it in the job summary and in an
open issue labelled deadline-check, so a change is something you are told
about rather than something you have to remember to look for.

ccf-deadlines keeps the computing venues current on its own. The venues
added by hand in build-conferences.py (control, neuroscience, sleep,
physics, mathematics, the society meetings) only change when someone edits
them, and an estimate rolled forward from last year quietly turns wrong the
week the venue announces its real date. This lists, by urgency:

  1. hand-kept deadlines in the next three weeks, to confirm on the site;
  2. estimated deadlines within two months, where the real date is
     probably out by now and the estimate should be replaced;
  3. every other estimate, for reference.
"""
import json, re, datetime

TODAY = datetime.date.today()
conf = open('src/data/conferences.js', encoding='utf-8').read()
def export(name):
    m = re.search(r'export const ' + name + r' = (\[.*?\]);\n', conf, re.S)
    return json.loads(m.group(1)) if m else []
labels = dict(re.findall(r"id: '([a-z]+)', label: '([^']+)'", open('src/data/domains.js', encoding='utf-8').read()))

venues = [v for v in export('ranked') + export('notable') if v.get('notable')]

def next_date(v):
    ds = [r.get('d') for r in v.get('rounds') or [] if r.get('d') and r['d'] >= TODAY.isoformat()]
    return min(ds) if ds else (v.get('nextDeadline') or '')

soon, est_close, est_rest = [], [], []
for v in venues:
    d = next_date(v)
    if not d: continue
    days = (datetime.date.fromisoformat(d) - TODAY).days
    row = (d, days, v['title'], labels.get(v.get('area'), v.get('area', '')), v.get('link', ''))
    if v.get('estimated'):
        (est_close if days <= 60 else est_rest).append(row)
    elif 0 <= days <= 21:
        soon.append(row)

def table(rows):
    out = ['| Deadline | In | Venue | Field |', '|---|---|---|---|']
    for d, days, t, f, link in sorted(rows):
        out.append(f'| {d} | {days}d | [{t}]({link}) | {f} |' if link else f'| {d} | {days}d | {t} | {f} |')
    return '\n'.join(out)

print(f'# Deadline check, {TODAY.isoformat()}\n')
print('Hand-kept venues only; ccf-deadlines maintains the rest. Edit them in '
      '`scripts/build-conferences.py` (NOTABLE), then the next refresh picks the change up.\n')
print(f'## Due in the next three weeks ({len(soon)})\n')
print((table(soon) if soon else 'Nothing.') + '\n')
print(f'## Estimated, and within two months ({len(est_close)})\n')
print('These are last year\'s dates rolled forward. The venue has probably announced the real one.\n')
print((table(est_close) if est_close else 'Nothing.') + '\n')
print(f'<details><summary>Every other estimate ({len(est_rest)})</summary>\n')
print((table(est_rest) if est_rest else 'Nothing.') + '\n')
print('</details>')
