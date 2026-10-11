"""Rebuild src/data/topics.js: what gets accepted, broken down by topic.

Run from the repo root:  python3 scripts/build-topics.py

Source is github.com/papercopilot/paperlists, which mirrors OpenReview into
one JSON per venue-year. Each record carries the author-declared primary_area
and the final status, which is everything needed to ask whether some topics
are harder to get in with than others.

Only venues whose list is a FULL submission pool can produce a rate. The
NeurIPS and ICML lists hold accepted papers plus a handful of rejects, so a
rate computed from them would read about 94 percent. The check below refuses
to emit a rate unless rejections make up a plausible share of the list.
"""
import json, re, os, datetime, collections, urllib.request

RAW = 'https://github.com/papercopilot/paperlists/raw/main'
CACHE = '.conf-cache/paperlists'
YEARS = 4
TODAY = datetime.date.today()

ACCEPT = {'poster', 'spotlight', 'oral'}
NOT_DECIDED = {'withdraw', 'desk reject', 'desk rejected', 'withdrawn'}
# Below this share of outright rejections the list is an accepted-papers list,
# not a submission pool, and no rate may be computed from it.
MIN_REJECT_SHARE = 0.15
MIN_PER_TOPIC = 40
MIN_PER_SUB = 10
# A rate off a dozen papers swings wildly. EDA was 69.2% in 2025 on 13
# papers and 25.9% in 2026 on 27, and reporting that as a 43 point fall
# would be reporting sampling noise. Below this, no change is shown.
MIN_FOR_DELTA = 25

# Hand-picked sub-topics, matched on the author keywords and the title. These
# are narrower than primary_area and they cut across it, so each one is hung
# under whichever area most of its papers chose. Edit this list freely: a term
# that matches fewer than MIN_PER_SUB papers is dropped rather than shown as
# noise.
SELECTED = [
    ('quantum computing', r'\bquantum\b'),
    ('knowledge editing',  r'knowledge[ -]?edit|model[ -]?edit'),
    ('music generation',   r'\bmusic\b'),
    # EDA, chip and circuit design. A bare \bEDA\b catches only two papers
    # here and would also pull in exploratory data analysis and easy data
    # augmentation, so the term list is explicit instead.
    ('EDA, chip design', r'electronic design automation|chip design|circuit design|logic synthesis'
                         r'|\bnetlist\b|\bVLSI\b|analog circuit|place(ment)? and rout|standard cell'
                         r'|lithograph|\bRTL\b|hardware description|\bverilog\b|chip floorplan'),
]

# ICLR renamed four of its primary areas for 2025. These are renames, not new
# topics, so the series is joined across them. The three areas genuinely added
# in 2025 (foundation models, infrastructure, time series) are left alone and
# simply start that year.
RENAME = {
 'representation learning for computer vision, audio, language, and other modalities':
   'applications to computer vision, audio, language, and other modalities',
 'societal considerations including fairness, safety, privacy':
   'alignment, fairness, safety, privacy, and societal considerations',
 'visualization or interpretation of learned representations':
   'interpretability and explainable AI',
 'general machine learning (i.e., none of the above)':
   'other topics in machine learning (i.e., none of the above)',
}

def norm_status(s):
    s = (s or '').lower()
    s = re.sub(r'^.*\b(conditional)?', lambda m: m.group(0), s)
    for k in ACCEPT:
        if k in s: return k
    for k in NOT_DECIDED:
        if k in s: return 'undecided'
    if 'reject' in s: return 'reject'
    return 'other'

def fetch(venue, year):
    os.makedirs(CACHE, exist_ok=True)
    dest = f'{CACHE}/{venue}{year}.json'
    if not os.path.exists(dest):
        url = f'{RAW}/{venue}/{venue}{year}.json'
        try:
            with urllib.request.urlopen(url, timeout=300) as r, open(dest, 'wb') as f:
                f.write(r.read())
        except Exception as e:
            print(f'  {venue}{year}: {e}')
            return None
    try:
        return json.load(open(dest))
    except Exception as e:
        print(f'  {venue}{year}: unreadable, {e}')
        return None

# Papers are carried over from the editions that have citation counts, since
# a just-decided edition has none. Keyed by topic.
exemplars = collections.defaultdict(list)
subs = collections.defaultdict(dict)   # (venue, year) -> label -> stats

out = {}
for venue in ('iclr', 'nips', 'icml'):
    for year in range(TODAY.year + 1, TODAY.year + 1 - YEARS - 1, -1):
        papers = fetch(venue, year)
        if not papers: continue
        st = [norm_status(p.get('status')) for p in papers]
        counts = collections.Counter(st)
        decided = sum(v for k, v in counts.items() if k != 'undecided')
        reject_share = counts['reject'] / decided if decided else 0
        full_pool = reject_share >= MIN_REJECT_SHARE
        print(f'{venue}{year}: {len(papers)} records, reject share {reject_share:.0%}, '
              f'{"full pool" if full_pool else "accepted-papers list, no rate"}')
        if not full_pool:
            continue

        rows = collections.defaultdict(lambda: [0, 0])   # decided, accepted
        for p, s in zip(papers, st):
            area = (p.get('primary_area') or '').strip()
            area = RENAME.get(area, area)
            if not area or s == 'undecided': continue
            rows[area][0] += 1
            if s in ACCEPT: rows[area][1] += 1
            cites = p.get('gs_citation') or 0
            if s in ACCEPT and cites > 0 and p.get('title'):
                exemplars[(venue, area)].append(
                    {'t': p['title'].strip(), 'y': year, 'c': cites,
                     'k': (p.get('status') or '').strip(),
                     'u': (p.get('site') or p.get('openreview') or '').strip()})
        pool = sum(n for n, _ in rows.values())
        topics = [{'area': a, 'n': n, 'acc': k, 'rate': round(100 * k / n, 1),
                   # Share of the submission pool. Absolute counts rise with
                   # the conference, so share is what says a topic is getting
                   # crowded rather than the field just getting bigger.
                   'share': round(100 * n / pool, 1)}
                  for a, (n, k) in rows.items() if n >= MIN_PER_TOPIC]
        if not topics: continue
        # Selected sub-topics over the same decided pool as the areas above.
        for label, pattern in SELECTED:
            rx = re.compile(pattern, re.I)
            hits = [p for p, st_ in zip(papers, st) if st_ != 'undecided'
                    and rx.search((p.get('keywords') or '') + ' ' + (p.get('title') or ''))]
            if len(hits) < MIN_PER_SUB: continue
            a = sum(1 for p in hits if norm_status(p.get('status')) in ACCEPT)
            home = collections.Counter(
                RENAME.get((p.get('primary_area') or '').strip(), (p.get('primary_area') or '').strip())
                for p in hits if p.get('primary_area'))
            top, top_n = home.most_common(1)[0] if home else ('', 0)
            subs[(venue, year)][label] = {
                'label': label, 'n': len(hits), 'acc': a,
                'rate': round(100 * a / len(hits), 1),
                'area': top, 'concentration': round(100 * top_n / len(hits))}

        topics.sort(key=lambda t: -t['rate'])
        overall = round(100 * sum(t['acc'] for t in topics) / sum(t['n'] for t in topics), 1)
        # Two denominators, because both are in circulation. The conference
        # quotes acceptances over every submission, which is the lower,
        # headline number. Per-topic rates have to use decided submissions,
        # since a withdrawal is not a rejection. Printing both stops the page
        # from looking like it disagrees with the official fact sheet.
        n_all = len(papers)
        n_acc = sum(1 for x in st if x in ACCEPT)
        n_gone = sum(1 for x in st if x == 'undecided')
        headline = round(100 * n_acc / n_all, 1) if n_all else 0
        out.setdefault(venue.upper().replace('NIPS', 'NeurIPS'), []).append(
            {'year': year, 'overall': overall, 'topics': topics,
             'decided': sum(t['n'] for t in topics),
             'submitted': n_all, 'accepted': n_acc, 'withdrawn': n_gone,
             'headline': headline})

for v in out: out[v].sort(key=lambda e: -e['year'])

# The ten most-cited accepted papers per topic, as a concrete answer to what
# work in this area actually looks like. The newest edition has no citation
# counts yet, so these come from the editions that do, with the year shown.
for venue, eds in out.items():
    key = 'nips' if venue == 'NeurIPS' else venue.lower()
    now_y, prev_y = eds[0]['year'], (eds[1]['year'] if len(eds) > 1 else None)
    picked = []
    for label, cur in subs.get((key, now_y), {}).items():
        was = subs.get((key, prev_y), {}).get(label)
        enough = was and was['n'] >= MIN_FOR_DELTA and cur['n'] >= MIN_FOR_DELTA
        cur['delta'] = round(cur['rate'] - was['rate'], 1) if enough else None
        cur['prevN'] = was['n'] if was else 0
        picked.append(cur)
    # They are listed separately rather than nested under an area. Most of
    # them cut across several: only 18% of the quantum papers sit in the area
    # that holds the most of them, so claiming one as its home would be false.
    picked.sort(key=lambda x: -x['rate'])
    if picked: eds[0]['selected'] = picked

    # Ten most-cited accepted papers per topic. The newest edition has no
    # citation counts yet, so these come from the editions that do.
    for t in eds[0]['topics']:
        got = sorted(exemplars.get((key, t['area']), []), key=lambda x: -x['c'])[:10]
        if got: t['papers'] = got

hdr = ('// Generated by scripts/build-topics.py, do not edit by hand.\n'
       '// Per-topic acceptance rates from github.com/papercopilot/paperlists,\n'
       '// which mirrors OpenReview. primary_area is declared by the authors.\n'
       '// Only venues publishing a full submission pool appear here: the\n'
       '// NeurIPS and ICML lists are accepted-papers lists, so no rate can be\n'
       '// computed from them. Denominator excludes withdrawn and desk-rejected.\n'
       f'// Built {TODAY.isoformat()}.\n')
with open('src/data/topics.js', 'w') as f:
    f.write(hdr + 'export const topicRates = ' + json.dumps(out, indent=2) + ';\n')

print('\nwritten | venues', list(out), '| editions',
      {k: [e['year'] for e in v] for k, v in out.items()})
