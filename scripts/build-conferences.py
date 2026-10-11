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

if not os.path.isdir('cs-conf-stats'):
    subprocess.run(['git','clone','--depth','1','-q',
                    'https://github.com/Xovee/cs-conf-stats.git'], check=True)
else:
    subprocess.run(['git','-C','cs-conf-stats','pull','-q'], check=True)

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
# Remember which README section each venue sits under, so the page can link
# straight to the table the numbers came from instead of the repo root.
rate_section={}
_sec=''
for line in open('ar.md'):
    if line.startswith('### '):
        _sec=re.sub(r'[^a-z0-9]+','-',line[4:].strip().lower()).strip('-')
        continue
    if not line.startswith('|') or '---' in line or line.startswith('| Conference'): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    m=re.match(r"([A-Za-z0-9&\-\. ]+?)[''](\d{2})(.*)", cells[0])
    if not m: continue
    name, yy, suffix = m.group(1).strip(), int(m.group(2)), m.group(3).strip()
    if 'finding' in suffix.lower(): continue      # Findings is a separate track
    pct=re.search(r'([\d.]+)%', cells[1] if len(cells)>1 else '')
    if not pct: continue
    year = 2000+yy
    key=AR_ALIAS.get(name, name)
    rates[key][year]=float(pct.group(1))
    rate_section.setdefault(key, _sec)

# cs-conf-stats carries accepted/submitted counts per year and is current to
# 2026 for most venues, so it is the primary source; the older compilation is
# kept only to fill venues it does not cover.
CSC_ALIAS={'KDD':'SIGKDD','IEEE S&P':'S&P','Interspeech':'InterSpeech'}
csc_rates={}; csc_slug={}
for c in json.load(open('cs-conf-stats/data/conf.json'))['conferences']:
    t=CSC_ALIAS.get(c['series'], c['series'])
    hist={}
    for y in c.get('yearly_data') or []:
        mt=y.get('main_track') or {}
        a,sb=mt.get('num_acc'), mt.get('num_sub')
        if a and sb: hist[y['year']]=round(100*a/sb, 1)
    if hist:
        csc_rates[t]=hist
        csc_slug[t]=c['series'].lower().replace(' ','-').replace('&','')
print('cs-conf-stats venues with rates:', len(csc_rates))

# Best-paper awards: Jeff Huang's compilation, the only maintained
# cross-conference list. Anchors verified against the live page.
BEST={'AAAI':'aaai','ACL':'acl','CIKM':'cikm','CVPR':'cvpr','ICCV':'iccv','ICML':'icml',
      'IJCAI':'ijcai','SIGKDD':'kdd','NeurIPS':'neurips','PODS':'pods','S&P':'s&p',
      'SIGIR':'sigir','SIGMOD':'sigmod','VLDB':'vldb','WWW':'www','FSE':'fse'}

# ---------- areas ----------
BIO={'APBC','BIBM','ISMB','ISBRA','RECOMB','MICCAI','EMBC'}
AREA_BY_SUB={'AI':'AI / ML / Data Mining','SC':'Security & Privacy','DB':'AI / ML / Data Mining'}
# CCF files WWW under 交叉/综合/新兴 because of its history, but everyone
# submitting to it treats it as a web-mining venue.
AREA_OVERRIDE={'WWW':'AI / ML / Data Mining'}
def area(sub, title):
    if title in EXTRA: return EXTRA[title]
    if title in AREA_OVERRIDE: return AREA_OVERRIDE[title]
    if sub in AREA_BY_SUB: return AREA_BY_SUB[sub]
    if title in BIO: return 'Medicine, Biology & Genetics'
    return 'Science & Interdisciplinary'

def tier_of(ccf, core):
    """1 = top by either table, 2 = strong by either, 3 = the rest."""
    if ccf=='A' or core=='A*': return 1
    if ccf=='B' or core=='A':  return 2
    return 3

def latest_link(confs):
    e=max(confs, key=lambda e: e.get('year',0)) if confs else {}
    return e.get('link','') or ''

def dstr(s):
    m=re.match(r'(\d{4}-\d{2}-\d{2})', str(s or '')); return m.group(1) if m else ''

EXTRA={'ICASSP':'AI / ML / Data Mining','InterSpeech':'AI / ML / Data Mining',
       'ICWSM':'AI / ML / Data Mining'}
out=[]
for sub in ['AI','SC','DB','MX','CG','HI']:
    for f in sorted(glob.glob(f'ccf-deadlines/conference/{sub}/*.yml')):
        for c in yaml.safe_load(open(f)):
            r=c.get('rank') or {}; t=c['title']; d=(c.get('description') or '').strip()
            if sub in ('CG','HI') and t not in EXTRA: continue
            confs=c.get('confs') or []
            # next deadline still ahead of today, across every published edition
            upcoming=[]
            for ed in confs:
                for tl in (ed.get('timeline') or []):
                    ds=dstr(tl.get('deadline'))
                    if ds and datetime.date.fromisoformat(ds) >= TODAY:
                        upcoming.append((ds, ed.get('year'), ed.get('link',''), dstr(tl.get('abstract_deadline'))))
            upcoming.sort()
            # Every round the venue runs, not just the soonest. The reference
            # edition is whichever recent one publishes the most rounds; a
            # round whose date has passed is rolled forward like any other
            # estimate, so a two-round venue always shows two.
            recent=sorted(confs, key=lambda e: e.get('year',0))[-2:]
            ref_rounds=[]
            for ed in recent:
                rs=[(dstr(t.get('deadline')), (t.get('comment') or '').strip())
                    for t in (ed.get('timeline') or []) if dstr(t.get('deadline'))]
                seen=set(); rs=[r for r in rs if not (r[0] in seen or seen.add(r[0]))]
                if len(rs) > len(ref_rounds): ref_rounds=rs
            rounds=[]
            for ds, label in ref_rounds:
                d0=datetime.date.fromisoformat(ds)
                if d0 >= TODAY:
                    rounds.append({'d':ds,'label':label,'est':False})
                    continue
                for bump in (1,2):
                    try: cand=d0.replace(year=d0.year+bump)
                    except ValueError: cand=d0.replace(year=d0.year+bump, day=28)
                    if cand >= TODAY:
                        rounds.append({'d':cand.isoformat(),'label':label,'est':True,'from':ds})
                        break
            # A real future date beats a rolled one within a fortnight of it.
            for u_ds, u_yr, u_lk, u_ab in upcoming:
                u_d0=datetime.date.fromisoformat(u_ds)
                for rd in [x for x in rounds
                           if abs((datetime.date.fromisoformat(x['d'])-u_d0).days) <= 14]:
                    rounds.remove(rd)
                if not any(x['d']==u_ds for x in rounds):
                    rounds.append({'d':u_ds,'label':'','est':False,'year':u_yr,'link':u_lk,'abstract':u_ab})
            rounds.sort(key=lambda x: x['d'])
            # The soonest round is the headline date, whether it is published
            # or rolled forward.
            nxt=None; est=False
            if rounds:
                r0=rounds[0]
                if r0['est']:
                    src=r0.get('from','')
                    base=next((e.get('year') for e in confs
                               if any(dstr(t.get('deadline'))==src for t in (e.get('timeline') or []))), None)
                    bumped=datetime.date.fromisoformat(r0['d']).year - datetime.date.fromisoformat(src).year if src else 1
                    nxt=(r0['d'], (base+bumped) if base else None, latest_link(confs), '')
                    est=True
                else:
                    nxt=(r0['d'], r0.get('year'), r0.get('link',''), r0.get('abstract',''))
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
            hist=sorted((csc_rates.get(t) or rates.get(t, {})).items())
            rsrc='csc' if t in csc_rates else ('ar' if t in rates else '')
            off=official(t,d); mirror=canon(r.get('core','N'))
            out.append({
                'title':t, 'desc':d, 'area':area(sub,t),
                'ccf':r.get('ccf','N'), 'core': off if off is not None else mirror,
                'coreVerified': off is not None,
                'nextDeadline': nxt[0] if nxt else '',
                'nextYear': nxt[1] if nxt else None,
                'nextAbstract': nxt[3] if nxt else '',
                'estimated': est,
                'estFrom': (rounds[0].get('from','') if rounds else '') if est else '',
                'rounds': rounds,
                'dblp': c.get('dblp',''),
                'best': BEST.get(t,''),
                'link': (nxt[2] if nxt else latest.get('link','')) or '',
                'date': latest.get('date',''), 'place': latest.get('place',''),
                'cycles': cycles, 'roundLabels': roundLabels,
                'proceedings': 'full',
                'rates': [{'y':y,'r':v} for y,v in hist],
                'rateSection': rate_section.get(t,''),
                'rateSrc': rsrc, 'rateSlug': csc_slug.get(t,''),
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
 # Society meetings: abstract- or minisymposium-driven, no archival
 # proceedings, so neither CCF nor CORE can index them at all.
 {'title':'INFORMS Annual Meeting','desc':'Institute for Operations Research and the Management Sciences','area':'Society meetings',
  'proceedings':'none','note':'The main annual gathering for operations research and analytics; abstract-driven, ~6,000 attendees.',
  'link':'https://meetings.informs.org/'},
 {'title':'SIAM MDS','desc':'SIAM Conference on Mathematics of Data Science','area':'Society meetings',
  'proceedings':'none','note':'Biennial. Where the mathematical side of data science meets; minisymposium format.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/mds26/'},
 {'title':'SIAM CSE','desc':'SIAM Conference on Computational Science and Engineering','area':'Society meetings',
  'proceedings':'none','note':'Biennial, odd years. The largest SIAM meeting and the main venue for scientific machine learning.',
  'date':'February 22-26, 2027','place':'Pittsburgh, Pennsylvania, USA',
  'link':'https://www.siam.org/conferences-events/siam-conferences/cse27/'},
 {'title':'SIAM UQ','desc':'SIAM Conference on Uncertainty Quantification','area':'Society meetings',
  'proceedings':'none','note':'Biennial, even years. The central applied-maths meeting for UQ; next edition 2028.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/uq26/'},
 {'title':'SIAM Annual Meeting','desc':'SIAM Annual Meeting (AN)','area':'Society meetings',
  'proceedings':'none','note':'Yearly, all of applied mathematics in one room. AN26 was July 6-10, 2026 in Cleveland; AN27 not yet announced.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/an26/'},
 {'title':'SIAM OP','desc':'SIAM Conference on Optimization','area':'Society meetings',
  'proceedings':'none','note':'Triennial. OP26 was June 2-5, 2026 in Edinburgh; the next edition is expected around 2029.',
  'link':'https://www.siam.org/conferences-events/siam-conferences/op26/'},
 {'title':'ICIAM','desc':'International Congress for Industrial and Applied Mathematics','area':'Society meetings',
  'proceedings':'none','note':'Every four years, the field-wide congress of applied mathematics.',
  'date':'July 12-16, 2027','place':'The Hague, Netherlands',
  'link':'https://www.siam.org/conferences-events/siam-conferences/iciam27/'},

 # Full proceedings, but too new or too far outside the catalogues to carry
 # a CCF or CORE rank. lastDeadline is the most recent published deadline;
 # the page rolls it forward and marks the result as an estimate.
 {'title':'COLM', 'equivalent':'CCF B / CORE A','desc':'Conference on Language Modeling','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings; founded 2024, too new for either ranking table.',
  'lastDeadline':'2026-03-31','link':'https://colm.cc/'},
 {'title':'MLSys', 'equivalent':'CCF B / CORE A','desc':'Conference on Machine Learning and Systems','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Full proceedings; unranked by both CCF and CORE despite being the main ML-systems venue.',
  'lastDeadline':'2025-10-30','link':'https://mlsys.org/'},
 {'title':'AMIA', 'equivalent':'CCF B / CORE A','desc':'AMIA Annual Symposium','area':'Medicine, Biology & Genetics',
  'proceedings':'full','note':'Full proceedings, indexed in PubMed; the central US biomedical-informatics meeting.',
  'lastDeadline':'2026-03-10','link':'https://amia.org/education-events/amia-annual-symposium'},
 {'title':'ASONAM', 'ccfManual':'C','coreManual':'B','desc':'IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining','area':'AI / ML / Data Mining',
  'proceedings':'full','note':'Ranked CCF C / CORE B, so below this page\'s usual bar, but it is the dedicated social-network analysis venue.',
  'lastDeadline':'2026-05-10','link':'https://asonam.cpsc.ucalgary.ca/2026/CFP.php'},
]

def roll(ds):
    """Last published deadline -> next plausible one, same month and day."""
    if not ds: return '', None, False
    d0=datetime.date.fromisoformat(ds)
    for bump in (1,2):
        try: cand=d0.replace(year=d0.year+bump)
        except ValueError: cand=d0.replace(year=d0.year+bump, day=28)
        if cand >= TODAY: return cand.isoformat(), cand.year, True
    return ('', None, False) if d0 < TODAY else (ds, d0.year, False)

for n in NOTABLE:
    n.setdefault('equivalent', None)   # editorial, not an official rank
    nd, ny, est = roll(n.get('lastDeadline',''))
    n.update({'ccf':n.get('ccfManual','N'),'core':n.get('coreManual','N'),'coreVerified':False,'nextAbstract':'',
              'cycles':1,'roundLabels':[],'rates':[],'rateSection':'','rateSrc':'','rateSlug':'','rounds':[],'dblp':'','best':'',
              'estimated':est,'estFrom':n.get('lastDeadline','') if est else '',
              'nextDeadline':nd,'nextYear':ny,'notable':True})
    n.setdefault('date',''); n.setdefault('place','')
    # An emerging venue carries a stated equivalence so it sorts with its peers;
    # a society meeting has no proceedings, so no tier is claimed for it.
    n['tier'] = 2 if n['equivalent'] else tier_of(n['ccf'], n['core'])

for c in out: c['tier']=tier_of(c['ccf'], c['core'])

CORE_ORDER={'A*':0,'A':1,'B':2,'C':3,'TBR':4,'JP':5,'N':6}
CCF_ORDER={'A':0,'B':1,'C':2,'N':3}
def listed(c): return c['core'] in ('A*','A') or c['ccf'] in ('A','B')
# inside an area, soonest deadline first; anything without one trails behind
def dkey(c): return (0, c['nextDeadline']) if c['nextDeadline'] else (1, c['title'].lower())
emerging=[n for n in NOTABLE if n['proceedings']=='full']
society=[n for n in NOTABLE if n['proceedings']=='none']
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
