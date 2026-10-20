"""Rebuild src/data/trends.js: what each field is publishing most.

Run from the repo root:  python3 scripts/build-trends.py
Expects src/data/conferences.js, so run build-conferences.py first.

Acceptance rates exist for a handful of computing conferences and nowhere
else, so this measures the one thing every field has: papers. For each
field it counts the last full year's papers in that field's journals (the
ones listed on its tab, plus the flagship proceedings for the fields that
publish at conferences) by OpenAlex keyword, keeps the ten largest, and
compares each topic's share with two years earlier. Share rather than raw
count, because the journals themselves grow and shrink.

Three grouped queries per field, at one OpenAlex credit each: about 60 a
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

def topics(sources, year, keywords=None, per_page=200):
    extra = (',keywords.id:' + '|'.join(keywords)) if keywords else ''
    url = ('https://api.openalex.org/works?filter=primary_location.source.id:' + '|'.join(sources) +
           f',publication_year:{year}{extra}&group_by=keywords.id&per_page={per_page}&mailto=site@zhiqian.ai')
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

# Keywords, not OpenAlex topics. A topic is a broad cluster with a generic
# name, so a trend like large language models is split across several of
# them and never appears under its own name. Keywords are the terms papers
# are actually about. They also include words that describe a study rather
# than its subject (who was studied, where, with which instrument, or a
# virtue every paper claims), and those are dropped here.
STOP = {
    # virtues and generic method words
    'benchmark', 'benchmarking', 'computational efficiency', 'generalization', 'inference efficiency',
    'communication efficiency', 'efficiency', 'robustness', 'scalability', 'optimization', 'accuracy',
    'performance', 'deep learning', 'machine learning', 'artificial intelligence', 'neural networks',
    'neural network', 'attention mechanism', 'class imbalance', 'resource-constrained devices',
    'simulation', 'numerical simulation', 'numerical simulations', 'modeling', 'stability', 'convergence',
    'real-time', 'computational cost', 'dataset', 'datasets', 'experimental validation', 'case study',
    'privacy', 'data privacy', 'uncertainty', 'interpretability',
    # properties a method is shown to have, not what it is about
    'convergence analysis', 'convergence rate', 'asymptotic normality', 'asymptotic distribution',
    'consistency', 'confidence intervals', 'data partitioning', 'mass conservation', 'np-hardness',
    'thermal stability', 'cycling stability', 'structure-property relationships', 'linear convergence',
    # model organisms: what was studied, not the question
    'escherichia coli', 'drosophila', 'caenorhabditis elegans', 'zebrafish', 'saccharomyces cerevisiae',
    # study designs and outcomes
    'survey', 'review', 'systematic review', 'meta-analysis', 'randomized controlled trial', 'cohort study',
    'cross-sectional study', 'retrospective study', 'non-inferiority', 'risk factors', 'mortality',
    'hospitalization', 'comorbidities', 'quality of life', 'prevalence', 'incidence', 'epidemiology',
    'health disparities', 'cross-national comparison', 'body mass index', 'obesity', 'depression', 'anxiety',
    # who was studied
    'older adults', 'children', 'adolescents', 'young adults', 'adults', 'women', 'men', 'infants',
    'sex differences', 'gender differences', 'age', 'immunocompromised patients', 'college students',
    'low- and middle-income countries', 'healthy volunteers', 'patients', 'age differences', 'mice', 'rats',
    # how sleep is measured, rather than what is studied
    'polysomnography', 'actigraphy', 'sleep efficiency', 'sleep latency', 'sleep onset latency',
    'total sleep time', 'wake after sleep onset', 'sleep architecture',
}
DROP = re.compile(r'\b(scale|index|questionnaire|inventory|score|europe|germany|china|united states|usa|'
                  r'africa|asia|india|japan|united kingdom|england|canada|australia|brazil|korea|france|'
                  r'italy|spain|netherlands|sweden|denmark|norway|finland|switzerland)\b', re.I)
def keep(name):
    return name.lower() not in STOP and not DROP.search(name)

fields = {}
by_area = {}
for j in journals:
    if j.get('oa'): by_area.setdefault(j['area'], []).append(j['oa'].rsplit('/', 1)[-1])
for area, journal_sources in by_area.items():
    confs, missing = CONF_SOURCES.get(area, ([], []))
    sources = journal_sources + [sid for sid, _ in confs]
    try:
        total, now = topics(sources, YEAR)
        now = [g for g in now if g['key'] and keep(g['key_display_name'])][:TOP]
        ids = [g['key'].rsplit('/', 1)[-1] for g in now]
        # The base year, asked about exactly these keywords, so a keyword
        # outside last time's top few hundred is still counted rather than
        # mistaken for new. One more query gives the base year's total.
        _, then = topics(sources, BASE, keywords=ids)
        total0, _ = topics(sources, BASE, per_page=1)
        time.sleep(0.3)
    except Exception as e:
        print('  kept last week for', area, '-', e)
        if area in prev: fields[area] = prev[area]
        continue
    before = {g['key']: g['count'] for g in then}
    rows = []
    for g in now:
        share = g['count'] / total * 100 if total else 0
        share0 = before.get(g['key'], 0) / total0 * 100 if total0 else 0
        rows.append({
            'topic': g['key_display_name'], 'label': g['key_display_name'],
            'id': g['key'].rsplit('/', 1)[-1],
            'n': g['count'], 'share': round(share, 1),
            # Relative change in share. None when the keyword was absent two
            # years ago, which the page shows as "new" rather than infinity.
            'growth': round((share / share0 - 1) * 100) if share0 else None,
        })
    fields[area] = {'total': total, 'journals': len(journal_sources),
                    'confs': [name for _, name in confs], 'missing': missing, 'rows': rows}
    print(f'  {area:10s} {total:6d} papers  top: {rows[0]["topic"] if rows else "-"}')

out = {'year': YEAR, 'base': BASE, 'fields': fields}
hdr = ('// Generated by scripts/build-trends.py, do not edit by hand.\n'
       f'// Papers per OpenAlex keyword in each field\'s journals, {YEAR}, against {BASE}.\n'
       f'// Built {TODAY.isoformat()}.\n')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(hdr + 'export const trends = ' + json.dumps(out, indent=1, ensure_ascii=False) + ';\n')
print('fields', len(fields))
