"""Rebuild src/data/trends.js and public/trend-papers/: what each field is
publishing most, and the papers that best represent each subject.

Run from the repo root:  python3 scripts/build-trends.py
Expects src/data/conferences.js, so run build-conferences.py first.

Acceptance rates exist for a handful of computing conferences and nowhere
else, so this measures the one thing every field has: papers. For each
field it takes the last full year's papers in that field's venues (the
journals listed on its tab, plus the flagship proceedings for fields that
publish at conferences), groups them by OpenAlex keyword, keeps the twenty
largest, and compares each keyword's share with two years earlier.

For each keyword it then picks ten representative recent papers. Candidates
are the most cited papers on that keyword in the field's venues since the
start of the year before last; they are re-ranked on three things together:
citations (log scale, so one runaway paper does not drown the rest), the
standing of the venue (a field flagship or CCF A counts most), and the
standing of the authors (the larger h-index of the first and last author).

Budget. OpenAlex gives 1,000 credits a day without a key, shared by every
user on the same IP address, which on a GitHub runner means strangers.
One field costs about thirty credits. The script therefore refreshes only
fields older than four weeks, oldest first, at most TRENDS_MAX_FIELDS per
run, stops cleanly when the remaining budget gets low, and leaves the rest
for the next run. With
OPENALEX_API_KEY set it uses that key's own, larger budget instead.
"""
import json, re, datetime, urllib.request, urllib.error, urllib.parse, time, os, math

TODAY = datetime.date.today()
YEAR = TODAY.year - 1          # the last full year
BASE = YEAR - 2                # what the share is compared against
TOP = 20
MIN_PAPERS = 2               # a keyword on one paper is not a topic
PAPERS = 10
CANDIDATES = 15
MAX_AGE_DAYS = 28              # refresh a field about once a month
RESERVE = 40                   # credits left untouched for anything else
OUT = 'src/data/trends.js'
PAPER_DIR = 'public/trend-papers'
KEY = os.environ.get('OPENALEX_API_KEY', '').strip()
AUTH = f'api_key={KEY}' if KEY else 'mailto=site@zhiqian.ai'
FORCE = os.environ.get('TRENDS_FORCE', '') == '1'
# At most this many fields per run (0: no cap). The workflow runs daily with
# a cap of one, so the fields spread themselves over the month: each is
# rebuilt when it turns 28 days old, one a day, instead of all 23 in one
# burst that a shared OpenAlex budget may not cover.
MAX_FIELDS = int(os.environ.get('TRENDS_MAX_FIELDS', '0') or 0)

conf = open('src/data/conferences.js', encoding='utf-8').read()
journals = json.loads(re.search(r'export const journals = (\[.*?\]);\n', conf, re.S).group(1))

prev = {}
if os.path.exists(OUT):
    m = re.search(r'export const trends = (\{.*\});', open(OUT, encoding='utf-8').read(), re.S)
    if m: prev = json.loads(m.group(1)).get('fields', {})

remaining = [10 ** 9]
class OutOfBudget(Exception): pass

def get(path, params):
    if remaining[0] < RESERVE:
        raise OutOfBudget()
    url = f'https://api.openalex.org/{path}?' + urllib.parse.urlencode(params, safe=':|,') + '&' + AUTH
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                rem = r.headers.get('x-ratelimit-remaining')
                if rem is not None and rem.isdigit(): remaining[0] = int(rem)
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = (e.read() or b'').decode('utf-8', 'ignore').lower()
            if e.code == 429 and 'budget' in body:
                raise OutOfBudget()
            if e.code != 429 or attempt == 3: raise
            time.sleep(5 * (attempt + 1))

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
    # properties a result is shown to have, not what it is about
    'convergence analysis', 'convergence rate', 'asymptotic normality', 'asymptotic distribution',
    'consistency', 'confidence intervals', 'data partitioning', 'mass conservation', 'np-hardness',
    'thermal stability', 'cycling stability', 'structure-property relationships', 'linear convergence',
    'lower bound', 'upper bound', 'lower bounds', 'upper bounds', 'polynomial time', 'existence',
    'uniqueness', 'regularity', 'well-posedness', 'first-principles calculations',
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

# Conference-led fields publish their main work in proceedings, so counting
# only their journals would describe the long versions, not the field. These
# are the flagship proceedings OpenAlex indexes for both years compared,
# each found by name and checked for 2023 and 2025 records in October 2026.
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
    'theory': ([('S7407087723', 'STOC'), ('S4210175768', 'FOCS')], ['SODA']),
    'audio': ([('S4363607879', 'ICASSP'), ('S4393918409', 'Interspeech')], ['ISMIR']),
    'control': ([('S4210221977', 'CDC'), ('S4210168941', 'ACC')], []),
    'biomed': ([('S4363605129', 'ISBI')], ['MICCAI']),
}

# Venue standing, for ranking papers. A flagship conference, a journal the
# field tags as top, or CCF A counts fully; CCF B half; the rest nothing.
VENUE, SHORT = {}, {}
for j in journals:
    sid = (j.get('oa') or '').rsplit('/', 1)[-1]
    if not sid: continue
    SHORT[sid] = j['title']
    VENUE[sid] = 1.0 if (j.get('rank') or j.get('ccf') == 'A') else 0.5 if j.get('ccf') == 'B' else 0.0
for confs, _ in CONF_SOURCES.values():
    for sid, name in confs:
        VENUE[sid], SHORT[sid] = 1.0, name

def keyword_groups(sources, year, keywords=None, per_page=200):
    f = f'primary_location.source.id:{"|".join(sources)},publication_year:{year}'
    if keywords: f += ',keywords.id:' + '|'.join(keywords)
    d = get('works', {'filter': f, 'group_by': 'keywords.id', 'per_page': per_page})
    return d['meta']['count'], d['group_by']

h_cache = {}
def h_index(ids):
    ids = [i for i in dict.fromkeys(ids) if i and i not in h_cache]
    for k in range(0, len(ids), 50):
        chunk = ids[k:k + 50]
        d = get('authors', {'filter': 'openalex_id:' + '|'.join(chunk), 'per_page': 50,
                            'select': 'id,summary_stats'})
        for a in d['results']:
            h_cache[a['id'].rsplit('/', 1)[-1]] = (a.get('summary_stats') or {}).get('h_index') or 0
        for i in chunk: h_cache.setdefault(i, 0)

def candidates(sources, kw):
    d = get('works', {
        'filter': f'primary_location.source.id:{"|".join(sources)},keywords.id:{kw},'
                  f'from_publication_date:{YEAR - 1}-01-01',
        'sort': 'cited_by_count:desc', 'per_page': CANDIDATES,
        'select': 'id,doi,title,publication_year,cited_by_count,primary_location,authorships'})
    return d['results']

def short_author(w):
    names = [a['author']['display_name'] for a in w.get('authorships') or [] if a.get('author')]
    if not names: return ''
    if len(names) == 1: return names[0]
    if len(names) == 2: return f'{names[0]} and {names[1]}'
    return names[0] + ' et al.'

def end_ids(w):
    au = [a['author']['id'].rsplit('/', 1)[-1] for a in w.get('authorships') or []
          if a.get('author') and a['author'].get('id')]
    return [au[0], au[-1]] if au else []

def build_field(area, journal_sources):
    confs, missing = CONF_SOURCES.get(area, ([], []))
    sources = journal_sources + [sid for sid, _ in confs]
    total, now = keyword_groups(sources, YEAR)
    # A small field runs out of real topics before twenty, and its tail is
    # keywords from a single paper. Those say nothing about the field.
    now = [g for g in now if g['key'] and keep(g['key_display_name']) and g['count'] >= MIN_PAPERS][:TOP]
    ids = [g['key'].rsplit('/', 1)[-1] for g in now]
    # The base year, asked about exactly these keywords, so a keyword
    # outside last time's top few hundred is still counted rather than
    # mistaken for new. One more query gives the base year's total.
    _, then = keyword_groups(sources, BASE, keywords=ids)
    total0, _ = keyword_groups(sources, BASE, per_page=1)
    before = {g['key']: g['count'] for g in then}
    rows = []
    for g in now:
        share = g['count'] / total * 100 if total else 0
        share0 = before.get(g['key'], 0) / total0 * 100 if total0 else 0
        rows.append({
            'label': g['key_display_name'], 'id': g['key'].rsplit('/', 1)[-1],
            'n': g['count'], 'share': round(share, 1),
            # Relative change in share; None when absent two years ago.
            'growth': round((share / share0 - 1) * 100) if share0 else None,
        })
    cands = {r['id']: candidates(sources, r['id']) for r in rows}
    h_index([i for ws in cands.values() for w in ws for i in end_ids(w)])
    papers = {}
    for kw, ws in cands.items():
        scored = []
        for w in ws:
            src = ((w.get('primary_location') or {}).get('source') or {})
            sid = (src.get('id') or '').rsplit('/', 1)[-1]
            h = max([h_cache.get(i, 0) for i in end_ids(w)] or [0])
            score = math.log1p(w.get('cited_by_count') or 0) + VENUE.get(sid, 0) + 0.3 * math.log1p(h)
            if not (w.get('title') or '').strip(): continue
            scored.append((score, {
                't': w['title'].strip(), 'u': w.get('doi') or w['id'],
                'y': w.get('publication_year'), 'c': w.get('cited_by_count') or 0,
                'v': SHORT.get(sid) or (src.get('display_name') or ''),
                'a': short_author(w), 'h': h,
            }))
        scored.sort(key=lambda x: -x[0])
        papers[kw] = [p for _, p in scored[:PAPERS]]
    for r in rows:
        r['papers'] = len(papers.get(r['id'], []))
    return ({'total': total, 'journals': len(journal_sources),
             'confs': [name for _, name in confs], 'missing': missing, 'rows': rows,
             'built': TODAY.isoformat()}, papers)

by_area = {}
for j in journals:
    if j.get('oa'): by_area.setdefault(j['area'], []).append(j['oa'].rsplit('/', 1)[-1])

os.makedirs(PAPER_DIR, exist_ok=True)
fields = dict(prev)
def is_fresh(area):
    f = prev.get(area) or {}
    if not f.get('built') or (len(f.get('rows', [])) < TOP and f.get('total', 0) >= 1000): return False
    if not os.path.exists(f'{PAPER_DIR}/{area}.json'): return False
    return (TODAY - datetime.date.fromisoformat(f['built'])).days < MAX_AGE_DAYS
# Oldest first, so a run that runs out of budget still moves the stalest on.
order = sorted(by_area, key=lambda a: ((prev.get(a) or {}).get('built') or '0000', a))
done, fresh_n = [], 0
for area in order:
    if is_fresh(area) and not FORCE:
        fresh_n += 1; continue
    if MAX_FIELDS and len(done) >= MAX_FIELDS:
        break
    try:
        field, papers = build_field(area, by_area[area])
    except OutOfBudget:
        print(f'  budget low ({remaining[0]} left); {area} and the rest wait for the next run')
        break
    except Exception as e:
        print('  kept previous for', area, '-', e)
        continue
    fields[area] = field
    with open(f'{PAPER_DIR}/{area}.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, separators=(',', ':'))
    done.append(area)
    print(f'  {area:10s} {field["total"]:6d} papers  top: {field["rows"][0]["label"] if field["rows"] else "-"}'
          f'  (credits left {remaining[0]})')

fields = {a: f for a, f in fields.items() if a in by_area}
out = {'year': YEAR, 'base': BASE, 'fields': fields}
hdr = ('// Generated by scripts/build-trends.py, do not edit by hand.\n'
       f'// Papers per OpenAlex keyword in each field\'s venues, {YEAR}, against {BASE}.\n'
       '// Representative papers per keyword are in public/trend-papers/<field>.json.\n')
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(hdr + 'export const trends = ' + json.dumps(out, indent=1, ensure_ascii=False) + ';\n')
print(f'refreshed {len(done)}, still fresh {fresh_n}, waiting {len(by_area) - len(done) - fresh_n}')
