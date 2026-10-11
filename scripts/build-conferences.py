"""Rebuild src/data/conferences.js from upstream sources.

Run from the repo root:  python3 scripts/build-conferences.py
It clones ccf-deadlines, pulls the official CORE2023 export and the
acceptance-rate table into .conf-cache/, then rewrites the data module.
"""
import yaml, glob, csv, re, json, datetime, collections, os, subprocess, urllib.request

TODAY = datetime.date.today()
CACHE = '.conf-cache'
os.makedirs(CACHE, exist_ok=True)
os.chdir(CACHE)

if not os.path.isdir('ccf-deadlines'):
    subprocess.run(['git','clone','--depth','1','-q',
                    'https://github.com/ccfddl/ccf-deadlines.git'], check=True)
else:
    subprocess.run(['git','-C','ccf-deadlines','pull','-q'], check=True)

for url, dest in [
    ('https://portal.core.edu.au/conf-ranks/?search=&by=all&source=CORE2023&sort=atitle&page=1&do=Export', 'core2023.csv'),
    ('https://raw.githubusercontent.com/lixin4ever/Conference-Acceptance-Rate/master/README.md', 'ar.md'),
]:
    with urllib.request.urlopen(url, timeout=120) as r, open(dest,'wb') as f:
        f.write(r.read())

# ---------- official CORE 2023 ----------
core_rows=[r for r in csv.reader(open('core2023.csv')) if len(r)>=5]
norm=lambda x: re.sub(r'[^a-z0-9]','',(x or '').lower())
toks=lambda x: set(re.findall(r'[a-z]{4,}',(x or '').lower()))
def canon(v):
    v=(v or '').strip()
    if v in ('A*','A','B','C'): return v
    if v.upper()=='TBR': return 'TBR'
    if 'journal' in v.lower(): return 'JP'
    return 'N'
by_title={norm(r[1]): r[4] for r in core_rows}
acr=collections.defaultdict(list)
for r in core_rows: acr[norm(r[2])].append(r)
def official(title, desc):
    v=by_title.get(norm(desc)) or by_title.get(norm(title))
    if v is not None: return canon(v)
    dt=toks(desc)
    for r in acr.get(norm(title), []):
        if dt and len(dt & toks(r[1]))>=2: return canon(r[4])
    return None

# ---------- acceptance rates ----------
# The rate table and the CCF catalogue spell several venues differently;
# without these, KDD and friends silently lose their whole history.
AR_ALIAS={'TheWebConf':'WWW','NAACL-HLT':'NAACL','KDD':'SIGKDD','SIGKDD':'SIGKDD',
          'CCS':'CCS','S&P':'S&P','Oakland':'S&P','IEEE S&P':'S&P',
          'USENIX':'USENIX Security','USENIX Sec':'USENIX Security','SP':'S&P',
          'MM':'ACM MM','ACMMM':'ACM MM'}
rates=collections.defaultdict(dict)
for line in open('ar.md'):
    if not line.startswith('|') or '---' in line or line.startswith('| Conference'): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    m=re.match(r"([A-Za-z0-9&\-\. ]+?)[''](\d{2})(.*)", cells[0])
    if not m: continue
    name, yy, suffix = m.group(1).strip(), int(m.group(2)), m.group(3).strip()
    if 'finding' in suffix.lower(): continue      # Findings is a separate track
    pct=re.search(r'([\d.]+)%', cells[1] if len(cells)>1 else '')
    if not pct: continue
    year = 2000+yy
    rates[AR_ALIAS.get(name, name)][year]=float(pct.group(1))

# ---------- areas ----------
BIO={'APBC','BIBM','ISMB','ISBRA','RECOMB','MICCAI','EMBC'}
AREA_BY_SUB={'AI':'AI / ML / Data Mining','SC':'Security & Privacy','DB':'AI / ML / Data Mining'}
def area(sub, title):
    if sub in AREA_BY_SUB: return AREA_BY_SUB[sub]
    if title in BIO: return 'Biomedical & Health'
    return 'Science & Interdisciplinary'

def dstr(s):
    m=re.match(r'(\d{4}-\d{2}-\d{2})', str(s or '')); return m.group(1) if m else ''

out=[]
for sub in ['AI','SC','DB','MX']:
    for f in sorted(glob.glob(f'ccf-deadlines/conference/{sub}/*.yml')):
        for c in yaml.safe_load(open(f)):
            r=c.get('rank') or {}; t=c['title']; d=(c.get('description') or '').strip()
            confs=c.get('confs') or []
            # next deadline still ahead of today, across every published edition
            upcoming=[]
            for ed in confs:
                for tl in (ed.get('timeline') or []):
                    ds=dstr(tl.get('deadline'))
                    if ds and datetime.date.fromisoformat(ds) >= TODAY:
                        upcoming.append((ds, ed.get('year'), ed.get('link',''), dstr(tl.get('abstract_deadline'))))
            upcoming.sort()
            nxt=upcoming[0] if upcoming else None
            latest=max(confs, key=lambda e: e.get('year',0)) if confs else {}
            # Count rounds only within the edition being shown. Taking the max
            # across every edition flagged AAAI, whose old NeurIPS fast track
            # looks like a second cycle but no longer exists.
            ref = next((e for e in confs if e.get('year')==(nxt[1] if nxt else None)), latest if confs else {})
            tl_ref = ref.get('timeline') or []
            labels=[(t.get('comment') or '').strip() for t in tl_ref]
            deadlines_in_ref={dstr(t.get('deadline')) for t in tl_ref if dstr(t.get('deadline'))}
            cycles=len(deadlines_in_ref) if len(deadlines_in_ref)>1 else 1
            roundLabels=[l for l in labels if l] if cycles>1 else []
            hist=sorted(rates.get(t, {}).items())
            off=official(t,d); mirror=canon(r.get('core','N'))
            out.append({
                'title':t, 'desc':d, 'area':area(sub,t),
                'ccf':r.get('ccf','N'), 'core': off if off is not None else mirror,
                'coreVerified': off is not None,
                'nextDeadline': nxt[0] if nxt else '',
                'nextYear': nxt[1] if nxt else None,
                'nextAbstract': nxt[3] if nxt else '',
                'link': (nxt[2] if nxt else latest.get('link','')) or '',
                'date': latest.get('date',''), 'place': latest.get('place',''),
                'cycles': cycles, 'roundLabels': roundLabels,
                'proceedings': 'full',
                'rates': [{'y':y,'r':v} for y,v in hist],
            })
json.dump(out, open('built.json','w'))
print('conferences:', len(out))
print('with a FUTURE deadline:', sum(1 for c in out if c['nextDeadline']))
print('with acceptance history:', sum(1 for c in out if c['rates']))
print('areas:', dict(collections.Counter(c['area'] for c in out)))
print('multi-cycle venues:', [(c['title'],c['cycles']) for c in out if c['cycles']>1])

# ---------- hand-maintained: venues the ranking tables simply do not cover ----------
# CCF and CORE only index conferences with archival proceedings, so society
# meetings and brand-new venues fall through. Edit this list by hand.
NOTABLE=[
 {'title':'INFORMS Annual Meeting','desc':'Institute for Operations Research and the Management Sciences','area':'Science & Interdisciplinary',
  'proceedings':'none','note':'Abstract-driven society meeting; no archival proceedings. The main annual gathering for operations research and analytics.',
  'link':'https://meetings.informs.org/'},
 {'title':'SIAM MDS','desc':'SIAM Conference on Mathematics of Data Science','area':'Science & Interdisciplinary',
  'proceedings':'none','note':'Minisymposium and talk format, no archival proceedings. Where the mathematical side of data science meets.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/mds26/'},
 {'title':'COLM', 'equivalent':'CCF B / CORE A','desc':'Conference on Language Modeling','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings; founded 2024, too new for either ranking table.',
  'link':'https://colmweb.org/'},
 {'title':'MLSys', 'equivalent':'CCF B / CORE A','desc':'Conference on Machine Learning and Systems','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings; unranked by both CCF and CORE despite being the main ML-systems venue.',
  'link':'https://mlsys.org/'},
 {'title':'AMIA', 'equivalent':'CCF B / CORE A','desc':'AMIA Annual Symposium','area':'Biomedical & Health',
  'proceedings':'full','note':'Full proceedings, indexed in PubMed; the central US biomedical-informatics meeting.',
  'link':'https://amia.org/education-events/amia-annual-symposium'},
]
for n in NOTABLE:
    n.setdefault('equivalent', None)   # editorial, not an official rank
    n.update({'ccf':'N','core':'N','coreVerified':False,'nextAbstract':'',
              'date':'','place':'','cycles':1,'roundLabels':[],'rates':[],
              'notable':True})
    n.setdefault('nextDeadline',''); n.setdefault('nextYear',None)
    # An emerging venue carries a stated equivalence so it sorts with its peers;
    # a society meeting has no proceedings, so no tier is claimed for it.
    n['tier'] = 2 if n['equivalent'] else 3

def tier_of(ccf, core):
    """1 = top by either table, 2 = strong by either, 3 = the rest."""
    if ccf=='A' or core=='A*': return 1
    if ccf=='B' or core=='A':  return 2
    return 3
for c in out: c['tier']=tier_of(c['ccf'], c['core'])

CORE_ORDER={'A*':0,'A':1,'B':2,'C':3,'TBR':4,'JP':5,'N':6}
CCF_ORDER={'A':0,'B':1,'C':2,'N':3}
def listed(c): return c['core'] in ('A*','A') or c['ccf'] in ('A','B')
# inside an area, soonest deadline first; anything without one trails behind
def dkey(c): return (0, c['nextDeadline']) if c['nextDeadline'] else (1, c['title'].lower())
emerging=[n for n in NOTABLE if n['equivalent']]
society=[n for n in NOTABLE if not n['equivalent']]
# One list, ordered by date alone — the reader filters by field in the page.
ranked=sorted([c for c in out if listed(c)] + emerging, key=dkey)
others=sorted([c for c in out if not listed(c)], key=lambda c:(CORE_ORDER[c['core']], CCF_ORDER[c['ccf']], c['title'].lower()))
notable=sorted(society, key=lambda c:(c['area'], c['title']))

hdr=("// Generated by scripts/build-conferences.py — do not edit by hand.\n"
     "// CCF ranks mirror the CCF catalogue via github.com/ccfddl/ccf-deadlines.\n"
     "// CORE ranks are cross-checked against the official CORE2023 export from\n"
     "// portal.core.edu.au. Acceptance rates come from\n"
     "// github.com/lixin4ever/Conference-Acceptance-Rate (main track only).\n"
     f"// Built {TODAY.isoformat()}.\n")
body=(hdr + "export const ranked = %s;\n\nexport const others = %s;\n\n"
      "// Hand-maintained; the ranking tables do not reach these.\nexport const notable = %s;\n"
      % tuple(json.dumps(x, indent=2, ensure_ascii=False) for x in (ranked, others, notable)))
open('../src/data/conferences.js','w').write(body)
import collections as _c
print('\nwritten | listed', len(ranked), '| folded', len(others), '| society', len(notable))
print('tiers:', dict(sorted(_c.Counter(c['tier'] for c in ranked).items())))
print('areas:', dict(_c.Counter(c['area'] for c in ranked)))
