"""Rebuild src/data/trends.js: what each field is publishing most.

Run from the repo root:  python3 scripts/build-trends.py
Expects src/data/conferences.js, so run build-conferences.py first.

Acceptance rates exist for a handful of computing conferences and nowhere
else, so this measures the one thing every field has: papers. For each
field it counts the last full year's papers in that field's journals (the
ones listed on its tab, plus the flagship proceedings for the fields that
publish at conferences) by OpenAlex topic, keeps the ten largest, and
compares each topic's share with two years earlier. Share rather than raw
count, because the journals themselves grow and shrink.

One grouped query per field per year, at one OpenAlex credit each: 38 a
week against a free budget of 1,000 a day.
"""
import json, re, datetime, urllib.request, urllib.error, time, os

TODAY = datetime.date.today()
YEAR = TODAY.year - 1          # the last full year
BASE = YEAR - 2                # what the share is compared against
TOP = 10
OUT = 'src/data/trends.js'

conf = open('src/data/conferences.js', encoding='utf-8').read()
journals = json.loads(re.search(r'export const journals = (\[.*?\]);\n', conf, re.S).group(1))

# Last week's numbers, kept for any field whose fetch fails this week.
prev = {}
if os.path.exists(OUT):
    m = re.search(r'export const trends = (\{.*\});', open(OUT, encoding='utf-8').read(), re.S)
    if m: prev = json.loads(m.group(1)).get('fields', {})

def topics(sources, year):
    url = ('https://api.openalex.org/works?filter=primary_location.source.id:' + '|'.join(sources) +
           f',publication_year:{year}&group_by=primary_topic.id&per_page=200&mailto=site@zhiqian.ai')
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
            return d['meta']['count'], d['group_by']
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 3: raise
            time.sleep(5 * (attempt + 1))

# Conference-led fields publish their main work in proceedings, so counting
# only their journals would describe the long versions, not the field. These
# are the flagship proceedings OpenAlex indexes for both years compared,
# each found by name and checked for 2023 and 2025 records on 2026-10-19.
# The ones it does not index are named, so the page can say what is missing.
CONF_SOURCES = {
    'security': ([('S4363608815', 'CCS'), ('S4210233669', 'S&P'), ('S4306420590', 'NDSS')],
                 ['USENIX Security']),
    'ai': ([('S4363606243', 'NeurIPS'), ('S4210191458', 'AAAI'), ('S4363608767', 'KDD'),
            ('S4210176548', 'CVPR'), ('S4363608652', 'ACL')],
           ['ICML', 'ICLR']),
    'eda': ([('S4210231368', 'DAC'), ('S4363608791', 'ASP-DAC'), ('S4393916863', 'ISCA'),
             ('S4210184388', 'HPCA')],
            ['ICCAD', 'DATE']),
    'audio': ([('S4363607879', 'ICASSP'), ('S4393918409', 'Interspeech')], ['ISMIR']),
    'control': ([('S4210221977', 'CDC'), ('S4210168941', 'ACC')], []),
    'biomed': ([('S4363605129', 'ISBI')], ['MICCAI']),
}

# A few OpenAlex topic names have not kept up with what is filed under them.
# "Topic Modeling" is where it puts language-model papers (its keywords are
# pretrained language models, retrieval-augmented generation, question
# answering), and the GAN topic is mostly diffusion and text-to-image now.
# The page shows the clearer name and keeps OpenAlex's in the tooltip.
RELABEL = {
    'Topic Modeling': 'Language models and NLP',
    'Generative Adversarial Networks and Image Synthesis': 'Image generation (diffusion, GANs)',
}

fields = {}
by_area = {}
for j in journals:
    if j.get('oa'): by_area.setdefault(j['area'], []).append(j['oa'].rsplit('/', 1)[-1])
for area, journal_sources in by_area.items():
    confs, missing = CONF_SOURCES.get(area, ([], []))
    sources = journal_sources + [sid for sid, _ in confs]
    try:
        total, now = topics(sources, YEAR)
        total0, then = topics(sources, BASE)
        time.sleep(0.3)
    except Exception as e:
        print('  kept last week for', area, '-', e)
        if area in prev: fields[area] = prev[area]
        continue
    # Papers with no topic assigned come back keyed "unknown"; they say
    # nothing about what the field works on.
    now = [g for g in now if g['key'] and 'unknown' not in g['key'].lower()]
    before = {g['key']: g['count'] for g in then}
    rows = []
    for g in now[:TOP]:
        share = g['count'] / total * 100 if total else 0
        share0 = before.get(g['key'], 0) / total0 * 100 if total0 else 0
        rows.append({
            'topic': g['key_display_name'], 'label': RELABEL.get(g['key_display_name'], g['key_display_name']),
            'id': g['key'].rsplit('/', 1)[-1],
            'n': g['count'], 'share': round(share, 1),
            # Relative change in share. None when the topic was absent two
            # years ago, which the page shows as "new" rather than infinity.
            'growth': round((share / share0 - 1) * 100) if share0 else None,
        })
    fields[area] = {'total': total, 'journals': len(journal_sources),
                    'confs': [name for _, name in confs], 'missing': missing, 'rows': rows}
    print(f'  {area:10s} {total:6d} papers  top: {rows[0]["topic"] if rows else "-"}')

out = {'year': YEAR, 'base': BASE, 'fields': fields}
hdr = ('// Generated by scripts/build-trends.py, do not edit by hand.\n'
       f'// Papers per OpenAlex topic in each field\'s journals, {YEAR}, against {BASE}.\n'
       f'// Built {TODAY.isoformat()}.\n')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(hdr + 'export const trends = ' + json.dumps(out, indent=1, ensure_ascii=False) + ';\n')
print('fields', len(fields))
